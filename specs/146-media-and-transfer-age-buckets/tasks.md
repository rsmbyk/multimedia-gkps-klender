# Tasks: the Media Library and the transfer history group by age

**Slice**: `specs/146-media-and-transfer-age-buckets` · **Plan**: [`plan.md`](./plan.md) · **Bump**: `patch`

`[P]` means order-independent, not concurrent — one agent, one thread. Each `test` row in the plan's
traceability table becomes a test task and the code task that passes it (C-SDD-TDD); a task naming two
tests is one behaviour measured on two surfaces.

## Phase 1 — Setup

- [X] T001 Record the baseline the change is measured against: on `05379336`, the Media Library draws one `h2.media-library__group` per upload day and the Transfers dialog draws none; capture the two routed companion payloads (`/v1/files`, `/v1/transfers`) the tests will serve

## Phase 2 — US1: the Media Library groups by age (P1)

- [X] T002 Write `tests/e2e/test_media_age_buckets.py` with its routed-companion helpers and the two edge tests — `test_a_file_buckets_at_its_edges`, `test_the_present_day_is_the_congregations_day` — calling `gkpsAgeBuckets.fileKey(row, nowMs)` with a pinned `now`; they fail on a missing global
- [X] T003 Add `static/web/age-buckets.js` with the file ladder, `presentDay`, `todayIso` and `fileKey`; load it in `base.html` before its callers — T002 goes green
- [X] T004 Write `test_the_list_draws_three_age_buckets` and `test_a_bucket_with_no_file_draws_no_heading`; they fail against the per-day heading
- [X] T005 Group the list in `static/web/media-library.js`: draw `h2.media-library__group[data-bucket]` per bucket from `gkpsAgeBuckets.group`, drop the per-date heading, and replace the local `todayJakarta` with `gkpsAgeBuckets.todayIso` — T004 goes green
- [X] T006 Write and pass `test_a_size_sort_draws_no_heading` and `test_an_ascending_sort_reverses_the_buckets` (the ladder reverses for `date-asc`; a size sort draws none)
- [X] T007 Write and pass `test_a_chip_that_empties_a_bucket_hides_its_heading` and `test_the_unused_chip_empties_a_bucket_and_hides_its_heading` — the type chips and the `Unused` chip filter the rows before the grouping, so a heading never sees an empty bucket
- [X] T008 Write and pass `test_the_heading_keeps_its_class_and_carries_the_bucket_key` — the element stays `h2.media-library__group`, its `textContent` is sentence case, its computed `text-transform` is uppercase, and its `data-bucket` is the ladder key

## Phase 3 — US2: the transfer history says when it happened (P1)

- [X] T009 Write `test_a_transfer_buckets_by_its_start` and `test_a_transfer_buckets_at_its_edges` (24 h, 7 d, 30 d, the year boundary) against `gkpsAgeBuckets.transferKey`; they fail on the missing rungs
- [X] T010 Add the transfer ladder to `static/web/age-buckets.js` — `last-24-hours`, `last-7-days`, then the file ladder's three — dated by `started_at`; T009 goes green
- [X] T011 Write `test_the_dialog_draws_five_age_buckets`; it fails because the dialog draws no heading
- [X] T012 Group `renderTransfers()` in `static/web/media-handoff.js`: compute each row's key, sort by (ladder index, active first, `ended_at` desc, `id` desc), draw `h3.media-transfers__group[data-bucket]` on each change — T011 goes green
- [X] T013 Add `.media-transfers__group` to `static/styles/design/components.css` beside `.media-transfers__divider`; write and pass `test_the_dialog_heading_is_a_third_level_heading` (level, class, numbers, sentence case)
- [X] T014 Write and pass `test_an_active_transfer_leads_its_own_bucket` and `test_rows_inside_a_bucket_keep_their_end_time_order` — an active row started earlier than a finished one sits in its own bucket, above that bucket's finished rows
- [X] T015 Write and pass `test_the_rail_draws_no_bucket_headings` — the dialog opened from `#mediaTransferRail` draws rows and the seen divider only

## Phase 4 — US3: the three lists use the same words (P2)

- [X] T016 Write and pass `test_the_three_shared_labels_read_the_same_on_all_three_lists` — `/tatib/`'s headings compared, string for string, with the Media Library's and the dialog's
- [X] T017 Write and pass `test_the_empty_states_are_unchanged` — `Local library unavailable on this computer.` and `No transfers yet.`, with no heading over either

## Phase 5 — Polish and delivery

- [X] T018 Re-run the preview probe (headings, numbers, 320px) and update `preview/README.md` if any number moved
- [X] T019 `preview/README.md` and `quickstart.md` reviewed against what shipped; `specs/README.md` index row added
- [X] T020 Board: card ITEM-155 to `In progress` at Implement, board row moved; `In review` and `Done` at delivery per C-SDD-BOARD
- [X] T021 `manage.py test multimedia.web` green (353 tests); the three media-library browser tests that touch this area green; the full browser suites run at the push step
- [ ] T022 Bump `VERSION` 1.22.4 → 1.22.5 and add the one `### Changed` line to `CHANGELOG.md` — **at delivery**, in the commit that closes the card (VER-04)
- [X] T023 Fold `docs/spec/reading.md` — `R20` (the list's buckets) and `R21` (the transfer ladder) added, header dated

## Acceptance

- `tests.e2e.test_media_age_buckets` — every test above green on a pinned `now`.
- The Media Library draws `LAST 30 DAYS`, `EARLIER THIS YEAR`, `OLDER` on the companion's own eight files;
  the Transfers dialog draws five headings on a fixture set and two on the real nine rows.
- Nothing else moves: `multimedia.web` green; the browser suites run at the push step with the board's
  known red-on-`develop` tests as the only failures.
