# Research Refresh Policy

How new research is added during the project, and whether finished chapters are updated.

---

## 1. Should we add a workflow/skill to scan for new information and update the plan?

**Recommendation: Yes — add a lightweight Research Refresh step, but keep it separate from the plan.**

- **Scan for new information:** Add a **Research Refresh** skill (see `skills/research-refresh-agent/SKILL.md`). It defines when and how to look for new evidence (e.g. targeted web/Perplexity queries by research section or chapter topic), and where to put results.
- **Update the plan only when structure changes:** New *facts* go into **`research/`** (new files or appendices to the synthesis). Update **`plan/`** only when new information implies a change to:
  - thesis or positioning (`plan/concept.md`),
  - TOC or chapter list (`plan/toc.md`),
  - or chapter hooks (`plan/chapter-hooks.md`).
- **Flow:** Scan → curate into `research/` → optionally update `plan/` only if thesis/TOC/hooks are affected. The Research Agent already scans the full `research/` folder for each new chapter, so new files are automatically used for all *future* chapter briefs.

This keeps the plan stable and makes "new information" a research-layer concern, not a structural one.

---

## 2. Use new content only for new chapters, or go back and update already-created chapters?

**Recommendation: Use new research only for new (not-yet-written) chapters. Do not routinely back-fill already-created chapters.**

| Approach | Use new research for new chapters only | Go back and update all existing chapters |
|----------|----------------------------------------|------------------------------------------|
| **Scope** | Controlled. Finish the manuscript, then decide on a second pass. | High. Every new batch of research can trigger rework of multiple chapters. |
| **Consistency** | Book can be framed as "research and context as of [date range]." Early and late chapters may differ in citation vintage; acceptable if you add a short note (e.g. "Key sources and data as of [date]"). | Maximally consistent if you re-run Research Agent + Writer (or manual edits) for every touched chapter. |
| **Risk** | Low. You avoid endless rework and scope creep. | Higher. Easy to slip into repeated rewrites and delayed completion. |

**Practical rule:**

- **Default:** New material in `research/` is used only when producing **research briefs and drafts for chapters that are not yet done** (Planner + Research Agent already use the full `research/` folder for each new chapter).
- **Exception:** If a single high-impact fact (e.g. a central stat or case) is superseded or corrected, make a **one-off, targeted edit** to the affected chapter(s) and note it in the file or in `plan/plan.md`. Do not re-run the full pipeline for that chapter unless you explicitly want a full revision pass.
- **Optional later pass:** After all chapters are drafted, you can run a deliberate **"Rev 2"** pass: list what new research matters most, then decide which chapters (if any) get a focused update. That stays a discrete decision, not part of the normal chapter workflow.

**Summary:** Prefer forward-only use of new content; back-fill only by exception or in a planned Rev 2 pass. This keeps the project finishable and avoids mixing "write the book" with "keep the whole book continuously up to date."

---

## 3. Where this is documented

- **Research Refresh skill:** `skills/research-refresh-agent/SKILL.md` — how to scan, what to add to `research/`, when to touch `plan/`.
- **Research Agent:** `skills/research-agent/SKILL.md` — already uses all of `research/` for each new chapter; no change needed.
- **Orchestrator / session start:** Optional: at start of session, check if `research/` was updated since last chapter and remind that new content applies to future chapters only (per this policy).
