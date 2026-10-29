# Implementation plan: the Media Library and the transfer history group by age

**Slice**: `specs/146-media-and-transfer-age-buckets` · **Branch**: `feat/146-media-and-transfer-age-buckets`
**Created**: 2026-10-28 · **Spec**: [`spec.md`](./spec.md) (Accepted at gate 1, 2026-10-28)
**Card**: `ITEM-158` · **Bump**: `patch`

## Technical Context

| aspect | value |
| --- | --- |
| Language | JavaScript as classic scripts (no modules, no build step), driven by `base.html`; Python 3.12 / Django 4.0 only for the tests |
| New dependencies | none |
| Storage | none — both rules are pure functions of a row and the present instant; the companion's SQLite is read, never written |
| Testing | Playwright (Python) through `StaticLiveServerTestCase`, plus the existing `multimedia.web` suites |
| Target | modern browsers (Chromium, Firefox, Safari) — `Intl.DateTimeFormat` with `timeZone`, `Date.parse` of offset-bearing ISO |
| Constraints | the media library's rows come from the loopback companion, so the tests route that fetch; static files ship through the manifest storage, so a new script must be referenced by `static` tag |
| Scale | 2 surfaces, 1 new script (~60 lines), 1 stylesheet rule, 1 template line, 1 test module |

## Constitution Check

**Before Phase 0.** No `CONSTITUTION.md` exists at the repo root and the process declares it optional
(`SDD-01`) — there is nothing to check against. The repo's own conventions in `AGENTS.md` and
`docs/PROCESS.md` are the standing bar and are followed by this pack.

**After Phase 1.** Re-run: still no constitution; the plan adds no dependency, no build step, no server
route, no stored state, and no new component. Nothing to justify in Complexity Tracking.

## Decisions

Phase 0 research: [`research.md`](./research.md) — D1 shared rule · D2 file windows in days · D3 rolling
transfer ladder dated by start · D4 bucket-index sort for transfers · D5 headings in the existing class ·
D6 browser tests with `now` as an argument · D7 no headings from the rail · D8 `bump: patch`.

Phase 1: [`data-model.md`](./data-model.md) · [`contracts/README.md`](./contracts/README.md) ·
[`quickstart.md`](./quickstart.md).

## Project structure

```
static/web/age-buckets.js                     NEW   the one rule + its ladders
static/web/media-library.js                   EDIT  group the list by the rule (drops todayJakarta + per-day headings)
static/web/media-handoff.js                   EDIT  group the rendered transfers; skip headings from the rail
static/styles/design/components.css           EDIT  .media-transfers__group beside .media-transfers__divider
multimedia/web/templates/reading/base.html    EDIT  load age-buckets.js before its two callers
tests/e2e/test_media_age_buckets.py           NEW   the browser acceptance for both surfaces
backlog/board.md, backlog/items/ITEM-158-*.md  NEW/EDIT  the card, Ready → In progress → In review → Done
VERSION, CHANGELOG.md                         EDIT  at delivery, patch level and one Changed line
docs/spec/reading.md                          EDIT  at Fold: R22 (the list), R23 (the transfer history)
specs/146-media-and-transfer-age-buckets/     this pack
```

## Traceability

Components: `rule` = `static/web/age-buckets.js` · `list` = `static/web/media-library.js` · `dialog` =
`static/web/media-handoff.js` · `css` = `static/styles/design/components.css` · `shell` =
`multimedia/web/templates/reading/base.html`.

Test functions are `tests/e2e/test_media_age_buckets.py::MediaAgeBucketE2ETests::<name>`.

### Functional requirements

| ID | Component | Verified by |
| --- | --- | --- |
| FR-001 the list's three buckets, labels and order | `list`, `rule` | test `test_the_list_draws_three_age_buckets` |
| FR-002 a file's edges: 30 days, then the calendar year | `rule` | test `test_a_file_buckets_at_its_edges` |
| FR-003 the present day is `Asia/Jakarta` | `rule` | test `test_the_present_day_is_the_congregations_day` |
| FR-004 an empty bucket draws no heading | `list` | test `test_a_bucket_with_no_file_draws_no_heading` |
| FR-005 headings only for date sorts; ascending reverses | `list` | tests `test_a_size_sort_draws_no_heading`, `test_an_ascending_sort_reverses_the_buckets` |
| FR-006 the heading keeps its class and carries `data-bucket` | `list`, `css` | test `test_the_heading_keeps_its_class_and_carries_the_bucket_key`; numbers by inspection of `components.css:619` |
| FR-007 a chip that empties a bucket hides its heading | `list` | tests `test_a_chip_that_empties_a_bucket_hides_its_heading`, `test_the_unused_chip_empties_a_bucket_and_hides_its_heading` |
| FR-008 the row is unchanged | `list` | inspection: `git diff 05379336 -- static/web/media-library.js` touches grouping only — the row builder, icon, meta, links, cloud and remove are byte-identical |
| FR-009 the dialog's five buckets, labels and order | `dialog`, `rule` | test `test_the_dialog_draws_five_age_buckets` |
| FR-010 dated by start; rolling windows | `rule` | tests `test_a_transfer_buckets_by_its_start`, `test_a_transfer_buckets_at_its_edges` |
| FR-011 an active row leads its own bucket | `dialog` | test `test_an_active_transfer_leads_its_own_bucket` |
| FR-012 order inside a bucket: end time, then id | `dialog` | test `test_rows_inside_a_bucket_keep_their_end_time_order` |
| FR-013 `h3.media-transfers__group`, keys, numbers | `dialog`, `css` | test `test_the_dialog_heading_is_a_third_level_heading`; numbers by inspection of the added rule |
| FR-014 the rail draws no headings | `dialog` | test `test_the_rail_draws_no_bucket_headings` |
| FR-015 the transfer row is unchanged | `dialog` | inspection: the same diff shows the row builder untouched apart from the heading walk |
| FR-016 one shared rule; both surfaces call it | `rule`, `shell`, both renderers | inspection: `grep -n "gkpsAgeBuckets" static/web/*.js multimedia/web/templates/reading/base.html` — the definition once, two callers, and no second bucket test anywhere |
| FR-017 empty states unchanged, never a heading over an empty list | `list`, `dialog` | test `test_the_empty_states_are_unchanged` |

### Success criteria

| ID | Verified by |
| --- | --- |
| SC-001 the three headings, once each and in order | test `test_the_list_draws_three_age_buckets` |
| SC-002 file edges at 0, 30, 31 days and across the year | test `test_a_file_buckets_at_its_edges` (pinned `now`) |
| SC-003 the five headings, once each and in order | test `test_the_dialog_draws_five_age_buckets` |
| SC-004 transfer edges at 24 h, 7 d, 30 d | test `test_a_transfer_buckets_at_its_edges` (pinned `now`) |
| SC-005 the three shared labels are identical on all three surfaces | test `test_the_three_shared_labels_read_the_same_on_all_three_lists` |
| SC-006 an active transfer leads its bucket | test `test_an_active_transfer_leads_its_own_bucket` |
| SC-007 nothing else moves | `manage.py test multimedia.web tests` (quickstart) — full browser suites at the push step |

### Story scenarios

| Scenario | Verified by |
| --- | --- |
| US1.1 files of the last 31 days in one bucket | test `test_the_list_draws_three_age_buckets` |
| US1.2 forty days ago, same year → `Earlier this year` | test `test_a_file_buckets_at_its_edges` |
| US1.3 last year → `Older` | test `test_a_file_buckets_at_its_edges` |
| US1.4 an empty bucket draws nothing | test `test_a_bucket_with_no_file_draws_no_heading` |
| US1.5 an ascending sort reverses the buckets | test `test_an_ascending_sort_reverses_the_buckets` |
| US2.1 within 24 h → `Last 24 hours` | test `test_a_transfer_buckets_by_its_start` |
| US2.2 1–7 days → `Last 7 days` | test `test_a_transfer_buckets_at_its_edges` |
| US2.3 7–30 days → `Last 30 days` | test `test_a_transfer_buckets_at_its_edges` |
| US2.4 >30 days, same year → `Earlier this year` | test `test_a_transfer_buckets_at_its_edges` |
| US2.5 last year → `Older` | test `test_a_transfer_buckets_at_its_edges` |
| US2.6 an active row still leads | test `test_an_active_transfer_leads_its_own_bucket` |
| US2.7 an empty rung draws nothing | test `test_the_dialog_draws_five_age_buckets` (fixture set omits a rung first) |
| US3.1 the shared three read the same on all three lists | test `test_the_three_shared_labels_read_the_same_on_all_three_lists` |
| US3.2 sentence case in the markup, uppercase in CSS only | tests `test_the_heading_keeps_its_class_and_carries_the_bucket_key`, `test_the_dialog_heading_is_a_third_level_heading` |

**Verification split: 14 test · 3 inspection · 0 manual** across the 17 functional requirements (FR-006
and FR-013 are tested *and* inspected, and count as test), and 6 test · 1 suite-run across the 7 success
criteria. No requirement is un-verifiable.

## Exit gate (SDD-14)

| check | result |
| --- | --- |
| requirement coverage | every FR-001…FR-017 has a row above |
| entity coverage | both entities in `data-model.md` (age bucket, the two ladders) are consumed by a requirement |
| interface coverage | the one interface is stated in `contracts/README.md`; the companion's API is explicitly unchanged |
| decision provenance | every D1–D8 names its source |
| constitution conformance | no constitution exists; nothing violated |
| zero unknowns | `research.md` says so and lists nothing open |
| verification declared | of the 17 requirement rows, 14 carry `test`, 3 carry `inspection` (two of the tested rows are also inspected), and none carry `manual` |
| quickstart runnable | the test command was run on this branch and passes; the preview opens from `file://` |

## Complexity Tracking

None. No violation to justify: no new dependency, no new server route, no stored state, no new component,
and the shared rule is smaller than the two copies it replaces.
