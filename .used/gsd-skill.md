# Phase 1 Plan — Jira Export Feature
**Status:** pending
**Phase Goal:** Users can export a FluidSpecs spec document to a Jira-compatible format

---

## Wave 1 (sequential — blocking)

### Task 1.1 — Define Jira Export Schema
**Type:** auto
**Files:** src/lib/exporters/jira-schema.ts
**Action:**
Research Jira's issue import format (CSV and JSON).
Define TypeScript types for JiraIssue, JiraEpic, and JiraSubtask.
Map FluidSpecs spec sections to Jira issue types.
**Verify:** `npx tsc --noEmit` passes with no errors on new types
**Done:** Types exported from jira-schema.ts, no TS errors

---

## Wave 2 (parallel — independent)

### Task 1.2 — Build Export Transformer
**Type:** auto
**Files:** src/lib/exporters/jira-transformer.ts, src/lib/exporters/jira-transformer.test.ts
**Action:**
Write a pure function `transformSpecToJira(spec: FluidSpec): JiraIssue[]`.
Write unit tests covering: empty spec, single user story, nested acceptance criteria.
**Verify:** `npm test -- jira-transformer` passes
**Done:** All tests green, function handles edge cases

### Task 1.3 — Add Export Button to UI
**Type:** auto
**Files:** src/components/SpecToolbar.tsx
**Action:**
Add "Export to Jira" button to SpecToolbar.
On click: call transformer, trigger CSV download.
Button disabled if spec is empty.
**Verify:** Manual check — button appears, clicking downloads file
**Done:** Export button visible, download works with sample spec

---

## Wave 3 (depends on 1.2 + 1.3)

### Task 1.4 — Integration Test + Docs
**Type:** auto
**Files:** src/lib/exporters/jira.integration.test.ts, docs/jira-export.md
**Action:**
Write end-to-end test: load fixture spec → transform → validate CSV structure.
Write brief user-facing docs for the export feature.
**Verify:** Integration test passes, docs file exists
**Done:** All tests pass, README updated with link to docs

---

## Verification Checklist
- [ ] Can a user click Export on a spec and get a downloaded file?
- [ ] Does the CSV import cleanly into a fresh Jira project?
- [ ] Are all TS types strict (no `any`)?
- [ ] Test coverage >80% on transformer logic?