# Analyze — the Tata Ibadah list groups by age

**Date**: 2026-10-25
**Artifacts read** (SHA-1, first 12): `spec.md` `fc67e806a7db` · `plan.md` `fe3da021c707` · `tasks.md`
`174180fbb0ed` · `research.md` `c91ba8ae7d0b` · `data-model.md` `b28522ff82a4` ·
`checklists/checklist.md` `e130a097b793`
**Metrics**: 13 `FR` · 6 `SC` · 4 stories · 21 tasks · 19/19 requirements carried by at least one task ·
19/19 with a declared verification · **0 CRITICAL** · 0 uncovered

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A-001 | MEDIUM | `FR-003` (the present day is `Asia/Jakarta`) is verified by inspection only: `present_day()` is a clock read, and a test that asserted it would assert the host clock. The behaviour it protects — a bucket boundary at 07:00 WIB — is covered by `FR-002`'s tests with the day passed in. | accepted as declared; the expression is the repo's own convention (`views.py` ×3, `local_transfers.py`) |
| A-002 | MEDIUM | `FR-007`, `FR-009` and `FR-013` (the saved render, the filter across buckets, the saved badge) rest on browser suites that are written but run at the push step, per the repo's practice. Until then those rows are held by inspection of the JavaScript. | accepted gap, recorded in `plan.md` (`SC-005` note) and in `tasks.md` T017/T020 |
| A-003 | MECHANICAL | `date_buckets.LABELS` was written and never read. | fixed — removed |
| A-004 | MECHANICAL | `search_lib.format_month_long` became dead when the month heading went (its only caller was `_tatib_groups`). | fixed — removed |
| A-005 | LOW | The badge's twelve CSS lines exist in two stylesheets. | accepted; Complexity Tracking in `plan.md` gives the reason (the two surfaces load different sheets) |
| A-006 | INFO | An earlier run in this session reported two `ServiceEntryViewTests` errors and called them pre-existing. That was wrong: the shell still had `DJANGO_DEVELOPMENT_MODE=true` exported from the preview seeding, so those tests ran against this worktree's SQLite file instead of the compose database. Re-run with a clean environment: `multimedia` 411 tests green, and the same class on `develop` green. | corrected; no code involved |

## Coverage

Every `FR` names a component and a verification in `plan.md`'s traceability table, and every `SC` names
how it is measured. The split is **11 test · 4 inspection · 0 manual**. No requirement is un-tasked, no
task carries no requirement, and no two requirements state the same thing twice in different words.

## History

- 2026-10-25 — run 1, after Implement and before Converge: 0 CRITICAL, 0 uncovered; five findings, two
  fixed mechanically, three accepted with their reasons above.
