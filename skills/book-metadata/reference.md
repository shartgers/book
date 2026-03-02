# Metadata Reference: PDF and EPUB

Short reference for metadata fields used when publishing. The generator script outputs these in Markdown; you can copy-paste into platforms or feed them into build tools.

## EPUB (Dublin Core / OPF)

EPUB uses the OPF file’s `<metadata>` section with Dublin Core elements. Required for EPUB 3.2:

| Field | OPF element | Required | Notes |
|-------|-------------|----------|--------|
| Title | `dc:title` | Yes | Main title; subtitle can be in a separate `meta` with `refines` pointing to title id. |
| Identifier | `dc:identifier` | Yes | Usually ISBN (e.g. `urn:isbn:978-...`). Must have a unique id. |
| Language | `dc:language` | Yes | BCP 47, e.g. `en`, `en-US`. |
| Modified | `dcterms:modified` | Yes | ISO 8601, e.g. `2026-03-02T12:00:00Z`. |

Recommended:

| Field | OPF element | Notes |
|-------|-------------|--------|
| Author | `dc:creator` | With `role` (e.g. `aut` for author). |
| Description | `dc:description` | Short blurb; no HTML in EPUB 2, HTML allowed in EPUB 3. |
| Subject | `dc:subject` | One subject per tag; multiple tags for multiple subjects. |
| Publisher | `dc:publisher` | Publisher name. |
| Publication date | `dc:date` | Publication or release date. |

## PDF (Document Information and XMP)

PDF supports two layers; both can be set for compatibility.

### Standard Document Information Dictionary

| Field | Key | Notes |
|-------|-----|--------|
| Title | `/Title` | Document title. |
| Author | `/Author` | Creator/author name. |
| Subject | `/Subject` | Short subject/description. |
| Keywords | `/Keywords` | Comma- or space-separated keywords. |
| Creator | `/Creator` | Application that created the document. |
| Producer | `/Producer` | Application that produced the PDF. |
| CreationDate | `/CreationDate` | D:YYYYMMDDHHmmSS. |
| ModDate | `/ModDate` | D:YYYYMMDDHHmmSS. |

### XMP (Extensible Metadata Platform)

XMP is XML-based and often preferred for rich metadata. Common namespaces:

- **Dublin Core (dc)**: title, creator, description.
- **XMP (xmp)**: CreateDate, ModifyDate, CreatorTool.
- **PDF**: PDF-specific properties.

Tools like pypdf can read/write both Document Info and XMP.

## KDP / IngramSpark (forms)

Typical form fields map to the above:

- **Title** → dc:title / PDF Title
- **Subtitle** → optional; some systems have a separate subtitle field
- **Author** → dc:creator / PDF Author
- **Description** → dc:description / PDF Subject (or long description)
- **Keywords** → dc:subject (multiple) / PDF Keywords
- **Language** → dc:language
- **ISBN** → dc:identifier
- **Publisher** → dc:publisher (if applicable)

The generated `book-metadata.md` provides an Overview section so you can copy these values into KDP or IngramSpark without looking up OPF/PDF keys.

---

## How to verify metadata in PDF and EPUB

### EPUB

The format-book-agent writes Dublin Core metadata into the EPUB when you run `--epub`. To verify:

**Option 1 – Script (easiest)**  
From the repo root:

```bash
python skills/book-metadata/scripts/verify_metadata.py output/book.epub
```

This prints title, creator, language, identifier, description (truncated), and all subjects (keywords) from the OPF.

**Option 2 – Python one-liner**  
Open the EPUB as a zip and read the OPF (EPUB is a zip; the OPF path is usually `EPUB/content.opf` or `OEBPS/content.opf`):

```bash
python -c "
import zipfile, re, sys
path = 'output/book.epub'  # or sys.argv[1]
z = zipfile.ZipFile(path, 'r')
names = [n for n in z.namelist() if n.endswith('.opf')]
xml = z.read(names[0]).decode('utf-8')
for tag in ['dc:title','dc:creator','dc:language','dc:identifier','dc:description','dc:subject']:
    for m in re.finditer(r'<' + tag + r'[^>]*>([^<]+)', xml):
        print(tag, ':', m.group(1).strip()[:80] + ('...' if len(m.group(1)) > 80 else ''))
z.close()
"
```

**Option 3 – Manual**  
Rename `book.epub` to `book.zip`, unzip, and open the `.opf` file in a text editor. Look for the `<metadata>` block and the `dc:*` elements.

**Option 4 – E-reader / Calibre**  
Open the EPUB in Calibre or an e-reader and check “Book details” or “Metadata” (title, author, description, etc.).

### PDF

The format-book-agent writes metadata into the PDF after building it (using pypdf): Title, Author, Subject, and Keywords from the same book-folder sources as EPUB. To verify what’s in the file:

**Option 1 – Script**  
If you have `pypdf` installed:

```bash
python skills/book-metadata/scripts/verify_metadata.py output/book.pdf
```

This prints the PDF Document Information dictionary (Title, Author, Subject, Keywords, etc.). If the build never set them, many of these will be empty.

**Option 2 – pypdf one-liner**  
```bash
pip install pypdf
python -c "
from pypdf import PdfReader
r = PdfReader('output/book.pdf')
info = r.metadata
for k in ['/Title','/Author','/Subject','/Keywords']:
    print(k, ':', info.get(k, '(not set)'))
"
```

**Option 3 – Viewer**  
- **Adobe Acrobat / Reader**: File → Properties → Description.  
- **Windows**: Right‑click PDF → Properties → Details.  
- **Chrome**: Open PDF → ⋮ → Print → “Destination” or open in browser and check document properties if available.

The format-book-agent injects this metadata into the PDF automatically when you run the PDF build (using pypdf and the same metadata from the book folder as for EPUB).
