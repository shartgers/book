---
name: rewrite-no-numbers
description: Rewrites a paragraph full of facts and research reference numbers to remove the numbers while maintaining the original narrative build-up, logic, and story.
---

# Rewrite Without Numbers Skill

## Purpose
This skill takes a text or paragraph that contains many statistics, data points, or research reference numbers and rewrites it to be more readable and narrative-driven. It completely removes the specific numbers and research references, while keeping the fundamental logic, build-up, and story intact.

## Instructions

1. **Analyze the Core Message:** Read the input paragraph to understand the underlying story, narrative build-up, and the main point the data is trying to support.
2. **Abstract the Data:** Identify all statistics, percentages, and specific research references. Abstract these into qualitative, descriptive statements (e.g., "a significant increase", "rapid improvement", "better performance").
3. **Consolidate Redundant Logic:** Often, multiple data points point to the exact same logical conclusion. Instead of listing them all qualitatively, consolidate them into a single, strong statement that captures the essence of the finding. Facts can be dropped if they are redundant to the main point.
4. **Maintain the Narrative Arc:** Keep the same build-up, tension, and resolution as the original text. The "story" should remain the same even if the specific facts are generalized.
5. **Focus on Readability:** The final rewritten paragraph should be highly engaging, smooth, and easy to read without bogging the reader down in numerical details or specific research citations.

## Writing Rules (Writer Agent Alignment)

- **No em dashes:** Use commas, colons, or rephrase.
- **Short paragraphs:** 3–4 lines maximum.
- **One idea per sentence.**
- **No preamble:** Get straight to the point.
- **No hype:** No marketing language, no filler.
- **British English:** colour, organise, behaviour, whilst, towards, focussed.
- **Tone:** Strategic, calm, direct.
- **Preferred vocabulary:** clarity, coherence, momentum, governance, framework, strategic, tangible, actionable.
- **No weasel words:** Avoid "might", "could", "perhaps" when stating a rule or fixed finding.
- **Inclusive leadership:** Prefer "leaders", "managers", or "boards".

## Quality Check (Reviewers Agent Alignment)

| Criterion | Pass condition |
|-----------|---------------|
| Paragraph length | 3–4 lines maximum |
| No filler | No "it is important to note", "in today's world", etc. |
| No em dashes | None used |
| Tone | Strategic, calm, direct — not hyped |
| Concreteness | Claims are grounded in logic; no vague assertions |
| British English | Consistent spelling and vocabulary |
| No Numbers | Ensure NO statistics, percentages, or reference numbers remain |

## Example

### Input Text
The gains are real, and they are seductive. A customer support study across more than 5,000 agents at a Fortune 500 firm found a 14% average productivity increase, with novice workers improving by 34%. Workers with two months of AI experience performed as well as colleagues with six months of experience without AI. Manager escalations declined by 25%. Results like these generate genuine excitement, and that excitement can obscure a structural problem.

### Output Text
The gains are real, and they are seductive. When large organisations deploy these tools in customer support, they see immediate and widespread productivity leaps. The most dramatic improvements happen among the newest employees, who rapidly match the performance of far more experienced colleagues. At the same time, problems requiring management intervention drop significantly. Results like these generate genuine excitement, and that excitement can obscure a structural problem.
