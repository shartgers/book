#!/usr/bin/env python3
"""
Print metadata embedded in built EPUB and/or PDF files.

Use this to verify that the format-book-agent wrote the expected metadata
(title, author, description, keywords) into the EPUB, and to see what
(if any) metadata is in the PDF.

Usage:
  python verify_metadata.py output/book.epub
  python verify_metadata.py output/book.pdf
  python verify_metadata.py output/book.epub output/book.pdf
"""

import re
import sys
import zipfile
from pathlib import Path


def verify_epub(path: Path) -> None:
    """Read OPF from EPUB (zip) and print Dublin Core metadata."""
    if not path.suffix.lower() == ".epub":
        print(f"Skip (not EPUB): {path}")
        return
    if not path.exists():
        print(f"File not found: {path}")
        return
    print(f"\n--- EPUB: {path} ---\n")
    try:
        with zipfile.ZipFile(path, "r") as z:
            opf_names = [n for n in z.namelist() if n.endswith(".opf")]
            if not opf_names:
                print("No .opf found inside EPUB.")
                return
            xml = z.read(opf_names[0]).decode("utf-8")
    except zipfile.BadZipFile:
        print("Not a valid ZIP/EPUB file.")
        return

    # Extract dc:* and key meta tags
    tags = ["dc:title", "dc:creator", "dc:language", "dc:identifier", "dc:description", "dc:subject"]
    for tag in tags:
        pattern = f"<{tag}[^>]*>([^<]+)"
        for m in re.finditer(pattern, xml):
            val = m.group(1).strip()
            if tag == "dc:description" and len(val) > 200:
                val = val[:200] + "..."
            print(f"  {tag}: {val}")
    # dcterms:modified
    for m in re.finditer(r'<meta property="dcterms:modified">([^<]+)', xml):
        print(f"  dcterms:modified: {m.group(1).strip()}")
    print()


def verify_pdf(path: Path) -> None:
    """Print PDF Document Information metadata using pypdf if available."""
    if path.suffix.lower() != ".pdf":
        print(f"Skip (not PDF): {path}")
        return
    if not path.exists():
        print(f"File not found: {path}")
        return
    print(f"\n--- PDF: {path} ---\n")
    try:
        from pypdf import PdfReader
    except ImportError:
        print("  Install pypdf to read PDF metadata: pip install pypdf")
        print("  Or check in viewer: File → Properties → Description (Acrobat/Reader)")
        print()
        return

    try:
        reader = PdfReader(path)
        info = reader.metadata or {}
        # Common keys: /Title, /Author, /Subject, /Keywords, /Creator, /Producer, /CreationDate, /ModDate
        for key in ["/Title", "/Author", "/Subject", "/Keywords", "/Creator", "/Producer"]:
            val = info.get(key, "")
            if val is None:
                val = ""
            val = str(val).strip()
            label = key.lstrip("/")
            if not val:
                val = "(not set)"
            print(f"  {label}: {val}")
        for key in ["/CreationDate", "/ModDate"]:
            val = info.get(key, "")
            if val:
                print(f"  {key.lstrip('/')}: {val}")
    except Exception as e:
        print(f"  Error reading PDF: {e}")
    print()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python verify_metadata.py <file.epub> [file.pdf ...]")
        print("Example: python verify_metadata.py output/book.epub output/book.pdf")
        sys.exit(1)

    for p in sys.argv[1:]:
        path = Path(p)
        if path.suffix.lower() == ".epub":
            verify_epub(path)
        elif path.suffix.lower() == ".pdf":
            verify_pdf(path)
        else:
            print(f"Skip (unknown type): {path}")


if __name__ == "__main__":
    main()
