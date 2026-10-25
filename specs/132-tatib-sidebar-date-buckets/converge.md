# Convergence — the Tata Ibadah list groups by age

## Pass 1 — 2026-10-25

**What was checked**: every row of `plan.md`'s traceability table, each by the method it declares. The
suite was run first (`multimedia`, 411 tests), then each `inspection` row by reading the running branch,
then the removed things by grep.

| Requirement | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001 labels and order | test | `…::test_tatib_list_buckets_its_services_by_age`; probe prints all four headings in order | met |
| FR-002 boundary rule | test | `test_date_buckets.py` 6 tests (0 · 1 · 30 · 31 · cross-year · leap day) | met |
| FR-003 Jakarta day | inspection | `date_buckets.present_day` is `timezone.now().astimezone(ZoneInfo('Asia/Jakarta')).date()`, the same expression `views.py` uses three times | met |
| FR-004 Upcoming order | test | the bucket test asserts `['Hari Ini', 'Dua Bulan Lagi', 'Minggu Depan']`; probe on real data shows today's four rows first | met |
| FR-005 empty bucket | test | `…::test_tatib_list_draws_no_heading_for_a_bucket_without_rows` — one heading, no `data-bucket="upcoming"` | met |
| FR-006 dock | test | `test_obs_dock…::test_the_dock_picker_names_the_same_date_buckets_as_the_reading_panel`; live page shows `Upcoming`/`Last 30 days`/`Earlier this year`/`Older` and four `servicerow__today` pills on real data | met |
| FR-007 saved buckets | inspection | `offline-render.js::tatibBucket` mirrors `bucket_key` line for line; `jakartaToday` uses `Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Jakarta'})`; `node --check` clean | met, browser suite deferred (accepted, A-002) |
| FR-008 key renamed | test + inspection | test asserts `data-bucket="upcoming"` present and `data-month=` absent; `grep -rn "data-month"` → only that negative assertion | met |
| FR-009 filter | inspection | `reading.js::applyFilter` is untouched and knows nothing of buckets: it counts `.book` rows per `.group` and toggles `is-hidden`, which the `.group.is-hidden + .group` rule follows | met, browser suite deferred |
| FR-010 template mode | test + inspection | `curl /tatib/?mode=template` → one `section.group`, one `Templates` heading, no `data-bucket`; the existing template-mode tests stay green | met |
| FR-011 heading and divider | inspection | probe: `drawn=uppercase 11.5px sticky`, divider `{'border': '2px', 'margin': '10px', 'padding': '10px'}` — unchanged on real data | met |
| FR-012 today badge | test | `…::test_a_today_row_carries_the_today_badge_and_no_other_row_does` (exactly one badge, `— today`) | met |
| FR-013 saved badge | inspection | `bookLink` writes `.book__today` for a service whose `today` flag is set by `servicePanel`; same class, same day | met, browser suite deferred |
| SC-001…SC-006 | as declared | the suite; the probe; the dock page; parity suite deferred | met |

**Removed things**: `grep -rn "data-month\|format_month_long\|is_upcoming\|is-today\|is-upcoming"` over
`multimedia/`, `static/`, `tests/` returns only the two negative assertions this slice wrote.

**Typed gaps**
- `missing` — none.
- `partial` — none. (The deferred browser rows are declared verifications, not gaps: `plan.md` says
  `test` → the E2E suite, and `tasks.md` T017/T020 record that they are written and run at the push step.)
- `contradicts` — none.
- `unrequested` — none. Two pieces of dead code this slice created were removed (`date_buckets.LABELS`,
  `search_lib.format_month_long`), which is cleanup inside the blast radius, not new work.

**Outcome**: converged on pass 1. No task left open; no requirement resting on nothing.

## Push-step evidence — the browser suites

Both suites the plan defers to the push step were run before the branch went out.

| Suite | Result |
| --- | --- |
| `tests.e2e.test_saved_render_parity` (7 tests) | green — the saved page's headings, bucket keys, rows and today badges equal the server's for `/tatib/`, `/tatib/?mode=template` and the other routes |
| `tests.e2e.test_reading` (84 tests) | 82 green; the slice's own test green once its fixtures moved into `setUp` (Playwright's loop is live during a test body and must not overlap an ORM write) |

Two corrections came out of that run, both applied:

- The parity fields first read `.group__head` and `dataset.bucket` on **every** route, so the Bible and home
  pages compared a key they do not have and five subtests failed. The fields are now scoped to the Tata
  Ibadah panel (`isTatib(doc)`), which is the only section they describe.
- `test_the_panel_shows_its_empty_view_when_no_songbook_exists` fails on `develop` too: it expects
  `No matching songbooks.` where spec 129 requires the empty copy. It is a stale assertion from another
  slice, not this one; recorded as card `ITEM-137` so it is not a silently red test (TDD-09).
