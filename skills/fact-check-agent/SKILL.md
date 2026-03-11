---
name: fact-check-agent
description: Reviews a chapter or section line by line and adds missing footnote references and source citations. Use when asked to fact-check a chapter, add footnotes, verify citations, or identify claims that need sourcing.
---

# Fact-Check Agent

Review every sentence in the input text. Identify which sentences already have a footnote, which need one, and which do not need one. For every sentence that needs a new footnote, find the source and add both the inline reference and the footnote entry.

---

## Input

A full chapter or section of a chapter, provided by the user.

---

## Criteria for a footnote

A sentence **needs a footnote** if it contains any of the following:

- **Numbers or statistics** — percentages (`x%`), counts (`300 projects`, `758 consultants`), ratios, financial figures, or any quantified claim
- **Sweeping assertions** — phrases like "many organisations", "most leaders", "research shows", "studies confirm", "the evidence suggests", "the vast majority"
- **Named findings or reports** — any reference to a named study, survey, framework, or institution's conclusion

A sentence does **not** need a footnote if it:

- States a definition, analogy, or conceptual point with no empirical claim
- Refers to something already established earlier in the same chapter
- Is a rhetorical or structural sentence (transitions, questions, conclusions)

---

## Step 1 — Line-by-line audit

Go through the text **sentence by sentence**. For each sentence, assign one of three labels:

| Label | Meaning |
|-------|---------|
| `Yes already` | Sentence has an inline footnote reference (e.g. `[^16]`) — no action needed |
| `Yes need new` | Sentence meets the criteria above but has no footnote — must add one |
| `No` | Sentence does not meet the criteria — no footnote needed |

Only act on sentences labelled `Yes need new`.

---

## Step 2 — Find the source

For every `Yes need new` sentence, find the source using this priority order:

### 1. Search the Research folder first

List all files in `Research/` and read the most relevant ones. Search for the specific claim, statistic, or assertion in the text. Look for:

- The original report or survey name
- The publishing organisation (company, consultancy, academic body)
- The year of publication

Key files to check:

| File | Contents |
|------|----------|
| `Research/book-research-claude.md` | Main synthesis — statistics, quotes, named studies |
| `Research/BCG-Matt-Crop-Agentic-AI-Five-Insights.md` | BCG primary source on agentic AI |
| `Research/chapter-{nn}-web-research.md` | Web research specific to this chapter (if it exists) |
| Other files in `Research/` | Check all — new research files may have been added |

### 2. Web search if not found in Research folder

If the claim is not traceable to a specific source in `Research/`, run a targeted web search. Use specific queries, for example:

- `"61% AI use individual level" research report 2025`
- `"758 consultants AI study" BCG OR Harvard 2024`
- `"psychological safety AI adoption" Google research`

Prefer sources that are:
- Recent (2023–2026)
- Attributable to a named organisation or author
- Reports, surveys, academic papers, or executive publications

---

## Step 3 — Determine the next footnote number

Before adding any footnotes, find the highest existing footnote number in the chapter. The new footnotes must continue from that number in sequence.

For example, if the last existing footnote is `[^18]`, the next new footnote is `[^19]`.

---

## Step 4 — Add footnotes

For each `Yes need new` sentence:

1. **Add the inline reference** at the end of the sentence, before the full stop if possible, or immediately after it. Follow the same style as existing footnotes in the chapter.

   Example: `...only four emerge.[^19]`

2. **Add the footnote entry** to the footnote block at the bottom of the chapter, immediately after the last existing footnote.

### Footnote format

```
[^19]: Organisation name, "Report or Article Title", Year
```

Examples:

```
[^17]: Typeface, "Signal Report", 2025
[^18]: BCG, "The Widening AI Value Gap", October 2025
[^19]: Harvard Business School / BCG, "Navigating the Jagged Technological Frontier", 2023
[^20]: McKinsey, "The State of AI", 2024
```

Rules for the footnote entry:
- **Organisation or author name** first (short form: BCG, not Boston Consulting Group)
- **Title in double quotes** — use the exact report or article title
- **Year** at the end; add month if known and relevant
- If a person is quoted directly, format as: `Surname, "Article or publication", Year`
- Keep each entry on one line

---

## Step 5 — Output

### Chapter file

Produce the full revised chapter text with:

- All `Yes need new` sentences updated with their inline references
- The footnote block at the bottom updated with all new entries
- No other changes to the chapter text

Do **not** append the audit log to the chapter file.

### Audit log — book/footnotes-log.md

Write the audit log to `book/footnotes-log.md`. If the file already exists, append to the bottom. If it does not exist, create it with the heading `# Footnotes` at the top.

Use this format for each run:

```
## Fact-check audit — [Chapter title]

| Sentence (first 8 words) | Label | Action |
|--------------------------|-------|--------|
| "Research shows that 61% of AI use..." | Yes need new | Added [^19] — Typeface, Signal Report, 2025 |
| "Only a small minority qualify..." | Yes need new | Added [^20] — McKinsey, State of AI, 2024 |
| "This is not a failure of ambition..." | No | — |
| "...makes AI literacy a legal requirement..." | Yes already | [^16] present |

**Unverified claims:** [list any claims where no source was found, or "None"]
**Notes:** [any discrepancies, numbering warnings, or follow-up actions]
Source lookup: Research folder checked / Web search used for [list queries if any]
```

---

## Step 6 — Renumber footnotes (explicit request only)

Run this step only when the user specifically asks to renumber footnotes — for example, after fact-checking has added new entries that created gaps or conflicts with adjacent chapters.

### 6a — Find the correct starting number

1. List all chapter files in `book/` sorted by filename prefix (`ch01-…`, `ch02-…`, etc.).
2. Identify the chapter immediately before the one being renumbered.
3. Read that preceding chapter file. Find the **highest** `[^N]` number that appears anywhere in it (both inline references and footnote block definitions).
4. The first footnote in the current chapter must be that number + 1. Call this `START`.

If there is no preceding chapter (this is chapter 01), `START = 1`.

### 6b — Build the remapping table

1. Scan the current chapter top to bottom.
2. Collect every unique footnote number in the order each first appears as an **inline reference** in the body text (not from the footnote block). This determines the correct reading order.
3. Assign new sequential numbers beginning at `START`. Build a mapping table:

```
Old → New
[^13] → [^15]   (first inline ref found)
[^17] → [^16]   (second inline ref found)
[^19] → [^17]   (third inline ref found)
…
```

### 6c — Apply the remapping

Replace in the chapter file:

- Every inline `[^OLD]` in the body text → `[^NEW]`
- Every `[^OLD]:` definition line in the footnote block → `[^NEW]:`

Work from **highest old number to lowest** to avoid cascading substitution errors (e.g. replacing `[^1]` before `[^12]` would corrupt `[^12]`).

### 6d — Verify

After applying:

1. Confirm every inline `[^N]` in the body has a matching `[^N]:` definition.
2. Confirm the footnote numbers in the block are in ascending order with no gaps.
3. Confirm the last number used matches what a subsequent chapter would need to continue from

---

## Rules

- **Do not renumber unless explicitly asked.** During a normal fact-check run, only add new footnotes; never change existing numbers.
- **When renumbering, always build and show the remapping table first** before writing any changes to the file.
- **Never invent a source.** If you cannot find a credible source for a claim, label it `Unverified` in the audit log and add a note: `[Source not found — claim should be reviewed]` in a comment or the audit log. Do not create a footnote with a fabricated title.
- **Do not add footnotes to the case study section** unless a specific external statistic is cited. Case study narrative drawn from the chapter's own research does not need a footnote.
- **Do not footnote the "Questions for the Board" section.**
- **Do not footnote the case study section**
- **Prefer the Research folder** over web search. Only web search when the claim is not traceable from existing files.
- **One footnote per sentence** is usually enough. If two distinct claims in a single sentence each need a source, use the most significant one.
- **Skip a footnote when it's a duplicate**. If it is the same as the previous footnote. This usually means the citation is from the same report. 
