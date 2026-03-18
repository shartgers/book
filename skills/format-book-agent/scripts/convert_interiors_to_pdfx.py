#!/usr/bin/env python3
"""
Build both interior PDFs (paperback + hardcover), then convert to PDF/X-3:2002
with filenames: <ISBN13>_txt_paperback.pdf and <ISBN13>_txt_hardcover.pdf.

Reads ISBN from input/ISBN paperback.md and input/ISBN hardcover.md (format:
"ISBN/EAN:  978-90-836902-1-6"). Extracts 13 digits (hyphens stripped) for
the output filename.

Usage (from repo root):
  python skills/format-book-agent/scripts/convert_interiors_to_pdfx.py

Expects:
  - output/book-interior-paperback.pdf (from npm run pdf:paperback)
  - output/book-interior-hardcover.pdf (from npm run pdf:hardcover)
  - input/ISBN paperback.md
  - input/ISBN hardcover.md

Outputs:
  - output/<ISBN13>_txt_paperback.pdf
  - output/<ISBN13>_txt_hardcover.pdf
"""

import re
import subprocess
import sys
from pathlib import Path

# Script is at skills/format-book-agent/scripts/convert_interiors_to_pdfx.py
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]

# Input PDFs (must exist; built by pdf:paperback / pdf:hardcover)
PAPERBACK_PDF = REPO_ROOT / "output" / "book-interior-paperback.pdf"
HARDCOVER_PDF = REPO_ROOT / "output" / "book-interior-hardcover.pdf"

# ISBN files: first line like "ISBN/EAN:               978-90-836902-1-6"
ISBN_PAPERBACK_FILE = REPO_ROOT / "input" / "ISBN paperback.md"
ISBN_HARDCOVER_FILE = REPO_ROOT / "input" / "ISBN hardcover.md"

CONVERT_SCRIPT = SCRIPT_DIR / "convert_to_pdfx.py"


def extract_isbn13(path: Path) -> str | None:
    """
    Read the ISBN file and return 13 digits (no hyphens).
    Expects a line like "ISBN/EAN:  978-90-836902-1-6".
    """
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    # Match digits; take first sequence that has 13 digits (with possible hyphens in between)
    for line in text.splitlines():
        digits = re.sub(r"\D", "", line)
        if len(digits) == 13:
            return digits
    return None


def main() -> int:
    isbn_pb = extract_isbn13(ISBN_PAPERBACK_FILE)
    isbn_hc = extract_isbn13(ISBN_HARDCOVER_FILE)

    if not isbn_pb:
        print(f"Error: Could not find 13-digit ISBN in {ISBN_PAPERBACK_FILE}")
        return 1
    if not isbn_hc:
        print(f"Error: Could not find 13-digit ISBN in {ISBN_HARDCOVER_FILE}")
        return 1

    out_pb = REPO_ROOT / "output" / f"{isbn_pb}_txt_paperback.pdf"
    out_hc = REPO_ROOT / "output" / f"{isbn_hc}_txt_hardcover.pdf"

    if not PAPERBACK_PDF.exists():
        print(f"Error: {PAPERBACK_PDF} not found. Run: npm run pdf:paperback")
        return 1
    if not HARDCOVER_PDF.exists():
        print(f"Error: {HARDCOVER_PDF} not found. Run: npm run pdf:hardcover")
        return 1

    for label, input_pdf, output_pdf in [
        ("paperback", PAPERBACK_PDF, out_pb),
        ("hardcover", HARDCOVER_PDF, out_hc),
    ]:
        cmd = [sys.executable, str(CONVERT_SCRIPT), str(input_pdf), str(output_pdf)]
        r = subprocess.run(cmd, cwd=str(REPO_ROOT))
        if r.returncode != 0:
            print(f"Conversion failed for {label}.")
            return r.returncode
        print(f"Created: {output_pdf}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
