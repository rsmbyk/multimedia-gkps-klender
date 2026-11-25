# Plan: the live entry header pins at the top when its block is above the view

**Spec**: `specs/242-dock-top-pin/spec.md` · **Bump**: `minor` — one new dock capability
(`dock/R19`); declared at Plan and shown at gate 2.

## Technical context

- Python 3.12 / Django 4.0 / DRF; the dock is a server-rendered page with vanilla JS and the
  design stylesheet served by WhiteNoise. No new dependency, migration, endpoint or template
  change.
- The pin is a `cloneNode(true)` of the live `.entryrow` in a list-level `li.topband-slot` that
  leads `#entryList`; the slot is sticky at `top: -4px`, the clone wears a flat top / 9 px bottom.
  Geometry is read from `runBody.getBoundingClientRect()` and the live `li`, reconciled by
  `updatePins()` on every path that moves or resizes the list.
- E2E: Playwright (Python) through Django's `LiveServerTestCase`, in
  `tests/e2e/test_dock_top_pin.py`, against throwaway database `gkps242` via
  `specs/242-dock-top-pin/preview/run-tests.sh` (copied from spec 208's harness).
- The preview already carries the product edit, uncommitted per live-preview-first; a single
  extra `updatePins()` at the head of `glideRow()` is paint-only reconciliation discovered while
  sampling the click glide.

## Constitution check

No `CONSTITUTION.md` in the repo (SDD-01); nothing to check.

## Decisions

Recorded in [research.md](./research.md): the block-above trigger is the boundary sticky cannot
reach (D001); the pin is a faithful list-level clone, not a second sticky (D002); the click is the
centre control's act (D003); the pin yields per frame through the shared `updatePins()` (D004);
the glide's first paint reconciles before the eased frames (D005).

## Change surface

| File | Change |
| --- | --- |
| `static/web/obs-dock.js` | `topBandSlot` + source cache; clone in `updateTopBand()`;  `updatePins()` includes it; renderList prepends a zero-height slot; go to hides it; click handler shares the centre act; `glideRow()` reconciles before its first eased frame |
| `static/styles/design/obs-dock.css` | `.topband-slot` sticky at the list head; clone face (selected fill, flat top, 9 px bottom) and hover tone |
| `tests/e2e/test_dock_top_pin.py` | new E2E pins: faithful stand, per-frame tracking, hand-scroll give-way, centre click, reduced motion |
| `specs/242-dock-top-pin/preview/` | live preview (8793), probe, README and test runner |
| `docs/spec/dock.md` | `dock/R19` added at Fold; header moved to today, slice prepended |
| `CHANGELOG.md`, `VERSION` | release bookkeeping at the pre-merge delivery commit |

## Traceability

| Requirement / story | Component | Verified by |
| --- | --- | --- |
| FR-001 | `obs-dock.js` `updateTopBand()` · `obs-dock.css` `.topband-slot` | test — `test_the_top_pin_stands_when_the_live_block_is_above` |
| FR-002 | `updatePins()` on scroll/sync/glide/morph/toggle/resize · reduced-motion path | test — `test_the_top_pin_tracks_the_block_per_frame`, `test_the_top_pin_lands_instantly_under_reduced_motion` |
| FR-003 | native sticky header untouched; clone covers at the boundary | inspection — diff of `obs-dock.js`/`.css` against base + `preview/shots/after/top-pin.png` |
| FR-004 | shared click branch in `entryList` handler | test — `test_clicking_the_top_pin_performs_the_centre_act` |
| FR-005 | bottom pin, NEXT band, go to strip, header wash unchanged | inspection — diff against base; test — existing dock modules (`SC-006`) |
| SC-001 / US1 AC1–3 | clone geometry, label, no double | test — `test_the_top_pin_stands_when_the_live_block_is_above` |
| SC-002 / US2 AC1 | per-frame visibility | test — `test_the_top_pin_tracks_the_block_per_frame` + probe |
| SC-003 / US2 AC2–3 | hand scroll and crossing give-way | test — `test_the_real_header_takes_over_when_the_block_returns` |
| SC-004 / US3 AC1 | click act, unchanged display state, following | test — `test_clicking_the_top_pin_performs_the_centre_act` |
| SC-005 / US1 AC3, US3 AC2 | reduced motion, go to unchanged | test — `test_the_top_pin_lands_instantly_under_reduced_motion` |
| SC-006 / US3 AC2 | regression | test — `tests/e2e/test_obs_dock.py`, `test_dock_stuck_corner.py`, `test_dock_open_reset.py` |

Verification split: **8 test · 2 inspection · 1 manual** (manual: owner's live review at
`http://127.0.0.1:8793/obs/dock`).

## Exit gate

- [x] requirement coverage · [x] entity coverage (no data model) · [x] interface coverage
  (`contracts.md`: none) · [x] decision provenance · [x] constitution conformance ·
  [x] zero unknowns · [x] verification declared · [x] quickstart commands runnable.
