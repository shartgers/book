# Agent Handoff Protocol

Standard for how agents complete tasks and pass work to the next wave.

---

## File Naming Convention

| Agent | Output file |
|-------|------------|
| Planner | `output/chapters/chapter-{nn}/ch{nn}-beats.md` |
| Research Agent | `output/chapters/chapter-{nn}/ch{nn}-research-brief.md` |
| Writer | `output/chapters/chapter-{nn}/ch{nn}-draft.md` (initial, with placeholder) |
| Case Study Agent | Merges into `output/chapters/chapter-{nn}/ch{nn}-draft.md` |
| Perplexity Gate | `output/chapters/chapter-{nn}/ch{nn}-draft-pg.md` |
| Reviewers | `output/chapters/chapter-{nn}/ch{nn}-review.md` + `output/chapters/chapter-{nn}/ch{nn}-final.md` |

Use zero-padded chapter numbers: `ch01`, `ch02`, ... `ch14`.

---

## Handoff Block

Every agent appends a handoff block to its output file on completion. The Orchestrator reads these to know when a wave is done and whether the next wave can start.

```
## Handoff — [Agent Role] — Chapter {nn}
Status: complete | blocked | escalated
Output: [file path]
[Role-specific fields — see each skill file]
Next agent: [role] (Wave [n])
```

**Status definitions:**
- `complete` — all pass conditions met; next wave can start
- `blocked` — a specific gap or missing input prevents completion; describe it
- `escalated` — a problem requires Orchestrator or human decision before proceeding

---

## Wave Gate Rules

The Orchestrator checks handoff blocks before starting each wave:

| Wave | Starts when |
|------|-------------|
| Wave 2 | Both Planner and Research Agent report `complete` |
| Wave 3 | Both Writer and Case Study Agent report `complete` |
| Wave 4 | Perplexity Gate reports `complete` |
| Chapter done | Reviewers report `complete` and plan/plan.md is updated |

If any agent reports `blocked` or `escalated`, Wave N+1 does not start until resolved.

---

## Escalation

If an agent cannot proceed, it writes `blocked` or `escalated` in the handoff block and stops. It does not attempt to resolve the issue independently. Common escalation triggers:

- Research brief has no data for the assigned company
- A continuity failure requires changes to a previously completed chapter
- The same review criterion fails across two consecutive chapters
- The beat sheet calls for a company not in the research file

The Orchestrator (main Claude Code session) decides whether to fix, reassign, or flag to the human.
