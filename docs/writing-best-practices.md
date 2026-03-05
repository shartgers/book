# Book Best Practices

Guidelines for writing a strategic, high-quality business book aimed at executive audiences.

---

## Audience & Tone

- **Target readers:** Leaders, managers, board members, executive teams, supervisory boards
- **Tone:** Strategic, reflective, independent, calm, non-hyped
- **Thesis required:** Every book must have a clear central argument
- **Single unifying idea:** One core idea that ties the book together
- **No marketing language:** Avoid promotional or sales-oriented phrasing

---

## Structure

### Section Flow

1. **Problem Definition**
2. **Core Frameworks**
3. **Integration**
4. **Practical Application**

### Chapter Count

- **3–6 chapters** per framework section

---

## Chapter Template

**Chapter opening:** Do not start the chapter draft with a level-1 heading (e.g. `# Chapter 1: Title`). The print build adds the chapter number and title in the layout. Start the draft with the first section heading; use the **Section heading** from the beat sheet for each section (section names are set by the Planner, not fixed labels).

Each chapter must include:

- Strategic tension
- Clear principle
- Named framework (optional — only substance chapters, e.g. key 3 or 5 elements, model, playbook; introduction and some opening or closing chapters stay readable without a framework)
- Structured case study
- Governance implications
- Executive reflection questions

---

## Content Ratio

Balance content types as follows:

| Type            | Share |
|-----------------|-------|
| Conceptual      | 40%  |
| Case studies    | 30%  |
| Research        | 15%  |
| Anecdotes       | 10%  |
| Practical tools | 5%   |

---

## Case Studies

### Must Include

- Strategic dilemma
- Decision context
- Trade-offs
- Outcome
- Transferable lesson

### Avoid

- Hero narratives
- Unverifiable claims
- Superficial company mentions

---

## Writing Principles

- **No em dashes:** Never use em dashes (—). They read as AI-generated. Use commas, colons, or rephrase instead.
- **Short paragraphs** — Keep paragraphs concise
- **Define terms explicitly** — Don’t assume reader familiarity
- **Avoid buzzwords** — Use plain, precise language
- **Use inclusive leadership references** — Prefer terms like leaders, managers, or boards. Use CEO only when a source, case, or context specifically requires it.
- **Acknowledge uncertainty** — Don’t oversimplify complex topics
- **Explicit trade-offs** — Show both benefits and costs of choices
- **No excess autobiography** — Focus on ideas, not personal story

---

## Definition Blocks

When a key term is introduced for the first time in the text, follow it with a **definition block**. This gives the reader a clear, styled reference they can return to.

### Format

Use a blockquote with a bold `Definition:` label on the first line. Keep the definition to 2–4 sentences. Write it as if the reader has never encountered the term before.

```markdown
> **Definition: The Agentic Employee**
>
> An agentic employee is a person who works alongside autonomous AI agents as teammates. They orchestrate rather than execute, create reusable AI workflows, and exercise judgment at the right moments. The best agentic employees build skills and share them, creating a compounding network effect across the organisation.
```

### Rules

- **One definition block per term, per book.** Define a term the first time it appears. Do not repeat the block in later chapters.
- **Place immediately after introduction.** The block goes right after the paragraph that first uses the term in context.
- **Keep it self-contained.** A reader should understand the definition without reading the surrounding paragraph.
- **British English.** Same rules as all other prose.
- **No jargon inside a definition.** If a definition needs another defined term, use plain language and add "(see Chapter X)" if needed.

### Term consistency: Agentic Organisation

**Use "Agentic Organisation" (capitalised) as the single defined concept for the book.** Do not use "Agentic Enterprise" for this concept. The book title is *The Agentic Organisation*; the definition block in Chapter 1 uses "The Agentic Organisation." In running prose you may use the words "organisation" or "enterprise" freely (e.g. "organisations must redesign roles," "enterprise-wide transformation"); only the defined, capitalised concept is always **Agentic Organisation**. When citing external sources, keep their wording (e.g. McKinsey's "The Agentic Organization").

### Key Terms Requiring Definition Blocks

This is the running list of terms that must receive a definition block when first introduced. Writers should check this list before drafting.

| Term | Likely first appears in |
|------|------------------------|
| The Agentic Organisation | Chapter 1 or 3 |
| The agentic employee | Chapter 3 |
| AI agent | Chapter 1 or 3 |
| The AI Transformation Framework (Product, People, Process, Technology, Data) | Chapter 5 (exact name and elements in `docs/instructions.md`) |
| A skill (reusable AI workflow) | Chapter 3 or 4 |
| Agentic AI | Chapter 1 |
| The four tiers of transformation | Chapter 4 (see The Four Tiers of Transformation in `docs/instructions.md`) |
| Value, Capabilities, Trust (framework) | Chapter 8 (see The AI Decision Framework in `docs/instructions.md`) |
| Human-in-the-loop | Chapter 3 |
| Human-agent collaboration | Chapter 6 |
| Tiered autonomy | Chapter 8 or 13 |
| Pilot purgatory | Chapter 13 |

Add new terms to this table as the book develops.

### Tables

Use standard Markdown pipe tables (header row, separator row, then data rows). Borders, header background, and cell padding are applied automatically by the format-book build (PDF, HTML, EPUB). Do not add HTML or inline styles for table appearance.

---

## Footnotes

Footnotes credit direct sources — consultants, practitioners, or named experts — when their specific expertise or testimony is drawn upon. They are not used for general citations or academic referencing.

### When to Use a Footnote

Use a footnote when:

- A named consultant, expert, or practitioner contributed a specific insight, framework, or finding that is reproduced or closely paraphrased
- The source is a direct voice (interview, commissioned report, advisory input) rather than a published book or article
- Attribution materially adds credibility or context for the reader

Do not use footnotes for:

- General research statistics or data (cite inline or in the research brief)
- Published books, studies, or reports (reference these in the body text where needed)
- Author's own analysis or conclusions

### Density

Aim for no more than two footnotes per page. This is a guide for balance, not a hard limit or a target to hit. The goal is to draw on external expertise where it genuinely strengthens the argument, whilst ensuring the book's own perspective and voice remain primary.

### Format

Use standard numeric superscript footnotes inline: `word or phrase¹`. Place footnote text at the bottom of the relevant page in the final layout.

```markdown
...as one senior CHRO noted during fieldwork.¹

---
¹ Interview with [Name], [Title], [Organisation], [Year].
```

If the source prefers anonymity, use: `¹ Senior CHRO, European financial services firm, 2024.`

### End-of-Book Footnote Log

All footnotes are collected into a single log at the end of the book, positioned **before the "About the Author" section**. The file is a clean reference for the print build: one title and one numbered list.

**File format:** `output/footnotes-log.md` contains only:
- A single heading: `# Footnotes`
- A single numbered list of all footnotes (e.g. `1. Interview with [Name], [Title], [Organisation], [Year].`)

No per-chapter headings, no explanatory text (e.g. "No direct expert footnotes in this chapter"), and no other sections.

**Writing Agent responsibility:** After completing each chapter draft, **append** this chapter's footnotes to `output/footnotes-log.md` as the next numbered list items. Continue the numbering from the last existing entry (e.g. if the file already has 1–3, add 4., 5., …). If the file is missing or has no list yet, ensure it starts with `# Footnotes` then a blank line, then the numbered list. Do not add a chapter heading or any "no footnotes" entry; if the chapter has no direct-expert footnotes, do not append anything. Do not consolidate or reformat existing entries.

---

## Quality Checks

Before finalizing, verify:

- [ ] Each framework (when present) can be visualized (diagram, model, etc.)
- [ ] Each claim has supporting evidence
- [ ] No duplicate or overlapping models; named models use exact names and elements from `docs/instructions.md`
- [ ] Thesis is reinforced in the conclusion
