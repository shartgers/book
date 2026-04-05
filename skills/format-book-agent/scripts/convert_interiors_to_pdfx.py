#!/usr/bin/env python3
"""
Convert output/book-interior.pdf to two PDF/X-3:2002 (grayscale) files for IngramSpark:

  1. Ghostscript once → output/<hardcover ISBN13>_txt.pdf (canonical build)
  2. Copy that file → output/<paperback ISBN13>_txt.pdf (same bytes; different ISBN filename)

ISBNs are read from input/ISBN hardcover.md and input/ISBN paperback.md (first line with 13 digits).

Typical workflow: npm run pdfx  (runs npm run pdf, then this script).

Expects:
  - output/book-interior.pdf
  - input/ISBN paperback.md
  - input/ISBN hardcover.md
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]

INTERIOR_PDF = REPO_ROOT / "output" / "book-interior.pdf"
ISBN_PAPERBACK_FILE = REPO_ROOT / "input" / "ISBN paperback.md"
ISBN_HARDCOVER_FILE = REPO_ROOT / "input" / "ISBN hardcover.md"
CONVERT_SCRIPT = SCRIPT_DIR / "convert_to_pdfx.py"


def extract_isbn13(path: Path) -> str | None:
    """Return 13 digits (no hyphens) from the first line in the file that contains exactly 13 digits."""
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
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
    if isbn_pb == isbn_hc:
        print("Error: Paperback and hardcover ISBN must differ for two output filenames.")
        return 1

    if not INTERIOR_PDF.exists():
        print(f"Error: {INTERIOR_PDF} not found. Run: npm run pdf")
        return 1

    out_hc = REPO_ROOT / "output" / f"{isbn_hc}_txt.pdf"
    out_pb = REPO_ROOT / "output" / f"{isbn_pb}_txt.pdf"

    cmd = [sys.executable, str(CONVERT_SCRIPT), str(INTERIOR_PDF), str(out_hc)]
    r = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        print("PDF/X conversion failed.")
        return r.returncode

    shutil.copy2(out_hc, out_pb)
    print(f"Created (hardcover ISBN): {out_hc}")
    print(f"Created (paperback ISBN, copy): {out_pb}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
