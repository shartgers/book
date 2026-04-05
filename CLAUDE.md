# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Identity

- **Book:** ~200 pages, European CEO audience
- **Thesis:** European CEOs are dangerously underprepared for the largest organisational paradigm shift since the industrial revolution
- **Tone:** Senior advisor to peer CEO — direct, evidence-based, structured, never dry
- **Language:** British English throughout (colour, organise, behaviour, whilst, towards, etc.)

---

## How the Layers Work

| Layer | Job | Key files |
|-------|-----|-----------|
| `plan/concept.md` | What the book is — thesis, research, author voice | Read at the start of any writing session |
| `plan/plan.md` | What to do next — phases, tasks, checkboxes | Check before starting work; update when tasks complete |
| `docs/` | Reference standards — voice, writing conventions | Consult when writing or editing |
| `skills/` | How to execute — one instruction set per agent role | Load the relevant skill before acting |

---

## Session Startup (Orchestrator)

Run these four steps at the start of every session before doing anything else:

1. Read `plan/plan.md` — find the current phase and the first unchecked task
2. Read `plan/concept.md` — refresh thesis and author voice context
3. Check `output/chapters/` for any handoff blocks from a previous session not yet acted on
4. Proceed with the workflow

---

## Current State

**Phase 0 — Foundation** is complete.

**Phase 1 — Chapters:** Book has **16 chapters** (see `plan/toc.md`). **All 16 chapters complete.**

**Next task when ready:** Run format-book-agent (`skills/format-book-agent/SKILL.md`) to build the print-ready PDF.

---

## Key Files

| Purpose | File |
|---------|------|
| Book concept & thesis | `plan/concept.md` |
| Progress tracker | `plan/plan.md` |
| Primary research synthesis | `research/book-research-claude.md` (10-section synthesis) |
| Other research sources | `research/` — imported papers and supplementary files |
| Writing conventions | `docs/writing-best-practices.md` |
| Brand voice | `docs/brand-voice.md` |
| Handoff protocol | `docs/agent-handoff-protocol.md` |
| Research refresh policy | `docs/research-refresh-policy.md` — when to add new research; use for new chapters only (no routine back-fill) |
| Ralph Wiggum writing skill | `skills/writing-ralph-wiggum-loop/SKILL.md` |
| Image designer skill | `skills/image-designer-agent/SKILL.md` |
| Research Refresh (optional) | `skills/research-refresh-agent/SKILL.md` — scan for new info, suggest additions to `research/`, update `plan/` only when structure changes |

---

## Output File Conventions

**Chapter files** (zero-padded: `ch01`, `ch02`, ...):

| File | Produced by |
|------|------------|
| `output/chapters/chapter-{nn}/ch{nn}-beats.md` | Planner |
| `output/chapters/chapter-{nn}/ch{nn}-research-brief.md` | Research Agent |
| `output/chapters/chapter-{nn}/ch{nn}-draft.md` | Writer + Case Study Agent (merged) |
| `output/chapters/chapter-{nn}/ch{nn}-draft-pg.md` | Perplexity Gate |
| `output/chapters/chapter-{nn}/ch{nn}-review.md` | Reviewers |
| `output/chapters/chapter-{nn}/ch{nn}-final.md` | Reviewers (chapter done) |

**Other outputs:**
- Book title / TOC → `plan/toc.md`
- Chapter hooks → `plan/chapter-hooks.md`
- Diagrams → `images/ch{nn}-[framework-kebab-name].png` (AI-generated) or `images/` via `npm run export` (React/SVG)

Create `output/chapters/` when drafting begins.

---

## Diagram Toolchain

React components that generate SVG diagrams in the book's visual style:

```bash
cd diagrams
npm install        # first time only
npm run export     # writes SVGs to images/
npm run export:watch  # rebuilds on change
```

To add a diagram: create `diagrams/src/diagrams/your-name.js`, register in `diagrams/src/export.js`. See `diagrams/README.md`.

Existing diagrams: `agentic-systems`, `ai-adoption-stages` (in `diagrams/src/diagrams/`).

For AI-generated diagrams, follow `skills/image-designer-agent/SKILL.md`.

---

## Multi-Agent Writing

| Role | Model | Skill |
|------|-------|-------|
| Orchestrator | Claude Code main | `skills/orchestrator-agent/SKILL.md` |
| Planner | Opus | `skills/planner-agent/SKILL.md` |
| Research Agent | Sonnet | `skills/research-agent/SKILL.md` |
| Writer | Opus | `skills/writer-agent/SKILL.md` |
| Case Study Agent | Sonnet | `skills/case-study-agent/SKILL.md` |
| Perplexity Gate | Sonnet | `skills/perplexity-gate-agent/SKILL.md` |
| Reviewers | Sonnet | `skills/reviewers-agent/SKILL.md` |

**Wave pattern per chapter:**
```
Wave 1 (parallel):  Planner + Research Agent
Wave 2 (parallel):  Writer + Case Study Agent
Wave 3:             Perplexity Gate
Wave 4:             Reviewers → chapter marked done
```

**Wave gate rule:** Each wave only starts when all agents in the previous wave append `Status: complete` to their output files. If any agent reports `blocked` or `escalated`, stop and resolve before continuing.

**Handoff block format** (appended to every output file on completion):
```
## Handoff — [Agent Role] — Chapter {nn}
Status: complete | blocked | escalated
Output: [file path]
Next agent: [role] (Wave [n])
```

**Case study placeholder:** The Writer leaves `<!-- CASE STUDY PLACEHOLDER -->` in `ch{nn}-draft.md`. The Case Study Agent replaces it in-place. Wave 2 is not complete until the placeholder is gone.

**Context management:** When checking wave completion, read handoff blocks only — not full draft files. `plan/plan.md` is the persistent state; the main session context is ephemeral. Reset context between chapters if the session becomes slow.

Full protocol: `docs/agent-handoff-protocol.md` | Orchestrator workflow: `skills/orchestrator-agent/SKILL.md`

**Research refresh (optional):** Between chapters, or when you add new files to `research/`, you can run the Research Refresh agent to scan for new evidence and suggest additions. New research is used for **future chapters only** unless you decide on a one-off fix or a Rev 2 pass. See `docs/research-refresh-policy.md`.
