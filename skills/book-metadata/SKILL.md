---
name: book-metadata
description: Generates publication-ready metadata (PDF, EPUB, KDP, IngramSpark) by reading the book folder and writing a single MD file. Use when preparing to publish, when the user asks for book metadata, or when the format-book-agent needs metadata for PDF/EPUB builds.
---

# Book Metadata Generator

Generates a single Markdown file containing **title, author, description, keywords, language, and identifiers** derived from the `book/` folder. The output is suitable for copy-paste into KDP, IngramSpark, or other publishing forms, and can be consumed by the format-book-agent when building PDF/EPUB.

## When to Use

- User asks for "book metadata," "publishing metadata," or "KDP/EPUB metadata"
- Preparing to publish and need a ready-to-paste metadata file
- Integrating metadata into the format-book-agent or other build pipelines

## Quick Start

From the **repository root** (where the `book/` folder lives):

```bash
# Generate metadata from book/ → output/book-metadata.md (default)
python skills/book-metadata/scripts/generate_metadata.py

# Custom output path
python skills/book-metadata/scripts/generate_metadata.py --output path/to/metadata.md

# Custom book folder (default: repo root’s book/)
python skills/book-metadata/scripts/generate_metadata.py --book-dir path/to/book

# Add keywords via CLI (merged with keywords from input/metadata.md if present)
python skills/book-metadata/scripts/generate_metadata.py --keywords "AI, transformation, CEO, Europe, EU AI Act"
```

No extra dependencies: the script uses only the Python standard library and reads Markdown as text.

## What the Script Reads

| Source | Used for |
|--------|----------|
| `book/toc.md` | Title, subtitle, working title |
| `book/introduction.md` | Short description (first paragraphs), completion date if mentioned |
| `book/about-the-author.md` | Author name (from first sentence “Name is a…”), optional bio snippet |
| `input/metadata.yaml` or `input/metadata.md` | Optional overrides (author, ISBN, publisher, keywords, language) |

If `input/metadata.yaml` or `input/metadata.md` exists, the script uses it for author, identifier (ISBN), publisher, keywords, and language before falling back to parsing the other files.

## Output MD File Structure

The generated file includes:

1. **Overview** — Single place for title, subtitle, author, description, language, identifier. Easy to copy-paste into web forms.
2. **EPUB / Dublin Core** — Fields aligned with EPUB OPF (dc:title, dc:creator, dc:language, dc:identifier, dcterms:modified, dc:description, dc:subject). Format-book-agent or EPUB tools can use these.
3. **PDF / Document Info & XMP** — Title, Author, Subject, Keywords, Creator, and dates. For PDF producers (e.g. pypdf, weasyprint) or manual entry in Acrobat.

The **full description** (subject text) is always included in full in the output, under "Full description (Subject / dc:description)" and in the EPUB/PDF sections—never truncated. Copy-paste from those blocks for KDP, Acrobat, or OPF.

See [reference.md](reference.md) for field-by-field notes for PDF and EPUB.

## Verify metadata in built files

To check that metadata is actually inside your built EPUB (and optionally PDF):

```bash
python skills/book-metadata/scripts/verify_metadata.py output/book.epub
python skills/book-metadata/scripts/verify_metadata.py output/book.epub output/book.pdf
```

The script prints Dublin Core fields from the EPUB OPF (title, creator, description, subjects). For PDF it prints Document Info (Title, Author, Subject, Keywords) if **pypdf** is installed. Full verification steps (including manual checks in Acrobat or e-readers) are in [reference.md](reference.md#how-to-verify-metadata-in-pdf-and-epub).

## Adding keywords

- **In a file**: Create `input/metadata.md` with a line `Keywords: AI, transformation, CEO, Europe` (comma-separated). Or use `input/metadata.yaml` with `keywords: ["AI", "transformation", "CEO"]` if PyYAML is installed.
- **On the command line**: Run with `--keywords "AI, transformation, CEO"`. These are merged with any keywords from the metadata file.

## Integration with format-book-agent

The format-book-agent builds PDF/EPUB from `book/` and does not yet read this metadata file by default. To use it:

- **Copy-paste**: Open the generated `book-metadata.md` and copy the Overview or PDF/EPUB sections into your publishing platform or into the build script.
- **Future**: The format-book-agent can be extended to accept an optional `--metadata path/to/metadata.md` and inject title, author, description, and keywords into the PDF (XMP/document info) and EPUB (OPF metadata).

## If Something Is Missing

- **Author**: Add `input/metadata.yaml` with `author: "Your Name"` or ensure `about-the-author.md` starts with a sentence like "Your Name is a…".
- **ISBN**: Add to `input/metadata.yaml` as `identifier: "978-..."` or paste into the generated MD after running.
- **Keywords**: Add `Keywords: AI, transformation, ...` in `input/metadata.md`, or use `--keywords "AI, transformation"` when running the script, or add `keywords: ["AI", ...]` in `input/metadata.yaml`.

## Requirements

- Python 3.9+
- No pip dependencies (stdlib only)
