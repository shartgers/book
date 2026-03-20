#!/usr/bin/env python3
"""
Move Markdown footnote definition lines (`[^N]: ...`) to immediately after the first line
of each chapter file. VS Code / Markdown language service validates references in document
order; definitions at the end trigger `link.no-such-reference` for earlier `[^N]` mentions.

Run from repo root: python scripts/move_chapter_footnotes_to_top.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"

# ch01 … ch15 style filenames
FN_LINE = re.compile(r"^\[\^[0-9]+\]:")


def relocate_footnotes(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    footnote_lines = [ln for ln in lines if FN_LINE.match(ln)]
    body_lines = [ln for ln in lines if not FN_LINE.match(ln)]

    if not footnote_lines:
        return False

    if not body_lines:
        return False

    # Avoid rewriting if footnotes already sit right after the title
    if len(body_lines) >= 2 and FN_LINE.match(body_lines[1]):
        return False

    title = body_lines[0]
    rest = body_lines[1:]

    out_lines = [title, ""] + footnote_lines + [""] + rest
    new_text = "\n".join(out_lines)
    if text.endswith("\n"):
        new_text += "\n"

    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    chapters = sorted(BOOK.glob("ch*.md"))
    moved = 0
    for p in chapters:
        if relocate_footnotes(p):
            print("Moved footnotes to top:", p.relative_to(ROOT))
            moved += 1
        else:
            print("Skip (no footnotes or already at top):", p.relative_to(ROOT))
    print("Done. Files updated:", moved)


if __name__ == "__main__":
    main()
