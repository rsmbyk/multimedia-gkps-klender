# Tasks: the Media Library list holds still while it refreshes

**Spec**: `specs/148-media-library-refresh-flicker/spec.md`
**Plan**: `specs/148-media-library-refresh-flicker/plan.md`
**Verification split**: 20 test · 3 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Confirm the shipped behaviour before touching anything: `frame_sampler.py` on
  `localhost:63404` printed `worst jolt: 56px | frames showing the placeholder on more than one row:
  8 of 72`, exit 1. No setup task exists: no dependency, no ignore-file change, no route, no fixture.

## Phase 2 — Foundational

The six E2E cases are the shared prerequisite of both stories, and TDD-01 forbids writing a test after
the code it covers — so they are written and run red here, before the one control-flow change that
serves both stories.

- [X] T002 [P] [US1] Module-level helpers in `tests/e2e/test_media_library.py`: a companion stub
  serving a library whose first row carries a two-line `uses` block, and an in-page frame sampler that
  records every `.media-library__file`'s `top`, the `.media-library__unused` count, `#mediaFileList`'s
  height and the number of draws, from a trigger until the list settles.
- [X] T003 [P] [US1] `test_a_library_refresh_never_moves_a_row` — **Remove → cancel** and then **Save
  setting**, asserting each row's `top` has a single value across every sampled frame and naming the
  trigger that moved it.
- [X] T004 [P] [US1] `test_clicking_share_online_never_moves_a_library_row` — the begin endpoint
  patched to `(None, share)` so the click reaches `refresh()` without an upload; same invariant.
- [X] T005 [P] [US1] `test_the_library_list_is_drawn_once_per_refresh` — one refresh replaces the
  list's children once, and the first load's list never grows after it appears.
  *Reconciled:* "a draw" is counted as a **frame whose list differs from the one before** — the row
  count, the tops and the height — not as a `MutationObserver` record nor as a `replaceChildren` call.
  An observer reports one record per removed and per added node (one draw read as 6–8), and a call
  count also numbers the 2s poll's identical rebuild, which FR-004 keeps. A refresh that shows nothing
  new therefore reads 0 changes, which is why the assertion is "at most one" (`converge.md`, pass 1).
- [X] T006 [P] [US2] `test_a_known_reference_never_shows_the_placeholder` — `**/media-library/references/`
  held 200 ms, then no sampled frame may carry `Service uses unavailable` for a file with references.
- [X] T007 [P] [US2] `test_a_failed_references_request_draws_the_placeholder_once` — that route
  fulfilled with a 500, then the placeholder is drawn once and the rows stay put.
- [X] T008 [US1] `test_the_status_poll_leaves_the_list_where_it_is` — after the list settles, one poll
  interval (2.5s) changes no row's top.
- [X] T009 Run the six against the **unmodified** `static/web/media-library.js`: three red, each on its
  own measurement — `rows moved while a cancelled remove: [0.0, 26.0]`, the same for Share online, and
  `2 not less than or equal to 1` list changes for one refresh, with a placeholder frame list of ones
  behind it. Two of the six are **guards** that are green on the shipped page by design — a failed
  references read and the 2s poll both end in the same picture either way, so there is no visible
  failure to start from; they guard against a fix that redraws the degraded list or moves a row.
  Recorded in `analysis.md`.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: no row moves while the list refreshes, and the list is drawn once.
**Independent test**: T003, T004, T005 and T008 green.

- [X] T010 [US1] `refresh()` in `static/web/media-library.js:146` assembles `files`, `uses`,
  `protected` and `status` in locals and applies them once, with the only `render()` call at the end of
  every path; the return value keeps its meaning (`false` when the references are unknown, so the
  remove handler still declines).
- [X] T011 [US1] Re-run T003, T004, T005 and T008: green. `6 tests … OK` in 28.4s.
- [X] T012 [US1] `preview/frame_sampler.py` takes an optional URL argument. *The live readout of the
  fixed page is not available before the merge* — the compose `web` service serves the `develop`
  checkout, and a worktree `runserver` is refused by the companion's origin allow-list
  (`multimedia/local_media.py:447`). Recorded in `converge.md`; the readout is T019.

## Phase 4 — US2 (P2)

**Goal**: a file whose references are known never shows `Service uses unavailable`, and a failed
references read still shows it — once.
**Independent test**: T006 and T007 green.

- [X] T013 [US2] Re-run T006 and T007 against T010: green. `inspection` — the diff's only `uses = null`
  assignment now sits inside the references `.catch`, which is the failed-read path.

## Phase 5 — Polish

- [X] T014 `inspection` — the diff touches `refresh()` only; `render()`, the row markup, the CSS, the
  templates, `media-handoff.js` and the references view are unchanged (FR-005). The module in full:
  `Ran 28 tests in 82.3s`, one failure —
  `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`, which fails identically on
  unmodified `develop` (`19.85` vs the pinned `12`) and is carded as ITEM-156. The unchanged re-run
  named above — `test_library_filter_sort_and_dialogs`,
  `test_connected_library_shows_file_and_status_details`, `test_connection_icon_tracks_status_refresh`,
  `test_disconnected_library_hides_local_inventory_details`,
  `test_empty_library_keeps_tall_create_modal_and_quiet_empty_state` — all pass.
- [X] T015 The spec's index row is in `specs/README.md`, naming 148 and `Accepted`.
- [X] T016 `VERSION` `1.22.7` → `1.22.8` (145, 146 and 147 landed 1.22.6–1.22.7 on `develop` first), and one `### Fixed` line under `## [Unreleased]` in
  `CHANGELOG.md`.
- [X] T017 Fold: R24 added to `docs/spec/reading.md`, the header's `last folded` and `slices` moved
  (`fold.md`).
- [ ] T018 Delivery, after the report: open the PR as a draft, then read `ITEM-158`'s state — if the
  owner has moved it to `Ready`, set `in-review`, write `pr:` and move the board row, and push that one
  commit (`C-BOARD-GIT`); if it is still in `Backlog`, stop and say so, because `Ready` is the owner's
  move and not the agent's. *Done after the report, on the owner's word: pushed, drafted, the card moved
  to `In review` and the PR marked ready; the card was renumbered `ITEM-156 → ITEM-158` when `develop`
  took the id for the spacing-E2E card.*

## Phase 6 — Convergence

- [X] T019 [Convergence, pass 1] After the merge, open `http://localhost:63404/media-library/` on the
  compose stack and run `preview/frame_sampler.py`: `worst jolt: 0px`, no placeholder frame, exit 0 —
  the live readout T012 could not take on the branch.
