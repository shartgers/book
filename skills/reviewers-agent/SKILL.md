---
name: reviewers-agent
description: Final quality gate for a chapter. Reviews Style, Character (author voice), and Continuity (thesis alignment). Produces a pass/fail report and a clean final draft. Use after the Perplexity Gate.
---

# Reviewers Agent

Run three sequential checks on the chapter: Style, Character, and Continuity. Produce a structured review report and a final draft with all issues resolved. This is the last gate before a chapter is marked done.

---

## Input

- `output/chapters/chapter-{nn}/ch{nn}-draft-pg.md` — Perplexity Gate output
- `plan/concept.md` — thesis and book-level argument
- `plan/toc.md` — chapter list (for continuity checks across chapters)
- `docs/brand-voice.md` — author voice reference
- `docs/writing-best-practices.md` — chapter template and quality checklist
- Previous completed chapter drafts in `output/chapters/chapter-{nn}/` — for cross-chapter continuity

---

## Output

Two files:

1. `output/chapters/chapter-{nn}/ch{nn}-review.md` — structured review report (pass/fail per check)
2. `output/chapters/chapter-{nn}/ch{nn}-final.md` — clean final chapter with all issues resolved

---

## Check 1 — Style

Verify that the chapter meets the structural and formatting conventions.

| Criterion | Pass condition |
|-----------|---------------|
| Chapter template complete | All 6 elements present: strategic tension, named framework, case study, governance implications, reflection questions, closing transition |
| Paragraph length | No paragraph longer than 4 lines |
| Framework is named and numbered | Framework has a name and 3–5 numbered elements |
| Framework is visualisable | Could be drawn as a diagram or model |
| Reflection questions | 3–5 questions, numbered, each prompting a specific decision |
| Word count | 2,500–3,500 words total |
| No filler | No phrases flagged in Perplexity Gate categories remain |
| No em dashes | Replace any em dashes (—) with commas, colons, or rephrasing |

---

## Check 2 — Character

Verify that the chapter sounds like Stephan Hartgers, not generic business writing.

| Criterion | Pass condition |
|-----------|---------------|
| Tone | Strategic, calm, direct — not hyped, not academic, not salesy |
| Concreteness | Claims are grounded in evidence or example; no vague assertions |
| Honesty about limits | Uncertainty is named where it exists; no overselling |
| Reader respect | Written for a capable executive; no hand-holding or over-explanation |
| British English | Consistent throughout — spelling, punctuation, vocabulary |
| Preferred vocabulary | Uses terms from brand voice: clarity, coherence, momentum, governance, framework, strategic, tangible, actionable |
| No credential-leading | Substance carries the weight; author voice doesn't rely on status signals |

---

## Check 3 — Continuity

Verify that the chapter fits into the book as a whole.

| Criterion | Pass condition |
|-----------|---------------|
| Thesis advancement | Chapter clearly advances the central argument |
| No duplicate frameworks | Named framework does not repeat a framework from a previous chapter |
| No duplicate case studies | Company used has not been the primary case study in another chapter |
| Transition coherence | Closing transition connects logically to the next chapter in the TOC |
| Argument progression | This chapter's claim builds on previous chapters; it is not self-contained |
| No concept re-introduction | Concepts, definitions, and quotes already introduced in an earlier chapter are not re-introduced as if the reader has never seen them. Reuse is fine; re-introduction is not. See resolution guidance below. |

---

## Report Format

File: `output/chapters/chapter-{nn}/ch{nn}-review.md`

```markdown
# Review Report — Chapter {nn} — [Working Title]

## Check 1 — Style
| Criterion | Status | Notes |
|-----------|--------|-------|
| Chapter template complete | PASS / FAIL | |
| Paragraph length | PASS / FAIL | |
...

**Style verdict: PASS / FAIL**

## Check 2 — Character
| Criterion | Status | Notes |
|-----------|--------|-------|
...

**Character verdict: PASS / FAIL**

## Check 3 — Continuity
| Criterion | Status | Notes |
|-----------|--------|-------|
...

**Continuity verdict: PASS / FAIL**

## Overall: PASS / FAIL
Issues to resolve: [list or "none"]
```

---

## Resolution Rules

- Fix all FAIL items before writing `ch{nn}-final.md`
- Do not change structure or argument to resolve a continuity failure — escalate to Orchestrator if resolving continuity requires changes to another chapter
- If the same criterion has failed in two consecutive chapters, escalate to Orchestrator rather than fixing in isolation

### Concept re-introduction fixes

When a concept, definition, or quote appears for the second time and is written as if it is new:

1. **Remove the redundant explanation.** Assume the reader already knows the concept.
2. **Reference the earlier introduction** where it helps the reader connect ideas — e.g. "As we saw in Chapter 2, …" or "Returning to Kotter's framework, …".
3. **Build on it, don't repeat it.** Add new depth, a new angle, or apply the concept to a different context rather than restating what was already said.
4. To detect these, read all completed final drafts in `output/chapters/` before reviewing the current chapter. Flag any concept, named framework, definition, or direct quote that was already introduced with a full explanation in an earlier chapter and is now explained again as if it is fresh.

---

## Handoff

Append to `output/chapters/chapter-{nn}/ch{nn}-final.md`:

```
## Handoff — Reviewers — Chapter {nn}
Status: complete | escalated
Output: output/chapters/chapter-{nn}/ch{nn}-final.md
Review report: output/chapters/chapter-{nn}/ch{nn}-review.md
Style: PASS / FAIL
Character: PASS / FAIL
Continuity: PASS / FAIL
Escalations: none | [description]
Chapter status: DONE
```

Update `plan/plan.md` — tick the four chapter checkboxes for this chapter.
