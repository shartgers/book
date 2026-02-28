# Print PDF Reference: KDP and IngramSpark

Specs and layout rules for the print-ready PDF produced by `scripts/build_print_pdf.py`.

---

## Trim Sizes (choose one per format)

| Use case | Trim size | Notes |
|----------|-----------|--------|
| US paperback (KDP / IngramSpark) | 6" × 9" | Common for business books |
| US paperback alternate | 5.5" × 8.5" | Slightly smaller |
| EU (metric) | 148 mm × 210 mm (A5) or 152 mm × 229 mm | Check platform dropdowns |

Set trim size in the script or via CSS `@page { size: ... }`. Default in script: **6" × 9"**.

---

## Margins and Bleed

- **Safe margin**: At least 0.5" (12.7 mm) from trim on all sides for text and critical content.
- **Bleed**: If you use full-bleed images, extend 0.125" (3 mm) past trim; KDP/IngramSpark specify bleed in their templates.
- **Gutter**: For bound books, inner margin (gutter) is often larger than outer; 0.75" inner / 0.5" outer is a typical starting point.

---

## Interior Layout Principles (from self-publishing guides)

- **Generous margins** and clear heading hierarchy.
- **Consistent chapter openings**: e.g. chapter title on a new page, optional drop cap or first-line emphasis.
- **Widows and orphans**: Avoid single lines at top/bottom of pages where possible (script/xhtml2pdf can help with break controls).
- **Definitions**: Rendered in a **box with background colour** so they are visually consistent and easy to spot.
- **Case studies**: Rendered with a **distinct layout** (e.g. serif font, tinted background, border) so they read as a separate "voice" from the main narrative.

---

## Definition Blocks (book convention)

In the manuscript, definitions use a blockquote with a bold label:

```markdown
> **Definition: The Agentic Enterprise**
>
> An agentic enterprise is an organisation redesigned around human-AI collaboration...
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
   - Trim size: default **6" × 9"** — a [supported KDP trim size](https://kdp.amazon.com/help?topicId=GVBQ3CMEQW3W2VL6).  
   - Margins: top/bottom 0.6", outside 0.5", inside (gutter) 0.75".  
   - KDP minimums: **0.25"** for top, bottom, and outside (no bleed); inside margin depends on page count (see [Set Trim Size, Bleed, and Margins](https://kdp.amazon.com/help?topicId=GVBQ3CMEQW3W2VL6)). Our values meet or exceed minimums. For **701–828 pages**, KDP requires gutter **0.875"**; the script uses 0.75", so for very long books consider increasing the inner margin in the script or CSS.  
   - **Bleed**: not used by default (text-only / no edge-to-edge images). If you add full-bleed images later, set up bleed per KDP (e.g. page size = trim + 0.125" bleed) and upload PDF only.

3. **Create front, body, and back matter**  
   The script includes: half title, title page, copyright page, table of contents (front); chapters (body); About the Author and Index (back). This matches KDP's [front, body, and back matter](https://kdp.amazon.com/help?topicId=GDDYZG2C7RVF5N9J) guidance (title pages, copyright, chapter headings, author bio).

4. **Save manuscript for upload**  
   Output is a single **PDF** (recommended by KDP). See [Save Your Manuscript File](https://kdp.amazon.com/help?topicId=G202145060): no crop/trim marks, no encryption; embed fonts (xhtml2pdf embeds by default); single-page layout; for best results use PDF optimized for print. After building, upload and preview in KDP.

---

## Sources

- Project: `input/self-publishing-tips.md`, `input/How-to-Self-Publish-Guide.pdf`
- KDP: [Format Your Paperback](https://kdp.amazon.com/help/topic/G201834190) (manuscript + cover); [Set Trim Size, Bleed, and Margins](https://kdp.amazon.com/help?topicId=GVBQ3CMEQW3W2VL6); [Save Your Manuscript File](https://kdp.amazon.com/help?topicId=G202145060); [Front, Body, Back Matter](https://kdp.amazon.com/help?topicId=GDDYZG2C7RVF5N9J).
- IngramSpark: Distribution and print specs on ingramspark.com; trim sizes and file requirements in their help/tools.
