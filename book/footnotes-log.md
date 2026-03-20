# Footnotes

## Footnote renumber audit — Global sequence realignment (ch01 to ch15)

This log was refreshed by comparing only chapter files in `book/` (`ch*.md`).
It checks inline references `[^N]` against footnote definitions `[^N]:`.

| Chapter file | Final inline range | Result |
|--------------|--------------------|--------|
| `ch01-the-largest-shift-since-the-industrial-revolution.md` | `[^1]` to `[^10]` | In sync |
| `ch02-when-sponsorship-is-not-enough.md` | `[^11]` to `[^21]` | In sync |
| `ch03-what-the-agentic-organisation-looks-like.md` | `[^22]` to `[^36]` | In sync |
| `ch04-when-local-wins-dont-add-up.md` | `[^37]` to `[^54]` | In sync |
| `ch05-every-transformation-needs-a-map.md` | `[^55]` to `[^59]` | In sync |
| `ch06-the-product-layer.md` | `[^60]` to `[^66]` | In sync |
| `ch07-the-operational-layer.md` | `[^67]` to `[^73]` | In sync |
| `ch08-the-foundational-layer.md` | `[^74]` to `[^76]` | In sync |
| `ch09-the-ai-decision-lens.md` | `[^77]` to `[^85]` | In sync |
| `ch10-europes-distinctive-edge.md` | `[^86]` to `[^93]` | In sync |
| `ch11-the-decisions-that-mattered.md` | `[^94]` to `[^96]` | In sync |
| `ch12-building-your-agentic-organisation.md` | `[^97]` to `[^101]` | In sync |
| `ch13-readiness.md` | `[^102]` to `[^105]` | In sync |
| `ch14-measuring-what-matters.md` | `[^106]` to `[^107]` | In sync |
| `ch15-a-leadership-decision.md` | `[^108]` to `[^111]` | In sync |

**Integrity checks passed:**
- No missing definitions (every inline `[^N]` has a matching `[^N]:`).
- No orphaned definitions (every `[^N]:` is referenced inline).
- Global numbering is continuous with no gaps.

**Periodic source-alignment validation performed:**
- `ch01`: corrected a citation shift in the "industry phases" paragraph so that the inline reference now points to a transformation-performance source, while EU venture-capital sourcing remains on the EU investment paragraph.
- `ch07`: corrected two semantic mismatches created by prior renumbering by aligning workforce-skills claims with BCG AI-at-work / talent research and social-dialogue claims with ETUI trade-union / collective-bargaining research (see current `[^70]`–`[^71]` definitions in `ch07`).
- Cross-chapter boundary validation confirms sequence continuity at each chapter handoff.

**Reference quality pass (2026-03-20):** Footnote definitions in `ch05`–`ch15` were updated with stable landing-page or primary-document URLs and tightened titles (aligned to `book/footnotes-remediation-sheet.md` where applicable). Spot-check PDFs and press URLs before print.

**VS Code Markdown validation (2026-03-20):** The editor reports `link.no-such-reference` for valid `[^N]` / `[^N]:` footnote syntax. Workspace setting `markdown.validate.referenceLinks.enabled` is set to `"ignore"` in `.vscode/settings.json` (see [microsoft/vscode#268605](https://github.com/microsoft/vscode/issues/268605)).

Source lookup scope: chapter files in `book/` only (`ch*.md`). No Research-folder or web re-validation in this renumber pass.