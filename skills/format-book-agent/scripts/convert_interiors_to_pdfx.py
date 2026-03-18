#!/usr/bin/env python3
"""
Build interior PDF (hardcover 5.5" x 8.5"), then convert to PDF/X-3:2002
with filename: <ISBN13>_txt.pdf.

Reads ISBN from input/ISBN hardcover.md (format: "ISBN/EAN:  978-90-836902-0-9").
Extracts 13 digits (hyphens stripped) for the output filename.

Usage (from repo root):
  python skills/format-book-agent/scripts/convert_interiors_to_pdfx.py

Expects:
  - output/book-interior-hardcover.pdf (from npm run pdf:hardcover)
  - input/ISBN hardcover.md

Outputs:
  - output/<ISBN13>_txt.pdf
"""

import re
import subprocess
import sys
from pathlib import Path

# Script is at skills/format-book-agent/scripts/convert_interiors_to_pdfx.py
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]

HARDCOVER_PDF = REPO_ROOT / "output" / "book-interior-hardcover.pdf"
ISBN_HARDCOVER_FILE = REPO_ROOT / "input" / "ISBN hardcover.md"
CONVERT_SCRIPT = SCRIPT_DIR / "convert_to_pdfx.py"


def extract_isbn13(path: Path) -> str | None:
    """
    Read the ISBN file and return 13 digits (no hyphens).
    Expects a line like "ISBN/EAN:  978-90-836902-0-9".
    """
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        digits = re.sub(r"\D", "", line)
        if len(digits) == 13:
            return digits
    return None


def main() -> int:
    isbn = extract_isbn13(ISBN_HARDCOVER_FILE)
    if not isbn:
        print(f"Error: Could not find 13-digit ISBN in {ISBN_HARDCOVER_FILE}")
        return 1

    output_pdf = REPO_ROOT / "output" / f"{isbn}_txt.pdf"

    if not HARDCOVER_PDF.exists():
        print(f"Error: {HARDCOVER_PDF} not found. Run: npm run pdf:hardcover")
        return 1

    cmd = [sys.executable, str(CONVERT_SCRIPT), str(HARDCOVER_PDF), str(output_pdf)]
    r = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        print("Conversion failed.")
        return r.returncode
    print(f"Created: {output_pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
