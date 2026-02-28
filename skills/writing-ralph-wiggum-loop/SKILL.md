---
name: writing-ralph-wiggum-loop
description: Write content iteratively until several explicit completion conditions are met. Use when the user wants Ralph Wiggum loop writing, iterative writing until conditions are satisfied, or autonomous write-check-fix cycles for drafts, chapters, or documents.
---

# Writing in a Ralph Wiggum Loop

Write iteratively until **all** completion conditions are met. The loop: write → check → feed back → write again. Stop only when every condition passes.

## When to Use

- User asks for "Ralph Wiggum loop" or "write until conditions are met"
- Long-form content (chapters, sections, drafts) that must satisfy multiple criteria
- Content that needs validation (fact-check, style, structure, length)

---

## Before Writing: Define Completion Conditions

**Required.** List explicit, checkable conditions before starting. Conditions must be:

- **Specific** — "Chapter covers X, Y, Z" not "chapter is good"
- **Verifiable** — Agent can check them (word count, checklist, tests)
- **Complete** — All must pass before stopping

Example conditions:

```
Conditions:
- [ ] Word count 1500 words
- [ ] All 5 key points from outline covered
- [ ] No passive voice in first 3 paragraphs
- [ ] Citations match research file
- [ ] Linter passes
```

---

## The Loop

1. **Write** — Produce or revise content toward the conditions.
2. **Check** — Evaluate against each condition (read, count, run tools).
3. **Feedback** — If any condition fails, capture what failed and why.
4. **Iterate** — Use feedback to fix. Repeat from step 1.
5. **Stop** — Only when all conditions pass, or a safety limit is hit.

---

## Four Pillars (Required for Success)

### 1. Clear, Detailed Spec

- Break the task into right-sized chunks (e.g., one section per loop).
- Describe the outcome in detail. Gaps invite wrong assumptions.
- Include constraints: tone, structure, sources, length.

### 2. Completion Communication

- Conditions must be **checkable** by the agent.
- After each iteration, explicitly state: which conditions pass, which fail.
- Do not declare "done" until every condition passes.

### 3. Context and Memory

- For long tasks, reset context between major sections to avoid drift.
- Keep a short "state" note: what’s done, what’s next, key decisions.
- Avoid summaries-of-summaries; prefer fresh context for new chunks.

### 4. Feedback Integration

- Feed failures back into the next prompt: "Condition X failed because…"
- Prefer structured feedback (e.g., "Missing: point 3 from outline") over raw dumps.
- Preserve the original spec as the stable goal; don’t let feedback overwrite it.

---

## Safety Limits

To avoid infinite or useless loops:

- **Max iterations** — Stop after N attempts (e.g., 5–10) and escalate.
- **Stagnation** — If the same error repeats 2+ times, stop and ask the user.
- **Scope** — If conditions are too broad, break the task into smaller pieces.

---

## Failure Modes to Avoid

| Failure | Cause | Fix |
|--------|-------|-----|
| Infinite loop | No firm stop condition | Define explicit, checkable conditions |
| Oscillation | Fix A breaks B, fix B breaks A | Broaden scope or simplify conditions |
| Context overload | Too much feedback in prompt | Summarize failures; reset context |
| Metric gaming | Agent optimizes for metric, not intent | Add conditions that reflect real quality |
| Hallucination | Wrong assumption becomes "fact" | Fix the spec and restart; don’t iterate on bad assumptions |

---

## Example Workflow

```
Task: Write section 2.1 of the book (800–1000 words).

Conditions:
- [ ] 1500 words
- [ ] Covers: definition, why it matters, one example
- [ ] Matches tone in section 1.1
- [ ] No undefined jargon

Iteration 1: Write draft → Check → 720 words, "definition" too vague.
Iteration 2: Expand definition, add example → Check → 950 words, "jargon" in para 2.
Iteration 3: Replace jargon → Check → All conditions pass. Stop.
```

---

## Summary

- Define **explicit, checkable** completion conditions before writing.
- Loop: write → check → feedback → iterate until all conditions pass.
- Use the four pillars: clear spec, completion communication, context management, feedback integration.
- Set safety limits and watch for stagnation or metric gaming.
- Stop only when every condition passes or a safety limit is reached.
