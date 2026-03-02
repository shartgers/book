# Review Report — Chapter 08 — Value, Capabilities, Trust

## Check 1 — Style

| Criterion | Status | Notes |
|-----------|--------|-------|
| Chapter template complete | PASS | All required elements present: strategic tension (The Thirty-One to Seven Problem), named framework (AI Decision Framework), case study (Allianz), governance implications (From Scorecard to Boardroom), reflection questions (5), closing transition (to Ch 9) |
| Paragraph length | FAIL | Several paragraphs exceed 4 lines: "Three structural errors recur" block (~10 sentences); case study strategic dilemma opening; decision context paragraphs; transferable lesson paragraphs. Fixed in final by splitting into shorter paragraphs. |
| Framework is named and numbered | PASS | The AI Decision Framework with three numbered elements: Value, Capabilities, Trust. Definition block present. |
| Framework is visualisable | PASS | Three-element model; image referenced (ch08-ai-decision-framework.png). Could be drawn as triangle, Venn, or radar. |
| Reflection questions | PASS | 5 questions, numbered, each prompting a specific board-level decision. |
| Word count | PASS | ~3,443 words (non-case-study: ~2,581; case study: ~862). Target ~3,600 at 8% of 45k. Slightly under; acceptable per TOC guidance. |
| No filler | PASS | Perplexity Gate cleaned all flagged categories. No residual filler phrases found. |
| No em dashes | PASS | Only em dash is in the case study heading ("Allianz — Turning…"), which is the permitted structural exception per chapter template. No em dashes in body text. |
| Footnotes correct | PASS | No footnotes in this chapter. No direct-expert sources requiring footnotes. |
| Footnotes log updated | PASS | No entries to add. Existing log at output/footnotes-log.md confirmed present with correct format. |
| Named models correct | PASS | "The AI Decision Framework" uses exact name and three elements (Value, Capabilities, Trust) from docs/instructions.md. Correctly stated as "not a layer of the AI Transformation Framework." References to AI Transformation Framework (Ch 5), 10/20/70 rule (Ch 1), tiered autonomy (Ch 3), and human-in-the-loop (Ch 3) all use correct names. |

**Style verdict: FAIL** (paragraph length)

---

## Check 2 — Character

| Criterion | Status | Notes |
|-----------|--------|-------|
| Tone | PASS | Strategic, calm, direct throughout. No hype ("The evidence on trust as a leading indicator is striking" is measured). No sales language. No academic jargon. |
| Concreteness | PASS | Claims grounded in specific evidence: ROI figures (31% → 7%), MIT 95%, Allianz 400 GenAI use cases, Project Nemo 80% reduction, EU AI Act penalties (€35M / 7% turnover), procurement cost reductions (27%), finance automation (90% reduction). |
| Honesty about limits | PASS | Explicit: "That 95% figure captures something important. It measured P&L impact of pilots at relatively short timescales, not long-term scaled deployments." Case study: "What remains uncertain deserves acknowledgement." |
| Reader respect | PASS | Written for capable executive. No hand-holding, no over-explanation. Assumes business literacy. |
| British English | PASS | Consistent: organisations, prioritisation, optimise, recognised, capitalise, behaviour. No American spellings found. |
| Preferred vocabulary | PASS | Uses: governance (throughout), framework (throughout), strategic (multiple), momentum (line 42), tangible, actionable. |
| No credential-leading | PASS | Substance carries weight. Expert quotes attributed but not credential-heavy. |

**Character verdict: PASS**

---

## Check 3 — Continuity

| Criterion | Status | Notes |
|-----------|--------|-------|
| Thesis advancement | PASS | Chapter directly addresses why European CEOs are underprepared: they lack a structured way to evaluate AI investments across value, capability readiness, and governance risk simultaneously. Provides the AI Decision Framework as the answer. |
| No duplicate frameworks | PASS | The AI Decision Framework (Value, Capabilities, Trust) is new in Ch 8. Previous named frameworks: Four Tiers (Ch 4), AI Transformation Framework (Ch 5). No overlap. |
| No duplicate case studies | PASS | Allianz is not the primary case study in any previous chapter. Ch 1 = Siemens, Ch 2 = DBS, Ch 3 = Klarna, Ch 4 = ING, Ch 5 = BBVA. Allianz appears as brief supporting reference in Ch 2 (Karuth-Zelle quote) and Ch 3 (Project Nemo mention, EU AI Pact), but never as the primary case study. |
| Transition coherence | PASS | Closing paragraph: "Chapter 9 makes the full case for why Europe's distinctive regulatory and cultural context is a strategic advantage, and what leaders must do to capitalise on it." Connects logically to Ch 9 (Europe's Distinctive Edge). |
| Argument progression | PASS | Builds on Ch 1 (95% failure rate, 10/20/70 rule), Ch 2 (domain leader role, board governance gap), Ch 3 (tiered autonomy, human-in-the-loop), Ch 5 (AI Transformation Framework). Not self-contained. |
| No concept re-introduction | FAIL | Four issues found: (1) Barbara Karuth-Zelle quote "Digital and AI transformations are not mainly about the technology but rather the mindset, the people, and the organisation" repeated verbatim from Ch 2 line 73; (2) "micro-productivity trap" re-explained with definition (already defined in Ch 1 line 61); (3) board governance statistics (66% of boards, 15% receive metrics, 88% use AI) re-presented as fresh findings, already introduced in Ch 1 lines 79–81 and referenced in Ch 2; (4) domain leader concept re-introduced without referencing Ch 2 where it was discussed extensively (lines 71, 93). Additionally, image path incorrect: `../images/` should be `../../../images/`. |

**Continuity verdict: FAIL**

---

## Overall: FAIL

Issues to resolve (all fixed in ch08-final.md):

1. **Paragraph length:** Break up all paragraphs exceeding 4 lines (opening "Three structural errors" block, case study strategic dilemma, decision context, transferable lesson paragraphs).
2. **Barbara Karuth-Zelle quote:** Replace verbatim repetition with back-reference to Ch 2: "Karuth-Zelle, whose conviction that transformation is about mindset, people, and organisation was noted in Chapter 2, shaped how Allianz approached its dilemma."
3. **Micro-productivity trap:** Replace re-definition with back-reference: "the micro-productivity trap identified in Chapter 1."
4. **Board governance statistics:** Add back-reference: "As Chapters 1 and 2 established, board oversight…" rather than re-presenting stats as new.
5. **Domain leader concept:** Add back-reference to Ch 2 discussion rather than re-introducing.
6. **Image path:** Corrected from `../images/ch08-ai-decision-framework.png` to `../../../images/ch08-ai-decision-framework.png`.
