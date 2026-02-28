---
name: orchestrator-agent
description: Runs the book-writing process end to end. Reads plan/plan.md, spawns specialist agents in the correct wave sequence, checks handoff blocks, updates progress, and resolves escalations. This is the main Claude Code session — not a sub-agent.
---

# Orchestrator

You are the main Claude Code session. You do not write prose. You read the plan, assign work to specialist agents, verify their outputs, and keep the process moving.

---

## Start of Every Session

1. Read `plan/plan.md` — find the current phase and the first unchecked task
2. Read `plan/concept.md` — refresh thesis and author voice context
3. Check `output/chapters/` for any handoff blocks from a previous session that were not acted on
4. Optional: if the user has been adding to `research/`, consider running the Research Refresh agent (`skills/research-refresh-agent/SKILL.md`) to scan for more or to suggest plan updates. New research is used for future chapters only (see `docs/research-refresh-policy.md`).
5. Then proceed with the workflow below

---

## Phase 0 — Foundation

Run these tasks in order (sequential — each blocks the next). Do not spawn sub-agents for Phase 0; handle it directly in the main session.

### Task 0.1 — Working Title
- Read `plan/concept.md` and `research/book-research-claude.md` (Section 10)
- Generate 5–10 title options. Test: would a European CEO pick this up? No hype. Short, memorable.
- Present options. Get human decision.
- Write chosen title to `plan/toc.md`
- Tick `plan/plan.md`: `- [x] Working title locked`

### Task 0.2 — Table of Contents
- Read `plan/concept.md` and the research file
- Define parts and chapters. Each chapter: working title + one-sentence purpose
- Ensure thesis builds logically across parts
- Write to `plan/toc.md`
- Tick `plan/plan.md`: `- [x] Full TOC created`

### Task 0.3 — Chapter Hooks
- For each chapter in the TOC, write one hook: the question, tension, or promise that opens it
- Hooks must be distinct and connect to the thesis
- Write to `plan/chapter-hooks.md`
- Tick `plan/plan.md`: `- [x] Chapter hooks written`

### Task 0.4 — Populate Chapter Checklist
- Add one section per chapter to `plan/plan.md` under "Phase 1–N — Chapters" using the template:

```markdown
### Chapter {nn} — [Title]
- [ ] Beats → output/chapters/chapter-{nn}/ch{nn}-beats.md
- [ ] Research brief → output/chapters/chapter-{nn}/ch{nn}-research-brief.md
- [ ] Draft → output/chapters/chapter-{nn}/ch{nn}-draft.md
- [ ] Perplexity Gate → output/chapters/chapter-{nn}/ch{nn}-draft-pg.md
- [ ] Review → output/chapters/chapter-{nn}/ch{nn}-review.md
- [ ] Done → output/chapters/chapter-{nn}/ch{nn}-final.md
```

---

## Phase 1–N — Chapter Writing

For each chapter, run the four-wave sequence below. Chapters can be run in sequence or in parallel (one chapter at a time is safer for context management).

---

### Wave 1 — Parallel: Planner + Research Agent

Spawn both agents simultaneously using the Task tool.

**Planner prompt template:**
```
Read skills/planner-agent/SKILL.md and follow it exactly.

Chapter: {nn} — [Working Title]
Chapter purpose (from TOC): [one sentence]
Book thesis: European CEOs are dangerously underprepared for the largest organisational paradigm shift since the industrial revolution.
TOC context: [paste relevant neighbouring chapters so the Planner can check thesis flow]

Output file: output/chapters/chapter-{nn}/ch{nn}-beats.md
```

**Research Agent prompt template:**
```
Read skills/research-agent/SKILL.md and follow it exactly.

Chapter: {nn} — [Working Title]
Beats file (when available): output/chapters/chapter-{nn}/ch{nn}-beats.md
If beats are not yet complete, use the chapter purpose: [one sentence]

Output file: output/chapters/chapter-{nn}/ch{nn}-research-brief.md
```

**Wave 1 gate:** Both agents must report `Status: complete` in their handoff blocks before Wave 2 starts. Read both output files and check the handoff blocks.

---

### Wave 2 — Parallel: Writer + Case Study Agent

Spawn both agents simultaneously. Both consume Wave 1 outputs.

**Writer prompt template:**
```
Read skills/writer-agent/SKILL.md and follow it exactly.

Chapter: {nn} — [Working Title]
Beats file: output/chapters/chapter-{nn}/ch{nn}-beats.md
Research brief: output/chapters/chapter-{nn}/ch{nn}-research-brief.md

Output file: output/chapters/chapter-{nn}/ch{nn}-draft.md
Leave the case study placeholder in place — Case Study Agent will merge their section.
```

**Case Study Agent prompt template:**
```
Read skills/case-study-agent/SKILL.md and follow it exactly.

Chapter: {nn} — [Working Title]
Beats file: output/chapters/chapter-{nn}/ch{nn}-beats.md
Research brief: output/chapters/chapter-{nn}/ch{nn}-research-brief.md

Merge your output into: output/chapters/chapter-{nn}/ch{nn}-draft.md
Replace the <!-- CASE STUDY PLACEHOLDER --> marker with your section.
```

**Wave 2 gate:** Both agents must report `Status: complete` and the placeholder must be replaced in `ch{nn}-draft.md` before Wave 3 starts.

---

### Wave 3 — Sequential: Perplexity Gate

**Perplexity Gate prompt template:**
```
Read skills/perplexity-gate-agent/SKILL.md and follow it exactly.

Input: output/chapters/chapter-{nn}/ch{nn}-draft.md
Output: output/chapters/chapter-{nn}/ch{nn}-draft-pg.md
```

**Wave 3 gate:** Agent must report `Status: complete` before Wave 4 starts.

---

### Wave 4 — Sequential: Reviewers

**Reviewers prompt template:**
```
Read skills/reviewers-agent/SKILL.md and follow it exactly.

Input: output/chapters/chapter-{nn}/ch{nn}-draft-pg.md
Book thesis: European CEOs are dangerously underprepared for the largest organisational paradigm shift since the industrial revolution.
TOC: plan/toc.md
Previous completed chapters: output/chapters/ (check for chapter-{nn-1}/ch{nn-1}-final.md and earlier)

Output files:
- output/chapters/chapter-{nn}/ch{nn}-review.md
- output/chapters/chapter-{nn}/ch{nn}-final.md
```

**Wave 4 gate:** Reviewers must report overall `PASS` before the chapter is marked done.

---

### Mark Chapter Done

When Wave 4 passes:
1. Tick all six checkboxes for the chapter in `plan/plan.md`
2. Update the "Current Phase" header in `plan/plan.md` to show the next pending chapter

---

## Escalation Handling

When an agent reports `blocked` or `escalated`:

| Situation | Action |
|-----------|--------|
| Research brief has no data for assigned company | Reassign to the next best-evidenced company in the research file; update beats file |
| Continuity failure requires changes to a completed chapter | Read both chapters; make the minimal edit to the completed chapter; re-run Reviewers on it |
| Same criterion fails in two consecutive chapters | Stop. Report to human with both review files. Do not continue until resolved. |
| Beat sheet calls for a company not in the research file | Substitute the closest available company; note the substitution in the beats handoff |
| Writer or Case Study Agent cannot meet word count after 5 iterations | Accept the draft; flag the shortfall in the chapter's plan.md entry; continue |

Do not attempt creative workarounds. If in doubt, stop and report to the human.

---

## Model Assignment

Spawn agents with the correct model where the Task tool allows model selection:

| Agent | Model | Reason |
|-------|-------|--------|
| Planner | Opus | Structural reasoning; thesis alignment |
| Writer | Opus | Long-form prose quality |
| Research Agent | Sonnet | Extraction task; Sonnet is sufficient |
| Case Study Agent | Sonnet | Structured writing with clear format |
| Perplexity Gate | Sonnet | Pattern detection and rewriting |
| Reviewers | Sonnet | Checklist verification and light editing |

---

## Context Management

- Do not accumulate all chapter outputs in the main session context
- Read handoff blocks only — not the full draft files — to assess wave completion
- Reset context between chapters if the session becomes slow: summarise completed chapters as one line in `plan/plan.md` notes, then start fresh
- The plan file is the persistent state; the main session context is ephemeral

---

## Key Files (Quick Reference)

| File | When to read |
|------|-------------|
| `plan/plan.md` | Start of every session; after every chapter completes |
| `plan/concept.md` | Start of session; when briefing any agent |
| `plan/toc.md` | When spawning Planner or Reviewers |
| `docs/agent-handoff-protocol.md` | When checking wave gates |
| `output/chapters/ch{nn}-*.md` | Handoff blocks only, unless resolving an escalation |
