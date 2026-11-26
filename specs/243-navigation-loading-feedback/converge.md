# Convergence: visible pending state for rail and sidebar fetches

**Spec**: `specs/243-navigation-loading-feedback/spec.md`
**Passes**: 1 of 1

## Pass 1 — 2026-11-26

Every traceability row was re-assessed against the present code, using the method the plan DECLARED.

**Consolidated run**: both modules named in `plan.md`, one command:

```
manage.py test tests.e2e.test_navigation_pending tests.e2e.test_navigation_freshness \
  --tag=e2e --noinput --keepdb -v 1
```

with `DATABASE_URL` pointed at `gkps243`, so Django used `test_gkps243`. Present build: **Found 15 tests, OK, 44.181s**. Same command on a clean detached worktree at base `14af227a` with the new test file copied in: **Found 15 tests, FAILED (failures=10, errors=1), 4 passed, 90.920s** — the new pending-state assertions fail on the base; the sibling navigation-freshness guards pass there.

| Requirement | Declared method | Evidence | Result |
| --- | --- | --- | --- |
| US1/AC1 | `test` | `test_a_rail_click_locks_the_item_and_bars_both_lists` — rail `aria-disabled`, icon opacity 0.45, both section bars visible | pass |
| US1/AC2–AC4 | `test` | `test_a_list_only_fetch_leaves_the_stage_untouched` — stage unchanged, no `aria-busy`, no bar, no placeholder | pass |
| US2/AC1–AC3 | `test` | `test_a_verse_write_seeds_the_bible_placeholder`, `test_a_song_write_matches_the_real_song_header`, `test_a_service_write_seeds_the_service_header`, `test_a_non_hymn_song_placeholder_names_its_songbook` | pass |
| US2/AC4 | `test` | `test_placeholder_origin_matches_the_real_read` — placeholder `.read` origin equals real `.read` at 1440px | pass |
| US2/AC5 | `test` | `test_settlement_clears_the_busy_state` | pass |
| US3/AC1–AC3 | `test` | `test_write_then_write_cancels_the_first`, `test_write_then_list_keeps_the_first_and_adds_a_list_bar`, `test_list_then_write_cancels_the_list` | pass |
| US3/AC4 | `test` | `test_a_cancelled_item_can_be_clicked_again` | pass |
| US3/AC5 | `inspection` | `navigate()` `fail()` sets `window.location.href` before `finish()`; pending state is not cleared on fallback | checked by inspection |
| FR-001, FR-002 | `test` + `inspection` | lock cases; `test_row_controls_are_disabled_while_its_fetch_is_pending`; no spinner/label/edge/ring marker in `reading.js` | pass / checked |
| FR-003 | `test` + `inspection` | bar cases; `probe11.py` measured bar-to-parent top offset 0px for all three sections | pass / checked |
| FR-004, FR-005 | `test` | list-only and write cases assert the stage state on both sides of the classification | pass |
| FR-006 | `inspection` | E2E counts: 5 Bible verse rows, 3 song verse rows, 3 service entry rows; non-hymn eyebrow falls back to the songbook name | checked by inspection |
| FR-007 | `test` | the three cancellation cases above | pass |
| FR-008 | `test` + `inspection` | settlement test; success/failure/supersede/fallback paths in `navigate()` | pass / checked |
| FR-009 | `inspection` | only the clicked item and its row controls carry the lock; `.stage` alone carries `aria-busy` | checked by inspection |
| FR-010 | `inspection` | no `navBusy` / `pendingNavigation` references remain; all pending state is in `navigate()` | checked by inspection |

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | MEDIUM | Three asks arrived after gate 2 and extended FR-001 and FR-006 without re-presenting either gate. | Recorded in `spec.md` §Clarifications with the owner's wording and in `tasks.md` T026–T028; treated as in-slice because they touch the same files and tests. Gates were not re-opened — stated plainly rather than hidden. |
| C2 | INFO | The base worktree did not contain the new E2E module, so the red baseline was run with that one file copied in. | Expected for a new-behaviour test; the module is an output of this slice, not a base fixture. |
| C3 | INFO | `multimedia.web.tests` has 2 failures (337 passes); both reproduce on base `14af227a` with the same venv and DB mode. | Accepted as pre-existing; not caused by this slice. |
| C4 | INFO | The stage is not a positioned ancestor and `.read` is `display:none` until `data-read="on"`; the placeholder needed `position:relative` on `.stage` and `display:block !important` on its inner `.read`. | Verified in `test_placeholder_origin_matches_the_real_read`; no requirement change. |
| C5 | INFO | Row-control disabling uses `data-gkps-pending-disabled` markers and restores only controls the slice disabled, so pre-existing `disabled` state is preserved. | Accepted; verified by the row-controls test and live probe. |
| C6 | INFO | Analysis findings A1–A6 were accepted at gate 2; `analysis.md` was written before that gate, not at delivery. | No action. |

No CRITICAL findings. Traceability coverage is 100%: every declared row has evidence with its declared method, and no requirement appears only in code.

## Outcome

Converged on pass 1. No gaps, no contradictions, no quarantined reds. Fold and delivery remain unauthorized.
