#!/usr/bin/env python3
"""
Build print-ready PDF and EPUB from the book/ folder.

Assembles front matter, chapters (book/chNN-*.md or book/chapter-NN.md), about
the author, and index. All content sources are read only from the book/ folder.
Applies consistent styling: definitions in a box, case studies in a distinct layout.

Usage:
  PDF (full or dry-run):
    python build_print_pdf.py --output path/to/book.pdf
    python build_print_pdf.py --dry-run [--pdf] --output path/to/dry-run.pdf

  EPUB (full or dry-run):
    python build_print_pdf.py --epub --output path/to/book.epub
    python build_print_pdf.py --epub --dry-run --output path/to/dry-run.epub
"""

import argparse
import html as html_module
import re
import os
import sys
import tempfile
import shutil
from collections import OrderedDict
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None

# On Windows, WeasyPrint needs Pango/GTK DLLs. Add DLL directories to PATH so
# ctypes.util.find_library() can locate them. Use WEASYPRINT_DLL_DIRECTORIES if set,
# otherwise try common MSYS2/GTK locations so PDF build works when run via npm etc.
if os.name == "nt":
    _default_dll = (
        "C:\\Program Files (x86)\\MSYS2\\mingw64\\bin;"
        "C:\\Program Files\\GTK3-Runtime Win64\\bin"
    )
    _dll_dirs = os.getenv("WEASYPRINT_DLL_DIRECTORIES", _default_dll).split(";")
    _existing = [d.strip() for d in _dll_dirs if d.strip() and os.path.isdir(d.strip())]
    for d in _existing:
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(d)
            except (OSError, Exception):
                pass
        os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")

try:
    from weasyprint import HTML as WeasyHTML
except (ImportError, OSError):
    WeasyHTML = None

try:
    import ebooklib
    from ebooklib import epub
except ImportError:
    epub = None

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    PdfReader = None
    PdfWriter = None

# Trim size and margins — single print interior (5.5" × 8.25"). PDF/X uses the same interior twice
# with different ISBN filenames (see convert_interiors_to_pdfx.py).
PRINT_PAGE = {
    "width": "5.5in",
    "height": "8.25in",
    "top": "0.6in",
    "bottom": "0.6in",
    "left": "0.55in",
    "right": "0.55in",
}
# Bound-book gutter: inner margin +6 mm, outer −6 mm (base 0.55 in each side; type block width unchanged).
# CSS @page :right → inner = left; @page :left → inner = right.
GUTTER_EXTRA = "6mm"
# Extra space below the running header on introduction/chapter/back-matter pages only (not front matter).
CONTENT_TOP_EXTRA_BELOW_HEADER = "6mm"
TRIM_WIDTH = PRINT_PAGE["width"]
TRIM_HEIGHT = PRINT_PAGE["height"]
PAGE_TOP = PRINT_PAGE["top"]
PAGE_BOTTOM = PRINT_PAGE["bottom"]
PAGE_LEFT = PRINT_PAGE["left"]
PAGE_RIGHT = PRINT_PAGE["right"]
# Footer: WeasyPrint uses @page margin boxes for page numbers (no frame height needed)


def find_repo_root(start: Path) -> Path:
    """Find directory containing the book/ folder (book repo root). All content sources live under book/."""
    current = start.resolve()
    for _ in range(10):
        if (current / "book").is_dir():
            return current
        current = current.parent
    return start


def load_text(path: Path) -> str:
    """Load file content; return empty string if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def resolve_chapter_path(book_dir: Path, chapter_num: int) -> Path | None:
    """
    Resolve the markdown file for a chapter. Tries, in order: book/chapter-NN.md,
    book/chNN-*.md (kebab-case), then book/NN - *.md. Returns path if found, None otherwise.
    """
    nn = f"{chapter_num:02d}"
    path = book_dir / f"chapter-{nn}.md"
    if path.exists():
        return path
    # Support chNN-kebab-case.md (e.g. ch01-the-ninety-five-per-cent-paradox.md)
    matches = list(book_dir.glob(f"ch{nn}-*.md"))
    if matches:
        return matches[0]
    # Support "NN - Title.md" naming
    matches = list(book_dir.glob(f"{nn} - *.md"))
    return matches[0] if matches else None


def discover_chapters_from_book(book_dir: Path) -> list[tuple[int, str]]:
    """
    When book/toc.md is missing, discover chapters from book/chapter-NN.md,
    book/chNN-*.md, or book/NN - *.md. Returns [(num, "Chapter N"), ...] in order.
    """
    seen = set()
    for path in sorted(book_dir.glob("chapter-*.md")):
        m = re.match(r"chapter-(\d+)", path.stem, re.IGNORECASE)
        if m:
            seen.add(int(m.group(1)))
    for path in sorted(book_dir.glob("ch[0-9][0-9]-*.md")):
        m = re.match(r"ch(\d+)-", path.stem, re.IGNORECASE)
        if m:
            seen.add(int(m.group(1)))
    for path in sorted(book_dir.glob("[0-9][0-9] - *.md")):
        m = re.match(r"(\d+)\s*-\s*.+", path.stem)
        if m:
            seen.add(int(m.group(1)))
    return sorted([(n, f"Chapter {n}") for n in seen], key=lambda x: x[0])


# In book/toc.md, chapter titles may use " | " (space-pipe-space) for a manual line break
# in PDF/EPUB chapter openers. Display uses <br/>; plain text (TOC line, running header, nav) collapses to a space.
CHAPTER_TITLE_LINE_BREAK = " | "


def chapter_title_plain(title: str) -> str:
    """Single-line title: strip manual break markers for headers, EPUB nav, and metadata."""
    return title.replace(CHAPTER_TITLE_LINE_BREAK, " ").strip()


def chapter_title_html(title: str) -> str:
    """
    Safe HTML for a chapter title on the page. Segments separated by CHAPTER_TITLE_LINE_BREAK
    become <br/>; each segment is escaped.
    """
    if CHAPTER_TITLE_LINE_BREAK not in title:
        return html_module.escape(title.strip())
    parts = [p.strip() for p in title.split(CHAPTER_TITLE_LINE_BREAK) if p.strip()]
    return "<br/>".join(html_module.escape(p) for p in parts)


def parse_toc(toc_content: str) -> tuple[str, str, list[tuple[int, str]]]:
    """
    Parse book/toc.md for title, subtitle, and chapter list.
    Returns (title, subtitle, [(num, title), ...]).
    """
    # Defaults aligned with book terminology: "Agentic Organisation" (not "Agentic Enterprise")
    title = "The Agentic Organisation"
    subtitle = "A complete AI transformation framework\nEUROPEAN EDITION"
    chapters = []
    # Match **Chapter N: Title** or **Chapter N: Title** (9%)
    for m in re.finditer(
        r"\*\*Chapter\s+(\d+):\s+([^*]+)\*\*",
        toc_content,
        re.IGNORECASE,
    ):
        num = int(m.group(1))
        name = m.group(2).strip()
        chapters.append((num, name))
    # First line: title (may be markdown heading "# The Agentic Organisation" or plain text)
    lines = toc_content.strip().split("\n")
    if lines:
        first = lines[0].strip().lstrip("#").strip()
        if first:
            title = first
        # Second line often has subtitle (e.g. "### A CEO's perspective...")
        if len(lines) > 1 and "CEO" in lines[1]:
            subtitle = lines[1].strip().lstrip("#").strip()
    return title, subtitle, chapters


# Next metadata key after a multi-line Description block (start of line, before colon).
_METADATA_BLOCK_START = re.compile(
    r"^(keywords|bisac|identifier|publisher|date|publication\s+date|author|language|title|subtitle)\s*:",
    re.IGNORECASE,
)


def _parse_simple_metadata(content: str) -> dict:
    """Parse key: value lines from input/metadata.md. Used for EPUB metadata overrides."""
    out: dict = {}
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()

        if key == "description":
            paragraphs: list[str] = []
            current: list[str] = [value] if value else []
            i += 1
            while i < len(lines):
                stripped = lines[i].strip()
                if stripped and _METADATA_BLOCK_START.match(stripped):
                    break
                if not stripped:
                    if current:
                        paragraphs.append(" ".join(current))
                        current = []
                else:
                    current.append(stripped)
                i += 1
            if current:
                paragraphs.append(" ".join(current))
            out["description"] = "\n\n".join(paragraphs).strip()
            continue

        if key == "keywords" and value:
            # Strip surrounding quotes from each keyword for cleaner PDF/EPUB metadata
            out[key] = [k.strip().strip('"').strip("'") for k in value.split(",") if k.strip()]
        elif value:
            out[key] = value
        i += 1
    return out


def _unicode_sans_bold_segment(s: str) -> str:
    """
    Map ASCII A–Z, a–z, 0–9 to Mathematical Sans-Serif Bold so dc:description stays
    plain-text (no HTML in OPF) while still appearing bold in readers and Calibre.
    Other characters (punctuation, spaces) are left unchanged.
    """
    out: list[str] = []
    for ch in s:
        o = ord(ch)
        if ord("A") <= o <= ord("Z"):
            out.append(chr(0x1D5D4 + (o - ord("A"))))
        elif ord("a") <= o <= ord("z"):
            out.append(chr(0x1D5EE + (o - ord("a"))))
        elif ord("0") <= o <= ord("9"):
            out.append(chr(0x1D7EC + (o - ord("0"))))
        else:
            out.append(ch)
    return "".join(out)


def _markdown_bold_to_unicode_bold(text: str) -> str:
    """Replace **segment** with Unicode bold letters (EPUB dc:description cannot use HTML)."""

    def repl(m: re.Match) -> str:
        return _unicode_sans_bold_segment(m.group(1))

    return re.sub(r"\*\*([^*]+)\*\*", repl, text)


def _description_plain_for_pdf(description: str) -> str:
    """Strip markdown **bold** markers for PDF /Subject (plain text; paragraphs preserved)."""
    if not description:
        return ""
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", description)
    paras = [re.sub(r"\s+", " ", p).strip() for p in s.split("\n\n")]
    return "\n\n".join(p for p in paras if p)


def _normalise_metadata_date(date_str: str) -> str:
    """
    Return W3CDTF date (YYYY-MM-DD) for EPUB dc:date where possible.
    Readers and distributors expect ISO-style dates; accept common prose forms too.
    """
    s = date_str.strip()
    if not s:
        return ""
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s
    from datetime import datetime

    for fmt in ("%d %B %Y", "%B %d, %Y", "%d %b %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return s


def _try_load_yaml_metadata(path: Path) -> dict:
    """If PyYAML is available, load input/metadata.yaml for EPUB overrides; else return {}."""
    if not path.exists():
        return {}
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        return {str(k).lower(): v for k, v in data.items()}
    except Exception:
        return {}


def _extract_author_from_about(content: str) -> str:
    """Extract author name from about-the-author.md (e.g. 'Name is a former...' -> Name)."""
    if not content:
        return ""
    first_block = content.lstrip("#").strip()
    for line in first_block.splitlines():
        line = line.strip().lstrip("#").strip()
        if not line:
            continue
        if re.match(r"^about\s+the\s+author$", line, re.IGNORECASE):
            continue
        match = re.match(r"^([^.\n]+)\s+is\s+a\s+", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        if re.match(r"^[\w\s\-']+$", line) and 2 <= len(line.split()) <= 5:
            return line
    return ""


def _extract_description_from_intro(content: str, max_chars: int = 4000) -> str:
    """Build description from introduction.md (first paragraphs, no headers)."""
    if not content:
        return ""
    text = re.sub(r"^#+\s*\S.*$", "", content, flags=re.MULTILINE).strip()
    paragraphs = []
    current = []
    length = 0
    for line in text.splitlines():
        if line.strip():
            current.append(line.strip())
        else:
            if current:
                para = " ".join(current)
                if length + len(para) + 1 > max_chars:
                    remaining = max_chars - length - 4
                    if remaining > 0:
                        paragraphs.append(para[:remaining].rsplit(" ", 1)[0] + " ...")
                    break
                paragraphs.append(para)
                length += len(para) + 1
                current = []
        if length >= max_chars:
            break
    if current and length < max_chars:
        para = " ".join(current)
        if length + len(para) + 1 <= max_chars:
            paragraphs.append(para)
        else:
            remaining = max_chars - length - 4
            if remaining > 0:
                paragraphs.append(para[:remaining].rsplit(" ", 1)[0] + " ...")
    return " ".join(paragraphs).replace("\n", " ").strip()


def load_epub_metadata(book_dir: Path) -> dict:
    """
    Load EPUB metadata from the book folder (toc, introduction, about-the-author) and optional
    input/metadata.md or input/metadata.yaml overrides.
    Returns dict with: title, subtitle, author, description, language, identifier, keywords (list),
    publisher, date (publication date, W3CDTF e.g. 2026-04-15).
    Used when building EPUB so the OPF gets Dublin Core metadata.
    """
    overrides = {}
    input_dir = book_dir.parent / "input"
    if (input_dir / "metadata.yaml").exists():
        overrides = _try_load_yaml_metadata(input_dir / "metadata.yaml")
    if (input_dir / "metadata.md").exists():
        overrides = {**overrides, **_parse_simple_metadata(load_text(input_dir / "metadata.md"))}

    toc_content = load_text(book_dir / "toc.md")
    title, subtitle, _ = parse_toc(toc_content)
    intro = load_text(book_dir / "introduction.md")
    about = load_text(book_dir / "about-the-author.md")

    author = (overrides.get("author") or "").strip() or _extract_author_from_about(about)
    description = (overrides.get("description") or "").strip() or _extract_description_from_intro(intro)
    language = (overrides.get("language") or "en").strip()
    identifier = (overrides.get("identifier") or "").strip()
    keywords = overrides.get("keywords")
    if isinstance(keywords, str):
        keywords = [k.strip().strip('"').strip("'") for k in keywords.split(",") if k.strip()]
    elif isinstance(keywords, list):
        keywords = [str(k).strip().strip('"').strip("'") for k in keywords if k]
    else:
        keywords = []

    # EPUB dc:publisher and dc:date — optional overrides from input/metadata.{md,yaml}
    publisher = str(overrides.get("publisher") or "").strip()
    date_raw = overrides.get("date") or overrides.get("publication_date")
    if date_raw is not None and hasattr(date_raw, "strftime"):
        pub_date = date_raw.strftime("%Y-%m-%d")
    else:
        date_str = str(date_raw or "").strip()
        pub_date = _normalise_metadata_date(date_str) if date_str else ""

    return {
        "title": (overrides.get("title") or title).strip(),
        "subtitle": (overrides.get("subtitle") or subtitle).strip(),
        "author": author,
        "description": description,
        "language": language,
        "identifier": identifier,
        "keywords": keywords,
        "publisher": publisher,
        "date": pub_date,
    }


def inject_pdf_metadata(pdf_path: Path, meta: dict) -> None:
    """
    Write PDF document info (Title, Author, Subject, Keywords) into an existing PDF.
    Uses pypdf; no-op if pypdf is not available. meta: same dict as load_epub_metadata().
    """
    if PdfReader is None or PdfWriter is None:
        return
    if not pdf_path.exists():
        return
    title = meta.get("title") or ""
    subtitle = (meta.get("subtitle") or "").strip()
    full_title = f"{title}: {subtitle}" if subtitle else title
    author = (meta.get("author") or "").strip()
    description = _description_plain_for_pdf((meta.get("description") or "").strip())
    keywords = meta.get("keywords") or []
    keywords_str = ", ".join(str(k) for k in keywords if k)

    pdf_meta = {}
    if full_title:
        pdf_meta["/Title"] = full_title
    if author:
        pdf_meta["/Author"] = author
    if description:
        pdf_meta["/Subject"] = description
    if keywords_str:
        pdf_meta["/Keywords"] = keywords_str

    if not pdf_meta:
        return
    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(pdf_meta)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=pdf_path.parent) as tmp:
            writer.write(tmp)
            tmp_path = Path(tmp.name)
        tmp_path.replace(pdf_path)
    except Exception:
        pass  # Leave PDF unchanged on any error


def _html_image_src_for_pdf_repo_base(html: str) -> str:
    """
    PDF is rendered with WeasyPrint using base_url = repository root.

    Chapters live under book/*.md and reference images as images/foo.png.
    That becomes <img src="images/foo.png">, which resolves to repo/images/
    (wrong). Files are at repo/book/images/foo.png.

    Rewrite img src only when it starts with images/ (not already book/images/).
    Cover and similar assets already use book/images/... and are unchanged.
    """
    return re.sub(
        r'(\ssrc=)(["\'])images/',
        r"\1\2book/images/",
        html,
        flags=re.IGNORECASE,
    )


def markdown_to_html(md: str) -> str:
    """Convert markdown to HTML with sensible extensions."""
    if not markdown:
        raise SystemExit("Install markdown: pip install markdown")
    html = markdown.markdown(
        md,
        extensions=["extra", "nl2br"],
        extension_configs={"extra": {}},
    )
    return html


def _add_intro_subhead_class(html: str) -> str:
    """Add class intro-subhead to <p> that contain only <strong>...</strong>, so we can keep them with the next paragraph (no page break between subhead and body)."""
    return re.sub(
        r"<p>\s*<strong>([^<]*)</strong>\s*</p>",
        r'<p class="intro-subhead"><strong>\1</strong></p>',
        html,
    )


def _flatten_definition_body(body_html: str) -> str:
    """
    Flatten definition body to inline content (replace <p>...</p> with <br/><br/>)
    so the definition box has one block = one drawn box in print.
    """
    s = body_html.strip()
    # Remove any stray "Definition: Term" paragraph (markdown can merge two defs into one blockquote)
    s = re.sub(r"<p>\s*<strong>Definition\s*:\s*[^<]+</strong>\s*</p>\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<strong>Definition\s*:\s*[^<]+</strong>\s*<br\s*/?>\s*", "", s, flags=re.IGNORECASE)
    # Paragraphs to line breaks
    s = re.sub(r"<p>\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*</p>", "<br/><br/>", s, flags=re.IGNORECASE)
    s = s.strip()
    if s.endswith("<br/><br/>"):
        s = s[:-10]
    return s


def _split_blockquote_definitions(inner: str) -> list[tuple[str, str]]:
    """
    Split blockquote inner HTML into separate (title, body_html) definition segments.
    A blockquote can contain multiple definitions; "Definition: Term" can be its own
    paragraph or in the middle of a paragraph (e.g. body text then <br/> then Definition: B).
    """
    segments = []
    current_title = None
    current_body_parts = []
    # Process each <p>...</p>
    rest = inner.strip()
    while rest:
        p_match = re.search(r"<p>(.*?)</p>", rest, re.DOTALL | re.IGNORECASE)
        if not p_match:
            break
        p_content = p_match.group(1)
        term_match = re.search(
            r"Definition\s*:\s*([^<]+)",
            p_content,
            re.IGNORECASE,
        )
        if term_match:
            term = term_match.group(1).strip()
            # Split paragraph into before and after "Definition: Term"
            before = p_content[: term_match.start()].strip()
            # Remove trailing opening tag (e.g. "<strong>") that precedes "Definition:"
            before = re.sub(r"<strong>\s*$", "", before, flags=re.IGNORECASE).strip()
            after_start = term_match.end()
            after = p_content[after_start:].strip()
            after = re.sub(r"^</strong>\s*", "", after, flags=re.IGNORECASE)
            # If there was text before "Definition: Term", it belongs to previous definition
            if before and current_title is not None:
                current_body_parts.append(f"<p>{before}</p>")
            if current_title is not None:
                segments.append((current_title, "".join(current_body_parts)))
            current_title = term
            current_body_parts = [f"<p>{after}</p>"] if after else []
        else:
            # No Definition: in this paragraph; it's body for current definition
            if current_title is not None:
                current_body_parts.append(rest[: p_match.end()])
            # else skip leading non-definition paragraphs
        rest = rest[p_match.end() :]
    if current_title is not None:
        segments.append((current_title, "".join(current_body_parts)))
    return segments


def wrap_definition_blocks(html: str) -> str:
    """
    Convert blockquotes containing 'Definition:' into one styled box per definition.
    Splits one blockquote with multiple definitions into separate boxes. Flattens
    each to a single block (title + body as inline) so the PDF draws one box each.
    """
    result = []
    pos = 0
    while True:
        start = html.find("<blockquote>", pos)
        if start == -1:
            result.append(html[pos:])
            break
        end = html.find("</blockquote>", start)
        if end == -1:
            result.append(html[pos:])
            break
        end += len("</blockquote>")
        block = html[start:end]
        if "Definition:" not in block:
            result.append(html[pos:end])
            pos = end
            continue
        inner_start = start + len("<blockquote>")
        inner_end = end - len("</blockquote>")
        inner = html[inner_start:inner_end]
        segments = _split_blockquote_definitions(inner)
        if not segments:
            # Fallback: single definition from first paragraph
            first_p = re.search(r"<p>(.*?)</p>", inner, re.DOTALL)
            title = "Definition"
            body = inner
            if first_p:
                first_p_content = first_p.group(1)
                term_match = re.search(
                    r"Definition\s*:\s*([^<]+)",
                    first_p_content,
                    re.IGNORECASE,
                )
                if term_match:
                    title = term_match.group(1).strip()
                body = inner[first_p.end() :].strip()
            segments = [(title, body)]
        result.append(html[pos:start])
        for title, body_html in segments:
            flat_body = _flatten_definition_body(body_html)
            # One box: wrap everything in a single <p> so .definition-box has one block child
            # (one box per block child in print; avoid span/div that could split)
            result.append('<div class="definition"><div class="definition-box">')
            result.append("<p class=\"definition-single\">")
            result.append(f'<span class="definition-title">{html_module.escape(title)}</span>')
            if flat_body:
                result.append("<br/><br/>")
                result.append(flat_body)
            result.append("</p></div><div class=\"definition-box-end\"></div></div>")
        pos = end
    return "".join(result)


def _case_study_extract_title_and_body(fragment: str) -> tuple[str, str]:
    """
    Extract case study title from <h2>Case Study: Title</h2> and return (title, body).
    Body is the rest of the fragment (block structure kept so box-decoration-break works per page).
    """
    match = re.search(
        r"<h2>\s*Case\s+Study\s*:\s*([^<]+)</h2>\s*",
        fragment,
        re.IGNORECASE,
    )
    if not match:
        return "Case Study", fragment
    title = match.group(1).strip()
    body = fragment[match.end() :].strip()
    return title, body


def wrap_case_study_sections(html: str) -> str:
    """
    Wrap content from <h2>Case Study: ...</h2> until the next <h2> in a box.
    Keeps block structure (p, h3, ul) so when the box spans pages, box-decoration-break: clone
    draws a border/background on each page fragment.
    """
    result = []
    pos = 0
    while True:
        match = re.search(
            r"<h2>\s*Case\s+Study\s*:\s*[^<]+</h2>",
            html[pos:],
            re.IGNORECASE,
        )
        if not match:
            result.append(html[pos:])
            break
        start_in_slice = match.start()
        section_start = pos + start_in_slice
        section_end = pos + match.end()
        next_h2 = html.find("<h2>", section_end)
        if next_h2 == -1:
            next_h2 = len(html)
        fragment = html[section_start:next_h2]
        title, body = _case_study_extract_title_and_body(fragment)
        result.append(html[pos:section_start])
        result.append('<div class="case-study"><div class="case-study-box">')
        result.append(f'<div class="case-study-title">{html_module.escape(title)}</div>')
        if body:
            result.append(body)
        result.append("</div></div>")
        pos = next_h2
    return "".join(result)


def build_chapter_html(repo: Path, chapter_num: int, strip_handoff: bool = True) -> str:
    """
    Load chapter markdown from book/ (chapter-NN.md or NN - Title.md), convert to HTML,
    apply definition and case-study wrappers. When strip_handoff is True (e.g. full build),
    remove Handoff sections from the PDF. When False (dry-run), keep Handoff sections.
    """
    book_dir = repo / "book"
    path = resolve_chapter_path(book_dir, chapter_num)
    if path is None:
        return ""
    md = load_text(path)
    # Strip ## Handoff section (e.g. ## Handoff — Writer — Chapter nn) so it is not in HTML/PDF
    if strip_handoff and "## Handoff" in md:
        # Match ## Handoff at start of file or after newline (covers "## Handoff — ..." or "## Handoff: ...")
        md = re.split(r"(?:^|\n)## Handoff\b", md, maxsplit=1)[0].rstrip()
    html = markdown_to_html(md)
    html = wrap_definition_blocks(html)
    html = wrap_questions_section_and_remove_hr(html)
    html = reposition_footnotes_before_questions(html)
    html = wrap_case_study_sections(html)
    return html


def chapter_number_word(num: int) -> str:
    """Spell chapter number for display (e.g. 1 -> 'One')."""
    words = (
        "One", "Two", "Three", "Four", "Five", "Six",
        "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
    )
    return words[num - 1] if 1 <= num <= len(words) else str(num)


def strip_first_h1(html: str) -> str:
    """Remove the first <h1>...</h1> so we can use .chapter-number and .chapter-title instead."""
    match = re.search(r"<h1>\s*.*?\s*</h1>", html, re.DOTALL | re.IGNORECASE)
    if not match:
        return html
    return html[: match.start()].rstrip() + html[match.end() :].lstrip()


def wrap_questions_section_and_remove_hr(html: str) -> str:
    """
    Wrap the 'Questions for the Board' h2 (and variants) in .questions-section so it
    starts on a new page. Remove all hr so there are no horizontal rules between sections.
    """
    # Remove horizontal rules (no line between sections)
    html = re.sub(r"<hr\s*/?>", "", html, flags=re.IGNORECASE)
    # Wrap <h2>Questions for the Board</h2> or <h2>Questions for the Board: ...</h2>
    html = re.sub(
        r"<h2>\s*Questions\s+for\s+the\s+Board\s*[^<]*</h2>",
        r'<div class="questions-section">\g<0></div>',
        html,
        flags=re.IGNORECASE,
    )
    return html


def reposition_footnotes_before_questions(html: str) -> str:
    """
    Move the footnote block (from Python markdown extra) to immediately before the
    Questions section. Wrap in .chapter-footnotes-anchor (page break + bottom align)
    and .chapter-footnotes (typography). Questions still start on the following page.
    """
    # Match <div class="footnote">...</div> (handles fn:1 or fn-1 id formats)
    footnote_match = re.search(
        r'<div\s+class="footnote">(.*?)</div>\s*$',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    if not footnote_match:
        return html
    footnote_block = footnote_match.group(0)
    html_without_footnotes = html[: footnote_match.start()].rstrip() + html[footnote_match.end() :]

    # Insert before <div class="questions-section">
    qs_match = re.search(r'<div\s+class="questions-section">', html_without_footnotes, re.IGNORECASE)
    if not qs_match:
        # No Questions section; same wrapper as chapters with Questions (break + bottom align)
        wrapped = f'<div class="chapter-footnotes-anchor"><div class="chapter-footnotes">{footnote_block}</div></div>'
        return html_without_footnotes + "\n" + wrapped

    # Wrap footnote block and insert before Questions
    wrapped = f'<div class="chapter-footnotes-anchor"><div class="chapter-footnotes">{footnote_block}</div></div>'
    return (
        html_without_footnotes[: qs_match.start()].rstrip()
        + "\n"
        + wrapped
        + "\n"
        + html_without_footnotes[qs_match.start() :]
    )


def inject_ordered_list_numbers(html: str) -> str:
    """
    Prepend "1. ", "2. ", ... to each <li> inside <ol> and wrap in a block so each item
    starts on a new line in PDF (explicit block display for list items).
    Reads the 'start' attribute if present to support continuous numbering.

    We do not insert <br/> between </li><li>: EPUBCheck forbids <br/> as a direct child of
    <ol>/<ul> (RSC-005), so EPUB builds strip those breaks anyway; keeping them out of PDF
    avoids double vertical spacing (block <li> + extra line break).
    """
    # Process all ol elements
    def replace_ol(match: re.Match) -> str:
        inner = match.group(1)
        # Check for start attribute (e.g. from make_footnotes_continuous)
        num_match = re.search(r'start="(\d+)"', match.group(0), re.IGNORECASE)
        num = int(num_match.group(1)) if num_match else 1

        def repl_li(li_match: re.Match) -> str:
            nonlocal num
            # Preserve id, class, and other attributes (footnote anchors use id on <li>).
            li_attrs = li_match.group(1)
            content = li_match.group(2)
            result = f'<li{li_attrs}><div class="li-block"><span class="list-number">{num}. </span>{content}</div></li>'
            num += 1
            return result

        inner = re.sub(r"<li([^>]*)>(.*?)</li>", repl_li, inner, flags=re.DOTALL)
        start_attr = f' start="{int(num_match.group(1))}"' if num_match else ""
        return f"<ol{start_attr}>" + inner + "</ol>"
    
    html_processed = re.sub(r"<ol[^>]*>(.*?)</ol>", replace_ol, html, flags=re.DOTALL)
    return html_processed


# Part separator pages: chapter number that starts each part -> part title (aligned with book/toc.md)
# Part II ends at Ch 10; Part III is Ch 11–12; Part IV is Ch 13–16.
PART_TITLES = {
    1: "Part I: Building Momentum",
    3: "Part II: The Model",
    11: "Part III: The European Advantage",
    13: "Part IV: The CEO's Playbook",
}
# Anchor ids for part separator divs (for TOC links and correct page numbers)
PART_IDS = {1: "part1", 3: "part2", 11: "part3", 13: "part4"}


def build_toc_html(
    chapters_included: list[int],
    toc_chapters: list[tuple[int, str]],
    *,
    has_introduction: bool = False,
) -> str:
    """
    Build TOC with nested structure: Introduction standalone; each Part as a section
    with a nested list of its chapters. Each link uses target-counter for correct
    page numbers in the PDF.
    """
    toc_by_num = dict(toc_chapters)
    part_starts = sorted(PART_TITLES.keys())
    items = []

    if has_introduction:
        items.append('<li><a href="#introduction">Introduction</a></li>')

    for i, part_start in enumerate(part_starts):
        next_start = part_starts[i + 1] if i + 1 < len(part_starts) else 999
        part_chapters = [n for n in chapters_included if part_start <= n < next_start]
        if not part_chapters:
            continue
        part_id = PART_IDS[part_start]
        part_title = html_module.escape(PART_TITLES[part_start])
        sub_items = []
        for num in part_chapters:
            name = chapter_title_plain(toc_by_num.get(num, f"Chapter {num}"))
            sub_items.append(
                f'<li><a href="#ch{num:02d}">Ch. {num} - {html_module.escape(name)}</a></li>'
            )
        items.append(
            f'<li class="toc-part"><a href="#{part_id}">{part_title}</a><ul>{"".join(sub_items)}</ul></li>'
        )

    return "<ul>" + "".join(items) + "</ul>"


def build_epub_nav_toc(
    chapters_included: list[int],
    toc_chapters: list[tuple[int, str]],
    *,
    has_introduction: bool,
) -> tuple:
    """
    EPUB navigation: Title, optional Introduction, Parts I–IV each wrapping their chapters
    (same boundaries as build_toc_html / PART_TITLES), then About the Author.

    Uses ebooklib nested (Section, (Link, ...)) so nav.xhtml shows Part headings; Section
    has no href so the heading is a span (EPUB3); NCX inherits first chapter href for the
    part node (ebooklib behaviour).
    """
    toc_by_num = dict(toc_chapters)
    entries: list = []

    entries.append(epub.Link("title.xhtml", "Title", "title"))
    if has_introduction:
        entries.append(epub.Link("introduction.xhtml", "Introduction", "introduction"))

    part_starts = sorted(PART_TITLES.keys())
    for i, part_start in enumerate(part_starts):
        next_start = part_starts[i + 1] if i + 1 < len(part_starts) else 999
        part_chapters = [n for n in chapters_included if part_start <= n < next_start]
        if not part_chapters:
            continue
        part_title = PART_TITLES[part_start]
        chapter_links = tuple(
            epub.Link(
                f"ch{num:02d}.xhtml",
                f"Chapter {num} - {chapter_title_plain(toc_by_num.get(num, f'Chapter {num}'))}",
                f"ch{num:02d}",
            )
            for num in part_chapters
        )
        entries.append((epub.Section(part_title), chapter_links))

    entries.append(epub.Link("about.xhtml", "About the Author", "about"))
    return tuple(entries)


def get_css(for_pdf: bool = True) -> str:
    """
    Return CSS for print typography and layout.
    When for_pdf=True uses WeasyPrint @page with margins and @bottom-right for page numbers.
    When for_pdf=False uses simple margin @page (for HTML preview).
    """
    pf = PRINT_PAGE
    w, h = pf["width"], pf["height"]
    t, r, b, l = pf["top"], pf["right"], pf["bottom"], pf["left"]
    # Inner/outer horizontal margins for facing pages (gutter wider than outer edge by GUTTER_EXTRA).
    m_inner = f"calc({l} + {GUTTER_EXTRA})"
    m_outer = f"calc({l} - {GUTTER_EXTRA})"
    # Numbered body pages use a larger top margin so body text sits lower; running heads stay in the top margin band.
    t_content = f"calc({t} + {CONTENT_TOP_EXTRA_BELOW_HEADER})"
    # Type area height on content pages: used to bottom-align chapter footnotes on their page
    content_area_height = f"calc({h} - {t} - {CONTENT_TOP_EXTRA_BELOW_HEADER} - {b})"
    if for_pdf:
        # WeasyPrint: front = no page number; content = numbered from 1.
        # Use built-in page counter: first content page resets to 1 (contentfirst),
        # so target-counter() in TOC works. See WeasyPrint #2114 workaround.
        page_setup = f"""
    /* PAGE SETUP: front = no number; contentfirst = reset page 1; content = continue */
    @page {{
        size: {w} {h};
        margin: {t} {r} {b} {l};
    }}
    @page cover {{
        size: {w} {h};
        margin: 0;
        @top-center {{ content: none; }}
        @bottom-right {{ content: none; }}
    }}
    @page front {{
        size: {w} {h};
        margin: {t} {r} {b} {l};
        @top-center {{ content: none; }}
        @bottom-right {{ content: none; }}
    }}
    /* First numbered page (introduction p.1): recto margins + reset counter */
    @page contentfirst:first {{
        counter-reset: page 1;
        size: {w} {h};
        margin: {t_content} {m_outer} {b} {m_inner};
        @top-right {{
            content: string(chapter-num) string(chapter-title);
            font-family: "Raleway", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-right {{
            content: counter(page);
            font-family: "Lora", serif;
            font-size: 8pt;
            color: #555;
        }}
    }}
    /* Left (even) pages: inner margin on the right; chapter title and page number on the left */
    @page contentfirst:left {{
        size: {w} {h};
        margin: {t_content} {m_inner} {b} {m_outer};
        @top-left {{
            content: string(chapter-num) string(chapter-title);
            font-family: "Raleway", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-left {{
            content: counter(page);
            font-family: "Lora", serif;
            font-size: 8pt;
            color: #555;
        }}
    }}
    /* Right (odd) pages: inner margin on the left */
    @page contentfirst:right {{
        size: {w} {h};
        margin: {t_content} {m_outer} {b} {m_inner};
        @top-right {{
            content: string(chapter-num) string(chapter-title);
            font-family: "Raleway", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-right {{
            content: counter(page);
            font-family: "Lora", serif;
            font-size: 8pt;
            color: #555;
        }}
    }}
    @page content:left {{
        size: {w} {h};
        margin: {t_content} {m_inner} {b} {m_outer};
        @top-left {{
            content: string(chapter-num) string(chapter-title);
            font-family: "Raleway", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-left {{
            content: counter(page);
            font-family: "Lora", serif;
            font-size: 8pt;
            color: #555;
        }}
    }}
    @page content:right {{
        size: {w} {h};
        margin: {t_content} {m_outer} {b} {m_inner};
        @top-right {{
            content: string(chapter-num) string(chapter-title);
            font-family: "Raleway", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-right {{
            content: counter(page);
            font-family: "Lora", serif;
            font-size: 8pt;
            color: #555;
        }}
    }}"""
    else:
        page_setup = f"""
    @page {{
        size: {w} {h};
        margin: {t} {r} {b} {l};
    }}"""
    return page_setup + f"""

    /* BASE TYPOGRAPHY: Lora for body text, Raleway for headings */
    body {{
        font-family: "Lora", serif;
        font-size: 9pt;
        line-height: 1.6;
        color: #111;
        text-rendering: optimizeLegibility;
    }}

    p {{
        margin: 0 0 0.6em 0;
        text-align: justify;
        text-indent: 1em;
        widows: 2;
        orphans: 2;
    }}

    p:first-of-type {{
        text-indent: 0;
    }}

    strong {{ font-weight: bold; }}
    em {{ font-style: italic; }}

    /* Front matter: no page number (page type "front") */
    .front-matter {{
        page: front;
    }}

    /* COVER PAGE: full-page image, no margins; image fills page and is centered if aspect ratio differs */
    .cover-page {{
        page: cover;
        margin: 0;
        padding: 0;
        width: {w};
        height: {h};
        page-break-after: always;
        box-sizing: border-box;
    }}
    .cover-page img {{
        display: block;
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
    }}

    /* BLANK PAGE: front matter filler so recto/verso sequence is correct (e.g. page 2, 4, 7) */
    .blank-page {{
        page: front;
        page-break-after: always;
        height: 0;
        overflow: hidden;
    }}

    /* EPIGRAPH PAGE: page 8, left-hand; blank or optional epigraph text */
    .epigraph-page {{
        page: front;
        page-break-after: always;
        min-height: 1em;
    }}

    /* HALF TITLE: page 3, right-hand */
    .half-title-page {{
        text-align: center;
        page-break-after: always;
    }}

    .half-title-page h1 {{
        margin-top: 2in;
        font-family: "Raleway", sans-serif;
        font-size: 24pt;
        font-weight: bold;
    }}

    /* TITLE PAGE: reduced top and spacing */
    .title-page {{
        text-align: center;
        page-break-after: always;
    }}

    .title-page h1 {{
        margin-top: 2in;
        font-family: "Raleway", sans-serif;
        font-size: 24pt;
        font-weight: bold;
    }}

    .title-page .subtitle {{
        margin-top: 0.8em;
        font-size: 12pt;
        font-style: italic;
        color: #444;
    }}

    .title-page .author {{
        margin-top: 2in;
        font-size: 12pt;
        letter-spacing: 0.7pt;
    }}

    /* COPYRIGHT PAGE: content anchored at bottom of page */
    .copyright-page {{
        font-size: 8pt;
        color: #555;
        page-break-after: always;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        min-height: 7in;
    }}

    .copyright-page p {{
        text-indent: 0;
        margin-bottom: 0.35em;
    }}

    /* DEDICATION PAGE */
    .dedication-page {{
        page-break-after: always;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 1.3in;
        min-height: 7in;
    }}

    .dedication-page p {{
        text-indent: 0;
        text-align: center;
        font-style: italic;
        font-size: 9pt;
        line-height: 1.3;
        margin-bottom: 0.5em;
    }}

    /* TABLE OF CONTENTS: tighter */
    .toc {{
        page-break-after: always;
    }}

    /* INTRODUCTION: first numbered page (page 1 in footer); always starts on right-hand page if possible */
    .introduction {{
        page: contentfirst;
        page-break-before: right;
    }}

    .introduction h1 {{
        text-align: center;
        margin-top: 1.4in;
        font-family: "Raleway", sans-serif;
        font-size: 22pt;
        font-weight: bold;
        string-set: chapter-title content(text), chapter-num "";
    }}

    .toc h2 {{
        text-align: center;
        font-family: "Raleway", sans-serif;
        font-size: 14pt;
        margin-bottom: 1.2em;
        font-weight: normal;
    }}

    .toc ul {{
        list-style: none;
        padding-left: 0;
    }}

    .toc li {{
        margin-bottom: 0.5em;
        font-size: 9pt;
        text-indent: 0;
    }}

    /* Part titles: slightly larger and medium weight for clear section headers */
    .toc li.toc-part {{
        font-size: 9pt;
        font-weight: 500;
    }}

    /* Nested TOC: Part titles at top level; chapters indented under each part */
    .toc ul ul {{
        margin: 0.25em 0 0.75em 1.25em;
        padding-left: 0;
    }}

    .toc ul ul li {{
        font-size: 9pt;
        line-height: 1.25;
        margin-bottom: 0.4em;
    }}

    .toc a {{
        color: #111;
        text-decoration: none;
    }}

    /* TOC: show page number of target (leader dots + target-counter uses page so TOC shows correct numbers) */
    .toc a::after {{
        content: leader(dotted) target-counter(attr(href url), page);
        font-variant-numeric: tabular-nums;
    }}

    /* TOC: static HTML list (WeasyPrint) */

    /* CHAPTER OPENING: all chapters use content (numbering continues from introduction). */
    /* Chapters always start on a right (recto) page; blank inserted if needed */
    .chapter {{
        page: content;
        page-break-before: right;
    }}

    .chapter-number {{
        text-align: center;
        margin-top: 1.4in;
        font-family: "Raleway", sans-serif;
        font-size: 9pt;
        letter-spacing: 2.75pt;
        text-transform: uppercase;
        color: #777;
    }}

    /* Chapter title: capture for running header (string-set used in @page @top-center) */
    .chapter-title {{
        text-align: center;
        margin-top: 1em;
        font-family: "Raleway", sans-serif;
        font-size: 22pt;
        font-weight: bold;
        /* One line in running header; <br/> in body uses data-title-plain (not content(text)) */
        string-set: chapter-title attr(data-title-plain), chapter-num attr(data-ch);
    }}

    /* Hidden element: "Chapter N - Title" for reference; TOC is static HTML with anchors */
    .toc-entry-hidden {{
        position: absolute;
        left: -9999px;
        font-size: 0;
        height: 0;
        overflow: hidden;
        visibility: hidden;
    }}

    .chapter-divider {{
        width: 60px;
        height: 1px;
        background: #000;
        margin: 1.2em auto 2em auto;
    }}

    /* CHAPTER FIGURES: natural flow, no forced size; max-width only to avoid overflow */
    .chapter img {{
        display: block;
        max-width: 100%;
        height: auto;
        margin: 1.2em 0;
    }}

    /* SECTION HEADINGS: keep with next paragraph so header is never split from following content */
    h2 {{
        font-family: "Raleway", sans-serif;
        font-size: 13pt;
        font-weight: normal;
        margin-top: 1.4em;
        margin-bottom: 0.5em;
        page-break-after: avoid;
    }}
    h2 + p {{
        page-break-before: avoid;
    }}

    h3 {{
        font-family: "Raleway", sans-serif;
        font-size: 11pt;
        margin-top: 1.1em;
        margin-bottom: 0.4em;
        font-style: italic;
        font-weight: normal;
        page-break-after: avoid;
    }}
    h3 + p {{
        page-break-before: avoid;
    }}

    /* BLOCKQUOTE (general) */
    blockquote {{
        margin: 1em 1.2em;
        font-style: italic;
        font-size: 9pt;
    }}

    /* LISTS: unordered = native bullets; ordered = inject_ordered_list_numbers() (no native markers) */
    ul, ol {{
        margin: 0.6em 0 0.8em 0;
        display: block;
    }}
    ul {{
        padding-left: 1.8em;
        list-style-type: disc;
        list-style-position: outside;
    }}
    ol {{
        list-style: none;
        padding-left: 0;
        margin-left: 0;
    }}
    ul li {{
        display: list-item;
        margin-top: 0.35em;
        margin-bottom: 0.35em;
    }}
    ul li:first-child {{
        margin-top: 0;
    }}
    /* Ordered list: flex row so numerals sit in a fixed left column; body text wraps in a hanging indent */
    ol > li {{
        display: block;
        margin: 0;
        padding: 0;
    }}
    ol > li > .li-block {{
        display: flex;
        align-items: flex-start;
        gap: 0.55em;
        margin-bottom: 0.78em;
    }}
    ol > li:last-child > .li-block {{
        margin-bottom: 0.5em;
    }}
    ol > li > .li-block > .list-number {{
        flex-shrink: 0;
        min-width: 2.25em;
        text-align: right;
        margin-right: 0;
        line-height: 1.35;
    }}
    .list-number {{
        margin-right: 0;
    }}
    ol > li > .li-block > p {{
        flex: 1 1 0%;
        min-width: 0;
        margin: 0;
    }}

    /* TABLES: bordered grid; keep entire table on one page (no split across page break) */
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
        font-family: "Gill Sans Nova", "Gill Sans", "Gill Sans MT", sans-serif;
        font-size: 9pt;
        page-break-inside: avoid;
    }}
    table th,
    table td {{
        border: 1px solid #666;
        padding: 0.4em 0.6em;
        text-align: left;
        vertical-align: top;
    }}
    table thead th {{
        background: #e8e8e8;
        font-weight: bold;
    }}

    /* CASE STUDY: starts on new page; entire section in one grey box; Gill Sans Nova, smaller size, tighter spacing */
    .case-study {{
        margin: 1.5em 0;
        page-break-before: always;
        font-family: "Gill Sans Nova", "Gill Sans", "Gill Sans MT", sans-serif;
        font-size: 9pt;
        line-height: 1.25;
    }}

    /* Box per page: when case study spans pages, each fragment gets its own border/background (clone). */
    .case-study-box {{
        padding: 1.2em 1.5em;
        border: 1px solid #999;
        background: #e8e8e8;
        font-family: "Gill Sans Nova", "Gill Sans", "Gill Sans MT", sans-serif;
        font-size: 9pt;
        line-height: 1.25;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
        display: block;
    }}

    /* Case study title: 13pt per spec */
    .case-study-title {{
        font-style: normal;
        font-weight: bold;
        letter-spacing: 1.1pt;
        font-size: 13pt;
        margin-bottom: 0.8em;
    }}

    .case-study-box p {{
        margin: 0 0 0.5em 0;
        text-indent: 0;
    }}
    .case-study-box h3 {{
        font-size: 11pt;
        font-style: italic;
        font-weight: normal;
        margin-top: 0.8em;
        margin-bottom: 0.3em;
    }}

    /* DEFINITION: one box per definition; no extra white space after (removed forced spacer). */
    .definition {{
        margin: 1.2em 0 0.5em 0;
    }}

    /* No visible spacer after definition box */
    .definition-box-end {{
        display: none;
    }}

    /* Space between two definitions in a row so each box is distinct */
    .definition + .definition {{
        margin-top: 1em;
    }}

    /* Definition box: left-aligned (not justified); text wraps to next line if it doesn't fit */
    .definition-box {{
        padding: 1em 1.5em;
        border: 1px solid #ccc;
        border-left: 3px solid #000;
        background: #fafafa;
        font-size: 9pt;
        page-break-inside: avoid;
        text-align: left;
    }}

    /* Definition term: allow wrap so long titles (e.g. "THE AI TRANSFORMATION FRAMEWORK") go to next line */
    .definition-title {{
        font-family: "Raleway", sans-serif;
        font-size: 10pt;
        font-weight: normal;
        letter-spacing: 2pt;
        text-transform: uppercase;
        color: #555;
        white-space: normal;
    }}

    /* Intro subheads (e.g. "Why a European perspective"): keep on one line so they don't break mid-word */
    .introduction strong {{
        white-space: nowrap;
    }}

    /* Keep intro subhead (p with only strong) with the following paragraph: no page break between them */
    .introduction p.intro-subhead {{
        break-after: avoid;
    }}

    /* Single paragraph = one block = one box; left-aligned, wraps inside box */
    .definition-single {{
        text-indent: 0;
        margin: 0;
        text-align: left;
    }}

    /* Blank page in content flow (after last chapter, after About the Author).
       Use page-break-before so the blank occupies its own page; min-height ensures it renders. */
    .blank-content-page {{
        page: content;
        page-break-before: always;
        min-height: 1px;
        overflow: hidden;
    }}

    /* BACK MATTER: same content page type; start on right (recto) page so About the Author aligns correctly */
    .back-matter {{
        page: content;
        page-break-before: right;
        /* Clear running-header strings from the last chapter; otherwise string(chapter-*) stays Ch N. */
        string-set: chapter-title "", chapter-num "";
    }}

    .back-matter h2 {{
        text-align: center;
        font-family: "Raleway", sans-serif;
        font-size: 13pt;
        margin-bottom: 1em;
    }}

    .index-placeholder {{
        font-style: italic;
        color: #666;
        text-indent: 0;
    }}

    /* Remove horizontal rules between sections */
    hr {{
        display: none;
    }}

    /* FOOTNOTES: end-of-chapter list in normal flow (not float:footnote — avoids overflow
       onto the Questions page). .chapter-footnotes-anchor: page break, then min-height =
       full type area + flex-end so the note block sits at the bottom of that page (short
       lists leave space above). Long lists extend the anchor past min-height and paginate
       normally. .questions-section keeps page-break-before: always for the next page. */
    .chapter-footnotes-anchor {{
        page-break-before: always;
        min-height: {content_area_height};
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        box-sizing: border-box;
        width: 100%;
        max-width: 100%;
        min-width: 0;
    }}
    sup a.footnote-ref,
    sup a.footnote-ref:hover,
    sup a.footnote-ref:visited {{
        font-size: 0.65em;
        color: #555;
        text-decoration: none;
        font-family: "Gill Sans Nova", "Gill Sans", "Gill Sans MT", sans-serif;
    }}
    .chapter-footnotes {{
        font-family: "Gill Sans Nova", "Gill Sans", "Gill Sans MT", sans-serif;
        font-size: 7.25pt;
        line-height: 1.0;
        color: #555;
        margin-top: 0;
        margin-bottom: 0;
        padding: 0;
        page-break-inside: auto;
        display: block;
        clear: both;
        /* Critical flex child of .chapter-footnotes-anchor: min-width:0 allows shrink below
           longest unbreakable string so overflow-wrap applies inside the type area. */
        width: 100%;
        max-width: 100%;
        min-width: 0;
        overflow-wrap: anywhere;
    }}
    .chapter-footnotes .footnote {{
        min-width: 0;
        max-width: 100%;
    }}
    /* When footnotes are in the footnote block, use Gill Sans and reset numbering styles */
    .chapter-footnotes .footnote ol {{
        margin: 0;
        padding-left: 0;
        list-style: none;
    }}
    .chapter-footnotes .footnote li {{
        display: block;
        margin: 0 0 0.8em 0;
        padding: 0;
    }}
    .chapter-footnotes .footnote li .li-block {{
        display: flex;
        align-items: flex-start;
        gap: 0.45em;
        min-width: 0;
        width: 100%;
    }}
    .chapter-footnotes .footnote li .list-number {{
        font-family: "Gill Sans Nova", "Gill Sans", "Gill Sans MT", sans-serif;
        color: #555;
        flex-shrink: 0;
        min-width: 2.25em;
        text-align: right;
    }}
    /* Block p as flex item so long URLs wrap inside the type area (inline + flex min-width:auto overflows). */
    .chapter-footnotes .footnote li p {{
        margin: 0;
        padding: 0;
        display: block;
        flex: 1 1 0%;
        min-width: 0;
        font-size: inherit;
        text-indent: 0;
        overflow-wrap: anywhere;
    }}
    .chapter-footnotes .footnote-backref {{
        display: none;
    }}
    /* Markdown [label](url) in footnote defs becomes <a>; without a colour rule, WeasyPrint
       uses default link blue. Plain URLs in other chapters stay grey text. Match footnote body. */
    .chapter-footnotes a {{
        overflow-wrap: anywhere;
        word-break: break-word;
        color: inherit;
        text-decoration: none;
    }}
    .chapter-footnotes a:visited,
    .chapter-footnotes a:hover {{
        color: inherit;
    }}

    /* Questions section: new page; no rule above heading */
    .questions-section {{
        page-break-before: always;
    }}

    /* PART SEPARATOR: always on its own page; no page number; blank page after for chapter */
    /* Parts always start on a right (recto) page; blank inserted if needed */
    .part-separator {{
        page: front;
        page-break-before: right;
        page-break-after: always;
        text-align: center;
        padding-top: 3in;
    }}
    .part-separator h2 {{
        font-family: "Raleway", sans-serif;
        font-size: 16pt;
        font-weight: normal;
        letter-spacing: 2pt;
        margin: 0;
        page-break-after: avoid;
    }}
    """


def make_footnotes_continuous(html: str, start_offset: int, chapter_id: str) -> tuple[str, int]:
    """
    Renumber the footnotes in the given HTML block starting from `start_offset + 1`.
    Ensures footnote IDs are unique across chapters by prepending `chapter_id-` to internal anchor names.
    Returns the modified HTML and the new next footnote offset.
    """
    # 1. Update the visible number inside <a class="footnote-ref">...</a>
    def repl_ref(m):
        num = int(m.group(2)) + start_offset
        return f"{m.group(1)}{num}{m.group(3)}"
    
    html = re.sub(
        r'(<a[^>]*?class="footnote-ref"[^>]*?>)(\d+)(</a>)',
        repl_ref,
        html,
        flags=re.IGNORECASE
    )
    
    # 2. Update the tooltip number in title="..."
    html = re.sub(
        r'(title="Jump back to footnote )(\d+)( in the text")',
        lambda m: f"{m.group(1)}{int(m.group(2)) + start_offset}{m.group(3)}",
        html,
        flags=re.IGNORECASE
    )
    
    # 3. Prevent ID clashes across chapters by prefixing IDs and HREFs
    html = re.sub(r'(id=["\']fn:)([^"\']+)', fr'\1{chapter_id}-\2', html)
    html = re.sub(r'(id=["\']fnref:)([^"\']+)', fr'\1{chapter_id}-\2', html)
    html = re.sub(r'(href=["\']#fn:)([^"\']+)', fr'\1{chapter_id}-\2', html)
    html = re.sub(r'(href=["\']#fnref:)([^"\']+)', fr'\1{chapter_id}-\2', html)
    
    # 4. Count the number of footnotes generated by python-markdown in this chapter
    count = len(re.findall(f'<li id="fn:{chapter_id}-', html, flags=re.IGNORECASE))
    
    # 5. Set the starting number on <ol> so PDF and browser lists style properly
    if start_offset > 0 and count > 0:
        def repl_ol(m):
            return f'{m.group(1)} start="{start_offset + 1}"{m.group(2)}'
        html = re.sub(
            r'(<div class="footnote"[^>]*>.*?<ol)([^>]*>)',
            repl_ol,
            html,
            count=1,
            flags=re.IGNORECASE | re.DOTALL
        )
        
    return html, start_offset + count


def _load_copyright_html(book_dir: Path) -> str:
    """Read book/copyright.md and return rendered HTML (markdown supported, e.g. _italic_)."""
    copyright_path = book_dir / "copyright.md"
    if copyright_path.exists():
        text = copyright_path.read_text(encoding="utf-8")
        return markdown_to_html(text) if text.strip() else "<p></p>"
    # Fallback if file is missing
    return f"<p>\u00a9 {__import__('datetime').datetime.now().year} The Agentic Organisation. All rights reserved.</p>"


def _load_dedication_html(book_dir: Path) -> str:
    """Read book/dedicated-to.md and return rendered HTML wrapped for the dedication page."""
    dedication_path = book_dir / "dedicated-to.md"
    if dedication_path.exists():
        text = dedication_path.read_text(encoding="utf-8")
        if text.strip():
            return markdown_to_html(text)
    return ""


def build_full_html(
    repo: Path,
    title: str,
    subtitle: str,
    chapters_included: list[int],
    toc_chapters: list[tuple[int, str]],
    about_author: str,
    dry_run: bool,
    for_pdf: bool = True,
    cover_rel: str | None = None,
) -> str:
    """Assemble full HTML document with optional cover, front matter, chapters, back matter."""
    html_parts = [
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"/>",
        "<title>" + title + "</title>",
        "<style>" + get_css(for_pdf=for_pdf) + "</style>",
        "</head><body>",
    ]
    # Front matter sequence: 1=cover, 2=blank, 3=half title, 4=blank, 5=full title, 6=copyright, 7=blank, 8=epigraph, 9+=TOC, then introduction (right-hand).
    book_dir = repo / "book"
    if cover_rel:
        src = html_module.escape(cover_rel, quote=True)
        html_parts.append(f'<div class="cover-page front-matter"><img src="{src}" alt="Book cover"/></div>')
        html_parts.append('<div class="blank-page"></div>')
    html_parts.append('<div class="half-title-page front-matter"><h1>' + html_module.escape(title) + "</h1></div>")
    html_parts.append('<div class="blank-page"></div>')
    # Full title page: title, subtitle, author (from metadata when available)
    author_name = ""
    try:
        meta = load_epub_metadata(book_dir)
        author_name = (meta.get("author") or "").strip()
    except Exception:
        pass
    html_parts.append('<div class="title-page front-matter">')
    html_parts.append("<h1>" + html_module.escape(title) + "</h1>")
    # Subtitle can contain newlines; each line is escaped and joined with <br/> (e.g. "EUROPEAN EDITION" on second line)
    subtitle_html = "<br/>".join(html_module.escape(p) for p in subtitle.split("\n"))
    html_parts.append('<div class="subtitle">' + subtitle_html + "</div>")
    html_parts.append('<div class="author">' + html_module.escape(author_name) + "</div>")
    html_parts.append("</div>")
    html_parts.append('<div class="copyright-page front-matter">')
    html_parts.append(_load_copyright_html(book_dir))
    html_parts.append("</div>")
    # Dedication page: right after copyright
    dedication_html = _load_dedication_html(book_dir)
    if dedication_html:
        html_parts.append('<div class="dedication-page front-matter">')
        html_parts.append(dedication_html)
        html_parts.append("</div>")
    html_parts.append('<div class="epigraph-page front-matter"></div>')
    # Load introduction early so TOC can include "Introduction" entry with correct page number
    introduction_md = load_text(repo / "book" / "introduction.md")
    has_intro = bool(introduction_md.strip())
    html_parts.append('<div class="toc front-matter"><h2>Contents</h2>'
        + build_toc_html(chapters_included, toc_chapters, has_introduction=has_intro)
        + "</div>")

    # Introduction: optional front matter from book/introduction.md (after TOC, before Chapter 1).
    if has_intro:
        introduction_html = markdown_to_html(introduction_md)
        introduction_html = _add_intro_subhead_class(introduction_html)
        # Introduction doesn't usually have many footnotes, but let's renumber them just in case.
        # But wait, introduction numbers start from 1.
        introduction_html, fn_offset = make_footnotes_continuous(introduction_html, 0, "intro")
        introduction_html = inject_ordered_list_numbers(introduction_html)
        html_parts.append('<div class="introduction front-matter" id="introduction">')
        html_parts.append(introduction_html)
        html_parts.append("</div>")

    # Part separator pages (Part I–IV) before the first chapter of each part; then chapters
    toc_by_num = dict(toc_chapters)
    strip_handoff = not dry_run
    
    if not has_intro:
        fn_offset = 0

    for num in chapters_included:
        # Insert part separator page when this chapter starts a part (id for TOC link/page number)
        if num in PART_TITLES:
            part_id = PART_IDS[num]
            part_title = html_module.escape(PART_TITLES[num])
            html_parts.append(f'<div class="part-separator" id="{part_id}"><h2>{part_title}</h2></div>')
        ch_html = build_chapter_html(repo, num, strip_handoff=strip_handoff)
        if not ch_html:
            continue
        
        chapter_id = f"ch{num:02d}"
        ch_html, fn_offset = make_footnotes_continuous(ch_html, fn_offset, chapter_id)
        ch_html = inject_ordered_list_numbers(ch_html)
        
        ch_title = toc_by_num.get(num, f"Chapter {num}")
        ch_plain = chapter_title_plain(ch_title)
        ch_title_html = chapter_title_html(ch_title)
        html_parts.append(f'<div class="chapter" id="{chapter_id}">')
        # Hidden TOC entry so PDF Contents shows "Chapter N - Title" (visible page keeps number + title separate)
        html_parts.append(
            f'<div class="toc-entry-hidden">Chapter {num} - {html_module.escape(ch_plain)}</div>'
        )
        html_parts.append(f'<div class="chapter-number">Chapter {chapter_number_word(num)}</div>')
        html_parts.append(
            f'<div class="chapter-title" data-ch="Ch {num}: " '
            f'data-title-plain="{html_module.escape(ch_plain)}">{ch_title_html}</div>'
        )
        html_parts.append('<div class="chapter-divider"></div>')
        html_parts.append(strip_first_h1(ch_html))
        html_parts.append("</div>")

    # Blank page after last chapter, then About the Author (on right page), then blank
    html_parts.append('<div class="blank-content-page"></div>')
    # Back matter: About the Author (page-break-before: right ensures it starts on recto)
    html_parts.append('<div class="back-matter">')
    if about_author.strip():
        # About the author may be markdown (e.g. ## About the Author\n\n...)
        author_html = markdown_to_html(about_author)
        html_parts.append('<div class="about-the-author">')
        html_parts.append(author_html)
        html_parts.append("</div>")
    else:
        html_parts.append('<p class="index-placeholder">[About the Author to be added.]</p>')

    html_parts.append("</div>")
    html_parts.append('<div class="blank-content-page"></div>')
    html_parts.append("</body></html>")
    return "".join(html_parts)


# Minimal reflowable CSS for EPUB (definitions and case studies still distinct).
# No page numbers or @page: reflowable EPUB best practice (content adapts to reader/viewport).
EPUB_CSS = """
body { font-family: Georgia, serif; font-size: 1em; line-height: 1.45; color: #111; }
p { margin: 0 0 0.6em 0; text-indent: 1em; }
p:first-of-type { text-indent: 0; }
strong { font-weight: bold; }
em { font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; page-break-inside: avoid; }
table th, table td { border: 1px solid #666; padding: 0.4em 0.6em; text-align: left; vertical-align: top; }
table thead th { background: #e8e8e8; font-weight: bold; }
.definition-box { background: #f5f5f0; border-left: 3px solid #666; padding: 0.75em 1em; margin: 1em 0; }
.definition-single { margin: 0; }
.case-study { background: #f8f8f4; border: 1px solid #ccc; padding: 1em; margin: 1em 0; }
.case-study h2 { font-size: 1.1em; margin-top: 0; }
h1 { font-size: 1.5em; margin: 1em 0 0.5em 0; }
h1.chapter-heading { text-align: center; }
h2 { font-size: 1.25em; margin: 1em 0 0.5em 0; }
.subtitle { font-size: 0.9em; color: #444; margin-bottom: 1em; }
.about-the-author { margin-top: 1em; }
img { max-width: 100%; height: auto; }
ul, ol { margin: 0.6em 0 0.8em 0; display: block; }
ul { padding-left: 1.8em; list-style-type: disc; list-style-position: outside; }
/* Ordered lists: inject_ordered_list_numbers() prepends .list-number spans; hide native markers. */
ol { list-style: none; padding-left: 0; margin-left: 0; }
ul li { display: list-item; margin-top: 0.35em; margin-bottom: 0.35em; padding-left: 0; }
ul li:first-child { margin-top: 0; }
ol > li { display: block; margin: 0; padding: 0; }
ol li:first-child, ul li:first-child { margin-top: 0; }
/* Match PDF: hanging indent for ordered lists; numerals in a fixed left column */
.list-number { margin-right: 0; }
.li-block { display: flex; align-items: flex-start; gap: 0.55em; margin-bottom: 0.78em; }
ol > li:last-child > .li-block { margin-bottom: 0.5em; }
ol > li > .li-block > .list-number {
    flex-shrink: 0;
    min-width: 2.25em;
    text-align: right;
    line-height: 1.35;
}
ol > li > .li-block > p {
    flex: 1 1 0%;
    min-width: 0;
    margin: 0;
}
/* Footnote block: same hanging-indent column as body lists */
.footnote > ol > li > .li-block > .list-number {
    flex-shrink: 0;
    min-width: 2.25em;
    text-align: right;
}
/* EPUB: aside epub:type="footnote" wraps each footnote body (popover scope for reading systems). */
.footnote aside {
    display: block;
    margin: 0;
    padding: 0;
}
/* Dedication page (wrapper class; was inline CSS before linked stylesheet). */
.dedication-epub p {
    font-style: italic;
    text-align: center;
    margin-top: 3em;
}
/*
 * Navigation document (nav.xhtml): ebooklib builds the TOC from nested <ol> elements.
 * Without a linked stylesheet, reading systems show default 1. 2. 3. markers at every level.
 * Scope rules to role="doc-toc" so landmarks/page-list nav (if present) is unaffected.
 */
nav[role="doc-toc"] ol {
    list-style: none;
    padding-left: 0;
    margin-left: 0;
}
nav[role="doc-toc"] ol ol {
    margin: 0.25em 0 0.6em 1.25em;
}
nav[role="doc-toc"] li {
    margin: 0.35em 0;
}
"""


def _epub_image_media_type(path: Path) -> str:
    """Return EPUB media type for an image path (e.g. image/png)."""
    suf = path.suffix.lower()
    if suf in (".jpg", ".jpeg"):
        return "image/jpeg"
    if suf == ".gif":
        return "image/gif"
    if suf == ".webp":
        return "image/webp"
    if suf == ".svg":
        return "image/svg+xml"
    return "image/png"


def _sniff_image_extension(data: bytes) -> str | None:
    """
    Detect image format from magic bytes. Returns extension including the dot (e.g. '.jpg').
    Used so EPUB manifest media-type matches bytes (OPF-029 / PKG-022).
    """
    if len(data) < 12:
        return None
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if data[:4] == b"RIFF" and len(data) >= 12 and data[8:12] == b"WEBP":
        return ".webp"
    return None


def _epub_cover_archive_filename(cover_path: Path, data: bytes) -> str:
    """
    File name inside the EPUB package for the cover (e.g. 'cover.jpg').

    Prefer magic-byte sniffing over the filesystem extension so a JPEG wrongly
    saved as cover.png still gets cover.jpg in the OPF. ebooklib sets media-type
    from the file name.
    """
    sniffed = _sniff_image_extension(data)
    if sniffed:
        return "cover" + sniffed
    suf = cover_path.suffix.lower()
    if suf == ".jpeg":
        return "cover.jpg"
    if suf in (".jpg", ".png", ".gif", ".webp", ".svg"):
        return "cover" + suf
    return "cover.png"


def _epub_cover_manifest_mime(data: bytes, archive_filename: str) -> str:
    """
    OPF manifest media-type for the cover image: must match actual bytes (EPUBCheck OPF-029).
    Set explicitly on EpubCover; do not rely on mimetypes.guess_type alone.
    """
    sniffed = _sniff_image_extension(data)
    if sniffed == ".jpg":
        return "image/jpeg"
    if sniffed == ".png":
        return "image/png"
    if sniffed == ".gif":
        return "image/gif"
    if sniffed == ".webp":
        return "image/webp"
    return _epub_image_media_type(Path(archive_filename))


def _add_epub_cover_to_book(book, cover_path: Path, cover_bytes: bytes):
    """
    Same end result as ebooklib EpubBook.set_cover(), but sets EpubCover.media_type
    explicitly from sniffed bytes so the OPF never declares image/png for JPEG data.

    Returns the EpubCoverHtml page item — it must be inserted into book.spine or readers
    will not show the cover in reading order (manifest + meta name=cover alone are not enough).
    """
    archive_name = _epub_cover_archive_filename(cover_path, cover_bytes)
    media_type = _epub_cover_manifest_mime(cover_bytes, archive_name)

    c0 = epub.EpubCover(uid="cover-img", file_name=archive_name)
    c0.content = cover_bytes
    c0.media_type = media_type
    book.add_item(c0)

    c1 = epub.EpubCoverHtml(image_name=archive_name)
    # ebooklib defaults EpubCoverHtml.is_linear to False (linear="no"), which drops the cover
    # from primary reading order in many apps; we want the cover as the first visible page.
    c1.is_linear = True
    book.add_item(c1)

    book.add_metadata(
        None,
        "meta",
        "",
        OrderedDict([("name", "cover"), ("content", "cover-img")]),
    )
    return c1


def _collect_epub_images_from_html(html: str, book_dir: Path) -> list[tuple[str, Path]]:
    """
    Find all <img src="..."> in HTML that point to book/images/ or images/.
    Returns list of (original_src, absolute_path) for existing files.
    """
    out = []
    # Match src="book/images/foo.png" or src="images/foo.png" (and variants)
    for m in re.finditer(r'<img\s[^>]*\ssrc=(["\'])([^"\']+)\1', html, re.IGNORECASE):
        src = m.group(2).strip()
        if not src:
            continue
        # Normalize: book/images/foo.png or images/foo.png -> book_dir/images/basename
        if src.startswith("book/images/"):
            rel = "images/" + src.split("book/images/")[-1].lstrip("/")
        elif src.startswith("images/"):
            rel = src
        else:
            continue
        path = book_dir / rel
        if path.exists():
            out.append((src, path))
    return out


def _rewrite_epub_html_images(html: str, src_mapping: dict[str, str]) -> str:
    """Replace img src values with EPUB-internal paths (e.g. images/foo.png)."""
    if not src_mapping:
        return html
    result = html
    for old_src, new_src in src_mapping.items():
        # Replace src="old_src" and src='old_src'
        result = result.replace(f'src="{old_src}"', f'src="{new_src}"')
        result = result.replace(f"src='{old_src}'", f"src='{new_src}'")
    return result


def _sanitize_html_for_epub(html: str) -> str:
    """
    EPUB-only sanitizer: fix HTML so it passes EPUBCheck (RSC-005, RSC-012).
    Does not modify the shared PDF/HTML pipeline; only call from build_epub().
    - RSC-005: <br/> is not allowed as direct child of <ul> or <ol> (only <li> allowed).
    - RSC-012: Remove fragment from href="#id" when id is not present in this document.
    """
    # RSC-005: Remove <br/> between </li> and <li> (inject_ordered_list_numbers adds these for PDF layout).
    html = re.sub(r"</li>\s*<br\s*/?>\s*<li", "</li><li", html, flags=re.IGNORECASE)
    # Remove <br/> immediately after <ol> or <ul> open tag.
    html = re.sub(r"(<ol[^>]*>)\s*<br\s*/?>\s*", r"\1", html, flags=re.IGNORECASE)
    html = re.sub(r"(<ul[^>]*>)\s*<br\s*/?>\s*", r"\1", html, flags=re.IGNORECASE)
    # Remove <br/> immediately before </ol> or </ul>.
    html = re.sub(r"\s*<br\s*/?>\s*(</ol>)", r" \1", html, flags=re.IGNORECASE)
    html = re.sub(r"\s*<br\s*/?>\s*(</ul>)", r" \1", html, flags=re.IGNORECASE)

    # RSC-012: Fragment identifiers: href="#id" must point to an id in this document.
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', html))

    def repl_href(match: re.Match) -> str:
        quote, frag = match.group(1), match.group(2)
        if frag.startswith("#") and len(frag) > 1 and frag[1:] not in ids:
            return f'href={quote}#{quote}'
        return match.group(0)

    html = re.sub(r'href=(["\'])(#[^"\']*)\1', repl_href, html)
    return html


# EPUB 3: epub:type on links/asides needs the namespace on the root element.
_EPUB_XHTML_NS = 'xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"'


def _epub_html_shell(body_inner: str) -> str:
    """Valid EPUB 3 XHTML document wrapper (namespace for epub:noteref / epub:footnote)."""
    return f"<html {_EPUB_XHTML_NS}><body>{body_inner}</body></html>"


def _epub_footnote_semantics(html: str) -> str:
    """
    EPUB-only: mark footnote references and bodies per EPUB 3 so reading systems (e.g. Apple
    Books) bound popovers to each footnote. Without aside epub:type=\"footnote\", the last
    footnote in a file often includes all following content until EOF.
    """
    # noteref on superscript links (class from python-markdown footnotes extension).
    def noteref_repl(m: re.Match) -> str:
        attrs = m.group(1)
        if re.search(r"\bepub:type\s*=", attrs, re.IGNORECASE):
            return m.group(0)
        return f'<a epub:type="noteref" {attrs}>'

    html = re.sub(
        r"<a\s+([^>]*\bclass\s*=\s*[\"']footnote-ref[\"'][^>]*)>",
        noteref_repl,
        html,
        flags=re.IGNORECASE,
    )

    def footnote_div_repl(dm: re.Match) -> str:
        open_tag, inner, close = dm.group(1), dm.group(2), dm.group(3)

        def li_repl(lm: re.Match) -> str:
            attrs, body = lm.group(1), lm.group(2)
            id_m = re.search(r'id\s*=\s*(["\'])(fn:[^"\']+)\1', attrs, re.IGNORECASE)
            if not id_m:
                return lm.group(0)
            fn_id = id_m.group(2)
            attrs_no_id = re.sub(
                r'\s*id\s*=\s*["\']fn:[^"\']+["\']',
                "",
                attrs,
                count=1,
                flags=re.IGNORECASE,
            ).strip()
            open_li = f"<li {attrs_no_id}>" if attrs_no_id else "<li>"
            return f'{open_li}<aside epub:type="footnote" role="doc-footnote" id="{fn_id}">{body}</aside></li>'

        inner_new = re.sub(r"<li([^>]*)>(.*?)</li>", li_repl, inner, flags=re.DOTALL | re.IGNORECASE)
        return f"{open_tag}{inner_new}{close}"

    # Match the footnote div that wraps a single <ol> only. Do not use (.*?)</div> — the first
    # </div> would close .li-block inside the first <li>, not the footnote container.
    return re.sub(
        r'(<div\s+class="footnote"[^>]*>)(\s*<ol[^>]*>.*?</ol>\s*)(</div>)',
        footnote_div_repl,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )


def build_epub(
    repo: Path,
    title: str,
    subtitle: str,
    chapters_included: list[int],
    toc_chapters: list[tuple[int, str]],
    about_author: str,
    dry_run: bool,
    cover_path: Path | None,
    out_path: Path,
    epub_metadata: dict | None = None,
) -> None:
    """
    Build an EPUB from the same book/ sources. Uses ebooklib; front matter, chapters,
    and back matter are separate XHTML documents with a simple TOC and spine.
    EPUB metadata (identifier, author, description, language, keywords, publisher, date)
    is read from epub_metadata when provided (from load_epub_metadata(book_dir)).
    """
    if epub is None:
        raise SystemExit("EPUB export requires ebooklib. Install with: pip install ebooklib")

    meta = epub_metadata or {}
    # Use metadata from book folder when available; fall back to build args
    meta_title = meta.get("title") or title
    meta_subtitle = meta.get("subtitle") or subtitle
    meta_lang = meta.get("language") or "en"
    meta_identifier = (meta.get("identifier") or "").strip()
    meta_author = (meta.get("author") or "").strip()
    meta_description = (meta.get("description") or "").strip()
    meta_keywords = meta.get("keywords") or []
    meta_publisher = (meta.get("publisher") or "").strip()
    meta_date = (meta.get("date") or meta.get("publication_date") or "").strip()

    book = epub.EpubBook()
    # Identifier: from metadata (e.g. ISBN) or fallback URN
    if meta_identifier:
        book.set_identifier(meta_identifier if meta_identifier.startswith("urn:") else f"urn:isbn:{meta_identifier}")
    else:
        book.set_identifier(f"urn:book:{meta_title.replace(' ', '-')[:50]}-{id(book)}")
    book.set_title(meta_title)
    book.set_language(meta_lang)
    if meta_author:
        book.add_author(meta_author)
    if meta_publisher:
        book.add_metadata("DC", "publisher", meta_publisher)
    if meta_date:
        book.add_metadata("DC", "date", meta_date)
    if meta_description:
        # dc:description is text-only in OPF; **bold** from metadata.md → Unicode bold.
        book.add_metadata("DC", "description", _markdown_bold_to_unicode_bold(meta_description))
    for kw in meta_keywords:
        if kw:
            book.add_metadata("DC", "subject", kw)

    # Linked stylesheet: ebooklib's EpubHtml discards any <head> from `content` when it
    # serialises XHTML (only body children are kept). Inline EPUB_CSS never reached the
    # package; use EpubItem + add_item() so footnote/list rules actually apply.
    epub_style = epub.EpubItem(
        uid="book_epub_style",
        file_name="style/book.css",
        media_type="text/css",
        content=EPUB_CSS.encode("utf-8"),
    )
    book.add_item(epub_style)

    # Cover image (optional): manifest + spine item so the cover page appears when opening the book
    epub_cover_page = None
    if cover_path and cover_path.exists():
        try:
            cover_bytes = cover_path.read_bytes()
            epub_cover_page = _add_epub_cover_to_book(book, cover_path, cover_bytes)
        except OSError:
            pass  # Skip cover if unreadable

    book_dir = repo / "book"
    toc_by_num = dict(toc_chapters)
    strip_handoff = not dry_run

    # Gather all HTML that may contain images (intro + chapters), collect image paths, add to EPUB
    epub_src_mapping: dict[str, str] = {}  # original src -> EPUB-internal path (e.g. images/foo.png)
    seen_paths: set[Path] = set()
    intro_html = ""
    if load_text(book_dir / "introduction.md").strip():
        intro_html = markdown_to_html(load_text(book_dir / "introduction.md"))
    for html_block in [intro_html] + [build_chapter_html(repo, num, strip_handoff=strip_handoff) for num in chapters_included]:
        if not html_block:
            continue
        for orig_src, abs_path in _collect_epub_images_from_html(html_block, book_dir):
            if abs_path in seen_paths:
                epub_src_mapping[orig_src] = "images/" + abs_path.name
                continue
            seen_paths.add(abs_path)
            try:
                img_content = abs_path.read_bytes()
            except OSError:
                continue
            internal_name = "images/" + abs_path.name
            epub_src_mapping[orig_src] = internal_name
            epub_img = epub.EpubImage(
                uid="img_" + abs_path.stem,
                file_name=internal_name,
                media_type=_epub_image_media_type(abs_path),
                content=img_content,
            )
            book.add_item(epub_img)

    # Spine: cover page first (if any), then nav. Without a cover itemref, cover.xhtml is
    # only in the manifest — many readers open at the first spine item and never show the cover.
    spine = []
    if epub_cover_page is not None:
        spine.append(epub_cover_page)
    spine.append("nav")

    # Front matter: title page + copyright (single xhtml)
    copyright_html = _load_copyright_html(repo / "book")
    title_content = f"""<h1>{html_module.escape(meta_title)}</h1>
<p class="subtitle">{html_module.escape(meta_subtitle)}</p>
{copyright_html}"""
    title_page = epub.EpubHtml(
        title="Title",
        file_name="title.xhtml",
        lang="en",
        content=_epub_html_shell(title_content),
    )
    title_page.add_item(epub_style)
    book.add_item(title_page)
    spine.append(title_page)

    # Dedication page (optional) — right after copyright
    dedication_html = _load_dedication_html(repo / "book")
    if dedication_html:
        dedication_html = _sanitize_html_for_epub(dedication_html)
        dedication_page = epub.EpubHtml(
            title="Dedication",
            file_name="dedication.xhtml",
            lang="en",
            content=_epub_html_shell(f'<div class="dedication-epub">{dedication_html}</div>'),
        )
        dedication_page.add_item(epub_style)
        book.add_item(dedication_page)
        spine.append(dedication_page)

    # Introduction (optional)
    introduction_md = load_text(repo / "book" / "introduction.md")
    has_introduction = bool(introduction_md.strip())
    fn_offset = 0
    if has_introduction:
        intro_html = markdown_to_html(introduction_md)
        intro_html, fn_offset = make_footnotes_continuous(intro_html, fn_offset, "intro")
        intro_html = inject_ordered_list_numbers(intro_html)
        intro_html = _rewrite_epub_html_images(intro_html, epub_src_mapping)
        intro_html = _sanitize_html_for_epub(intro_html)
        intro_html = _epub_footnote_semantics(intro_html)
        intro_page = epub.EpubHtml(
            title="Introduction",
            file_name="introduction.xhtml",
            lang="en",
            content=_epub_html_shell(intro_html),
        )
        intro_page.add_item(epub_style)
        book.add_item(intro_page)
        spine.append(intro_page)

    # Chapters
    for num in chapters_included:
        ch_html = build_chapter_html(repo, num, strip_handoff=strip_handoff)
        if not ch_html:
            continue
        chapter_id = f"ch{num:02d}"
        ch_html, fn_offset = make_footnotes_continuous(ch_html, fn_offset, chapter_id)
        ch_html = inject_ordered_list_numbers(ch_html)
        ch_html = _rewrite_epub_html_images(ch_html, epub_src_mapping)
        ch_html = _sanitize_html_for_epub(ch_html)
        ch_html = _epub_footnote_semantics(ch_html)
        ch_title = toc_by_num.get(num, f"Chapter {num}")
        ch_plain = chapter_title_plain(ch_title)
        ch_title_html = chapter_title_html(ch_title)
        # Keep first h1 or add chapter title for nav
        body = strip_first_h1(ch_html)
        full = f'<h1 class="chapter-heading">{ch_title_html}</h1>{body}'
        file_name = f"ch{num:02d}.xhtml"
        ch_page = epub.EpubHtml(
            title=ch_plain,
            file_name=file_name,
            lang="en",
            content=_epub_html_shell(full),
        )
        ch_page.add_item(epub_style)
        book.add_item(ch_page)
        spine.append(ch_page)

    # Back matter: About the Author
    if about_author.strip():
        author_html = markdown_to_html(about_author)
        author_html = _sanitize_html_for_epub(author_html)
        about_content = _epub_html_shell(f'<div class="about-the-author">{author_html}</div>')
    else:
        about_content = _epub_html_shell("<p>[About the Author to be added.]</p>")
    about_page = epub.EpubHtml(
        title="About the Author",
        file_name="about.xhtml",
        lang="en",
        content=about_content,
    )
    about_page.add_item(epub_style)
    book.add_item(about_page)
    spine.append(about_page)

    book.toc = build_epub_nav_toc(
        chapters_included,
        toc_chapters,
        has_introduction=has_introduction,
    )
    book.spine = spine
    book.add_item(epub.EpubNcx())
    # EpubNav must reference the same stylesheet as body XHTML or nav.xhtml keeps default <ol> numbering.
    nav_page = epub.EpubNav()
    nav_page.add_item(epub_style)
    book.add_item(nav_page)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(out_path), book, {})


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build print-ready PDF for KDP and IngramSpark.",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output path (.pdf for full book or dry-run --pdf; .html for dry-run default)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Include only Chapter 1 in body; output HTML by default, or PDF if --pdf is set",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="With --dry-run: output PDF instead of HTML. Ignored for full book (always PDF).",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Book repository root (default: auto-detect from script location)",
    )
    parser.add_argument(
        "--cover",
        default="book/images/cover.png",
        metavar="PATH",
        help="Cover image path relative to repo (default: book/images/cover.png); omitted if file missing",
    )
    parser.add_argument(
        "--epub",
        action="store_true",
        help="Build EPUB (output path .epub). Full book from book/ folder.",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Build full book as a single HTML file (output path .html).",
    )
    parser.add_argument(
        "--interior",
        action="store_true",
        help="Interior only: exclude cover. Use for book-interior.pdf/epub/html (IngramSpark interior file).",
    )
    args = parser.parse_args()

    # Resolve repo root (script lives in skills/format-book-agent/scripts/; repo has book/ folder)
    if args.repo:
        repo = Path(args.repo)
    else:
        repo = find_repo_root(Path(__file__).parent)
    book_dir = repo / "book"
    if not book_dir.is_dir():
        raise SystemExit("Repository root not found (no book/ folder). Use --repo /path/to/repo.")

    # TOC: from book/toc.md; if missing, use defaults and discover chapters from book/chapter-*.md
    toc_content = load_text(book_dir / "toc.md")
    if toc_content.strip():
        title, subtitle, toc_chapters = parse_toc(toc_content)
    else:
        title = "The Agentic Organisation"
        subtitle = "A complete guide for AI transformations\nEUROPEAN EDITION"
        toc_chapters = discover_chapters_from_book(book_dir)

    if args.dry_run:
        chapters_included = [1]
    else:
        # Include every chapter that has a file in book/ (chapter-NN.md or NN - Title.md)
        chapters_included = []
        for num, _ in toc_chapters:
            if resolve_chapter_path(book_dir, num) is not None:
                chapters_included.append(num)

    if not chapters_included:
        raise SystemExit(
            "No chapter files found in book/. Use book/chapter-01.md or book/01 - Title.md. For dry-run, chapter 1 must exist."
        )

    # About the Author: back matter at end of book (from book folder only)
    about_author = load_text(repo / "book" / "about-the-author.md")

    # Cover: omit when --interior; else prefer JPEG in book/images/ (common case), then PNG, then --cover
    cover_rel = None
    cover_path_for_epub = None
    if not args.interior:
        # Prefer cover.jpg before cover.png so a real JPEG is not skipped when an older
        # or mis-tagged cover.png also exists in the same folder.
        _cover_candidates = [
            book_dir / "images" / "cover.jpg",
            book_dir / "images" / "cover.jpeg",
            book_dir / "images" / "cover.png",
            book_dir / "cover.jpg",
            book_dir / "cover.jpeg",
            book_dir / "cover.png",
        ]
        for cp in _cover_candidates:
            if cp.exists():
                try:
                    cover_rel = str(cp.relative_to(repo)).replace("\\", "/")
                except ValueError:
                    cover_rel = cp.name
                cover_path_for_epub = cp
                break
        if cover_path_for_epub is None:
            candidate = repo / args.cover.lstrip("/")
            if candidate.exists():
                cover_rel = args.cover
                cover_path_for_epub = candidate

    # EPUB output: build EPUB and exit (same sources as PDF). Use metadata from book folder.
    if args.epub:
        out_path = Path(args.output)
        if out_path.suffix.lower() != ".epub":
            out_path = out_path.with_suffix(".epub")
        epub_metadata = load_epub_metadata(book_dir)
        build_epub(
            repo=repo,
            title=title,
            subtitle=subtitle,
            chapters_included=chapters_included,
            toc_chapters=toc_chapters,
            about_author=about_author,
            dry_run=args.dry_run,
            cover_path=cover_path_for_epub,
            out_path=out_path,
            epub_metadata=epub_metadata,
        )
        print(f"Wrote {out_path}.")
        return

    # PDF vs HTML: --html forces HTML; otherwise PDF (or dry-run PDF when --pdf)
    want_pdf = not args.html and ((not args.dry_run) or args.pdf)
    full_html = build_full_html(
        repo=repo,
        title=title,
        subtitle=subtitle,
        chapters_included=chapters_included,
        toc_chapters=toc_chapters,
        about_author=about_author,
        dry_run=args.dry_run,
        for_pdf=want_pdf,
        cover_rel=cover_rel,
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if want_pdf:
        if WeasyHTML is None:
            _msg = (
                "PDF export requires WeasyPrint and its system libraries (Pango/GTK).\n"
                "  pip install weasyprint\n"
                "On Windows, install Pango via MSYS2: https://www.msys2.org/\n"
                "  In MSYS2 shell: pacman -S mingw-w64-x86_64-pango\n"
                "  Then set WEASYPRINT_DLL_DIRECTORIES if needed, e.g.:\n"
                "  set WEASYPRINT_DLL_DIRECTORIES=C:\\Program Files (x86)\\MSYS2\\mingw64\\bin\n"
                "  See: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows"
            )
            raise SystemExit(_msg)
        try:
            # base_url = repo root: map chapter-relative images/... -> book/images/...
            pdf_html = _html_image_src_for_pdf_repo_base(full_html)
            html_doc = WeasyHTML(string=pdf_html, base_url=str(repo))
            # Load Raleway and Lora from Google Fonts for PDF typography (Gill Sans Nova requires local/Adobe Fonts)
            font_urls = [
                "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&display=swap",
                "https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700&display=swap",
            ]
            html_doc.write_pdf(str(out_path), stylesheets=font_urls)
            # Inject metadata (title, author, subject, keywords) from book folder
            pdf_metadata = load_epub_metadata(book_dir)
            inject_pdf_metadata(out_path, pdf_metadata)
            print(f"Wrote {out_path}.")
        except OSError as e:
            raise SystemExit(f"Failed to write PDF: {e}")
    else:
        html_path = out_path.with_suffix(".html")
        html_path.write_text(full_html, encoding="utf-8")
        # The generated HTML references images as relative paths like "images/foo.png"
        # (because markdown image refs in book/ chapters use "images/...").
        # For local viewing of output/*.html, copy book/images -> output/images.
        #
        # PDF uses base_url=str(repo) plus _html_image_src_for_pdf_repo_base() so
        # images resolve. Standalone HTML keeps src="images/..." + this copy.
        try:
            src_images = book_dir / "images"
            if src_images.is_dir():
                dst_images = html_path.parent / "images"
                shutil.copytree(src_images, dst_images, dirs_exist_ok=True)
        except Exception:
            # HTML is still useful without images; don't fail the whole build.
            pass
        print(f"Wrote {html_path}.")


if __name__ == "__main__":
    main()
