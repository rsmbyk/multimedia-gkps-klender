# Analysis: Verse modal header draws one rule

**Date**: 2026-11-23 · **Gate**: opens at zero CRITICAL and 100% coverage.

**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `7dba5aa0d074` |
| `plan.md` | `9881f55df54b` |
| `research.md` | `69eaf8de15d1` |
| `data-model.md` | `ca78fe9f6dec` |
| `contracts/none.md` | `6d181f25e391` |
| `quickstart.md` | `1a23ff85e629` |
| `tasks.md` | `80c25e8f504b` |
| `checklists/requirements.md` | `654f0805c594` |

**Metrics**: 6 requirements · 3 success criteria · 7 story scenarios · 2 edge cases (16 traceability
rows) · 12 tasks, seven of them test work · coverage **16/16 = 100%** · CRITICAL **0**.

Coverage is read from the plan's traceability table, not re-derived from tasks: every `FR-###`,
`SC-###` and `US1 ACn` has a row. No mechanical fix was needed, so there is no before/after delta.

## Findings

| # | Class | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | low | The E2E asserts a 16–17px title-to-rule gap rather than the literal 16.5px, because the line box of the 21px face can differ by a fraction across renderers. | Accepted — the requirement is the other editors' rhythm (16px), not a fixed coordinate. The spec records 16.5px as the measured candidate. |
| F2 | low | `FR-004` and `SC-003` are inspected from the selector scope: both changed selectors require `[data-editor-size="large"]`. | Accepted — the non-verse dialog also has a characterisation E2E (T007), so the inspection row is backed by a browser check. |
| F3 | note | `reading/R54` is provisional until Fold; a sibling slice can claim the number while this pack is open. | Recorded — re-check `### R<n>` on `origin/develop` before the delivery commit and renumber if taken. |
| F4 | note | `CONSTITUTION.md` does not exist, so Plan's Constitution Check is a no-op. | Recorded in `plan.md`. |
| F5 | low | The card's tracker anchor (issue #593) was created at Ready; the issue list is never read back, per ADR 0005. | Recorded — the card carries the number and `Refs #593` will go in the PR body. |
| F6 | note | The 30px divider-to-label gap in the large dialog differs from other editors' 16px. | Accepted at gate 1 — the owner's change request named the title-to-border gaps only; `FR-006` pins the 30px gap. |

## History

- 2026-11-23 — first run, pack as of the digests above: coverage 16/16, CRITICAL 0, two low
  findings accepted with their evidence and four notes recorded. Gate 2 may open.
- 2026-11-23 — after gate 2, two mechanical edits: the plan's AC1/AC2 notes now say "no ruled
  descendants" to match the measured assertion, and the tasks' Convergence section records zero
  appended tasks. The digests above were refreshed; no requirement changed.
- 2026-11-23 — red run before the CSS edit: 5 cases, 5 failures, each
  `AssertionError: the title still paints a 1px bottom border`; no import or timeout errors. The
  first draft of the edit-verse case timed out on a transparent pencil; switching the harness to a
  DOM click fixed the harness before the red run was accepted.
- 2026-11-23 — green run after `components.css:539–545`: 7 cases (5 new +
  `tests.e2e.test_song_empty_placement`), `OK` in 20.182s.
- 2026-11-23 — live read-back on the slice worktree server
  `http://127.0.0.1:8766/songs/1820/`: both dialogs paint title border `0px`, a 16.5px title-to-rule
  gap and an 840px head with no ruled descendants; no page errors.
