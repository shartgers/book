# Print PDF Reference: KDP and IngramSpark

Specs and layout rules for the print-ready PDF produced by `scripts/build_print_pdf.py`.

---

## Trim Sizes (choose one per format)

| Use case | Trim size | Notes |
|----------|-----------|--------|
| US trade (KDP / IngramSpark) | 5.5" × 8.25" | Default in `build_print_pdf.py` (`PRINT_PAGE`) |
| US alternate | 6" × 9" | Edit `PRINT_PAGE` in `build_print_pdf.py` if you switch trim |
| EU (metric) | 148 mm × 210 mm (A5) or 152 mm × 229 mm | Check platform dropdowns |

One interior PDF is used for paperback and hardcover uploads; PDF/X duplicates use the same file with per-ISBN filenames (see `convert_interiors_to_pdfx.py`).

---

## Margins and Bleed

- **Safe margin**: At least 0.5" (12.7 mm) from trim on all sides for text and critical content.
- **Bleed**: If you use full-bleed images, extend 0.125" (3 mm) past trim; KDP/IngramSpark specify bleed in their templates.
- **Gutter**: The interior PDF uses a **0.55"** base on each side, then shifts **+6 mm** to the inner (binding) edge and **−6 mm** to the outer edge so the type block width stays the same. Introduction, chapters, and back matter also use **+6 mm** extra top margin below the running header (front matter/cover unchanged).

---

## Interior Layout Principles (from self-publishing guides)

- **Generous margins** and clear heading hierarchy.
- **Consistent chapter openings**: e.g. chapter title on a new page, optional drop cap or first-line emphasis.
- **Widows and orphans**: Avoid single lines at top/bottom of pages where possible (script/weasyprint can help with break controls).
- **Definitions**: Rendered in a **box with background colour** so they are visually consistent and easy to spot.
- **Case studies**: Rendered with a **distinct layout** (e.g. serif font, tinted background, border) so they read as a separate "voice" from the main narrative.

---

## Definition Blocks (book convention)

In the manuscript, definitions use a blockquote with a bold label:

```markdown
> **Definition: The Agentic Organisation**
>
> An agentic organisation is redesigned around human-AI collaboration...
```

The script detects this pattern and applies a **definition box** style: background colour (e.g. light blue or light grey), padding, optional left border, so every definition looks the same.

---

## Case Study Sections

Chapters use a level-2 heading:

```markdown
## Case Study: DBS Bank: Benchmarking Against the Wrong Competitors
```

The script wraps the section (until the next `##`) in a **case-study** container with:

- Different typeface (e.g. serif for case study vs sans for body)
- Tinted background (e.g. cream / light tan)
- Border (e.g. 1px solid) to frame the block

---

## PDF/X-3:2002 for IngramSpark (B&W interior)

IngramSpark recommends PDF/X-1a:2001 or PDF/X-3:2002. The WeasyPrint build does not add Output Intents. To produce a PDF/X-3:2002 grayscale interior:

1. **Install Ghostscript** (required):
   - Windows: Download from [ghostscript.com](https://ghostscript.com/releases/gsdnld.html) or `choco install ghostscript` (run as Administrator)
   - macOS: `brew install ghostscript`
   - Linux: `apt install ghostscript`

2. **Run the conversion** (builds `book-interior.pdf`, then PDF/X + copy):
   ```bash
   npm run pdfx
   ```
   This runs **`npm run pdf`**, converts **`output/book-interior.pdf`** to **`output/<hardcover ISBN13>_txt.pdf`**, then copies it to **`output/<paperback ISBN13>_txt.pdf`**. ISBNs come from `input/ISBN hardcover.md` and `input/ISBN paperback.md`. Trim is **`PRINT_PAGE`** in `build_print_pdf.py` (currently **5.5" × 8.25"**).

   Or manually:
   ```bash
   python skills/format-book-agent/scripts/build_print_pdf.py --interior --output output/book-interior.pdf
   python skills/format-book-agent/scripts/convert_interiors_to_pdfx.py
   ```

3. **Image resolution**: Ghostscript downsamples **embedded raster images** (colour, grey, mono) to **300 dpi** so the file passes IngramSpark’s validation (max 600 ppi; source PDFs can be 720 ppi from WeasyPrint). Vector text and vector graphics should remain sharp; if the entire page looks pixelated when zoomed and the PDF/X file is vastly larger than `book-interior.pdf`, Ghostscript likely rasterised whole pages (often because PDF/X mode defaulted to **PDF 1.3**, which cannot keep PDF 1.4 transparency). The conversion script sets **`CompatibilityLevel=1.7`** and **`HaveTransparency=true`** so typical WeasyPrint interiors stay vector-based. Re-run **`npm run pdfx`** after updating `convert_to_pdfx.py`.

4. **ICC profile**: The script downloads a grayscale ICC profile from Adobe if needed, or uses a system profile. Place `Gray Gamma 2.2.icc` in `input/icc/` to use a specific profile.

---

## ISBN and Barcode

- **KDP**: You can use a free KDP-assigned ISBN or your own; barcode goes on the **cover**, not in the interior PDF.
- **IngramSpark**: Purchase your own ISBN(s) per format (ebook, paperback, hardcover). Barcode on back cover; include in cover file, not interior.
- **Interior PDF**: No barcode; optional "Also by this author" or copyright page with ISBN mentioned in text.

---

## Index

The script can produce:

- A **placeholder** "Index" page (e.g. "Index to be completed before final print"), or
- A **simple heading index** (all `##` and `###` from the included chapters listed, without page numbers).

Full index with page numbers usually requires a second pass or a dedicated indexing tool; the script focuses on structure and styling first.

---

## File Names for Upload

- **Interior**: e.g. `TheAgenticEnterprise-Interior.pdf` (no spaces in filename for some platforms).
- **Cover**: Prepared separately (Cover Creator, designer, or template); KDP and IngramSpark have different cover templates and trim/bleed requirements.

---

## KDP alignment (Format Your Paperback)

The build script is designed to match [KDP's "Format Your Paperback"](https://kdp.amazon.com/help/topic/G201834190) flow:

1. **Two files**  
   KDP requires a **manuscript (interior)** file and a **cover** file. This skill produces only the interior PDF; the cover is created separately (Cover Creator, template, or designer).

2. **Set trim size and margins**  
   - Trim size: default **5.5" × 8.25"** — a [supported KDP trim size](https://kdp.amazon.com/help?topicId=GVBQ3CMEQW3W2VL6).  
   - Margins: top/bottom 0.6", outside 0.5", inside (gutter) 0.75".  
   - KDP minimums: **0.25"** for top, bottom, and outside (no bleed); inside margin depends on page count (see [Set Trim Size, Bleed, and Margins](https://kdp.amazon.com/help?topicId=GVBQ3CMEQW3W2VL6)). Our values meet or exceed minimums. For **701–828 pages**, KDP requires gutter **0.875"**; the script uses 0.75", so for very long books consider increasing the inner margin in the script or CSS.  
   - **Bleed**: not used by default (text-only / no edge-to-edge images). If you add full-bleed images later, set up bleed per KDP (e.g. page size = trim + 0.125" bleed) and upload PDF only.

3. **Create front, body, and back matter**  
   The script includes: half title, title page, copyright page, table of contents (front); chapters (body); About the Author and Index (back). This matches KDP's [front, body, and back matter](https://kdp.amazon.com/help?topicId=GDDYZG2C7RVF5N9J) guidance (title pages, copyright, chapter headings, author bio).

4. **Save manuscript for upload**  
   Output is a single **PDF** (recommended by KDP). See [Save Your Manuscript File](https://kdp.amazon.com/help/topic/G202145060): no crop/trim marks, no encryption; embed fonts (weasyprint embeds by default); single-page layout; for best results use PDF optimized for print. After building, upload and preview in KDP.

---

## Windows: WeasyPrint setup

PDF build uses WeasyPrint, which on Windows needs Pango/GTK libraries.

1. **Install MSYS2** (https://www.msys2.org/) with default options.
2. **Open the MSYS2 shell** and run:
   ```bash
   pacman -S mingw-w64-x86_64-pango
   ```
3. **Close MSYS2.** In a normal Windows terminal (PowerShell or cmd), from the repo:
   ```bash
   .venv\Scripts\Activate.ps1
   pip install weasyprint
   npm run pdf
   ```
4. If the DLL is still not found, set the DLL path before running (MSYS2 in `C:\Program Files (x86)\MSYS2`):
   ```bash
   $env:WEASYPRINT_DLL_DIRECTORIES = "C:\Program Files (x86)\MSYS2\mingw64\bin"
   npm run pdf
   ```
   The build script also prepends these directories to `PATH` when they exist, so often step 4 is not needed.

See [WeasyPrint first steps (Windows)](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows) and [troubleshooting](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#troubleshooting).

---

## Sources

- Project: `input/self-publishing-tips.md`, `input/How-to-Self-Publish-Guide.pdf`
- KDP: [Format Your Paperback](https://kdp.amazon.com/help/topic/G201834190) (manuscript + cover); [Set Trim Size, Bleed, and Margins](https://kdp.amazon.com/help?topicId=GVBQ3CMEQW3W2VL6); [Save Your Manuscript File](https://kdp.amazon.com/help/topic/G202145060); [Front, Body, Back Matter](https://kdp.amazon.com/help?topicId=GDDYZG2C7RVF5N9J).
- IngramSpark: Distribution and print specs on ingramspark.com; trim sizes and file requirements in their help/tools.
