---
name: format-book-agent
description: Builds print-ready PDF, EPUB, and HTML from the book manuscript. Use for KDP/IngramSpark, e-readers, or browser preview.
---

# Format-Book-Agent — PDF, EPUB, HTML

Build a print-ready PDF (for KDP/IngramSpark), an EPUB (for e-readers), or a single HTML file from the same `book/` sources. All outputs include full front matter, chapters, and back matter, with distinct styling for definitions and case studies.

## When to Use

- User asks to publish the book for Amazon KDP or IngramSpark (PDF)
- User wants an **EPUB** for e-readers or Kindle
- User wants **HTML** for browser preview or web
- User wants a PDF, EPUB, or HTML with all chapters and author bio

## Quick Start

From the **book repository root** (where the `book/` folder lives):

```bash
# Interior PDF — paperback trim (5.5"×8.25"); default filename
npm run pdf              # → output/book-interior.pdf
npm run pdf:paperback    # → output/book-interior-paperback.pdf (same build as pdf)

# Interior PDF — hardcover *target* (same trim as paperback until HARDCOVER is edited in build_print_pdf.py)
npm run pdf:hardcover    # → output/book-interior-hardcover.pdf

npm run epub   # → output/book-interior.epub
npm run epub:validate   # build EPUB then validate with EPUBCheck (industry/IngramSpark standard)
npm run html   # → output/book-interior.html

# PDF/X-3:2002 (runs pdf:hardcover, then Ghostscript) — for IngramSpark B&W interior
npm run pdfx   # → output/<ISBN13>_txt.pdf (ISBN from input/ISBN hardcover.md)

# Full book with cover
npm run full   # → output/book-full.pdf
```

**Paperback vs PDF/X:** Use **`npm run pdf`** (or **`pdf:paperback`**) for a normal interior PDF at paperback trim. Use **`npm run pdfx`** when you need the grayscale PDF/X file named with the hardcover ISBN (`<ISBN13>_txt.pdf`). Those pipelines differ by output filename and PDF/X conversion, not by layout, until you give `HARDCOVER` a different trim in code.

**When asked to create PDF/X files for the interior:** Produce **`<ISBN13>_txt.pdf`**. Page size follows **`HARDCOVER`** in `build_print_pdf.py` (currently matches paperback). ISBN 13 digits are read from `input/ISBN hardcover.md` (line `ISBN/EAN: 978-...`); hyphens are stripped for the filename.

Equivalent Python commands:

```bash
python skills/format-book-agent/scripts/build_print_pdf.py --interior --output output/book-interior.pdf
python skills/format-book-agent/scripts/build_print_pdf.py --interior --epub --output output/book-interior.epub
python skills/format-book-agent/scripts/build_print_pdf.py --interior --html --output output/book-interior.html
```

To create the PDF/X interior (hardcover only):

```bash
python skills/format-book-agent/scripts/build_print_pdf.py --interior --format hardcover --output output/book-interior-hardcover.pdf
python skills/format-book-agent/scripts/convert_interiors_to_pdfx.py
```

Use `--interior` for interior-only output (no cover). Use `--format paperback` (default) or `--format hardcover` for page size. Omit `--interior` to include cover. Use `--cover path/to/other.png` to override the default cover path.

**EPUB validation (industry / IngramSpark):** After building the EPUB, validate it with the official W3C EPUBCheck via `npm run validate:epub` (validates existing `output/book-interior.epub`) or `npm run epub:validate` (build then validate). Requires Java 7+. Distributors typically require EPUBCheck to pass; fix reported errors before submitting.

Install dependencies first (see [Requirements](#requirements) below).

## What the Script Produces

1. **Cover page** (optional): When `book/images/cover.png` exists and `--interior` is not set, the first page is a full-page cover image.
2. **Front matter**: Half title, title page, copyright, table of contents
3. **Body**: Introduction (optional, from `book/introduction.md` when present), then chapters from `book/chNN-*.md` or `book/chapter-NN.md`
4. **Back matter**: About the Author (from `book/about-the-author.md`), Index (heading-based or placeholder)
5. **Styling**:
   - **Definitions**: Blockquotes matching `> **Definition: Term**` are rendered in a box with a light background colour so they stand out consistently
   - **Case studies**: Sections starting with `## Case Study:` get a distinct layout (e.g. serif font, tinted background, border) so they read as a separate voice
   - **Tables**: Markdown pipe tables are rendered with borders (grid), header background, and cell padding in PDF, HTML, and EPUB

## Requirements

- Python 3.9+
- Dependencies in `skills/format-book-agent/requirements.txt`:
  - `markdown` — Markdown to HTML
  - `weasyprint` — HTML to PDF (with full control of @page, margins, and counters)
  - `ebooklib` — EPUB creation (for `--epub`)
  - `pypdf` — inject title, author, subject, keywords into PDF after build

Install from repo root:

```bash
pip install -r skills/format-book-agent/requirements.txt
```

## Inputs (all content from `book/` only)

All manuscript content is read **only** from the `book/` folder. Nothing outside `book/` is used for body, front matter, or back matter text.

| Input | Location | Purpose |
|-------|----------|---------|
| Book root | Auto-detected (parent of `book/`) or `--repo` | Repository root; content comes from `book/` |
| Cover image | `book/images/cover.png` (use `--cover PATH`) | First page when file exists; path relative to repo. All images live in `book/images/`. |
| Chapters | `book/chapter-01.md`, `book/chapter-02.md`, … | One file per chapter; only existing files are included |
| TOC | `book/toc.md` | Title, subtitle, chapter list. If missing, defaults are used and chapters are discovered from `book/chapter-*.md` |
| Introduction | `book/introduction.md` | Optional front matter after TOC, before Chapter 1 |
| About the Author | `book/about-the-author.md` | Back matter author bio |
| EPUB/PDF metadata | `input/metadata.md` or `input/metadata.yaml` | Optional overrides: Author, Identifier (ISBN), Description, Keywords, Language. The script derives title, author, and description from toc, about-the-author, and introduction. **EPUB:** written into OPF. **PDF:** injected after build (Title, Author, Subject, Keywords) via pypdf. |

Dry-run limits the **body** to Chapter 1 only; front and back matter are unchanged.

**EPUB metadata:** When building `--epub`, the script reads metadata from the book folder and writes it into the EPUB OPF (Dublin Core): title, subtitle, author, description, language, identifier (ISBN), and subjects (keywords). **PDF metadata:** When building PDF, the script injects the same metadata into the PDF document info (Title, Author, Subject, Keywords) after weasyprint runs, using pypdf. Sources for both: `book/toc.md`, `book/about-the-author.md`, `book/introduction.md`, and optional `input/metadata.md` or `input/metadata.yaml`. This matches the book-metadata skill so you can use the same `input/metadata.md` for the metadata MD file and for both EPUB and PDF builds.

## Platform Notes

- **Amazon KDP**: Use the PDF as the **interior (manuscript)** file. KDP requires two files: interior + cover; this skill builds only the interior. Prepare the cover separately (Cover Creator, template, or designer). The build matches [KDP's "Format Your Paperback"](https://kdp.amazon.com/help/topic/G201834190) steps (trim/margins, front/body/back matter, save for upload). Use Kindle Create for e-book formatting if needed.
- **IngramSpark**: Use the same PDF for print (paperback/hardcover). Ensure trim size and bleed match IngramSpark specs; see [reference.md](reference.md) for trim sizes and margins.

For detailed specs and KDP alignment (trim, margins, bleed, gutter by page count, save guidelines), see [reference.md](reference.md).

## If the Script Fails

- **PDF export**: The script uses **weasyprint** for PDF. Install with `pip install weasyprint`. On Windows, this also requires Pango/GTK (see [reference.md](reference.md#windows-weasyprint-setup)). Full book always outputs PDF; dry-run defaults to HTML (use `--dry-run --pdf` for a PDF preview).
- **EPUB export**: Requires **ebooklib**. Install with `pip install ebooklib`. Use `--epub --output path/to/book.epub` (extension is forced to `.epub` if omitted).
- **EPUB validation (EPUBCheck)**: Run `npm run validate:epub` to validate `output/book-interior.epub`, or `npm run epub:validate` to build then validate. Uses **epubchecker** (npm), which runs the official W3C EPUBCheck; **Java 7+** is required. A JSON report is written to `output/epubcheck-report.json`. Most distributors (including IngramSpark) expect EPUBs to pass EPUBCheck; fix any reported errors before submission.
- **Missing chapter**: Script skips missing `book/chapter-NN.md` or `book/chNN-*.md`; dry-run only needs chapter 1.
- **No about-the-author**: If `book/about-the-author.md` is missing, back matter still renders with a placeholder.
