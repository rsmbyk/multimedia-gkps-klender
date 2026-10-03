# Tasks 007: The old rows — editable, and one running order

- **Status:** Draft — needs the owner's Accept (SDD gate). No implementation before that.
- **Plan:** [./plan.md](./plan.md) · **Spec:** [./spec.md](./spec.md)

## Before starting

- [ ] Spec Accepted by the project owner
- [ ] The open questions in ./spec.md answered (the order namespace, editing vs migrating, the bump)
- [ ] Branch from `feat/006-service-entries` (`feat/007-old-rows`)
- [ ] The compatibility pass over the old dock, its sources and `/api/tatib/items/` exists before
      touching anything

## Slice 1 — the old rows can be edited and deleted

- [ ] Red: the update and delete endpoints per item kind, their rules and their refusals; the pane
      rendering the controls on an old row (`multimedia/web/tests.py`)
- [ ] Green: the endpoints, the item fragment, the pane's controls, and `static/web/entries.js`
- [ ] Red: e2e — an old row edited, and deleted after a confirmation (`tests/e2e/test_old_rows.py`)
- [ ] Green: e2e

## Slice 2 — one running order

- [ ] Red: the migration preserves the rendered order; insertion after an old row; the gap closes on
      delete; the old API still answers (`multimedia/tatib/tests.py`, `multimedia/web/tests.py`)
- [ ] Green: the migration, the merged stage sort, and the insertion rule across both tables
- [ ] Red: e2e — add under the second old row, and find it there
- [ ] Green: e2e

## The compatibility promise

- [ ] A regression pass over the old OBS pages and `/api/tatib/items/`, run before and after

## Done when

- [ ] All acceptance scenarios in ./spec.md hold
- [ ] The tests named above are green
- [ ] Traceability in ./spec.md filled; ITEM and board updated in the same PR
- [ ] `VERSION` and the changelog bumped in the same PR (0.10.0 → 0.11.0 once spec 006 ships)
