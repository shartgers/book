#!/usr/bin/env python3
"""
Build a print-ready PDF for Amazon KDP and IngramSpark.

Assembles front matter, chapters (from ch{nn}-final.md), about the author,
and index. Applies consistent styling: definitions in a box with background,
case studies in a distinct layout (serif, background, border).

Usage:
  python build_print_pdf.py --output path/to/book.pdf [--dry-run] [--repo /path/to/book]
  --dry-run: include only Chapter 1 in the body; front and back matter unchanged.
"""

import argparse
import re
import os
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None
# WeasyPrint requires GTK/Pango on Windows; if import fails we fall back to HTML-only output
try:
    from weasyprint import HTML as WeasyHTML
    from weasyprint import CSS
except (ImportError, OSError):
    WeasyHTML = None

# Default trim size: 6" x 9" (common for business books)
TRIM_WIDTH = "6in"
TRIM_HEIGHT = "9in"
INNER_MARGIN = "0.75in"
OUTER_MARGIN = "0.5in"
TOP_BOTTOM_MARGIN = "0.6in"


def find_repo_root(start: Path) -> Path:
    """Find directory containing plan/toc.md (book root)."""
    current = start.resolve()
    for _ in range(10):
        if (current / "plan" / "toc.md").exists():
            return current
        current = current.parent
    return start


def load_text(path: Path) -> str:
    """Load file content; return empty string if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def parse_toc(toc_content: str) -> tuple[str, str, list[tuple[int, str]]]:
    """
    Parse plan/toc.md for title, subtitle, and chapter list.
    Returns (title, subtitle, [(num, title), ...]).
    """
    title = "The Agentic Enterprise"
    subtitle = "A European CEO's Guide to Leading AI Transformation"
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
    # First line often has title and subtitle
    lines = toc_content.strip().split("\n")
    if lines:
        first = lines[0].strip()
        if first and not first.startswith("#"):
            title = first
        if len(lines) > 1 and "CEO" in lines[1]:
            subtitle = lines[1].strip().lstrip("#").strip()
    return title, subtitle, chapters


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


def wrap_definition_blocks(html: str) -> str:
    """
    Wrap blockquotes that contain 'Definition:' in a div.definition-block
    so they can be styled with a box and background.
    """
    # Find <blockquote>...</blockquote> that contains Definition:
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
        if "Definition:" in block or "**Definition:" in block:
            result.append(html[pos:start])
            result.append('<div class="definition-block">')
            result.append(block)
            result.append("</div>")
        else:
            result.append(html[pos:end])
        pos = end
    return "".join(result)


def wrap_case_study_sections(html: str) -> str:
    """
    Wrap content from <h2>Case Study: ...</h2> until the next <h2>
    in a div.case-study for distinct layout (serif, background, border).
    """
    result = []
    pos = 0
    while True:
        # Case-insensitive match for h2 containing "Case Study:"
        match = re.search(
            r"<h2>\s*Case\s+Study\s*:\s*[^<]+</h2>",
            html[pos:],
            re.IGNORECASE,
        )
        if not match:
            result.append(html[pos:])
            break
        start_in_slice = match.start()
        end_of_h2 = match.end()
        section_start = pos + start_in_slice
        section_end = pos + end_of_h2
        # Find next <h2> after this one
        next_h2 = html.find("<h2>", section_end)
        if next_h2 == -1:
            next_h2 = len(html)
        result.append(html[pos:section_start])
        result.append('<div class="case-study">')
        result.append(html[section_start:next_h2])
        result.append("</div>")
        pos = next_h2
    return "".join(result)


def build_chapter_html(repo: Path, chapter_num: int) -> str:
    """Load ch{nn}-final.md, convert to HTML, apply definition and case-study wrappers."""
    nn = f"{chapter_num:02d}"
    path = repo / "output" / "chapters" / f"chapter-{nn}" / f"ch{nn}-final.md"
    if not path.exists():
        return ""
    md = load_text(path)
    # Strip handoff/metadata sections (e.g. ## Handoff: Reviewers) so they don't appear in print
    if "## Handoff:" in md:
        md = md.split("## Handoff:")[0].rstrip()
    html = markdown_to_html(md)
    html = wrap_definition_blocks(html)
    html = wrap_case_study_sections(html)
    return html


def build_toc_html(chapters_included: list[int], toc_chapters: list[tuple[int, str]]) -> str:
    """Build a simple TOC list for the chapters we actually include."""
    items = []
    for num, name in toc_chapters:
        if num in chapters_included:
            items.append(f'<li><a href="#ch{num:02d}">Chapter {num}: {name}</a></li>')
    return "<ul class=\"toc-list\">" + "".join(items) + "</ul>"


def get_css() -> str:
    """Return CSS for print: page setup, typography, definition boxes, case studies."""
    return f"""
    @page {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {TOP_BOTTOM_MARGIN} {OUTER_MARGIN} {TOP_BOTTOM_MARGIN} {INNER_MARGIN};
    }}

    @page :first {{
        margin-top: 2in;
    }}

    body {{
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #1a1a1a;
    }}

    h1 {{
        font-size: 1.8em;
        margin-top: 0.5em;
        margin-bottom: 0.4em;
        page-break-after: avoid;
    }}

    h2 {{
        font-size: 1.35em;
        margin-top: 1.2em;
        margin-bottom: 0.5em;
        page-break-after: avoid;
    }}

    h3 {{
        font-size: 1.15em;
        margin-top: 0.9em;
        margin-bottom: 0.35em;
        page-break-after: avoid;
    }}

    p {{
        margin-top: 0.4em;
        margin-bottom: 0.4em;
        text-align: justify;
    }}

    /* Definition blocks: box with background for consistent treatment */
    .definition-block {{
        margin: 1em 0;
        padding: 0.9em 1em;
        background-color: #e8f4f8;
        border-left: 4px solid #2a7a9e;
        border-radius: 0 4px 4px 0;
        page-break-inside: avoid;
    }}

    .definition-block blockquote {{
        margin: 0;
        padding: 0;
        border: none;
        background: transparent;
    }}

    .definition-block p {{
        margin: 0.25em 0;
    }}

    .definition-block strong {{
        color: #1a5a72;
    }}

    /* Case studies: distinct layout — serif, tinted background, border */
    .case-study {{
        font-family: Georgia, "Times New Roman", serif;
        margin: 1.5em 0;
        padding: 1.2em 1.25em;
        background-color: #faf8f5;
        border: 1px solid #c4b8a8;
        border-radius: 4px;
        page-break-inside: avoid;
    }}

    .case-study h2 {{
        font-family: Georgia, "Times New Roman", serif;
        color: #3d3528;
        border-bottom: 1px solid #c4b8a8;
        padding-bottom: 0.3em;
    }}

    .case-study p {{
        font-size: 10.5pt;
    }}

    .toc-list {{
        list-style: none;
        padding-left: 0;
    }}

    .toc-list li {{
        margin: 0.4em 0;
    }}

    .toc-list a {{
        color: #1a1a1a;
        text-decoration: none;
    }}

    .half-title-page, .title-page {{
        text-align: center;
        page-break-after: always;
    }}

    .half-title-page h1 {{
        margin-top: 2.5in;
        font-size: 1.6em;
    }}

    .title-page h1 {{
        margin-top: 1.5in;
        font-size: 1.8em;
    }}

    .title-page .subtitle {{
        font-size: 1.1em;
        margin-top: 0.5em;
        color: #444;
    }}

    .copyright-page {{
        font-size: 9pt;
        color: #555;
        page-break-after: always;
    }}

    .toc-page h2 {{
        page-break-after: always;
    }}

    .chapter {{
        page-break-before: always;
    }}

    .chapter h1:first-child {{
        margin-top: 0.25in;
    }}

    .back-matter {{
        page-break-before: always;
    }}

    .index-placeholder {{
        font-style: italic;
        color: #666;
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
) -> str:
    """Assemble full HTML document with front matter, chapters, back matter."""
    # Front matter
    html_parts = [
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"/>",
        "<title>" + title + "</title>",
        "<style>" + get_css() + "</style>",
        "</head><body>",
        '<div class="half-title-page"><h1>' + title + "</h1></div>",
        '<div class="title-page">',
        "<h1>" + title + "</h1>",
        '<p class="subtitle">' + subtitle + "</p>",
        "</div>",
        '<div class="copyright-page">',
        "<p>© " + str(__import__("datetime").datetime.now().year) + " " + title + ". All rights reserved.</p>",
        "<p>This work is for distribution via Amazon KDP and IngramSpark.</p>",
        "</div>",
        '<div class="toc-page"><h2>Contents</h2>',
        build_toc_html(chapters_included, toc_chapters),
        "</div>",
    ]

    # Chapters
    for num in chapters_included:
        ch_html = build_chapter_html(repo, num)
        if not ch_html:
            continue
        html_parts.append(f'<div class="chapter" id="ch{num:02d}">')
        html_parts.append(ch_html)
        html_parts.append("</div>")

    # Back matter: About the Author
    html_parts.append('<div class="back-matter">')
    if about_author.strip():
        # About the author may be markdown (e.g. ## About the Author\n\n...)
        author_html = markdown_to_html(about_author)
        html_parts.append('<div class="about-the-author">')
        html_parts.append(author_html)
        html_parts.append("</div>")
    else:
        html_parts.append('<p class="index-placeholder">[About the Author to be added.]</p>')

    # Index: placeholder or simple note
    html_parts.append('<h2>Index</h2>')
    html_parts.append(
        '<p class="index-placeholder">Index entries can be added before final print. '
        'Use your layout tool or a dedicated indexer for page numbers.</p>'
    )
    html_parts.append("</div>")
    html_parts.append("</body></html>")
    return "".join(html_parts)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build print-ready PDF for KDP and IngramSpark.",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output PDF path",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Include only Chapter 1 in body; front and back matter unchanged",
    )
    parser.add_argument(
        "--repo",
        default=None,
        help="Book repository root (default: auto-detect from script location)",
    )
    args = parser.parse_args()

    # Resolve repo root (script lives in .cursor/skills/.../scripts/; book root has plan/toc.md)
    if args.repo:
        repo = Path(args.repo)
    else:
        repo = find_repo_root(Path(__file__).parent)
    if not (repo / "plan" / "toc.md").exists():
        raise SystemExit("Repository root not found (no plan/toc.md). Use --repo /path/to/book.")

    toc_content = load_text(repo / "plan" / "toc.md")
    title, subtitle, toc_chapters = parse_toc(toc_content)

    if args.dry_run:
        chapters_included = [1]
    else:
        # Include every chapter that has a final file
        chapters_included = []
        for num, _ in toc_chapters:
            nn = f"{num:02d}"
            if (repo / "output" / "chapters" / f"chapter-{nn}" / f"ch{nn}-final.md").exists():
                chapters_included.append(num)

    if not chapters_included:
        raise SystemExit("No chapter files found. In dry-run, ch01-final.md must exist.")

    about_author = load_text(repo / "input" / "about-the-author.md")

    full_html = build_full_html(
        repo=repo,
        title=title,
        subtitle=subtitle,
        chapters_included=chapters_included,
        toc_chapters=toc_chapters,
        about_author=about_author,
        dry_run=args.dry_run,
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if WeasyHTML is None:
        # Write HTML when WeasyPrint unavailable (e.g. Windows without GTK/Pango)
        html_path = out_path.with_suffix(".html")
        html_path.write_text(full_html, encoding="utf-8")
        print(
            f"Wrote {html_path} (dry-run: chapter 1 only). "
            "For PDF: install WeasyPrint system deps (see reference.md) or convert HTML to PDF in a browser (Print to PDF)."
        )
        return

    html_doc = WeasyHTML(string=full_html, base_url=str(repo))
    html_doc.write_pdf(out_path)
    print(f"Wrote {out_path} ({'dry-run: chapter 1 only' if args.dry_run else 'full book'}).")


if __name__ == "__main__":
    main()
