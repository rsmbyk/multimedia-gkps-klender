# Tasks 007: The old rows — editable, and one running order

- **Status:** Accepted (owner, 2026-10-05)
- **Plan:** [./plan.md](./plan.md) · **Spec:** [./spec.md](./spec.md)

## Before starting

- [x] Spec Accepted by the project owner (2026-10-05)
- [x] The open questions are answered: one contiguous order per Tata Ibadah; keep editing the existing `TataIbadahItem` rows (do not migrate them to entries); minor bump to 0.11.0 after spec 006 ships as 0.10.0
- [x] Branch `feat/007-service-order-editor` exists, based on `feat/006-service-entries`
- [x] The compatibility pass over the old dock, its sources and `/api/tatib/items/` exists before
      touching anything

## Slice 1 — the old rows can be edited and deleted

- [x] Red: the update and delete endpoints per item kind, their rules and their refusals; the pane
      rendering the controls on an old row (`multimedia/web/tests.py`)
- [x] Green: the endpoints, the item fragment, the pane's controls, and `static/web/entries.js`
- [x] E2E: an old row edited, and deleted after a confirmation (`tests/e2e/test_old_rows.py`)

## Slice 2 — one running order

- [x] Red: the migration preserves the rendered order; insertion after an old row; the gap closes on
      delete; the old API still answers (`multimedia/tatib/tests.py`, `multimedia/web/tests.py`)
- [x] Green: the migration, the merged stage sort, and the insertion rule across both tables
- [x] E2E: add under the second old row and find it there; entry-only reorder preserves old-row
      slots in the sidebar and pane (`tests/e2e/test_old_rows.py`, `tests/e2e/test_reorder.py`)

## The compatibility promise

- [x] A regression pass over the old OBS pages and `/api/tatib/items/`, run before and after;
      `multimedia.web.tests`, `multimedia.tatib.tests`, `multimedia.api.tatib.tests`: 163 green

## Done when

- [x] All acceptance scenarios in ./spec.md hold in the focused tests
- [x] Targeted browser suites: entries, old rows and projector (27 green), reorder (18 green)
- [x] Traceability in ./spec.md filled
- [x] `VERSION`, changelog and ITEM `release_version` set to 0.11.0 in this branch
- [x] Full Django suite: 292 tests, no skips; `check` and `makemigrations --check --dry-run` green
- [x] Draft PR #265 open; ITEM and board moved to In review with its number in the same PR
