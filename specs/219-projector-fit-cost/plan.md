# Implementation Plan: a text screen arrives as fast as the entries beside it

**Spec**: `specs/219-projector-fit-cost/spec.md` (Draft, Gate 1 pending)
**Branch**: `fix/219-projector-fit-cost`
**Bump**: `patch` (D007; shown at Gate 2)
**Preview**: `live preview at http://127.0.0.1:8791/projector?service=144` — the real projector
served from this worktree, because the change is the time a screen takes to arrive.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | vanilla JS in `static/web/projector.js`; no framework, no build step |
| Primary dependencies | none new; `requestIdleCallback` with a `setTimeout` fallback |
| Existing patterns | `fit()` fits one screen and `render()` calls it once per paint; `tests/e2e/test_projector.py` drives the real page with Playwright and reads computed styles |
| Storage | none; the fitted size is remembered on the element's `dataset` for the life of the page |
| Testing | `tests/e2e/test_projector.py` — one new test, four existing fitting tests unchanged |
| Target platform | the projector page in Chromium, at 1440 × 900 and on a projector at 1920 × 1080 |
| Constraints | the largest fitting size must not change (R14); a screen not fitted ahead of time must still be fitted correctly; nothing may depend on the idle work having run |
| Scale / scope | 1 source file changed (`static/web/projector.js`), ~60 lines net; 1 test module; 1 new test |

## Constitution Check

No `CONSTITUTION.md` in this repository — nothing to check (SDD-01). Re-checked after Phase 1:
unchanged.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Seven decisions: the exact walk (D001), fitting at rest
(D002), the idle neighbour fit (D003), the memory key (D004), the halved cut (D005), containment
rejected (D006), the bump (D007).

## Phase 1 — Design

- `data-model.md` — explicitly none.
- `contracts/none.md` — explicitly none: no route, payload or API changes.
- `quickstart.md` — the commands that reproduce every number and run every test.

### Design notes

- **`fit()` gains a key and a `force` flag.** The key is `stage width x height | header text | row
  count | text length` — exactly the inputs the fit reads. `force` is what the fonts-ready handler
  uses after clearing every key, because a face swap changes the metrics without changing the key.
- **`render()` fits before the morph.** `syncEmptyNotice()` still runs first (the notice's band is part
  of the stage while it is painted), then `applyPassageTranslation()`, then `fit()`, then the `is-in` /
  `is-out` classes. Nothing else moves: `previousIndex`, `data-current-screen`, the media renderers,
  the cue and the display-state write keep their order.
- **`fitNeighbours()` is scheduled at the end of every `render()`**, cancelling the previous request,
  and returns without work while a Go To detour is on the stage. It fits `current ± 1` only where the
  screen carries `.screen__lines`; a screen with no words has nothing to fit.
- **`truncateText()` halves both loops.** Rows are hidden for the trial and removed once the count is
  chosen, so the DOM ends where the one-at-a-time loop left it; the last row's characters are trimmed
  by halving, then the ellipsis is appended as before.
- **The walk from 200 px down is untouched**, and the stage's box is read once per fit instead of once
  per trial.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 (fitted at rest) | `static/web/projector.js` `render()` | `test` → `tests/e2e/test_projector.py::ProjectorE2ETests::test_a_text_screen_arrives_without_being_fitted` (every fitted screen fits and is maximal once the morph settles) | `manual` — `preview/verify_sizes.py`: the arrival size equals the resize size on all 126 screens |
| FR-002 (neighbours fitted in idle time; arrival still fits) | `fitNeighbours()`, `render()` | `test` → the same test (one layout read per paced advance) | |
| FR-003 (remembered by stage and body; cleared on the faces) | `fit()`, `fitKey()`, the `document.fonts.ready` handler | `test` → `test_a_body_too_long_for_the_screen_comes_down_to_fit` (the resize path re-fits) | `inspection` — the key's four parts are the fit's four inputs |
| FR-004 (largest fitting size kept) | `fitSize()` | `test` → `test_a_body_too_long_for_the_screen_comes_down_to_fit` (one pixel more does not fit), `test_a_text_screen_arrives_without_being_fitted` (every fitted screen is maximal) | |
| FR-005 (the cut halves, same cut) | `truncateText()` | `test` → `test_a_single_screen_text_fits_its_whole_body_on_one_screen` | `manual` — a 400-row body keeps 116 rows / 10 711 characters / 2 px on both builds |
| FR-006 (resize, faces, translation re-fit) | `render()`, the `resize` and `fonts.ready` handlers | `test` → `test_a_gap_opens_between_the_words_own_lines` (re-fits on `resize`), `test_a_body_too_long_for_the_screen_comes_down_to_fit` | |
| SC-001 (no fitting on arrival) | `fitNeighbours()` | `test` → `test_a_text_screen_arrives_without_being_fitted` (max 1 read per paced advance) | `manual` — `preview/probe.py` paced run |
| SC-002 (paced advance inside a frame) | `static/web/projector.js` | `manual` — `preview/probe.py`: 16.4 → 3.7 ms median, 66.9 → 7.4 ms worst | |
| SC-003 (rapid advance no worse) | `fit()` on arrival | `manual` — `preview/probe.py` rapid run: 13.9 → 2.3 ms median, 70.4 → 67 ms worst | the fallback path |
| SC-004 (arrival size = at-rest size) | `render()` ordering | `manual` — `preview/verify_sizes.py`: 53 mismatches on develop, 0 on the slice | |
| SC-005 (existing fitting contracts) | `tests/e2e/test_projector.py` | `test` → the four fitting tests | |
| SC-006 (the cut) | `truncateText()` | `manual` — 2 992 → 81.5 ms, same rows and characters | |
| FR-007 (a held key cuts) | `static/web/projector.js` `render()` (`morphing`, `startMorphWindow()`), `static/styles/design/projector.css` (`.screen.is-quiet`) | `test` → `test_a_held_arrow_key_cuts_instead_of_stacking_screens` | `manual` — `preview/hold_probe.py`: 7 → 1 screens painted at once |
| FR-008 (a single move still morphs) | the same | `test` → `test_a_single_move_still_morphs`, `test_moving_and_toggling_morph_rather_than_jump` | |
| SC-007, SC-008 | as above | as above | |
| US1/AC1–3, US2/AC1–3, US3/AC1, US4/AC1–3, the edge cases | as above | as above | |

**Verification split**: `6 test · 1 inspection · 6 manual`.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/219-projector-fit-cost/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  converge.md  fold.md
  contracts/none.md  checklists/requirements.md
  preview/probe.py            (the advance cost, both builds, two cadences)
  preview/verify_sizes.py     (arrival size against the at-rest size, both builds)
```

### Source

```
static/web/projector.js                  (fit key, fit before the morph, idle neighbour fit, halved cut)
tests/e2e/test_projector.py              (one new test; the COUNTER_* helpers)
docs/spec/projector.md                   (Fold: R14 added)
backlog/board.md, backlog/items/ITEM-234-projector-fit-cost.md
CHANGELOG.md, VERSION                    (delivery commit)
```

### Structure Decision

No new directory and no new module: the change stays inside the fitting section of the one file that
owns it, and the preview lives in the slice folder with the probes that produced its numbers.
