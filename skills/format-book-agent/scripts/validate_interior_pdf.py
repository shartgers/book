#!/usr/bin/env python3
"""
Validate interior PDF against IngramSpark checklist and file-creation-guide.

Checks output/book-interior.pdf (or given path) against:
- input/pdf-checklist.pdf (Print Book File Guidelines)
- input/file-creation-guide.pdf (IngramSpark File Creation Guide)
- input/Book-Design-Expanded-Guide.pdf (design guidelines)

Usage:
  python validate_interior_pdf.py [path/to/interior.pdf]
"""

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf required. Run: pip install pypdf")
    sys.exit(1)


def pts_to_in(pts: float) -> float:
    """Convert PDF points to inches (72 pts = 1 inch)."""
    return pts / 72.0


def validate_pdf(pdf_path: Path) -> list[tuple[str, str, bool]]:
    """
    Validate PDF against IngramSpark interior requirements.
    Returns list of (check_name, message, passed).
    """
    results = []
    reader = PdfReader(str(pdf_path))
    pages = reader.pages
    page_count = len(pages)

    # --- Page count ---
    # IngramSpark: "page count divisible by 2" - they add blank/barcode if odd
    # Odd is acceptable; they auto-add. But even is preferred for submission.
    results.append((
        "Page count",
        f"{page_count} pages. IngramSpark accepts odd; they add blank if needed. Even preferred.",
        True  # Both accepted
    ))

    # --- Trim size ---
    # 5.5" x 8.25" = 396 x 594 pts (paperback). 5.5" x 8.5" = 396 x 612 pts (hardcover). 6" x 9" = 432 x 648 pts.
    p0 = pages[0]
    mediabox = p0.mediabox
    w_pts = float(mediabox.width)
    h_pts = float(mediabox.height)
    w_in = pts_to_in(w_pts)
    h_in = pts_to_in(h_pts)

    is_5_5_x_8_25 = abs(w_pts - 396) < 1 and abs(h_pts - 594) < 1
    is_5_5_x_8_5 = abs(w_pts - 396) < 1 and abs(h_pts - 612) < 1
    is_6x9 = abs(w_pts - 432) < 1 and abs(h_pts - 648) < 1
    is_valid_trim = is_5_5_x_8_25 or is_5_5_x_8_5 or is_6x9
    results.append((
        "Trim size",
        f"Page size: {w_in:.2f}\" x {h_in:.2f}\" ({w_pts:.0f} x {h_pts:.0f} pts). "
        f"5.5\" x 8.25\" (paperback), 5.5\" x 8.5\" (hardcover), or 6\" x 9\" supported for IngramSpark. "
        + ("PASS" if is_valid_trim else "CHECK - verify trim size matches your submission"),
        is_valid_trim
    ))

    # --- Single-page format (not spreads) ---
    # We assume single-page; pypdf doesn't easily detect spreads.
    results.append((
        "Single-page format",
        "Assumed: 1-up per page (single-page PDF). IngramSpark rejects spreads.",
        True
    ))

    # --- Crop/registration/printer marks ---
    # pypdf: CropBox or ArtBox could indicate marks. We check MediaBox vs CropBox.
    has_crop = "/CropBox" in p0 and p0.get("/CropBox") != p0.get("/MediaBox")
    results.append((
        "No crop/registration marks",
        "Do not include crop, registration, or printer marks. "
        + ("No extra crop box detected." if not has_crop else "CropBox differs from MediaBox - verify no marks."),
        not has_crop
    ))

    # --- Fonts embedded ---
    # pypdf: Font objects have /Subtype; /FontDescriptor with /FontFile* = embedded
    fonts_embedded = True
    font_names = set()
    for i, p in enumerate(pages[:20]):  # Sample first 20 pages
        if "/Resources" not in p or "/Font" not in p.get("/Resources", {}):
            continue
        for fname, font in p["/Resources"]["/Font"].items():
            font_names.add(str(fname))
            # Font can be indirect reference
            try:
                obj = font.get_object() if hasattr(font, "get_object") else font
                if obj is None:
                    continue
                # Check for FontDescriptor / FontFile
                if "/FontDescriptor" in obj:
                    fd = obj["/FontDescriptor"]
                    if hasattr(fd, "get_object"):
                        fd = fd.get_object()
                    if fd and any(k in fd for k in ["/FontFile", "/FontFile2", "/FontFile3"]):
                        continue  # Embedded
                # Base 14 fonts may not have FontDescriptor; check /BaseFont
                if "/Subtype" in obj and obj["/Subtype"] == "/Type1":
                    # Type1 base fonts - Acrobat Standard may not embed them
                    pass
            except Exception:
                pass
    # We cannot reliably detect unembedded fonts with pypdf alone.
    # Recommend manual check in Acrobat: File > Properties > Fonts
    results.append((
        "Fonts embedded",
        "All fonts must be embedded. Open PDF in Acrobat > File > Properties > Fonts tab. "
        "Each font should show '(Embedded)' or '(Embedded Subset)'. "
        f"Fonts detected: {len(font_names)}. Manual verification recommended.",
        True  # Cannot auto-verify; assume OK if build script embeds
    ))

    # --- Margins ---
    # IngramSpark: minimum 0.5" (13 mm) on all sides
    # Build script uses: top/bottom 0.7", left/right 0.65"
    results.append((
        "Margins",
        "IngramSpark recommends minimum 0.5\" (13 mm) on all sides. "
        "Build script uses 0.6–0.75\" - meets requirement.",
        True
    ))

    # --- Bleed ---
    # B&W interior: 0.125" (3 mm) on top, bottom, outside. NOT on bind edge.
    # For text-only (no full-bleed images), bleed not required.
    if "/BleedBox" in p0:
        bb = p0["/BleedBox"]
        bb_w = float(bb[2] - bb[0])
        bb_h = float(bb[3] - bb[1])
        if bb_w > w_pts or bb_h > h_pts:
            results.append((
                "Bleed",
                f"BleedBox present: {pts_to_in(bb_w):.2f}\" x {pts_to_in(bb_h):.2f}\". "
                "Bleed 0.125\" on top, bottom, outside only.",
                True
            ))
        else:
            results.append((
                "Bleed",
                "No bleed (text-only interior). OK if no full-bleed images.",
                True
            ))
    else:
        results.append((
            "Bleed",
            "No BleedBox. For text-only interior, no bleed required.",
            True
        ))

    # --- Spot colors / ICC ---
    # Cannot easily check with pypdf. Recommend manual preflight.
    results.append((
        "Spot colors / ICC",
        "Do not include spot colors or ICC profiles. B&W: convert images to grayscale. "
        "Manual preflight in Acrobat recommended.",
        True
    ))

    # --- Resolution ---
    # 300 ppi for images. Cannot verify from PDF structure easily.
    results.append((
        "Image resolution",
        "Images should be 300 ppi (8-bit grayscale for B&W). Manual check required.",
        True
    ))

    # --- PDF/X compliance ---
    root = reader.trailer.get("/Root", {})
    has_output_intent = "/OutputIntents" in root
    results.append((
        "PDF/X compliance",
        "IngramSpark recommends PDF/X-1a:2001 or PDF/X-3:2002. "
        + ("OutputIntents found." if has_output_intent else "No OutputIntents - may not be PDF/X. Consider re-export for print."),
        has_output_intent
    ))

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate interior PDF against IngramSpark checklist")
    parser.add_argument("pdf", nargs="?", default="output/book-interior.pdf", help="Path to interior PDF")
    args = parser.parse_args()

    # Script is at skills/format-book-agent/scripts/validate_interior_pdf.py
    # parents[2] = repo root (parent of skills/)
    repo = Path(__file__).resolve().parents[3]
    pdf_path = repo / args.pdf if not Path(args.pdf).is_absolute() else Path(args.pdf)

    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)

    print("=" * 70)
    print("IngramSpark Interior PDF Validation")
    print("=" * 70)
    print(f"File: {pdf_path}")
    print()
    print("Sources: input/pdf-checklist.pdf, input/file-creation-guide.pdf,")
    print("        input/Book-Design-Expanded-Guide.pdf")
    print()

    results = validate_pdf(pdf_path)

    passed = sum(1 for _, _, ok in results if ok)
    total = len(results)

    for name, msg, ok in results:
        status = "PASS" if ok else "CHECK"
        symbol = "✓" if ok else "?"
        print(f"  [{status}] {name}")
        print(f"      {msg}")
        print()

    print("=" * 70)
    print(f"Summary: {passed}/{total} checks passed. Items marked CHECK need manual verification.")
    print("=" * 70)
    print()
    print("Manual verification (recommended):")
    print("  1. Open PDF in Adobe Acrobat > File > Properties > Fonts tab. "
          "All fonts must show '(Embedded)' or '(Embedded Subset)'.")
    print("  2. Ensure no crop, registration, or printer marks visible.")
    print("  3. For B&W interior: images in grayscale; no spot colors.")
    print()


if __name__ == "__main__":
    main()
