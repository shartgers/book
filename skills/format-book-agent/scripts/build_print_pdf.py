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
    if _existing:
        _path_prepend = os.pathsep.join(_existing)
        os.environ["PATH"] = _path_prepend + os.pathsep + os.environ.get("PATH", "")

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

# Trim size and margins: 6" x 9"; tighter margins to fit more content
TRIM_WIDTH = "6in"
TRIM_HEIGHT = "9in"
PAGE_TOP = "0.7in"
PAGE_BOTTOM = "0.7in"
PAGE_LEFT = "0.65in"
PAGE_RIGHT = "0.65in"
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


def _parse_simple_metadata(content: str) -> dict:
    """Parse key: value lines from input/metadata.md. Used for EPUB metadata overrides."""
    out = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        if key == "keywords" and value:
            # Strip surrounding quotes from each keyword for cleaner PDF/EPUB metadata
            out[key] = [k.strip().strip('"').strip("'") for k in value.split(",") if k.strip()]
        elif value:
            out[key] = value
    return out


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
    Returns dict with: title, subtitle, author, description, language, identifier, keywords (list).
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

    return {
        "title": (overrides.get("title") or title).strip(),
        "subtitle": (overrides.get("subtitle") or subtitle).strip(),
        "author": author,
        "description": description,
        "language": language,
        "identifier": identifier,
        "keywords": keywords,
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
    description = (meta.get("description") or "").strip()
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
    html = wrap_case_study_sections(html)
    html = wrap_questions_section_and_remove_hr(html)
    html = inject_ordered_list_numbers(html)
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
    gets a new page and a line above it. Remove all other hr so there are no lines
    between sections except before Questions.
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


def inject_ordered_list_numbers(html: str) -> str:
    """
    Prepend "1. ", "2. ", ... to each <li> inside <ol> and wrap in a block so each item
    starts on a new line in PDF (explicit block display for list items).
    """
    def replace_ol(match: re.Match) -> str:
        inner = match.group(1)
        num = 1
        def repl_li(li_match: re.Match) -> str:
            nonlocal num
            content = li_match.group(1)
            # Wrap in div so the item is a block and starts on a new line
            result = f'<li><div class="li-block"><span class="list-number">{num}. </span>{content}</div></li>'
            num += 1
            return result
        inner = re.sub(r"<li[^>]*>(.*?)</li>", repl_li, inner, flags=re.DOTALL)
        # Force each item onto a new line (block display for list items)
        inner = re.sub(r"</li>\s*<li>", "</li><br/><li>", inner)
        return "<ol>" + inner + "</ol>"
    return re.sub(r"<ol[^>]*>(.*?)</ol>", replace_ol, html, flags=re.DOTALL)


# Part separator pages: chapter number that starts each part -> part title (from toc.md)
PART_TITLES = {
    1: "Part I: The Burning Platform",
    3: "Part II: The Model",
    9: "Part III: The European Advantage",
    11: "Part IV: The CEO's Playbook",
}
# Anchor ids for part separator divs (for TOC links and correct page numbers)
PART_IDS = {1: "part1", 3: "part2", 9: "part3", 11: "part4"}


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
            name = toc_by_num.get(num, f"Chapter {num}")
            sub_items.append(
                f'<li><a href="#ch{num:02d}">Chapter {num} - {html_module.escape(name)}</a></li>'
            )
        items.append(
            f'<li class="toc-part"><a href="#{part_id}">{part_title}</a><ul>{"".join(sub_items)}</ul></li>'
        )

    return "<ul>" + "".join(items) + "</ul>"


def get_css(for_pdf: bool = True) -> str:
    """
    Return CSS for print typography and layout.
    When for_pdf=True uses WeasyPrint @page with margins and @bottom-right for page numbers.
    When for_pdf=False uses simple margin @page (for HTML preview).
    """
    if for_pdf:
        # WeasyPrint: front = no page number; content = numbered from 1.
        # Use built-in page counter: first content page resets to 1 (contentfirst),
        # so target-counter() in TOC works. See WeasyPrint #2114 workaround.
        page_setup = f"""
    /* PAGE SETUP: front = no number; contentfirst = reset page 1; content = continue */
    @page {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {PAGE_TOP} {PAGE_RIGHT} {PAGE_BOTTOM} {PAGE_LEFT};
    }}
    @page cover {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: 0;
        @top-center {{ content: none; }}
        @bottom-right {{ content: none; }}
    }}
    @page front {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {PAGE_TOP} {PAGE_RIGHT} {PAGE_BOTTOM} {PAGE_LEFT};
        @top-center {{ content: none; }}
        @bottom-right {{ content: none; }}
    }}
    /* Reset page counter only on the first numbered page (first introduction page), not on every contentfirst page */
    @page contentfirst:first {{
        counter-reset: page 1;
    }}
    /* Left (even) pages: chapter title and page number on the left; no reset here so numbering continues */
    @page contentfirst:left {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {PAGE_TOP} {PAGE_RIGHT} {PAGE_BOTTOM} {PAGE_LEFT};
        @top-left {{
            content: string(chapter-title);
            font-family: "DM Sans", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-left {{
            content: counter(page);
            font-family: "DM Sans", sans-serif;
            font-size: 9pt;
            color: #555;
        }}
    }}
    /* Right (odd) pages: chapter title and page number on the right */
    @page contentfirst:right {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {PAGE_TOP} {PAGE_RIGHT} {PAGE_BOTTOM} {PAGE_LEFT};
        @top-right {{
            content: string(chapter-title);
            font-family: "DM Sans", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-right {{
            content: counter(page);
            font-family: "DM Sans", sans-serif;
            font-size: 9pt;
            color: #555;
        }}
    }}
    @page content:left {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {PAGE_TOP} {PAGE_RIGHT} {PAGE_BOTTOM} {PAGE_LEFT};
        @top-left {{
            content: string(chapter-title);
            font-family: "DM Sans", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-left {{
            content: counter(page);
            font-family: "DM Sans", sans-serif;
            font-size: 9pt;
            color: #555;
        }}
    }}
    @page content:right {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {PAGE_TOP} {PAGE_RIGHT} {PAGE_BOTTOM} {PAGE_LEFT};
        @top-right {{
            content: string(chapter-title);
            font-family: "DM Sans", sans-serif;
            font-size: 8pt;
            color: #555;
        }}
        @bottom-right {{
            content: counter(page);
            font-family: "DM Sans", sans-serif;
            font-size: 9pt;
            color: #555;
        }}
    }}"""
    else:
        page_setup = f"""
    @page {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {PAGE_TOP} {PAGE_RIGHT} {PAGE_BOTTOM} {PAGE_LEFT};
    }}"""
    return page_setup + f"""

    /* BASE TYPOGRAPHY: DM Sans for all text */
    body {{
        font-family: "DM Sans", sans-serif;
        font-size: 11pt;
        line-height: 1.45;
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
        width: {TRIM_WIDTH};
        height: {TRIM_HEIGHT};
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
        font-size: 24pt;
        font-weight: normal;
    }}

    /* TITLE PAGE: reduced top and spacing */
    .title-page {{
        text-align: center;
        page-break-after: always;
    }}

    .title-page h1 {{
        margin-top: 2in;
        font-size: 24pt;
        font-weight: normal;
    }}

    .title-page .subtitle {{
        margin-top: 0.8em;
        font-size: 13pt;
        font-style: italic;
        color: #444;
    }}

    .title-page .author {{
        margin-top: 4in;
        font-size: 13pt;
        letter-spacing: 0.7pt;
    }}

    /* COPYRIGHT PAGE */
    .copyright-page {{
        font-size: 9pt;
        color: #555;
        page-break-after: always;
    }}

    .copyright-page p {{
        text-indent: 0;
        margin-bottom: 0.35em;
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
        font-size: 22pt;
        font-weight: normal;
    }}

    .toc h2 {{
        text-align: center;
        font-size: 16pt;
        margin-bottom: 1.2em;
        font-weight: normal;
    }}

    .toc ul {{
        list-style: none;
        padding-left: 0;
    }}

    .toc li {{
        margin-bottom: 0.5em;
        font-size: 11pt;
        text-indent: 0;
    }}

    /* Part titles: slightly larger and medium weight for clear section headers */
    .toc li.toc-part {{
        font-size: 12pt;
        font-weight: 500;
    }}

    /* Nested TOC: Part titles at top level; chapters indented under each part */
    .toc ul ul {{
        margin: 0.25em 0 0.75em 1.25em;
        padding-left: 0;
    }}

    .toc ul ul li {{
        font-size: 10.5pt;
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
        font-size: 10pt;
        letter-spacing: 2.75pt;
        text-transform: uppercase;
        color: #777;
    }}

    /* Chapter title: capture for running header (string-set used in @page @top-center) */
    .chapter-title {{
        text-align: center;
        margin-top: 1em;
        font-size: 22pt;
        font-weight: normal;
        string-set: chapter-title content(text);
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
        font-size: 14pt;
        font-weight: normal;
        margin-top: 1.4em;
        margin-bottom: 0.5em;
        page-break-after: avoid;
    }}
    h2 + p {{
        page-break-before: avoid;
    }}

    h3 {{
        font-size: 12pt;
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
        font-size: 10.5pt;
    }}

    /* LISTS: each item on its own line; block display so PDF/HTML break between items */
    ul, ol {{
        margin: 0.6em 0 0.8em 0;
        padding-left: 1.8em;
        display: block;
    }}
    ol {{
        list-style-type: decimal;
        list-style-position: outside;
    }}
    ul {{
        list-style-type: disc;
        list-style-position: outside;
    }}
    li {{
        display: block;
        margin-top: 0.25em;
        margin-bottom: 0.15em;
        padding-left: 0.25em;
    }}
    ol li:first-child, ul li:first-child {{
        margin-top: 0;
    }}
    .list-number {{
        font-weight: bold;
        margin-right: 0.2em;
    }}
    /* Ordered list items (e.g. questions): default line spacing (no xhtml2pdf-era extra gap) */
    .li-block {{
        display: block;
    }}

    /* TABLES: bordered grid; keep entire table on one page (no split across page break) */
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
        font-size: 10.5pt;
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
        font-size: 10pt;
        line-height: 1.32;
    }}

    /* Box per page: when case study spans pages, each fragment gets its own border/background (clone). */
    .case-study-box {{
        padding: 1.2em 1.5em;
        border: 1px solid #999;
        background: #e8e8e8;
        font-family: "Gill Sans Nova", "Gill Sans", "Gill Sans MT", sans-serif;
        font-size: 10pt;
        line-height: 1.32;
        box-decoration-break: clone;
        -webkit-box-decoration-break: clone;
        display: block;
    }}

    /* Case study title: 2 font sizes bigger than body (10pt -> 14pt) */
    .case-study-title {{
        font-style: normal;
        font-weight: bold;
        letter-spacing: 1.1pt;
        font-size: 14pt;
        margin-bottom: 0.8em;
    }}

    .case-study-box p {{
        margin: 0 0 0.5em 0;
        text-indent: 0;
    }}
    .case-study-box h3 {{
        font-size: 12pt;
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
        font-size: 10.5pt;
        page-break-inside: avoid;
        text-align: left;
    }}

    /* Definition term: allow wrap so long titles (e.g. "THE AI TRANSFORMATION FRAMEWORK") go to next line */
    .definition-title {{
        font-size: 12pt;
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
    }}

    .back-matter h2 {{
        text-align: center;
        font-size: 14pt;
        margin-bottom: 1em;
    }}

    .index-placeholder {{
        font-style: italic;
        color: #666;
        text-indent: 0;
    }}

    /* Remove horizontal rules between sections (line only before Questions, on new page) */
    hr {{
        display: none;
    }}

    /* Questions section: new page with a line above the heading */
    .questions-section {{
        page-break-before: always;
    }}
    .questions-section::before {{
        content: "";
        display: block;
        height: 2px;
        background: #000;
        margin-bottom: 0.8em;
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
        font-size: 18pt;
        font-weight: normal;
        letter-spacing: 2pt;
        margin: 0;
        page-break-after: avoid;
    }}
    """


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
    html_parts.append("<p>© " + str(__import__("datetime").datetime.now().year) + " " + html_module.escape(title) + ". All rights reserved.</p>")
    html_parts.append("<p>This work is for distribution via Amazon KDP and IngramSpark.</p>")
    html_parts.append("</div>")
    html_parts.append('<div class="blank-page"></div>')
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
        introduction_html = inject_ordered_list_numbers(introduction_html)
        html_parts.append('<div class="introduction front-matter" id="introduction">')
        html_parts.append(introduction_html)
        html_parts.append("</div>")

    # Part separator pages (Part I–IV) before the first chapter of each part; then chapters
    toc_by_num = dict(toc_chapters)
    strip_handoff = not dry_run
    for num in chapters_included:
        # Insert part separator page when this chapter starts a part (id for TOC link/page number)
        if num in PART_TITLES:
            part_id = PART_IDS[num]
            part_title = html_module.escape(PART_TITLES[num])
            html_parts.append(f'<div class="part-separator" id="{part_id}"><h2>{part_title}</h2></div>')
        ch_html = build_chapter_html(repo, num, strip_handoff=strip_handoff)
        if not ch_html:
            continue
        ch_title = toc_by_num.get(num, f"Chapter {num}")
        html_parts.append(f'<div class="chapter" id="ch{num:02d}">')
        # Hidden TOC entry so PDF Contents shows "Chapter N - Title" (visible page keeps number + title separate)
        html_parts.append(
            f'<div class="toc-entry-hidden">Chapter {num} - {html_module.escape(ch_title)}</div>'
        )
        html_parts.append(f'<div class="chapter-number">Chapter {chapter_number_word(num)}</div>')
        html_parts.append(f'<div class="chapter-title">{html_module.escape(ch_title)}</div>')
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
h2 { font-size: 1.25em; margin: 1em 0 0.5em 0; }
.subtitle { font-size: 0.9em; color: #444; margin-bottom: 1em; }
.about-the-author { margin-top: 1em; }
img { max-width: 100%; height: auto; }
ul, ol { margin: 0.6em 0 0.8em 0; padding-left: 1.8em; display: block; }
ol { list-style-type: decimal; list-style-position: outside; }
ul { list-style-type: disc; list-style-position: outside; }
li { display: block; margin-top: 0.5em; margin-bottom: 0.25em; padding-left: 0.25em; }
ol li:first-child, ul li:first-child { margin-top: 0; }
.list-number { font-weight: bold; margin-right: 0.2em; }
.li-block { display: block; margin-bottom: 0.5em; }
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
    EPUB metadata (identifier, author, description, language, keywords) is read from
    epub_metadata when provided (from load_epub_metadata(book_dir)).
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
    if meta_description:
        book.add_metadata("DC", "description", meta_description)
    for kw in meta_keywords:
        if kw:
            book.add_metadata("DC", "subject", kw)

    # Cover image (optional): add first so it appears as cover in readers
    if cover_path and cover_path.exists():
        try:
            book.set_cover("cover.png", cover_path.read_bytes())
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

    spine = ["nav"]
    toc_entries = []

    # Front matter: title page + copyright (single xhtml)
    title_content = f"""<h1>{html_module.escape(meta_title)}</h1>
<p class="subtitle">{html_module.escape(meta_subtitle)}</p>
<p>© {__import__('datetime').datetime.now().year} {html_module.escape(meta_title)}. All rights reserved.</p>
<p>This work is for distribution via Amazon KDP and IngramSpark.</p>"""
    title_page = epub.EpubHtml(
        title="Title",
        file_name="title.xhtml",
        lang="en",
        content=f'<html><head><style>{EPUB_CSS}</style></head><body>{title_content}</body></html>',
    )
    book.add_item(title_page)
    spine.append(title_page)
    toc_entries.append(epub.Link("title.xhtml", "Title", "title"))

    # Introduction (optional)
    introduction_md = load_text(repo / "book" / "introduction.md")
    if introduction_md.strip():
        intro_html = markdown_to_html(introduction_md)
        intro_html = inject_ordered_list_numbers(intro_html)
        intro_html = _rewrite_epub_html_images(intro_html, epub_src_mapping)
        intro_page = epub.EpubHtml(
            title="Introduction",
            file_name="introduction.xhtml",
            lang="en",
            content=f'<html><head><style>{EPUB_CSS}</style></head><body>{intro_html}</body></html>',
        )
        book.add_item(intro_page)
        spine.append(intro_page)
        toc_entries.append(epub.Link("introduction.xhtml", "Introduction", "introduction"))

    # Chapters
    for num in chapters_included:
        ch_html = build_chapter_html(repo, num, strip_handoff=strip_handoff)
        if not ch_html:
            continue
        ch_html = _rewrite_epub_html_images(ch_html, epub_src_mapping)
        ch_title = toc_by_num.get(num, f"Chapter {num}")
        # Keep first h1 or add chapter title for nav
        body = strip_first_h1(ch_html)
        full = f'<h1>{html_module.escape(ch_title)}</h1>{body}'
        file_name = f"ch{num:02d}.xhtml"
        ch_page = epub.EpubHtml(
            title=ch_title,
            file_name=file_name,
            lang="en",
            content=f'<html><head><style>{EPUB_CSS}</style></head><body>{full}</body></html>',
        )
        book.add_item(ch_page)
        spine.append(ch_page)
        toc_entries.append(epub.Link(file_name, f"Chapter {num} - {ch_title}", f"ch{num:02d}"))

    # Back matter: About the Author
    if about_author.strip():
        author_html = markdown_to_html(about_author)
        about_content = f'<html><head><style>{EPUB_CSS}</style></head><body><div class="about-the-author">{author_html}</div></body></html>'
    else:
        about_content = '<html><head><style>{EPUB_CSS}</style></head><body><p>[About the Author to be added.]</p></body></html>'
    about_page = epub.EpubHtml(
        title="About the Author",
        file_name="about.xhtml",
        lang="en",
        content=about_content,
    )
    book.add_item(about_page)
    spine.append(about_page)
    toc_entries.append(epub.Link("about.xhtml", "About the Author", "about"))

    book.toc = tuple(toc_entries)
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

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
        subtitle = "A complete AI transformation framework\nEUROPEAN EDITION"
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

    # Cover: omit when --interior; otherwise prefer book/images/cover.png, then book/cover.png, then --cover
    cover_rel = None
    cover_path_for_epub = None
    if not args.interior:
        if (book_dir / "images" / "cover.png").exists():
            cover_rel = "book/images/cover.png"
            cover_path_for_epub = book_dir / "images" / "cover.png"
        elif (book_dir / "cover.png").exists():
            cover_rel = "book/cover.png"
            cover_path_for_epub = book_dir / "cover.png"
        else:
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
            # base_url resolves relative URLs (e.g. cover image book/images/cover.png)
            html_doc = WeasyHTML(string=full_html, base_url=str(repo))
            # Load DM Sans from Google Fonts for PDF typography (Gill Sans Nova requires local/Adobe Fonts)
            font_url = "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&display=swap"
            html_doc.write_pdf(str(out_path), stylesheets=[font_url])
            # Inject metadata (title, author, subject, keywords) from book folder
            pdf_metadata = load_epub_metadata(book_dir)
            inject_pdf_metadata(out_path, pdf_metadata)
            print(f"Wrote {out_path}.")
        except OSError as e:
            raise SystemExit(f"Failed to write PDF: {e}")
    else:
        html_path = out_path.with_suffix(".html")
        html_path.write_text(full_html, encoding="utf-8")
        print(f"Wrote {html_path}.")


if __name__ == "__main__":
    main()
