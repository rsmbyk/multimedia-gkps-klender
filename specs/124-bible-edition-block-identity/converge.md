# Convergence: Keep a chapter's verse text when the reading page updates in place

**Spec**: `specs/124-bible-edition-block-identity/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-24

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The spec's edge case "SIM selected before an in-place move keeps SIM visible" had no pin — it was only checked by hand on the dev server | `partial` | FR-002 / US1-AC2 | `tests/e2e/test_reading.py::ReadingE2ETests::test_same_name_edition_blocks_keep_the_verse_text`, new closing leg |

**Outcome**: appended as `## Phase N+1 — Convergence` T010 in `tasks.md`; the assertion was added and the
test re-run green (3.99 s).

## Pass 2 — 2026-10-24

Re-read the spec against the diff and the suite: FR-001…FR-004 each backed by the file and the pin the plan
named; SC-001…SC-003 by the new test and the re-run classes (17 browser tests green); no file changed
outside the plan's structure (`static/web/reading.js`, `tests/e2e/test_reading.py`, plus the pack, card,
board, VERSION and changelog the plan lists). Nothing remains.

**Outcome**: Converged — nothing remains.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| The saved/offline view inherits the corrected identity through the same `data-ed` markup, but no offline fixture exercises a same-name book | `partial` | LOW | 2026-10-24 (analysis A2, owner accepted at gate 2) |
