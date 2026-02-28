# Brand Voice

This document describes the tone, style, and conventions used across this project's contributions—directives, prompts, documentation, and code comments. Use it to keep new content consistent.

---

## Summary

**Voice in one line:** Clear, pragmatic, and instructional—like well-written SOPs for a capable teammate.

---

## Core Principles

### 1. Direct and pragmatic

- Say what something does and why it matters. Avoid filler.
- Prefer short sentences. One idea per sentence when it helps clarity.
- Examples from the repo: *"Be pragmatic. Be reliable. Self-anneal."* / *"You're the glue between intent and execution."*

### 2. Structured and scannable

- Use a consistent layout: **Goal** → **Inputs** → **Steps/Tools** → **Output** (and **Edge cases** when relevant).
- Use numbered steps for sequences, bullets for options or lists.
- Use headings and bold labels so readers can jump to what they need.

### 3. Honest about status and limits

- Be explicit about what works, what’s optional, and what’s not implemented.
- Use clear status language (e.g. ✅ Complete, ⚠️ Pending, ❌ Not implemented) where it helps.
- Don’t oversell; document limitations and known issues in the same place as the feature.

### 4. Instructional, not decorative

- Write like instructions for a mid-level teammate: clear goals, clear steps, clear constraints.
- Explain *why* when it prevents mistakes or wrong assumptions (e.g. "90% accuracy per step → 59% over 5 steps; push complexity into deterministic code").
- No marketing fluff in directives or prompts.

### 5. Rule-oriented where it matters

- When behavior must be strict, state it as rules: **RULES**, **CRITICAL**, **Do NOT**.
- Use blockquotes or callouts for non-negotiable behavior (e.g. manual review gates, output format).
- Keep rules short and actionable.

### 6. Living documents

- Directives and key docs improve over time. Treat them as updated when we learn (API limits, errors, better flows).
- Preserve intent: improve and clarify, don’t overwrite or discard without asking.

### 7. Human-in-the-loop as a feature

- Manual steps (e.g. review → ready) are intentional. Describe them as design choices, not workarounds.
- Use phrases like "intentional manual gate" and "features, not bugs" when explaining why automation stops for human approval.
- Don’t suggest or implement bypasses of approval steps without explicit user agreement.

### 8. Errors as learning

- Frame failures as chances to improve the system: fix → test → update directive → stronger system.
- Use the "self-annealing" idea: read errors, fix the tool, document the lesson.

---

## Terminology

Use these terms consistently:

| Concept | Preferred term | Avoid |
|--------|-----------------|--------|
| High-level procedures | Directives, SOPs | "docs", "instructions" (when referring to directives) |
| Who runs the workflow | Orchestration, agent | — |
| Scripts that do the work | Execution, execution scripts | "scripts" alone when context is execution layer |
| Collecting ideas | Harvest, harvesting | Scrape, collect (unless referring to a specific script name) |
| Generated post text | Draft, draft post | Post (until it’s published) |
| Workflow state | status = "new" / "review" / "ready" / "posted" | Mixed case or different wording |
| Improving after failure | Self-anneal, self-annealing | "fix and document" (ok in prose, but keep the concept) |
| Human approval step | Manual gate, review gate | "manual step" (ok) but "bug" or "missing automation" (wrong) |

---

## Formatting Conventions

- **Directives:** Goal at top, then Inputs, Steps (with **Tool** and **Action**), Output, then Edge cases / Known issues.
- **Prompts:** Clear role/task, then bullet rules, then **CRITICAL** or **RULES** for output format (e.g. "Output ONLY…", "Do NOT…").
- **Docs:** Short intro, then sections with headings. Use code blocks for commands and examples.
- **Code comments:** Explain *why* or *what* at module/function level; keep comments in short sentences.

---

## What to avoid

- Long preambles before the main instruction or answer.
- Vague weasel words ("might", "could consider") when a rule or decision is fixed.
- Treating "no items to process" or "no ready drafts" as a bug when it’s the expected result of a manual gate.
- Changing workflow logic to skip manual approval without explicit user request.
- Deleting or overwriting directives without asking.

---

## Audience

Primary audience: maintainers and AI agents working in the repo. Secondary: anyone reading directives or running scripts. Write so that both can follow steps and understand intent without extra context.

---

*This brand voice is derived from existing contributions (directives, prompts, CLAUDE.md, PROJECT_ANALYSIS.md, implementation plan, and execution script docstrings). Update this file when the project’s voice evolves.*
