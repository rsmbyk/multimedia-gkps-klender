# Tasks: the first refresh authenticates its references write

**Spec**: `specs/150-references-token-order/spec.md`
**Plan**: `specs/150-references-token-order/plan.md`
**Verification split**: 15 test · 4 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 Confirm the failure before touching anything: on `develop` at `1.22.9`, the live
  `/media-library/` shows `POST /v1/references` 403 on the first refresh and two draws 190ms apart. No
  setup task exists: no dependency, no ignore-file change, no route.

## Phase 2 — Foundational

Both stories rest on the same pair — a stub that refuses a tokenless write, and the page that must not
send one — so the stricter stub and the new case are written and run red here, before the fix.

- [X] T002 [P] [US2] In `tests/e2e/test_media_library.py:977` (`_sampled_library`'s `companion`), answer a
  `/references` POST whose `x-gkps-media-token` is not `test-token` with `403 {'error': 'Not authorized.'}`
  and the CORS header, as `local_media.py:515` does.
- [X] T003 [P] [US1] Write
  `test_the_first_refresh_writes_its_references_with_the_token` in the same file: capture the page's
  `/references` request, assert its `X-GKPS-Media-Token` equals the stub's `write_token`, and assert the
  first draw already carried the references (no `Service uses unavailable` in a row that has them).
- [X] T004 Run T003 and the six spec-148 cases against the **unmodified** `static/web/media-library.js` and
  record the red output in `analysis.md`: the new case fails on the header (`''`), and the six fail because
  the refused write degrades the first draw.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a page's first refresh writes its references with its own token and draws the list once.
**Independent test**: T003 green; the six spec-148 cases green under the stricter stub.

- [X] T005 [US1] In `static/web/media-library.js:157`, assign `token = next.status.write_token` (guarded)
  immediately after the `/status` and `/files` results; leave `setStatus(next.status)` and `render()` at
  the end of the chain.
- [X] T006 [US1] Re-run T003: green. Re-run the six spec-148 cases — `test_the_library_list_is_drawn_once_per_refresh`,
  `test_a_library_refresh_never_moves_a_row`, `test_clicking_share_online_never_moves_a_library_row`,
  `test_a_known_reference_never_shows_the_placeholder`,
  `test_a_failed_references_request_draws_the_placeholder_once`,
  `test_the_status_poll_leaves_the_list_where_it_is` — all green under the stricter stub. Run the module in
  full; the existing cases must be unchanged (one pre-existing red, ITEM-156).

## Phase 4 — US2 (P2)

**Goal**: the suite cannot pass a tokenless write again.
**Independent test**: the six spec-148 cases are red before T005 and green after it, with their assertions
untouched.

- [X] T007 [US2] `inspection` — read the stub's refusal: the 403 body is the companion's own
  (`local_media.py:515`), the CORS header is present, and no case was written against the old permissive
  branch.

## Phase 5 — Polish

- [X] T008 `inspection` — read the diff: one statement in `refresh()` plus the stub; `write()`,
  `setStatus`, `render()`, `share()`, `media-handoff.js`, the templates, the CSS and the companion are
  untouched (FR-004). Re-run `…::test_library_filter_sort_and_dialogs` and
  `…::test_connected_library_shows_file_and_status_details`.
- [X] T009 Add the spec's index row to `specs/README.md`, naming 150 and `Accepted`.
- [X] T010 Bump `VERSION` `1.22.9` → `1.22.10` and add one `### Fixed` line under `## [Unreleased]` in
  `CHANGELOG.md`.
- [X] T011 Fold: add R25 to `docs/spec/reading.md` and move the header's `last folded` and `slices`.
- [ ] T012 Delivery, after the report: open the PR as a draft, then read `ITEM-160`'s state — if the owner
  has moved it to `Ready`, set `in-review`, write `pr:` and move the board row, and push that one commit
  (`C-BOARD-GIT`); if it is still in `Backlog`, stop and say so.

## Phase 6 — Convergence

- [ ] T013 [Convergence, post-merge] `manual` — after the merge, `collectstatic` inside the `web`
  container, restart it, then run `specs/148-media-library-refresh-flicker/preview/frame_sampler.py`:
  `worst jolt: 0px`, exit 0, and `POST /v1/references` answered 200 on the page's first refresh.
