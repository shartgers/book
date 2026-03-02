# Book Progress

## Current Phase: COMPLETE — All 14 chapters written

---

## Project status (as of Mar 2026)

- **Structure:** TOC locked at 14 chapters in `plan/toc.md`. Plan, chapter hooks, docs, prompts (ch01–ch14), and agent skills are aligned to this structure.
- **Writing:** Chapters 1–11 complete (beats, research brief, draft, Perplexity Gate, review, final). **Chapter 12 next** — Readiness.
- **Skills:** All core agent skills live under `skills/` (orchestrator, planner, research, writer, case-study, perplexity-gate, reviewers, research-refresh). Additional skills: `format-book-agent`, `image-designer-agent`, `writing-ralph-wiggum-loop`.
- **Research:** `research/` expanded with chapter-focused notes and book synthesis. Prompts in `prompts/` cover ch02–ch14 (research prompts per chapter).
- **Publishing:** Print pipeline in place. `skills/format-book-agent/` builds print-ready PDF for KDP/IngramSpark; dry-run (Chapter 1 only) has been run. Inputs: `input/book-layout.html`, `output/misc/introduction.md`, `output/misc/about-the-author.md` (or placeholders).

---

## Phase 0: Foundation

Tasks must complete in order before chapter drafting begins.

- [x] Working title locked → `plan/toc.md`
- [x] Full TOC created → `plan/toc.md`
- [x] Chapter hooks written → `plan/chapter-hooks.md`

---

## Agent Team Setup

Skills to create before running parallel writing waves.

| Role | Model | Skill file |
|------|-------|------------|
| Orchestrator | Claude Code main | `skills/orchestrator-agent/SKILL.md` |
| Planner | Opus | `skills/planner-agent/SKILL.md` |
| Research Agent | Sonnet | `skills/research-agent/SKILL.md` |
| Writer | Opus | `skills/writer-agent/SKILL.md` |
| Case Study Agent | Sonnet | `skills/case-study-agent/SKILL.md` |
| Perplexity Gate | Sonnet | `skills/perplexity-gate-agent/SKILL.md` |
| Reviewers | Sonnet | `skills/reviewers-agent/SKILL.md` |

- [x] `skills/orchestrator-agent/SKILL.md`
- [x] `skills/planner-agent/SKILL.md`
- [x] `skills/research-agent/SKILL.md`
- [x] `skills/writer-agent/SKILL.md`
- [x] `skills/case-study-agent/SKILL.md`
- [x] `skills/perplexity-gate-agent/SKILL.md`
- [x] `skills/reviewers-agent/SKILL.md`
- [x] `docs/agent-handoff-protocol.md`

**Additional skills (outside the wave):** `skills/format-book-agent/` (print PDF for KDP/IngramSpark), `skills/image-designer-agent/`, `skills/writing-ralph-wiggum-loop/`, `skills/research-refresh-agent/` (optional refresh).

**Wave pattern per chapter:**
```
Wave 1 (parallel):  Planner + Research Agent
Wave 2 (parallel):  Writer + Case Study Agent
Wave 3:             Perplexity Gate
Wave 4:             Reviewers → chapter marked done
```

**Research refresh (optional):** When you add or update files in `research/`, new content is used for **future chapters only** (see `docs/research-refresh-policy.md`). Optionally run `skills/research-refresh-agent/SKILL.md` to scan for more evidence or to suggest plan updates.

---

## Phase 1–N: Chapters

### Chapter 01: The Largest Shift Since the Industrial Revolution
- [x] Beats → output/chapters/chapter-01/ch01-beats.md
- [x] Research brief → output/chapters/chapter-01/ch01-research-brief.md
- [x] Draft → output/chapters/chapter-01/ch01-draft.md
- [x] Perplexity Gate → output/chapters/chapter-01/ch01-draft-pg.md
- [x] Review → output/chapters/chapter-01/ch01-review.md
- [x] Case study → output/chapters/chapter-01/ch01-case-study.md
- [x] Done → output/chapters/chapter-01/ch01-final.md

### Chapter 02: Leadership Is Not Optional
- [x] Beats → output/chapters/chapter-02/ch02-beats.md
- [x] Research brief → output/chapters/chapter-02/ch02-research-brief.md
- [x] Draft → output/chapters/chapter-02/ch02-draft.md
- [x] Perplexity Gate → output/chapters/chapter-02/ch02-draft-pg.md
- [x] Review → output/chapters/chapter-02/ch02-review.md
- [x] Case study → output/chapters/chapter-02/ch02-case-study.md
- [x] Done → output/chapters/chapter-02/ch02-final.md

### Chapter 03: What the Agentic Organisation Looks Like
- [x] Beats → output/chapters/chapter-03/ch03-beats.md
- [x] Research brief → (incorporated from book-research-claude.md sections 1, 3, 5, 7, 8, 9 and research/the-agentic-employee.md)
- [x] Draft → output/chapters/chapter-03/ch03-draft.md
- [x] Perplexity Gate → output/chapters/chapter-03/ch03-draft-pg.md
- [x] Review → output/chapters/chapter-03/ch03-review.md
- [x] Done → output/chapters/chapter-03/ch03-final.md

### Chapter 04: The Four Tiers of Transformation
- [x] Beats → output/chapters/chapter-04/ch04-beats.md
- [x] Research brief → output/chapters/chapter-04/ch04-research-brief.md
- [x] Draft → output/chapters/chapter-04/ch04-draft.md
- [x] Perplexity Gate → output/chapters/chapter-04/ch04-draft-pg.md
- [x] Review → output/chapters/chapter-04/ch04-review.md
- [x] Done → output/chapters/chapter-04/ch04-final.md

### Chapter 05: The AI Transformation Framework
- [x] Beats → output/chapters/chapter-05/ch05-beats.md
- [x] Research brief → output/chapters/chapter-05/ch05-research-brief.md
- [x] Draft → output/chapters/chapter-05/ch05-draft.md
- [x] Perplexity Gate → output/chapters/chapter-05/ch05-draft-pg.md
- [x] Review → output/chapters/chapter-05/ch05-review.md
- [x] Done → output/chapters/chapter-05/ch05-final.md

### Chapter 06: The Operational Layer
- [x] Beats → output/chapters/chapter-06/ch06-beats.md
- [x] Research brief → output/chapters/chapter-06/ch06-research-brief.md
- [x] Draft → output/chapters/chapter-06/ch06-draft.md
- [x] Perplexity Gate → output/chapters/chapter-06/ch06-draft-pg.md
- [x] Review → output/chapters/chapter-06/ch06-review.md
- [x] Done → output/chapters/chapter-06/ch06-final.md

### Chapter 07: Foundations of the AI Transformation
- [x] Beats → output/chapters/chapter-07/ch07-beats.md
- [x] Research brief → output/chapters/chapter-07/ch07-research-brief.md
- [x] Draft → output/chapters/chapter-07/ch07-draft.md
- [x] Perplexity Gate → output/chapters/chapter-07/ch07-draft-pg.md
- [x] Review → output/chapters/chapter-07/ch07-review.md
- [x] Done → output/chapters/chapter-07/ch07-final.md

### Chapter 08: Value, Capabilities, Trust
- [x] Beats → output/chapters/chapter-08/ch08-beats.md
- [x] Research brief → output/chapters/chapter-08/ch08-research-brief.md
- [x] Draft → output/chapters/chapter-08/ch08-draft.md
- [x] Perplexity Gate → output/chapters/chapter-08/ch08-draft-pg.md
- [x] Review → output/chapters/chapter-08/ch08-review.md
- [x] Done → output/chapters/chapter-08/ch08-final.md

### Chapter 09: Europe's Distinctive Edge
- [x] Beats → output/chapters/chapter-09/ch09-beats.md
- [x] Research brief → output/chapters/chapter-09/ch09-research-brief.md
- [x] Draft → output/chapters/chapter-09/ch09-draft.md
- [x] Perplexity Gate → output/chapters/chapter-09/ch09-draft-pg.md
- [x] Review → output/chapters/chapter-09/ch09-review.md
- [x] Done → output/chapters/chapter-09/ch09-final.md

### Chapter 10: What the Leaders Did
- [x] Beats → output/chapters/chapter-10/ch10-beats.md
- [x] Research brief → output/chapters/chapter-10/ch10-research-brief.md
- [x] Draft → output/chapters/chapter-10/ch10-draft.md
- [x] Perplexity Gate → output/chapters/chapter-10/ch10-draft-pg.md
- [x] Review → output/chapters/chapter-10/ch10-review.md
- [x] Done → output/chapters/chapter-10/ch10-final.md

### Chapter 11: Building Your Agentic Organisation
- [x] Beats → output/chapters/chapter-11/ch11-beats.md
- [x] Research brief → output/chapters/chapter-11/ch11-research-brief.md
- [x] Draft → output/chapters/chapter-11/ch11-draft.md
- [x] Perplexity Gate → output/chapters/chapter-11/ch11-draft-pg.md
- [x] Review → output/chapters/chapter-11/ch11-review.md
- [x] Done → output/chapters/chapter-11/ch11-final.md

### Chapter 12: Readiness
- [x] Beats → output/chapters/chapter-12/ch12-beats.md
- [x] Research brief → output/chapters/chapter-12/ch12-research-brief.md
- [x] Draft → output/chapters/chapter-12/ch12-draft.md
- [x] Perplexity Gate → output/chapters/chapter-12/ch12-draft-pg.md
- [x] Review → output/chapters/chapter-12/ch12-review.md
- [x] Done → output/chapters/chapter-12/ch12-final.md

### Chapter 13: Measuring What Matters
- [x] Beats → output/chapters/chapter-13/ch13-beats.md
- [x] Research brief → output/chapters/chapter-13/ch13-research-brief.md
- [x] Draft → output/chapters/chapter-13/ch13-draft.md
- [x] Perplexity Gate → output/chapters/chapter-13/ch13-draft-pg.md
- [x] Review → output/chapters/chapter-13/ch13-review.md
- [x] Done → output/chapters/chapter-13/ch13-final.md

### Chapter 14: A Leadership Decision
- [x] Beats → output/chapters/chapter-14/ch14-beats.md
- [x] Research brief → output/chapters/chapter-14/ch14-research-brief.md
- [x] Draft → output/chapters/chapter-14/ch14-draft.md
- [x] Perplexity Gate → output/chapters/chapter-14/ch14-draft-pg.md
- [x] Review → output/chapters/chapter-14/ch14-review.md
- [x] Done → output/chapters/chapter-14/ch14-final.md
