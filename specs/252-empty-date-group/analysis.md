# Analysis: No empty groups after the last row is deleted

**Date**: 2026-11-28
**Artifacts read** (first 16 hex of SHA-256): `spec.md` `cb4293c2b2008fd7`, `plan.md`
`587f347498276e99`, `tasks.md` `5d80c2a235df36ee`, `research.md` `84eaddccdd381fcc`.

**Metrics**: 4 FR · 3 SC · 2 stories · 6 scenarios · 15 traceability rows · 4 decisions ·
25 tasks · verification split 5 test · 9 inspection · 1 manual · 0 CRITICAL · 15/15 coverage.

| ID | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| A1 | The gate-1 preview is a live server holding uncommitted work; code and served bytes can drift before gate 2. | MEDIUM | **Resolved**: both URLs answered 200 and both probes were re-run after the finding; every count matches the frozen `UI/UX` table. Cost paid: one probe pair. |
| A2 | `ITEM-269` was `ready` with an empty `issue:` field; gate 1 gave no remote-write permission. | LOW | **Resolved**: owner directed the fix; anchor issue #648 created with `board:item`, verified absent beforehand, and `issue: 648` written in the card. PR will use `Refs #648`. |
| A3 | One neighbouring sort E2E error existed on unmodified `1c86096f` (strict-mode locator saw two article titles). | LOW | **Resolved**: owner chose the in-slice test-only fix; `tests/e2e/test_song_sort_retained.py:144` now names the incoming title. 6/6 green on the slice and 6/6 green on unmodified base with the same test file copied in temporarily; base file restored. |
| A4 | The preview probe relaxed Django's async DB guard to reseed between cases while Playwright ran. | LOW | **Resolved**: seeding moved to `preview/reseed.py` in its own process; the guard is gone from `probe.py`; both probes re-run green. |
| A5 | An earlier attempt committed before the gates; that commit was reset to base in this re-run. | MEDIUM | **Resolved**: branch remains 0 commits ahead of `1c86096f`; chronology is in `spec.md` Assumptions 4; the old commit stays in the reflog only, as the undo trail. |

**Mechanical check**: every FR, SC and story scenario appears in Plan's traceability table; every `test`
row has a paired red/green task; no stale spec/card IDs; no duplicate statements; `quickstart.md` links
the contracts and data model instead of copying them. No mechanical delta was needed.

**Coverage** reads Plan's table: 15/15 rows have a task and a declared verification method. Zero CRITICAL
findings, full coverage, and every HIGH/MEDIUM/LOW finding now resolved — gate 2 may be re-presented.

## History

- 2026-11-28 — first Analyze of the re-run; five findings reported, gate 2 answered with a free-text
  request to fix them rather than a gate word.
- 2026-11-28 — all five findings resolved with the evidence above; gate 2 re-presented.
