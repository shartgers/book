---
name: format-book-agent
description: Builds a print-ready PDF for Amazon KDP and IngramSpark from the book manuscript. Use when publishing the book, preparing interior files for KDP/IngramSpark, testing a dry-run (chapter 1 only), or styling definitions and case studies for print.
---

# Format-Book-Agent — Publish for KDP and IngramSpark

Build a single print-ready PDF containing all front matter, chapters, about the author, and index. Styled for professional interior layout with distinct treatment for definitions (box + background) and case studies (serif, background, border).

## When to Use

- User asks to publish the book for Amazon KDP or IngramSpark
- User wants a PDF with all chapters, author bio, index, and proper layout
- User wants to **dry-run** (only Chapter 1 in body; full front/back matter still included)
- User wants definitions in a box with background and case studies in a different layout

## Quick Start

From the **book repository root** (where `plan/toc.md` and `output/chapters/` live):

```bash
# Full book (all chapters) — outputs PDF only
python skills/format-book-agent/scripts/build_print_pdf.py --output output/book-print.pdf

# Dry run: Chapter 1 only; defaults to HTML (quick preview in browser)
python skills/format-book-agent/scripts/build_print_pdf.py --dry-run --output output/book-dry-run.html

# Dry run as PDF when you want a PDF preview
python skills/format-book-agent/scripts/build_print_pdf.py --dry-run --pdf --output output/book-dry-run.pdf
```

Install dependencies first (see [Requirements](#requirements) below).

## What the Script Produces

1. **Front matter**: Half title, title page, copyright, table of contents
2. **Body**: Introduction (optional, from `output/misc/introduction.md` when present), then chapters from `output/chapters/chapter-{nn}/ch{nn}-final.md` (in dry-run, only chapter 1)
3. **Back matter**: About the Author (from `output/misc/about-the-author.md`), Index (heading-based or placeholder)
4. **Styling**:
   - **Definitions**: Blockquotes matching `> **Definition: Term**` are rendered in a box with a light background colour so they stand out consistently
   - **Case studies**: Sections starting with `## Case Study:` get a distinct layout (e.g. serif font, tinted background, border) so they read as a separate voice

## Requirements

- Python 3.9+
- Dependencies in `skills/format-book-agent/requirements.txt`:
  - `markdown` — Markdown to HTML
  - `xhtml2pdf` — HTML to PDF (pure Python, no system dependencies)

Install from repo root:

```bash
pip install -r skills/format-book-agent/requirements.txt
```

## Inputs (configurable via script or env)

| Input | Default | Purpose |
|-------|---------|---------|
| Book root | Auto-detected (parent of `plan/toc.md`) or `--repo` | Where chapters and plan live |
| Chapters | `output/chapters/chapter-{01..10}/ch{nn}-final.md` | Final chapter markdown; only existing files are included |
| TOC | `plan/toc.md` | Title, subtitle, chapter list for TOC page |
| Introduction | `output/misc/introduction.md` | Optional front matter after TOC, before Chapter 1 |
| About the Author | `output/misc/about-the-author.md` | Back matter author bio |

Dry-run limits the **body** to Chapter 1 only; front and back matter are unchanged.

## Platform Notes

- **Amazon KDP**: Use the PDF as the **interior (manuscript)** file. KDP requires two files: interior + cover; this skill builds only the interior. Prepare the cover separately (Cover Creator, template, or designer). The build matches [KDP's "Format Your Paperback"](https://kdp.amazon.com/help/topic/G201834190) steps (trim/margins, front/body/back matter, save for upload). Use Kindle Create for e-book formatting if needed.
- **IngramSpark**: Use the same PDF for print (paperback/hardcover). Ensure trim size and bleed match IngramSpark specs; see [reference.md](reference.md) for trim sizes and margins.

For detailed specs and KDP alignment (trim, margins, bleed, gutter by page count, save guidelines), see [reference.md](reference.md).

## If the Script Fails

- **PDF export**: The script uses **xhtml2pdf** for PDF. Install with `pip install xhtml2pdf`. Full book always outputs PDF; dry-run defaults to HTML (use `--dry-run --pdf` for a PDF preview).
- **Missing chapter**: Script skips missing `ch{nn}-final.md`; dry-run only needs `ch01-final.md`.
- **No about-the-author**: If `output/misc/about-the-author.md` is missing, back matter still renders with a placeholder.
