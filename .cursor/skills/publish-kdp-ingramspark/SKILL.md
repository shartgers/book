---
name: publish-kdp-ingramspark
description: Builds a print-ready PDF for Amazon KDP and IngramSpark from the book manuscript. Use when publishing the book, preparing interior files for KDP/IngramSpark, testing a dry-run (chapter 1 only), or styling definitions and case studies for print.
---

# Publish for KDP and IngramSpark

Build a single print-ready PDF containing all front matter, chapters, about the author, and index. Styled for professional interior layout with distinct treatment for definitions (box + background) and case studies (serif, background, border).

## When to Use

- User asks to publish the book for Amazon KDP or IngramSpark
- User wants a PDF with all chapters, author bio, index, and proper layout
- User wants to **dry-run** (only Chapter 1 in body; full front/back matter still included)
- User wants definitions in a box with background and case studies in a different layout

## Quick Start

From the **book repository root** (where `plan/toc.md` and `output/chapters/` live):

```bash
# Full book (all chapters)
python .cursor/skills/publish-kdp-ingramspark/scripts/build_print_pdf.py --output output/book-print.pdf

# Dry run: only Chapter 1 in body; front matter, TOC, About the Author, Index still included
python .cursor/skills/publish-kdp-ingramspark/scripts/build_print_pdf.py --dry-run --output output/book-print-dry-run.pdf
```

Install dependencies first (see [Requirements](#requirements) below).

## What the Script Produces

1. **Front matter**: Half title, title page, copyright, table of contents
2. **Body**: Chapters from `output/chapters/chapter-{nn}/ch{nn}-final.md` (in dry-run, only chapter 1)
3. **Back matter**: About the Author (from `input/about-the-author.md`), Index (heading-based or placeholder)
4. **Styling**:
   - **Definitions**: Blockquotes matching `> **Definition: Term**` are rendered in a box with a light background colour so they stand out consistently
   - **Case studies**: Sections starting with `## Case Study:` get a distinct layout (e.g. serif font, tinted background, border) so they read as a separate voice

## Requirements

- Python 3.9+
- Dependencies in `.cursor/skills/publish-kdp-ingramspark/requirements.txt`:
  - `markdown` — Markdown to HTML
  - `weasyprint` — HTML/CSS to PDF (install system dependencies per [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) if needed)

Install from repo root:

```bash
pip install -r .cursor/skills/publish-kdp-ingramspark/requirements.txt
```

## Inputs (configurable via script or env)

| Input | Default | Purpose |
|-------|---------|---------|
| Book root | Auto-detected (parent of `plan/toc.md`) or `--repo` | Where chapters and plan live |
| Chapters | `output/chapters/chapter-{01..10}/ch{nn}-final.md` | Final chapter markdown; only existing files are included |
| TOC | `plan/toc.md` | Title, subtitle, chapter list for TOC page |
| About the Author | `input/about-the-author.md` | Back matter author bio |

Dry-run limits the **body** to Chapter 1 only; front and back matter are unchanged.

## Platform Notes

- **Amazon KDP**: Use the PDF as the interior file. Prepare manuscript and cover per [KDP](https://kdp.amazon.com); use Kindle Create for e-book formatting if needed.
- **IngramSpark**: Use the same PDF for print (paperback/hardcover). Ensure trim size and bleed match IngramSpark specs; see [reference.md](reference.md) for trim sizes and margins.

For detailed specs (trim sizes, bleed, margins, ISBN/barcode), see [reference.md](reference.md).

## If the Script Fails

- **WeasyPrint errors**: Install GTK3/Pango/Cairo per your OS (see WeasyPrint first steps). On Windows, WeasyPrint often cannot load GTK; the script then writes an **HTML file** (same path as `--output` but with `.html`) so you can open it in a browser and use **Print → Save as PDF** for a quick PDF. For native PDF on Windows, install WeasyPrint’s system dependencies or use another HTML-to-PDF tool.
- **Missing chapter**: Script skips missing `ch{nn}-final.md`; dry-run only needs `ch01-final.md`.
- **No about-the-author**: If `input/about-the-author.md` is missing, back matter still renders with a placeholder.
