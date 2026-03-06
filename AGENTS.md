# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a book authoring repository for "The Agentic Organisation". It has two toolchains:

1. **Book build pipeline** (Python): Markdown → PDF / EPUB / HTML via `npm run pdf`, `npm run epub`, `npm run html`. See `skills/format-book-agent/SKILL.md` for full usage.
2. **Diagram generator** (Node/React): SVG diagrams via `cd diagrams && npm run export`. See `diagrams/README.md`.

There is no lint tool, no automated test suite, and no long-running dev server. The "development loop" is: edit Markdown in `book/`, run a build command, inspect output in `output/`.

### Gotchas

- The `package.json` scripts call `python` (not `python3`). A symlink `/usr/local/bin/python → python3` must exist. The update script handles this.
- After `npm install` in `diagrams/`, esbuild's binary may lack execute permission. Run `chmod +x diagrams/node_modules/.bin/esbuild` if `npm run export` fails with "Permission denied".
- WeasyPrint requires system libraries (Pango, Cairo). These are pre-installed in the VM snapshot; if missing, install via `sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libcairo2 libffi-dev`.
- PDF build (`npm run pdf`) downloads Google Fonts on each run — takes ~6s. HTML and EPUB builds are sub-second.

### Build commands (from repo root)

| Command | Output |
|---------|--------|
| `npm run html` | `output/book-interior.html` |
| `npm run pdf` | `output/book-interior.pdf` |
| `npm run epub` | `output/book-interior.epub` |
| `npm run build` | All three above |
| `cd diagrams && npm run export` | SVGs in `images/` |
| `python scripts/wordcount_chapter.py` | Word count to stdout |
