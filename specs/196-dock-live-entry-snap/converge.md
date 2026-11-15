# Converge — dock live entry snap

**Spec**: `specs/196-dock-live-entry-snap/spec.md` · **Plan**: `specs/196-dock-live-entry-snap/plan.md`
**Pass**: 1 of 3 · **Date**: 2026-11-15

## What was checked

Every traceability row in `plan.md`, by the method it declared:

- **`test` rows** — ran both suites against the final code:
  `tests.e2e.test_obs_dock_snap` 9/9 OK; `tests.e2e.test_obs_dock` 8/8 OK
  (regression, SC-006). The 15 rows marked `test` map onto the 9 distinct E2E tests —
  the US rows cite the same tests as the SC rows behind them.
- **`inspection` rows** — read the code and the diff:
  - FR-001 off-top branch: `liBottom <= viewTop → glideScroll(liTop)`; the live
    inner is `is-open` before the snap (`sync()` sets it in the same pass).
  - FR-002/FR-003 off-bottom branch: `liTop >= viewBottom →
    glideScroll(liBottom - clientHeight - protrude)`, `protrude` = the band's
    `bottom: -10px` magnitude, `0` when `nextBand.hidden`.
  - FR-004 partly-visible branch: `scheduleCenter()` — today's centre formula.
  - FR-005 trigger moments: the guard is `live && !morphing` inside `sync()`;
    `sync` is subscribed at boot (first paint) and on every state notice; the
    morph's finish goes through `finishMorph → centerRow(node)` (see C-05).
  - FR-006 `cancelPendingCenter` is bound to `wheel` and `pointerdown` on
    `runBody` (`:617-618`) and cancels `glideFrame` — the snap's glide included.
  - FR-008 `git diff --stat` shows no CSS and no template change.
  - FR-009 the `if (dock.goto)` branch returns at `:1080`, before the parking
    code; `test_go_to_keeps_todays_behaviour` is green.
- **`manual` rows** — the two quickstart hand checks (wheel-cancel feel,
  reduced-motion visual) are marked checked by inspection: no command can run
  them; the owner runs them on the live dock per `quickstart.md`.

## Findings

| ID | Type | Finding | Disposition |
| --- | --- | --- | --- |
| C-001 | `contradicts` (code) | The first bottom-snap target `liBottom - clientHeight` parked the li's foot flush at the scroller's bottom edge, which trips `updateBand`'s hide rule (`liveEntry.bottom <= box.bottom + 6`, `:645`) — the band vanished, violating FR-002. | **Fixed in pass** — target is now `liBottom - clientHeight - protrude`, the band's `bottom: -10px` magnitude (0 when hidden). Geometry dump after the fix: `scrollTop 173 == 951 - 768 - 10`; band rect 797.81..833, bottom flush at the scroller edge 833, visible, labelling "Entry 21"; the entry's content foot meets the band's top inside the inner's 7 px bottom padding. |
| C-002 | `contradicts` (test) | The off-bottom E2E projected the LAST entry, so FR-002's band-visible path was never exercised — only FR-003's hidden band. | **Fixed in pass** — the test now projects entry 20 of 28 (`_project_entry(dock, 20)`) and asserts the band is visible, bottom-flush at the scroller edge, and names "Entry 21". |
| C-003 | `contradicts` (test) | The off-bottom test evaluated `.nextband`'s rect and `#runBody`'s bottom BEFORE `_wait_scroll_top`, so it asserted mid-glide geometry (band bottom 908.125 at scrollTop 0) instead of the post-snap rest (833). | **Fixed in pass** — the viewport-relative evaluates moved after `_wait_scroll_top`; the layout-relative ones (`offsetTop`, `clientHeight`) stay before it. |
| C-004 | `partial` (spec artifact) | `plan.md`'s traceability cited `tests/e2e/test_obs_dock.py::SnapTests::` — wrong file and class — and SC-002's note described a measurement ("li bottom vs band top") the test does not make; FR-009's note cited line 1069. `analysis.md`'s F-001/F-002 dispositions and `tasks.md`'s T003/T005 carried the sketch's formulas (`scrollHeight` floor, `layoutTop + 4`, `bandHeight + 4`), and `tasks.md`'s header split said "4 test" against 9 written tests. | **Fixed in pass** — paths, notes, formulas and the split corrected to the shipped code. |
| C-005 | `partial` (spec wording) | FR-005 names "the morph's finish" among the snap's trigger moments, but `finishMorph` re-centres via `centerRow(node)` with no entirely-out-of-view check. | **Accepted — vacuous moment.** The spec's own assumption records why: the morph's curve centres the arriving row by construction, so "entirely out of view" cannot hold at the finish. The observable content of FR-005 — the operator never sees the live entry entirely off-screen after a re-settle — holds. R14 carries the assumption. If a future morph can end off-screen, that is fresh demand, not this slice. |

No `missing` and no `unrequested` rows. No new requirement appeared in the code
that lacks a traceability row.

## Outcome

**Converged.** All 9 FRs verified by their declared method; the two E2E suites
are green against the final code; one accepted vacuous moment (C-005) and no
accepted behaviour gaps. Proceed to Fold.
