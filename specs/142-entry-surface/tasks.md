# Tasks: a service entry draws no box until it is pointed at

**Slice**: `specs/142-entry-surface` · **Plan**: [`plan.md`](./plan.md) · **Bump**: `patch`

Order: setup, then one phase per story in priority order, then the delivery steps. `[P]` means
order-independent, not concurrent — this slice was run in one thread.

## Phase 1 — Setup

- [X] T001 [P] Verify `tests/test_design_tokens.py` before touching the palette: 6 tests, green (`~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.test_design_tokens`)

## Phase 2 — US1: an entry is the page until you point at it (P1)

- [X] T002 Write the failing assertion first: `specs/142-entry-surface` was previewed live before any edit, and `test_the_resting_surface_matches_spec_068_in_both_themes` was the test that had to change (`tests/e2e/test_tatib_entry_controls.py`)
- [X] T003 Remove `background` and the inset `box-shadow` from `.tatib__item--acts, .tatib__eos` in `static/styles/design/components.css`
- [X] T004 Delete `--tatib-entry-fill` and `--tatib-entry-outline` from both theme blocks in `static/styles/design/tokens.css`
- [X] T005 Rewrite the surface test as `test_the_resting_surface_is_the_canvas_in_both_themes`, keeping the padding, the 56px floor and the reserved-column assertions (`tests/e2e/test_tatib_entry_controls.py`)

## Phase 3 — US2: the row appears when it is pointed at (P1)

- [X] T006 Point `_resting_background` at the canvas instead of the deleted token (`tests/e2e/test_tatib_hover.py`)
- [X] T007 Confirm the existing hover / deliberate-focus / modal-origin rule still fills the row with `--icon-hover-bg`, and that quiet restoration does not (`components.css`, unchanged rule)

## Phase 4 — US3: every kind keeps its geometry (P2)

- [X] T008 Confirm on `/tatib/144/` that the media row keeps `min-height: 80px`, `padding: 16px 16px 16px 64px` and its 42px tile at `left: 13px`, and the break its 56px box plus rule and diamond — no edit needed

## Phase 5 — Polish

- [X] T009 [P] Freeze the pre-change stylesheets at `ca71c850` in `specs/142-entry-surface/preview/assets/` so the comparison's **Now** column keeps drawing the retired box
- [X] T010 [P] Regenerate `specs/142-entry-surface/preview/preview.html` from the live markup via `preview/build_preview.py`
- [X] T011 Card ITEM-152, and ITEM-153 for the touch-controls E2E found red on `develop` while running this suite (`backlog/`)
- [X] T012 Board row and `specs/README.md` index row
- [ ] T013 Bump `VERSION` 1.22.2 → 1.22.3 and write the `CHANGELOG.md` line — **held until the branch is split** (see `analysis.md` F1)
- [ ] T014 Mark spec 068 superseded in `specs/README.md` and its own `Status` line — **at merge**, so a superseded spec never points at an unaccepted one

## Acceptance

- `tests.test_design_tokens` — 6/6 green.
- `tests.e2e.test_tatib_entry_controls` + `tests.e2e.test_tatib_hover` — 29/42, with 13 red documents
  belong to slice 143's stacked add-bar commit or predate this branch; see `analysis.md` F1 for the
  disposition.
