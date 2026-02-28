# Book Progress

## Current Phase: Phase 1: Chapter 3

---

## Project status (as of Feb 2025)

- **Writing:** Chapter 1 complete. Chapter 2 complete (all beats, research brief, draft, case study, Perplexity Gate, review, final). Chapter 3 not started.
- **Skills:** All core agent skills live under `skills/` (orchestrator, planner, research, writer, case-study, perplexity-gate, reviewers, research-refresh). Additional skills: `publish-kdp-ingramspark`, `image-designer-agent`, `writing-ralph-wiggum-loop`.
- **Research:** `research/` expanded with chapter-focused notes (e.g. ch3 agentic enterprise, ch4 four tiers, ch5 mental framework) and other references.
- **Publishing:** Print pipeline in place. `skills/publish-kdp-ingramspark/` builds print-ready PDF for KDP/IngramSpark; dry-run (Chapter 1 only) has been run (`output/dry-run.html`, `output/dry-run.pdf`). Inputs: `input/book-layout.html`, `output/misc/introduction.md`, `output/misc/about-the-author.md` (or placeholders).

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

**Additional skills (outside the wave):** `skills/publish-kdp-ingramspark/` (print PDF for KDP/IngramSpark), `skills/image-designer-agent/`, `skills/writing-ralph-wiggum-loop/`, `skills/research-refresh-agent/` (optional refresh).

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

### Chapter 03: What the Agentic Enterprise Looks Like
- [ ] Beats → output/chapters/chapter-03/ch03-beats.md
- [ ] Research brief → output/chapters/chapter-03/ch03-research-brief.md
- [ ] Draft → output/chapters/chapter-03/ch03-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-03/ch03-draft-pg.md
- [ ] Review → output/chapters/chapter-03/ch03-review.md
- [ ] Done → output/chapters/chapter-03/ch03-final.md

### Chapter 04: The Four Tiers of Transformation
- [ ] Beats → output/chapters/chapter-04/ch04-beats.md
- [ ] Research brief → output/chapters/chapter-04/ch04-research-brief.md
- [ ] Draft → output/chapters/chapter-04/ch04-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-04/ch04-draft-pg.md
- [ ] Review → output/chapters/chapter-04/ch04-review.md
- [ ] Done → output/chapters/chapter-04/ch04-final.md

### Chapter 05: Value, Capabilities, Trust
- [ ] Beats → output/chapters/chapter-05/ch05-beats.md
- [ ] Research brief → output/chapters/chapter-05/ch05-research-brief.md
- [ ] Draft → output/chapters/chapter-05/ch05-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-05/ch05-draft-pg.md
- [ ] Review → output/chapters/chapter-05/ch05-review.md
- [ ] Done → output/chapters/chapter-05/ch05-final.md

### Chapter 06: Europe's Distinctive Edge
- [ ] Beats → output/chapters/chapter-06/ch06-beats.md
- [ ] Research brief → output/chapters/chapter-06/ch06-research-brief.md
- [ ] Draft → output/chapters/chapter-06/ch06-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-06/ch06-draft-pg.md
- [ ] Review → output/chapters/chapter-06/ch06-review.md
- [ ] Done → output/chapters/chapter-06/ch06-final.md

### Chapter 07: What the Leaders Did
- [ ] Beats → output/chapters/chapter-07/ch07-beats.md
- [ ] Research brief → output/chapters/chapter-07/ch07-research-brief.md
- [ ] Draft → output/chapters/chapter-07/ch07-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-07/ch07-draft-pg.md
- [ ] Review → output/chapters/chapter-07/ch07-review.md
- [ ] Done → output/chapters/chapter-07/ch07-final.md

### Chapter 08: Building Your Agentic Enterprise
- [ ] Beats → output/chapters/chapter-08/ch08-beats.md
- [ ] Research brief → output/chapters/chapter-08/ch08-research-brief.md
- [ ] Draft → output/chapters/chapter-08/ch08-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-08/ch08-draft-pg.md
- [ ] Review → output/chapters/chapter-08/ch08-review.md
- [ ] Done → output/chapters/chapter-08/ch08-final.md

### Chapter 09: Foundations of the AI transformation
- [ ] Beats → output/chapters/chapter-09/ch09-beats.md
- [ ] Research brief → output/chapters/chapter-09/ch09-research-brief.md
- [ ] Draft → output/chapters/chapter-09/ch09-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-09/ch09-draft-pg.md
- [ ] Review → output/chapters/chapter-09/ch09-review.md
- [ ] Done → output/chapters/chapter-09/ch09-final.md

### Chapter 10: Measuring What Matters
- [ ] Beats → output/chapters/chapter-10/ch10-beats.md
- [ ] Research brief → output/chapters/chapter-10/ch10-research-brief.md
- [ ] Draft → output/chapters/chapter-10/ch10-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-10/ch10-draft-pg.md
- [ ] Review → output/chapters/chapter-10/ch10-review.md
- [ ] Done → output/chapters/chapter-10/ch10-final.md

### Chapter 11: A leadership decision
- [ ] Beats → output/chapters/chapter-11/ch11-beats.md
- [ ] Research brief → output/chapters/chapter-11/ch11-research-brief.md
- [ ] Draft → output/chapters/chapter-11/ch11-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-11/ch11-draft-pg.md
- [ ] Review → output/chapters/chapter-11/ch11-review.md
- [ ] Done → output/chapters/chapter-11/ch11-final.md
