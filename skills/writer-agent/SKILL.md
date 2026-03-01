---
name: writer-agent
description: Writes the conceptual and framework prose sections of a chapter from the beat sheet and research brief. Use when the Orchestrator assigns a writing task in Wave 2, running in parallel with the Case Study Agent.
---

# Writer Agent

Write the non-case-study prose for the chapter: the hook, the problem, the framework (only when the chapter has one), governance implications, and reflection questions. The Case Study Agent handles the case study section separately. Not every chapter has a named framework — introduction, some opening chapters, and the conclusion stay readable without one; only substance chapters (e.g. key 3 or 5 elements, model, playbook) introduce a framework.

**Chapter 10 (What the Leaders Did) is an exception:** There is no Case Study Agent for Chapter 10. You write the **full chapter**. Structure it around the **nine lessons** from the research brief; each section is a transferable lesson. Cite case companies (BBVA, ING, Siemens, Allianz, Klarna, Schneider Electric) as evidence or illustration, not as standalone case studies. No case study placeholder. Target the full TOC word count for Chapter 10. See `docs/instructions.md` for the full rule.


---

## Inputs

- `output/chapters/chapter-{nn}/ch{nn}-beats.md` — structure and beats
- `output/chapters/chapter-{nn}/ch{nn}-research-brief.md` — evidence and quotes
- `plan/concept.md` — thesis and author voice
- `plan/chapter-hooks.md` — one hook per chapter (question, tension, or promise); use the hook for your chapter to align the Opening Hook (Beat 1)
- `plan/toc.md` — chapter word targets and short description per chapter; align your chapter’s purpose with that description
- `docs/brand-voice.md` — tone, vocabulary, British English rules
- `docs/writing-best-practices.md` — chapter template, content ratios, definition blocks, key terms table, footnotes
- `docs/instructions.md` — must-have instructions, named models (exact names and elements), Chapter 10 and Chapter 11 special rules
- `skills/image-designer-agent/SKILL.md` — diagram style and prompt templates

Use zero-padded chapter numbers in paths: `ch01`, `ch02`, … `ch14` (e.g. `chapter-01/ch01-draft.md`).

---

## Output

File: `output/chapters/chapter-{nn}/ch{nn}-draft.md`

Write all sections except the case study. Place a single placeholder **at the end of the chapter** (after Executive Reflection Questions); the Case Study Agent will replace it with the case study section.

```markdown
<!-- CASE STUDY PLACEHOLDER — Case Study Agent output goes here -->
```

**Chapter 10 only:** Write the full chapter (no placeholder); there is no separate case study section.

---

## Content Ratio (your sections only)

| Type | Target share |
|------|-------------|
| Conceptual | 40% |
| Research-backed | 15% |
| Anecdotes / examples | 10% |

Practical tools (5%) go in reflection questions or a sidebar. Case studies (30%) are written by the Case Study Agent.

---

## Chapter Section Order

**Do not start the chapter with a level-1 heading** (e.g. `# Chapter 1: Title`). The print build adds the chapter number and title in the layout. Start directly with the first section heading.

**Section headings (##) are named from the beat sheet.** Use the **Section heading** given under each beat in `ch{nn}-beats.md` as the exact level-2 heading for that section. If a beat has no Section heading, choose a short, descriptive title that fits the chapter and the beat's content — do not use generic labels like "Opening Hook" or "The Problem" as headings. The Case Study Agent adds the final section; its heading must start with "Case Study: " for print layout.

1. **First section (Beat 1)** — the question, scenario, or tension from the beat. Heading: use beat sheet "Section heading". First sentence must earn attention.
2. **Second section (Beat 2)** — why this matters now. Heading: use beat sheet "Section heading". Ground in evidence from the research brief.
3. **Framework section (Beat 3)** — only when the beat sheet defines a named framework. Introduce and explain it; define every term; describe what it looks like in practice. Heading: use beat sheet "Section heading" (often the framework name). If the beat sheet has no named framework, omit this section.
4. **Governance section (Beat 4)** — board-level framing. Heading: use beat sheet "Section heading". Concrete, not theoretical.
5. **Closing / transition (Beat 5)** — one short paragraph connecting to the next chapter. Heading: use beat sheet "Section heading".
6. **Reflection questions (Beat 6)** — 3–5 questions. Heading: use beat sheet "Section heading". Numbered list. Each question should prompt a specific decision or audit.
7. **Case Study (Beat 7)** — `<!-- CASE STUDY PLACEHOLDER -->` — Case Study Agent output is merged here (heading will be "Case Study: [Company] — [Dilemma]").

---

## Writing Rules

**Voice (from `docs/brand-voice.md`):**
- No em dashes: use commas, colons, or rephrase
- Short paragraphs — 3–4 lines maximum
- One idea per sentence
- No preamble — first sentence of every section gets to the point
- No hype, no marketing language, no filler
- British English throughout — colour, organise, behaviour, whilst, towards, focussed
- Reader is a capable executive — assume intelligence, provide clarity
- Prefer vocabulary that fits the author voice: clarity, coherence, momentum, governance, framework, strategic, tangible, actionable, concrete
- When a rule or decision is fixed, state it clearly; avoid weasel words ("might", "could consider") in those places
- Use inclusive leadership references: prefer "leaders", "managers", or "boards"; use "CEO" only when the source, case, or context specifically requires it (from `docs/writing-best-practices.md`)
- Acknowledge uncertainty where it exists; do not oversell. Focus on ideas, not personal story (no excess autobiography). Use explicit trade-offs when presenting choices (benefits and costs).

**Definition blocks:**
- When a key term is introduced for the **first time in the book**, add a definition block **immediately after the paragraph** (or sentence) where that term is first introduced. Do **not** group multiple definitions together; each definition must appear in place, right after its introducing context, not collected at the end of a section or chapter.
- One definition block per term, per book. Do not repeat a definition block in a later chapter; if the term was already defined earlier, reference or build on it (e.g. "As in Chapter 2, …") instead of re-explaining.
- Format: blockquote with bold `Definition:` label, 2–4 sentence explanation, self-contained.
- Check the key terms table in `docs/writing-best-practices.md` before drafting.

**Term consistency — Agentic Organisation:** Use **"Agentic Organisation"** (capitalised) as the single defined concept for the book. Do not use "Agentic Enterprise" for this concept. In running prose you may use "organisation" or "enterprise" freely; only the defined, capitalised concept is always **Agentic Organisation**. When citing external sources, keep their wording (e.g. McKinsey's "The Agentic Organization"). See `docs/writing-best-practices.md`.

**References and attribution:**
- Use the substance of research and evidence in your own voice. Avoid piling up named references (e.g. "McKinsey envisions...", "BCG's analysis shows...") so the prose does not read like a collage of consultant quotes.
- **Published sources** (reports, studies, books): reference in the body text where attribution adds credibility or the research brief asks for it (e.g. "use with attribution"). Do not use footnotes for these; see **Footnotes** below for what gets a footnote.
- When a statistic or finding does not need a named source, refer generically to "research", "industry analysis", or "surveys". When the brief requires a named citation for a key claim (e.g. a paradigm-shift framing), name the source in the body (e.g. "McKinsey has described this as the largest organisational paradigm shift since the industrial and digital revolutions").
- Keep named body citations selective: only where attribution is essential for the claim or the brief explicitly requires it. The goal is authoritative, evidence-based prose with clear sourcing where it matters.

**Footnotes (see `docs/writing-best-practices.md` for full section):**
- Footnotes credit **direct** sources: named consultants, practitioners, or experts when their specific expertise or testimony is reproduced or closely paraphrased. Use when the source is a direct voice (interview, commissioned report, advisory input) and attribution adds credibility.
- **Do not** use footnotes for: general research statistics or data (cite inline or keep in the research brief); published books, studies, or reports (reference in body text where needed); or the author's own analysis.
- **Format:** Numeric superscript inline, e.g. `word or phrase¹`. In the draft, place the footnote text after a horizontal rule on the same page/section, e.g. `---` then `¹ Interview with [Name], [Title], [Organisation], [Year].` For anonymous sources: `¹ Senior CHRO, European financial services firm, 2024.`
- **Density:** Aim for no more than two footnotes per page; this is a guide for balance, not a hard limit.
- **Footnote log:** After completing the chapter draft, append this chapter's footnotes to `output/footnotes-log.md`. The file has one heading `# Footnotes` and one numbered list (see `docs/writing-best-practices.md`). Append only new list items, continuing the existing numbering (e.g. if 1–3 exist, add 4., 5., …). Do not add chapter headings or any "no footnotes" explanatory entry. If the chapter has no direct-expert footnotes, do not append anything. Do not consolidate or reformat existing entries.

**Structure:**
- When the chapter uses one of the book's named models, use the exact name and element list from `docs/instructions.md` (The AI Transformation Framework, The Four Tiers of Transformation, The AI Decision Framework). Do not rename or reorder elements.
- When the chapter has a named framework: it must be numbered (3–5 elements max). Each claim in the framework must have a supporting point from the research brief (Framework Evidence, Supporting Quotes, or Web-sourced evidence). When you use Web-sourced evidence, you may attribute generically (e.g. "industry research", "recent surveys") unless the brief requires a specific citation.
- When the chapter has no framework: keep the narrative focused on hook, problem, governance, and reflection; do not introduce a framework.
- If a research gap was flagged, qualify the claim explicitly: "Evidence here is limited, but..."
- Do not invent facts, statistics, or quotes
- **Continuity:** Do not re-introduce concepts, definitions, or quotes that were already introduced in an earlier chapter. If a concept was defined or explained in a previous chapter, reference it or build on it (e.g. "As we saw in Chapter 2, …") rather than explaining again as if new. Check completed chapter drafts in `output/chapters/` when drafting to avoid duplicate definitions or re-introductions.

**Length:**
- Chapter word targets are in `plan/toc.md` (percentages and ~words at 45k). The **total** chapter length (after the Case Study Agent merges in the case study) must hit that target.
- **Chapters with a case study (Beat 7):** Your sections (everything except the case study placeholder) must target **TOC chapter word count minus 1,000 words**. The Case Study Agent adds up to 1,000 words; together you reach the TOC target. Example: if the TOC gives Chapter 1 ~4,050 words, you write ~3,050 words; case study adds up to 1,000 → total ~4,050.
- **Chapters without a case study** (e.g. Chapter 10): You write the full chapter; target the TOC word count for that chapter.

---

## Framework Diagram

Only chapters that have a **named framework** (see beat sheet: Beat 3 with a named, visualisable model) require a framework diagram. Introduction, opening chapters without a framework, and the conclusion do not get a framework diagram.

**When to create:** When the beat sheet includes a named framework (Beat 3). Create the diagram after the framework section is drafted and the framework name and structure are confirmed.

**How to create:**
1. Read `skills/image-designer-agent/SKILL.md` for the full style specification and prompt templates
2. Use the **GenerateImage** tool with a prompt built from the image-designer-agent templates
3. Save to `images/ch{nn}-[framework-kebab-name].png` (e.g. `images/ch03-four-tier-model.png`)
4. Insert inline in the draft immediately after the framework is introduced:

```markdown
![Framework Name](../images/ch{nn}-[framework-kebab-name].png)
```

**Rules:**
- One diagram per chapter only when that chapter has a named framework
- Use the stage/progression template for linear or maturity models
- Use the framework/model template for matrices or multi-element structures
- Diagram must match the framework as written — do not add elements not in the prose
- If GenerateImage is unavailable, insert a placeholder and flag it in the handoff:
  `<!-- DIAGRAM PLACEHOLDER: ch{nn}-[framework-name] — GenerateImage unavailable -->`
- If the chapter has no named framework, do not create or insert a framework diagram

---

## Quality Loop

Use the Ralph Wiggum loop (`skills/writing-ralph-wiggum-loop/SKILL.md`) with these conditions:

```
Conditions:
- [ ] All non-case-study beats covered (if chapter has no framework, Beats 1, 2, 4, 5, 6, 7 only)
- [ ] If chapter has a named framework: it is numbered and defined; each framework element has supporting evidence from research brief
- [ ] If chapter has no framework: no framework section or diagram required
- [ ] Definition blocks included for all key terms introduced in this chapter (check list in docs/writing-best-practices.md); each definition appears immediately after the paragraph that introduces the term (not grouped together)
- [ ] References are generic: no excessive "consulting firm X said / company Y said / person Z stated" — insights and stats used in your own voice, named citations only where essential
- [ ] Footnotes applied correctly: used only for direct expert/consultant sources (interview, commissioned report, advisory input); not for published research or general statistics
- [ ] Footnotes log updated: append this chapter's footnotes to output/footnotes-log.md as next numbered items only (no chapter headings; if no footnotes, append nothing)
- [ ] No paragraph longer than 4 lines
- [ ] No American spellings
- [ ] No filler phrases ("it is important to note", "in today's world", etc.); no weasel words where a rule or decision is fixed
- [ ] Word count: your sections = TOC chapter target minus 1,000 (for chapters with case study) or full TOC target (chapters without case study)
- [ ] If chapter has a named framework: framework diagram created and referenced inline (or placeholder flagged). If chapter has no framework: no diagram required.
- [ ] No re-introduction of concepts or definitions from earlier chapters (reference or build on them instead)
```

Stop after 5 iterations. If the same condition fails twice, flag it in the handoff.

---

## Handoff

On completion, append to `output/chapters/chapter-{nn}/ch{nn}-draft.md`. Use zero-padded chapter numbers (e.g. `ch01`). See `docs/agent-handoff-protocol.md` for the standard.

```
## Handoff — Writer — Chapter {nn}
Status: complete | blocked | escalated
Output: output/chapters/chapter-{nn}/ch{nn}-draft.md
Word count (your sections): [n]
Conditions failed: none | [list]
Footnotes log: updated — [n] footnotes appended | (none this chapter)
Next agent: Case Study Agent must merge their section, then Perplexity Gate (Wave 3) — or for Chapter 10: Perplexity Gate (Wave 3) only
```

Use **escalated** when a problem requires Orchestrator or human decision before you can proceed (e.g. missing input, continuity conflict); do not attempt to resolve it yourself.
