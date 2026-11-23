# Convergence: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-23

Every traceability row was re-assessed against the present code, not against its checkbox.

| Requirement | Declared method | Evidence | Result |
| --- | --- | --- | --- |
| FR-001 | `test` | `tests/e2e/test_song_sort_retained.py::test_create_keeps_alphabetical_order` — base fails `['Beta','Zebra','Alpha']`, present code passes `['Alpha','Beta','Zebra']`; `static/web/reading.js:1657` re-applies the chosen order after reconciliation | pass |
| FR-002 | `test` | same test asserts `#songSort[data-order="title"]` alongside the alphabetical rows | pass |
| FR-003 | `test` | `test_create_in_default_order_leads` — green on base and present code; `songSort` still initialises to `m` | pass |
| FR-004 | `inspection` | `songRowEls()` filters `#chList` children on `.songrow`; with no such rows the sorter appends an empty fragment. Hymn-book pages omit `#songSort`, so its rows stay in number order | checked by inspection |
| SC-001 | `test` | `test_create_keeps_alphabetical_order`, plus `performance.timeOrigin` and in-page marker assertions | pass |
| SC-002 | `test` | `test_edit_refresh_keeps_alphabetical_order`, `test_delete_refresh_keeps_alphabetical_order`, `test_row_click_refresh_keeps_alphabetical_order` — all red on base, green now | pass |
| SC-003 | `test` | `test_default_order_and_other_sections_unchanged` green; adjacent `tests/e2e/test_reading.py::test_song_sort_toggles_between_last_modified_and_alphabetical` green | pass |
| US1/AC1–AC3 | `test` | create tests above | pass |
| US2/AC1–AC3 | `test` | edit, delete and row-click tests above | pass |
| US2/AC4 | `inspection` | hymn book renders no `#songSort` (server gate checked in spec 125); `applySongOrder()` does not touch non-song rows | checked by inspection |
| US3/AC1 | `inspection` | `songRowEls()` filter at `static/web/reading.js:1029` | checked by inspection |
| US3/AC2 | `test` | `test_default_order_and_other_sections_unchanged` and the existing toggle test | pass |

**Outcome**: no gaps — Converged in one pass. The six-test module passes on the present code and
five of its six tests fail on base with the exact wrong orders recorded; the adjacent sort-toggle
and spec-225 create-open tests stay green.

## Mechanical alignment applied during the pass

- `ITEM-247` was opened directly in `In progress` rather than passing through the `Speccing` row:
  gate 1 was already accepted and the implementation was under way, so the card's state records
  where the work actually is. No behaviour changes with this alignment.
- The temporary reproduction module was removed once its cases lived in the promoted suite.

## Accepted gaps

None.

## Cap reached

Not applicable — Converged on pass 1.
