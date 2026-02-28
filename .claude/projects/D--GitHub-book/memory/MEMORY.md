# Project Memory — book (D:\GitHub\book)

## User Preferences

- **Plans go in the project folder:** Always write plan files to `D:\GitHub\book\plan\` (not the hidden `.claude/plans/` folder). Use descriptive filenames like `plan/agent-team-plan.md`.
- **Stop between chapters:** User reviews each chapter before continuing. Do not auto-start the next chapter — wait for explicit instruction.

## Output File Structure

Each chapter has its own folder:
- `output/chapters/chapter-{nn}/ch{nn}-beats.md`
- `output/chapters/chapter-{nn}/ch{nn}-research-brief.md`
- `output/chapters/chapter-{nn}/ch{nn}-draft.md`
- `output/chapters/chapter-{nn}/ch{nn}-draft-pg.md`
- `output/chapters/chapter-{nn}/ch{nn}-review.md`
- `output/chapters/chapter-{nn}/ch{nn}-final.md`
- `output/chapters/chapter-{nn}/ch{nn}-case-study.md` (standalone copy, Case Study Agent)

This convention is set in all skill files, CLAUDE.md, docs/agent-handoff-protocol.md, and plan/plan.md.

## Current Book State (end of session 2026-02-27)

- **Phase 0:** Complete — title, TOC, hooks all done
- **Chapter 01:** Complete — all 6 tasks done, files in `output/chapters/chapter-01/`
  - Framework: Paradigm Shift Curve (3 phases)
  - Case study: DBS Bank
  - Diagram placeholder present (GenerateImage unavailable during writing)
- **Chapter 02:** Next — Leadership Is Not Optional

## Multi-Agent Pipeline Notes

- Wave 2 runs Writer and Case Study Agent in parallel; Case Study Agent must wait for the draft file to exist before merging
- Reviewers agent auto-updates plan/plan.md checkboxes on completion — do not duplicate
- Review FAIL that is resolved before ch{nn}-final.md is written counts as effectively PASS for gate purposes
- The orchestrator-agent SKILL.md is the authoritative source for wave prompt templates
