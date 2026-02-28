#!/usr/bin/env python3
"""
Build a print-ready PDF for Amazon KDP and IngramSpark.

Assembles front matter, chapters (from ch{nn}-final.md), about the author,
and index. Applies consistent styling: definitions in a box with background,
case studies in a distinct layout (serif, background, border).

Uses xhtml2pdf for PDF export (pure Python, no system deps).

Usage:
  Full book (PDF only):
    python build_print_pdf.py --output path/to/book.pdf [--repo /path/to/book]

  Dry run (Chapter 1 only): defaults to HTML; use --pdf to get PDF.
    python build_print_pdf.py --dry-run --output path/to/dry-run.html
    python build_print_pdf.py --dry-run --pdf --output path/to/dry-run.pdf
"""

import argparse
import html as html_module
import re
import os
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None

try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None

# Trim size and margins: 6" x 9"; tighter margins to fit more content
TRIM_WIDTH = "6in"
TRIM_HEIGHT = "9in"
PAGE_TOP = "0.7in"
PAGE_BOTTOM = "0.7in"
PAGE_LEFT = "0.65in"
PAGE_RIGHT = "0.65in"
# Footer: height (pt) and distance from bottom of page (pt); used when using @frame
FOOTER_HEIGHT_PT = 24
FOOTER_FROM_BOTTOM_PT = 14  # Page number sits this far above the physical bottom edge


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
    subtitle ="A CEO's perspective on AI transformations in Europe"
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


def _flatten_definition_body(body_html: str) -> str:
    """
    Flatten definition body to inline content (replace <p>...</p> with <br/><br/>)
    so the definition box has one block = one drawn box in xhtml2pdf.
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
    each to a single block (title + body as inline) so xhtml2pdf draws one box each.
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
            # (xhtml2pdf draws one box per block child; avoid span/div that could split)
            result.append('<div class="definition"><div class="definition-box">')
            result.append("<p class=\"definition-single\">")
            result.append(f'<span class="definition-title">{html_module.escape(title)}</span>')
            if flat_body:
                result.append("<br/><br/>")
                result.append(flat_body)
            result.append("</p></div><div class=\"definition-box-end\"></div></div>")
        pos = end
    return "".join(result)


def _flatten_case_study_to_single_block(fragment: str) -> str:
    """
    Flatten case-study HTML into a single block of inline content so xhtml2pdf
    draws one box (it draws border/background around each block child otherwise).
    Converts block elements to <strong> + <br/> so we keep structure but one block.
    """
    # Replace block boundaries with inline equivalents; result stays in one block.
    s = fragment
    # Headings -> strong + line breaks
    s = re.sub(r"<h2>\s*", r"<strong class=\"case-study-h2\">", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*</h2>", r"</strong><br/><br/>", s, flags=re.IGNORECASE)
    s = re.sub(r"<h3>\s*", r"<br/><strong class=\"case-study-h3\">", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*</h3>", r"</strong><br/><br/>", s, flags=re.IGNORECASE)
    # Paragraphs -> content + double break (remove <p> and </p>)
    s = re.sub(r"<p>\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*</p>", "<br/><br/>", s, flags=re.IGNORECASE)
    # Lists: ul/ol -> break; li -> break + bullet
    s = re.sub(r"<ul>\s*", "<br/>", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*</ul>", "<br/>", s, flags=re.IGNORECASE)
    s = re.sub(r"<li>\s*", "<br/>• ", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*</li>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<ol>\s*", "<br/>", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*</ol>", "<br/>", s, flags=re.IGNORECASE)
    # hr -> break
    s = re.sub(r"<hr\s*/?>", "<br/>", s, flags=re.IGNORECASE)
    # Trim leading break from start
    s = s.strip()
    if s.startswith("<br/>"):
        s = s[5:]
    return s


def wrap_case_study_sections(html: str) -> str:
    """
    Wrap content from <h2>Case Study: ...</h2> until the next <h2> in a single box.
    xhtml2pdf draws border/background around each block child, so we flatten the
    section to one block of inline content (strong + br) so it renders as one box.
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
        flattened = _flatten_case_study_to_single_block(fragment)
        result.append(html[pos:section_start])
        # One block = one box; start on new page
        result.append('<div class="case-study"><div class="case-study-box">')
        result.append(flattened)
        result.append("</div></div>")
        pos = next_h2
    return "".join(result)


def build_chapter_html(repo: Path, chapter_num: int, strip_handoff: bool = True) -> str:
    """
    Load ch{nn}-final.md, convert to HTML, apply definition and case-study wrappers.
    When strip_handoff is True (e.g. full build), remove Handoff sections from the PDF.
    When False (dry-run HTML or PDF), keep Handoff sections for review.
    """
    nn = f"{chapter_num:02d}"
    path = repo / "output" / "chapters" / f"chapter-{nn}" / f"ch{nn}-final.md"
    if not path.exists():
        return ""
    md = load_text(path)
    # Strip handoff/metadata sections (e.g. ## Handoff: Reviewers) only for final PDF build
    if strip_handoff and "## Handoff:" in md:
        md = md.split("## Handoff:")[0].rstrip()
    html = markdown_to_html(md)
    html = wrap_definition_blocks(html)
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


def build_toc_html(chapters_included: list[int], toc_chapters: list[tuple[int, str]]) -> str:
    """Build TOC list for the chapters we include; each entry shows 'Chapter N - Title'."""
    items = []
    for num, name in toc_chapters:
        if num in chapters_included:
            items.append(f'<li><a href="#ch{num:02d}">Chapter {num} - {name}</a></li>')
    return "<ul>" + "".join(items) + "</ul>"


def get_css(for_pdf: bool = True) -> str:
    """
    Return CSS for print typography and layout.
    When for_pdf=True uses @page with content frame + footer frame for page numbers.
    When for_pdf=False uses simple margin @page (for HTML preview).
    """
    if for_pdf:
        # 6in x 9in = 432pt x 648pt; margins 0.7in=50.4pt, 0.65in=46.8pt
        left_pt = 47
        top_pt = 50
        bottom_pt = 50
        width_pt = 432 - left_pt * 2
        # Content height: full for front matter; reduced for content pages (room for footer)
        content_height_pt = 648 - top_pt - bottom_pt - FOOTER_HEIGHT_PT
        front_content_height_pt = 648 - top_pt - bottom_pt  # No footer on front matter
        # Place footer near bottom of page (in bottom margin) so page number sits much lower
        footer_top_pt = 648 - FOOTER_FROM_BOTTOM_PT - FOOTER_HEIGHT_PT
        page_setup = f"""
    /* PAGE SETUP: two templates — front (no page numbers), content (with footer) */
    /* Default template: half-title, title, copyright, TOC — no page numbers */
    @page {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        @frame content_frame {{
            left: {left_pt}pt;
            width: {width_pt}pt;
            top: {top_pt}pt;
            height: {front_content_height_pt}pt;
        }}
    }}
    /* Content template: from Introduction onwards — page numbers in footer */
    @page content {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        @frame content_frame {{
            left: {left_pt}pt;
            width: {width_pt}pt;
            top: {top_pt}pt;
            height: {content_height_pt}pt;
        }}
        @frame footer_frame {{
            -pdf-frame-content: footer_content;
            left: {left_pt}pt;
            width: {width_pt}pt;
            top: {footer_top_pt}pt;
            height: {FOOTER_HEIGHT_PT}pt;
        }}
    }}"""
    else:
        page_setup = f"""
    @page {{
        size: {TRIM_WIDTH} {TRIM_HEIGHT};
        margin: {PAGE_TOP} {PAGE_RIGHT} {PAGE_BOTTOM} {PAGE_LEFT};
    }}"""
    return page_setup + f"""

    /* BASE TYPOGRAPHY: slightly smaller, denser line spacing */
    body {{
        font-family: Georgia, "Times New Roman", serif;
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

    /* HALF TITLE: reduced top space */
    .half-title-page {{
        text-align: center;
        page-break-after: always;
    }}

    .half-title-page h1 {{
        margin-top: 2in;
        font-size: 24pt;
        font-weight: normal;
        -pdf-outline: false;  /* Exclude from TOC: front matter before Contents */
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
        -pdf-outline: false;  /* Exclude from TOC: front matter before Contents */
    }}

    .title-page .subtitle {{
        margin-top: 0.8em;
        font-size: 13pt;
        font-style: italic;
        color: #444;
    }}

    .title-page .author {{
        margin-top: 1.5em;
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

    /* INTRODUCTION: front matter after TOC, before Chapter 1 */
    .introduction {{
        page-break-before: always;
    }}

    .introduction h1 {{
        text-align: center;
        margin-top: 1.4in;
        font-size: 22pt;
        font-weight: normal;
        -pdf-outline: true;
        -pdf-outline-level: 0;
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

    .toc a {{
        color: #111;
        text-decoration: none;
    }}

    /* TOC from xhtml2pdf: page numbers filled automatically */
    pdftoc {{
        color: #111;
        font-size: 11pt;
    }}
    pdftoc.pdftoclevel0 {{
        margin-bottom: 0.5em;
        list-style: none;
    }}

    /* Section headings not in TOC (only chapters) */
    h2 {{ -pdf-outline: false; }}
    h3 {{ -pdf-outline: false; }}

    /* CHAPTER OPENING: less empty space */
    .chapter {{
        page-break-before: always;
    }}

    .chapter-number {{
        text-align: center;
        margin-top: 1.4in;
        font-size: 10pt;
        letter-spacing: 2.75pt;
        text-transform: uppercase;
        color: #777;
    }}

    .chapter-title {{
        text-align: center;
        margin-top: 1em;
        font-size: 22pt;
        font-weight: normal;
        -pdf-outline: false;  /* TOC uses .toc-entry-hidden for "Chapter N - Title" */
    }}

    /* Hidden element used only for PDF TOC so entries show "Chapter N - Title" */
    .toc-entry-hidden {{
        position: absolute;
        left: -9999px;
        font-size: 0;
        height: 0;
        overflow: hidden;
        visibility: hidden;
        -pdf-outline: true;
        -pdf-outline-level: 0;
    }}

    .chapter-divider {{
        width: 60px;
        height: 1px;
        background: #000;
        margin: 1.2em auto 2em auto;
    }}

    /* SECTION HEADINGS: tighter */
    h2 {{
        font-size: 14pt;
        font-weight: normal;
        margin-top: 1.4em;
        margin-bottom: 0.5em;
    }}

    h3 {{
        font-size: 12pt;
        margin-top: 1.1em;
        margin-bottom: 0.4em;
        font-style: italic;
        font-weight: normal;
    }}

    /* BLOCKQUOTE (general) */
    blockquote {{
        margin: 1em 1.2em;
        font-style: italic;
        font-size: 10.5pt;
    }}

    /* LISTS: compact */
    ul, ol {{
        margin: 0.5em 0 0.5em 1.2em;
        padding-left: 1em;
    }}

    li {{
        margin-bottom: 0.25em;
    }}

    /* CASE STUDY: one box; tighter padding; Arial Narrow throughout */
    .case-study {{
        margin: 1.5em 0;
        page-break-before: always;
        font-family: "Arial Narrow", Arial, sans-serif;
    }}

    .case-study-box {{
        padding: 1.2em 1.5em;
        border: 1px solid #ccc;
        background: #f9f9f9;
        page-break-inside: avoid;
        font-family: "Arial Narrow", Arial, sans-serif;
    }}

    .case-study-h2 {{
        font-style: normal;
        letter-spacing: 1.1pt;
        text-transform: uppercase;
        font-size: 10pt;
    }}

    .case-study-h3 {{
        font-size: 12pt;
        font-style: italic;
        font-weight: normal;
    }}

    /* DEFINITION: one dedicated box per definition (title + text together);
       consecutive definitions get clear separation. */
    .definition {{
        margin: 1.2em 0 1.8em 0;
    }}

    /* Force an empty line after each definition box so the next paragraph is
       visually separated. Using ::after avoids margin collapse with the next block. */
    .definition::after {{
        content: "";
        display: block;
        height: 1em;
    }}

    /* PDF parser: definition box ends here; next block is body text.
       .definition-box-end is a line item after each definition so PDF and HTML parsers
       can detect definition boundaries. */
    .definition-box-end {{
        display: block;
        height: 0;
        margin: 0;
        padding: 0;
        border-top: 1px solid transparent;
        clear: both;
    }}

    /* Space between two definitions in a row so each box is distinct */
    .definition + .definition {{
        margin-top: 1em;
    }}

    .definition-box {{
        padding: 1em 1.5em;
        border: 1px solid #ccc;
        border-left: 3px solid #000;
        background: #fafafa;
        font-size: 10.5pt;
        page-break-inside: avoid;
    }}

    /* Definition term: uppercase, one font size bigger, wider letter spacing for emphasis */
    .definition-title {{
        font-size: 12pt;
        font-weight: normal;
        letter-spacing: 5pt;
        text-transform: uppercase;
        color: #555;
    }}

    /* Single paragraph = one block = one box; title stays inline inside it */
    .definition-single {{
        text-indent: 0;
        margin: 0;
    }}

    /* BACK MATTER */
    .back-matter {{
        page-break-before: always;
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
) -> str:
    """Assemble full HTML document with front matter, chapters, back matter."""
    html_parts = [
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"/>",
        "<title>" + title + "</title>",
        "<style>" + get_css(for_pdf=for_pdf) + "</style>",
        "</head><body>",
    ]
    if for_pdf:
        html_parts.append(
            # Footer for every page (xhtml2pdf static frame; right-aligned, lower — leaves more space)
            '<div id="footer_content" style="text-align: right; font-size: 9pt; color: #555;">'
            "Page <pdf:pagenumber>\nof <pdf:pagecount>\n</div>"
        )
    html_parts.extend([
        '<div class="half-title-page"><h1>' + title + "</h1></div>",
        '<div class="title-page">',
        "<h1>" + title + "</h1>",
        '<div class="subtitle">' + subtitle + "</div>",
        '<div class="author"></div>',
        "</div>",
        '<div class="copyright-page">',
        "<p>© " + str(__import__("datetime").datetime.now().year) + " " + title + ". All rights reserved.</p>",
        "<p>This work is for distribution via Amazon KDP and IngramSpark.</p>",
        "</div>",
        '<div class="toc"><h2>Contents</h2>'
        + (
            '<div><pdf:toc /></div>'
            if for_pdf
            else build_toc_html(chapters_included, toc_chapters)
        )
        + "</div>",
    ])

    # Switch to content page template so page numbers appear only from Introduction onwards
    if for_pdf:
        html_parts.append('<div><pdf:nexttemplate name="content"></div>')

    # Introduction: optional front matter from output/misc/introduction.md (after TOC, before Chapter 1)
    introduction_md = load_text(repo / "output" / "misc" / "introduction.md")
    if introduction_md.strip():
        introduction_html = markdown_to_html(introduction_md)
        html_parts.append('<div class="introduction" id="introduction">')
        html_parts.append(introduction_html)
        html_parts.append("</div>")

    # Chapters: opening per book-layout (chapter-number, chapter-title, divider); strip first h1 from content
    # For dry-run (HTML or PDF) keep handoff sections; for full build strip them from the PDF
    toc_by_num = dict(toc_chapters)
    strip_handoff = not dry_run
    for num in chapters_included:
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
    args = parser.parse_args()

    # Resolve repo root (script lives in skills/publish-kdp-ingramspark/scripts/; book root has plan/toc.md)
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

    # About the Author: back matter at end of book (from output/misc)
    about_author = load_text(repo / "output" / "misc" / "about-the-author.md")

    want_pdf = (not args.dry_run) or args.pdf
    full_html = build_full_html(
        repo=repo,
        title=title,
        subtitle=subtitle,
        chapters_included=chapters_included,
        toc_chapters=toc_chapters,
        about_author=about_author,
        dry_run=args.dry_run,
        for_pdf=want_pdf,
    )

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if want_pdf:
        if pisa is None:
            raise SystemExit(
                "PDF export requires xhtml2pdf. Install with: pip install xhtml2pdf"
            )
        try:
            with open(out_path, "wb") as pdf_file:
                status = pisa.CreatePDF(
                    full_html.encode("utf-8"),
                    dest=pdf_file,
                    encoding="utf-8",
                    path=str(repo),
                )
            if status.err:
                raise SystemExit("xhtml2pdf reported errors while creating PDF.")
            print(
                f"Wrote {out_path} ({'dry-run: chapter 1 only' if args.dry_run else 'full book'})."
            )
        except OSError as e:
            raise SystemExit(f"Failed to write PDF: {e}")
    else:
        # Dry run, default: output HTML (same stem as --output, force .html)
        html_path = out_path.with_suffix(".html")
        html_path.write_text(full_html, encoding="utf-8")
        print(f"Wrote {html_path} (dry-run: chapter 1 only). Use --dry-run --pdf to export PDF.")


if __name__ == "__main__":
    main()
