#!/usr/bin/env python3
"""
Run EPUBCheck (via npm / local epubchecker) and print a short summary to the terminal.

Usage from repository root:
  python skills/format-book-agent/scripts/epubcheck_with_summary.py <path-to.epub> [report.json]

Default report path is output/epubcheck-report.json (second arg overrides).

Exit code matches EPUBCheck so CI / npm scripts still fail on errors.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    """Walk up until package.json is found (npm scripts run from repo root)."""
    for p in [start.resolve()] + list(start.resolve().parents):
        if (p / "package.json").is_file():
            return p
    return start.resolve()


def print_epubcheck_summary(report_path: Path) -> None:
    """Print a short human-readable summary from epubcheck JSON output."""
    if not report_path.is_file():
        print(
            f"EPUBCheck summary: no report file at {report_path} (check failed before write?)",
            file=sys.stderr,
        )
        return

    try:
        data = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"EPUBCheck summary: could not read report: {e}", file=sys.stderr)
        return

    checker = data.get("checker") or {}
    pub = data.get("publication") or {}
    messages = data.get("messages") or []

    nf = int(checker.get("nFatal") or 0)
    ne = int(checker.get("nError") or 0)
    nw = int(checker.get("nWarning") or 0)
    nu = int(checker.get("nUsage") or 0)
    ver = checker.get("checkerVersion") or "?"

    title = pub.get("title") or "(unknown title)"
    epub_ver = pub.get("ePubVersion") or "?"
    layout = pub.get("renditionLayout") or "?"
    n_spines = pub.get("nSpines")
    spine_s = f"{n_spines} spine items" if n_spines is not None else "spine n/a"

    if nf == 0 and ne == 0:
        status = "PASS"
    else:
        status = "FAIL"

    # Blank line after any EPUBCheck/Java log noise, then a compact block.
    print()
    print("EPUBCheck — short report")
    print(f"  {status}  ·  fatal {nf}, errors {ne}, warnings {nw}, usage {nu}")
    print(f"  EPUBCheck {ver}  ·  EPUB {epub_ver}  ·  {layout}  ·  {spine_s}")
    print(f"  {title}")
    print(f"  Report file: {report_path.as_posix()}")

    if messages:
        print(f"  Messages: {len(messages)} (see JSON for full detail)")
        for i, m in enumerate(messages[:8]):
            if isinstance(m, dict):
                mid = m.get("ID") or m.get("id") or "?"
                sev = m.get("severity") or m.get("level") or "?"
                msg = m.get("message") or m.get("text") or str(m)
                one = msg.replace("\n", " ").strip()
                if len(one) > 120:
                    one = one[:117] + "..."
                print(f"    [{sev}] {mid}: {one}")
            else:
                print(f"    {m}")
        if len(messages) > 8:
            print(f"    ... and {len(messages) - 8} more")
    print()


def main() -> None:
    repo = find_repo_root(Path.cwd())
    argv = sys.argv[1:]
    if not argv:
        print(
            "Usage: epubcheck_with_summary.py <path-to.epub> [report.json]",
            file=sys.stderr,
        )
        sys.exit(2)

    epub_arg = Path(argv[0])
    epub_path = epub_arg if epub_arg.is_absolute() else (repo / epub_arg).resolve()

    if len(argv) >= 2:
        report_arg = Path(argv[1])
        report_path = (
            report_arg if report_arg.is_absolute() else (repo / report_arg).resolve()
        )
    else:
        report_path = (repo / "output" / "epubcheck-report.json").resolve()

    if not epub_path.is_file():
        print(f"EPUBCheck: file not found: {epub_path}", file=sys.stderr)
        sys.exit(2)

    report_path.parent.mkdir(parents=True, exist_ok=True)

    # Use npm exec so the local devDependency epubchecker is used (same as npx in package.json).
    npx = shutil.which("npx")
    if npx:
        cmd = [
            npx,
            "--yes",
            "epubchecker",
            str(epub_path),
            "--output",
            str(report_path),
        ]
        proc = subprocess.run(cmd, cwd=str(repo))
    else:
        print("EPUBCheck: npx not on PATH; install Node.js or run epubchecker manually.", file=sys.stderr)
        proc = subprocess.CompletedProcess(args=[], returncode=127)

    print_epubcheck_summary(report_path)
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
