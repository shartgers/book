#!/usr/bin/env python3
"""
Count words in a chapter draft, excluding placeholders, handoff, headings, and separators.
Use from repo root: python scripts/wordcount_chapter.py [path/to/draft.md]
Defaults to output/chapters/chapter-02/ch02-draft.md if no path given.
"""
import re
import sys
from pathlib import Path

# Default path relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DRAFT = REPO_ROOT / "output" / "chapters" / "chapter-02" / "ch02-draft.md"


def wordcount_prose_only(filepath: Path) -> int:
    """Strip placeholders/headings/etc. and return word count of prose only."""
    text = filepath.read_text(encoding="utf-8")
    body = text
    # Remove placeholder blocks and handoff section
    body = re.sub(r"<!-- CASE STUDY PLACEHOLDER.*?-->", "", body, flags=re.DOTALL)
    body = re.sub(r"<!-- DIAGRAM PLACEHOLDER.*?-->", "", body, flags=re.DOTALL)
    body = re.sub(r"## Handoff.*", "", body, flags=re.DOTALL)
    # Remove markdown headings and horizontal rules
    body = re.sub(r"^#{1,3} .*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^---$", "", body, flags=re.MULTILINE)
    return len(body.split())


def main():
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.is_absolute():
            path = REPO_ROOT / path
    else:
        path = DEFAULT_DRAFT

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    words = wordcount_prose_only(path)
    print(f"Word count (prose only, non-case-study): {words}")


if __name__ == "__main__":
    main()
