"""Escape [^N] patterns in footnotes-remediation-sheet.md so Markdown link validation
does not treat them as reference links (link.no-such-reference).

Run from repo root: python scripts/fix_remediation_footnote_markers.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "book" / "footnotes-remediation-sheet.md"


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    # Remove old stub section if present (between markers)
    text = re.sub(
        r"\n---\n\n## Markdown linter stubs \(read first\)\n\n.*?\n---\n\n## Compact index",
        r"\n---\n\n## Compact index",
        text,
        count=1,
        flags=re.DOTALL,
    )

    # Wrap [^N] in backticks when not already wrapped and not a definition line [^N]:
    pat = re.compile(r"(?<!`)\[\^([0-9]{1,3})\](?!:)(?!`)")

    prev = None
    while prev != text:
        prev = text
        text = pat.sub(lambda m: "`[^" + m.group(1) + "]`", text)

    PATH.write_text(text, encoding="utf-8")
    print("Updated", PATH)


if __name__ == "__main__":
    main()
