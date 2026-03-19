#!/usr/bin/env python3
"""
Generate publication-ready metadata from the book/ folder.

Reads book/toc.md, book/introduction.md, book/about-the-author.md, and optional
input/metadata.md (or input/metadata.yaml if PyYAML is available). Writes a single
Markdown file with Overview, EPUB (Dublin Core), and PDF (Document Info / XMP)
sections for copy-paste into KDP, IngramSpark, or use by format-book-agent.

Usage:
  python generate_metadata.py [--output path] [--book-dir path] [--keywords "key1, key2"]
"""

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def find_repo_root(start: Path) -> Path:
    """Find directory containing the book/ folder (repository root)."""
    current = start.resolve()
    for _ in range(10):
        if (current / "book").is_dir():
            return current
        current = current.parent
    return start


def load_text(path: Path) -> str:
    """Return file content or empty string if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def parse_simple_metadata(content: str) -> dict:
    """
    Parse key: value lines from input/metadata.md or similar.
    Supports: Author: Name, Identifier: 978-..., Keywords: a, b, c, BISAC: code1, code2, code3
    """
    out = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()
        if key == "keywords" and value:
            # Strip surrounding quotes from each keyword for cleaner PDF/EPUB metadata
            out[key] = [k.strip().strip('"').strip("'") for k in value.split(",") if k.strip()]
        elif key == "bisac" and value:
            # Up to 3 BISAC codes; comma-separated
            codes = [c.strip() for c in value.split(",") if c.strip()][:3]
            out[key] = codes
        elif value:
            out[key] = value
    return out


def try_load_yaml_metadata(path: Path) -> dict:
    """If PyYAML is available, load metadata from a YAML file; else return {}."""
    if not path.exists():
        return {}
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        # Normalise keys to lowercase; support author, identifier, publisher, keywords, language
        return {str(k).lower(): v for k, v in data.items()}
    except Exception:
        return {}


def parse_toc(toc_content: str) -> tuple[str, str]:
    """
    Parse book/toc.md for title and subtitle.
    Uses first line as title (strip #), second as subtitle if present.
    """
    title = "Untitled"
    subtitle = ""
    lines = [ln.strip().lstrip("#").strip() for ln in toc_content.splitlines() if ln.strip()]
    if lines:
        title = lines[0] or title
    if len(lines) > 1 and lines[1] and not lines[1].startswith("---"):
        subtitle = lines[1]
    return title, subtitle


def extract_author_from_about(content: str) -> str:
    """
    Extract author name from about-the-author.md.
    Expects a sentence like "Name is a former..." -> "Name".
    Skips the heading line "About the author".
    """
    if not content:
        return ""
    # Drop markdown headings and skip the "About the author" line
    first_block = content.lstrip("#").strip()
    for line in first_block.splitlines():
        line = line.strip().lstrip("#").strip()
        if not line:
            continue
        # Skip section title
        if re.match(r"^about\s+the\s+author$", line, re.IGNORECASE):
            continue
        # "Stephan Hartgers-Rus is a former..." -> "Stephan Hartgers-Rus"  
        match = re.match(r"^([^.\n]+)\s+is\s+a\s+", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        # Fallback: line that looks like a name (words, hyphens, no punctuation)
        if re.match(r"^[\w\s\-']+$", line) and 2 <= len(line.split()) <= 5:
            return line
    return ""


def extract_description_from_intro(content: str, max_chars: int = 4000) -> str:
    """
    Build full description from introduction.md: first paragraphs, no headers.
    Uses a high character limit so Subject/dc:description is complete for metadata.
    """
    if not content:
        return ""
    # Drop leading # headers
    text = re.sub(r"^#+\s*\S.*$", "", content, flags=re.MULTILINE).strip()
    # Collect paragraphs until we hit max_chars or end of content
    paragraphs = []
    current = []
    length = 0
    for line in text.splitlines():
        if line.strip():
            current.append(line.strip())
        else:
            if current:
                para = " ".join(current)
                if length + len(para) + 1 > max_chars:
                    # Add as much of this paragraph as fits
                    remaining = max_chars - length - 4  # " ..."
                    if remaining > 0:
                        paragraphs.append(para[:remaining].rsplit(" ", 1)[0] + " ...")
                    break
                paragraphs.append(para)
                length += len(para) + 1
                current = []
        if length >= max_chars:
            break
    if current and length < max_chars:
        para = " ".join(current)
        if length + len(para) + 1 <= max_chars:
            paragraphs.append(para)
        else:
            remaining = max_chars - length - 4
            if remaining > 0:
                paragraphs.append(para[:remaining].rsplit(" ", 1)[0] + " ...")
    combined = " ".join(paragraphs)
    return combined.replace("\n", " ").strip()


def build_metadata(book_dir: Path, cli_keywords: Optional[str] = None) -> dict:
    """
    Gather all metadata from book folder. Returns a flat dict with keys:
    title, subtitle, author, description, language, identifier, publisher,
    keywords (list), modified (ISO str). cli_keywords (comma-separated) are merged with file keywords.
    """
    # Optional overrides: input/metadata.yaml or input/metadata.md (key: value)
    overrides = {}
    input_dir = book_dir.parent / "input"
    yaml_path = input_dir / "metadata.yaml"
    md_meta_path = input_dir / "metadata.md"
    if yaml_path.exists():
        overrides = try_load_yaml_metadata(yaml_path)
    if md_meta_path.exists():
        overrides = {**overrides, **parse_simple_metadata(load_text(md_meta_path))}

    toc = load_text(book_dir / "toc.md")
    title, subtitle = parse_toc(toc)
    intro = load_text(book_dir / "introduction.md")
    about = load_text(book_dir / "about-the-author.md")

    author = (overrides.get("author") or "").strip() or extract_author_from_about(about)
    description = (overrides.get("description") or "").strip() or extract_description_from_intro(intro)
    language = (overrides.get("language") or "en").strip()
    identifier = (overrides.get("identifier") or "").strip()
    publisher = (overrides.get("publisher") or "").strip()
    keywords = overrides.get("keywords")
    if isinstance(keywords, str):
        keywords = [k.strip().strip('"').strip("'") for k in keywords.split(",") if k.strip()]
    elif isinstance(keywords, list):
        keywords = [str(k).strip().strip('"').strip("'") for k in keywords if k]
    else:
        keywords = []
    # Merge CLI keywords (e.g. --keywords "AI, transformation")
    if cli_keywords:
        extra = [k.strip().strip('"').strip("'") for k in cli_keywords.split(",") if k.strip()]
        keywords = list(dict.fromkeys(keywords + extra))

    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # BISAC codes: up to 3 from overrides (metadata.md or metadata.yaml)
    bisac = overrides.get("bisac")
    if isinstance(bisac, str):
        bisac = [c.strip() for c in bisac.split(",") if c.strip()][:3]
    elif isinstance(bisac, list):
        bisac = [str(c).strip() for c in bisac if c][:3]
    else:
        bisac = []

    return {
        "title": (overrides.get("title") or title).strip(),
        "subtitle": (overrides.get("subtitle") or subtitle).strip(),
        "author": author,
        "description": description,
        "language": language,
        "identifier": identifier,
        "publisher": publisher,
        "keywords": keywords,
        "bisac": bisac,
        "modified": modified,
    }


def write_metadata_md(meta: dict, out_path: Path) -> None:
    """Write a single Markdown file with Overview, EPUB, and PDF sections. Full description is never truncated."""
    title = meta["title"]
    subtitle = meta["subtitle"]
    full_title = f"{title}: {subtitle}" if subtitle else title
    author = meta["author"] or "(Set author in input/metadata.md or about-the-author.md)"
    description = meta["description"] or "(Add description or ensure book/introduction.md exists)"
    lang = meta["language"] or "en"
    identifier = meta["identifier"] or "(Add ISBN in input/metadata.md as Identifier: 978-...)"
    publisher = meta["publisher"] or ""
    keywords = meta["keywords"]
    modified = meta["modified"]
    keywords_str = ", ".join(keywords) if keywords else "(Add keywords via input/metadata.md or --keywords)"
    bisac = meta.get("bisac") or []
    bisac_str = ", ".join(bisac) if bisac else "(Add up to 3 BISAC codes in input/metadata.md as BISAC: code1, code2, code3)"

    # EPUB: one subject per tag
    dc_subjects = "\n".join(f"- `dc:subject` — {s}" for s in keywords) if keywords else "- `dc:subject` — (optional)"

    # Use full description everywhere (no truncation); tables get full text for copy-paste
    lines = [
        "# Book metadata",
        "",
        "Generated from the `book/` folder. Use for KDP, IngramSpark, or as input to the format-book-agent.",
        "",
        "---",
        "",
        "## Overview (copy-paste)",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| **Title** | {full_title} |",
        f"| **Author** | {author} |",
        f"| **Language** | {lang} |",
        f"| **Identifier (ISBN)** | {identifier} |",
        f"| **Keywords** | {keywords_str} |",
        f"| **BISAC** | {bisac_str} |",
        "",
        "### Full description (Subject / dc:description)",
        "",
        "Copy the text below for **Description** or **Subject** fields:",
        "",
        description,
        "",
        "---",
        "",
        "## EPUB (Dublin Core / OPF)",
        "",
        "Required and recommended metadata for EPUB. Use in OPF `<metadata>` or feed to ebooklib.",
        "",
        "| Element | Value |",
        "|---------|-------|",
        f"| `dc:title` | {title} |",
        f"| (subtitle) | {subtitle or '—'} |",
        f"| `dc:creator` | {author} |",
        f"| `dc:language` | {lang} |",
        f"| `dc:identifier` | {identifier} |",
        f"| `dcterms:modified` | {modified} |",
        f"| `dc:subject` | {keywords_str} |",
        "",
        "**Full `dc:description`** (copy below):",
        "",
        description,
        "",
        "Subjects (one per tag):",
        "",
        dc_subjects,
        "",
        "---",
        "",
        "## PDF (Document information & XMP)",
        "",
        "Standard PDF document info and XMP-friendly fields for pypdf, weasyprint, or Acrobat.",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| **Title** | {full_title} |",
        f"| **Author** | {author} |",
        f"| **Keywords** | {keywords_str} |",
        f"| **ModDate** | {modified} |",
        "",
        "**Full Subject** (copy below):",
        "",
        description,
        "",
    ]
    if publisher:
        lines.extend([f"| **Publisher** | {publisher} |", ""])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate book metadata MD from book/ folder for PDF, EPUB, and publishing platforms."
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output Markdown file path (default: output/book-metadata.md under repo root)",
    )
    parser.add_argument(
        "--book-dir", "-b",
        type=Path,
        default=None,
        help="Path to book folder (default: repo root / book)",
    )
    parser.add_argument(
        "--keywords", "-k",
        type=str,
        default=None,
        help="Comma-separated keywords (e.g. 'AI, transformation, CEO'). Merged with keywords from metadata file.",
    )
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    book_dir = args.book_dir if args.book_dir is not None else repo_root / "book"
    if not book_dir.is_dir():
        raise SystemExit(f"Book directory not found: {book_dir}")

    out_path = args.output if args.output is not None else repo_root / "output" / "book-metadata.md"

    meta = build_metadata(book_dir, cli_keywords=args.keywords)
    write_metadata_md(meta, out_path)
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
