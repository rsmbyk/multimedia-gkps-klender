# Convergence: The first sidebar's idle rule, restored and set to fifteen minutes

**Spec**: `specs/199-sidebar-activity/spec.md`
**Pass**: 1 · **Checked**: every row of `plan.md`'s traceability table, by the method it declared
**Outcome**: converged

## Pass 1 — 2026-11-18

What was checked, row by row:

| Row | Method | Evidence |
| --- | --- | --- |
| US1/AC1 | test | `tests/e2e/test_reading.py::test_panel_scroll_restarts_sidebar_idle_timeout` — green; `#panelBody` overflows (888 px), a non-bubbling `scroll` at 30 s is followed by `open` at 899 s and `mini` at 900 s. Red with the capture flag removed: the bubble listener never sees the event. |
| US1/AC1 (thumb) | manual — checked by inspection | `quickstart.md` carries the by-hand steps (drag the panel's thumb, read `scrollTop > 0` and `data-nav = open`). The test dispatches exactly the event that drag emits; the list is asserted to be a real scroller. |
| US1/AC2 | test | `::test_panel_wheel_restarts_sidebar_idle_timeout` — green; a bubbling `WheelEvent` on the scroller restarts the interval: `open` at 899 s, `mini` at 900 s. Green before the fix, as predicted. |
| US1/AC3 | inspection | `static/web/reading.js:140` keeps `keydown` in the one six-name list; a key that scrolls emits `scroll`, which AC1 pins. No second list or key handler was added. |
| US1/AC4 | inspection | `reading.js:114-132` arms a timer only inside `setTimeout`; nothing runs on the absence of an event. Chromium emits no `scroll` at a list's limit, so there is no event to assert. |
| US2/AC1 | test | `::test_short_drag_restarts_sidebar_idle_timeout` — green; grip down at 14:00, release at 14:05, `open` at release + 899 s and `closed` at + 900 s. Red before the observer: the panel collapsed on the old load-time deadline. |
| US2/AC2 | test | `::test_drag_defers_sidebar_idle_collapse_then_restarts` — green; a drag held across 900 s keeps the panel open, and the release gives a full interval. |
| US2/AC3 | test | `::test_dialog_defers_sidebar_idle_collapse_then_restarts` — green; the dialog holds the panel open past the expiry, and closing it gives a full interval (five seconds of settle in the final pin for the focus return). |
| US2/AC4 | test | both deferral tests — green; measurement starts from the moment the interaction ends, not from an expiry poll tick. |
| US3/AC1 | test | `::test_second_sidebar_and_stage_activity_does_not_restart_sidebar_idle_timeout` — green; `#chBody` is scrolled (asserted > 0) at 30 s; collapse still lands at 900 s. |
| US3/AC2 | test | the same test — green; a real pointer and wheel over the stage restart nothing. |
| US3/AC3 | test | the dialog test — green; the panel stays open across the expiry while the dialog holds it, and restarts only when it ends. |
| US3/AC4 | test | `::test_narrow_layout_keeps_matching_sidebar_open` — green; at 390 px the drawer is opened, `#panelBody` is scrolled with the movement asserted, and 900 s elapse with the panel still open. |
| FR-001 | test | panel-scroll, wheel, rail-activity and negative tests — green; the six names appear once at `reading.js:140`, bound to two surfaces. |
| FR-002 | test | panel-scroll test; `reading.js:142-143` passes `{ capture: true, passive: true }` to both bindings. The browser probe in `research.md` records capture 1 / target 2 and `bubbles: false`. |
| FR-003 | test | `::test_sidebar_timeout_waits_while_filter_has_focus` — green; the `focusout` guard at `reading.js:145-148` still ignores moves inside the panel. |
| FR-004 | test | the negative test — green; no activity listener is registered on `#chapters`, `#read` or `document`. |
| FR-005 | test | the drag and dialog tests — green; `idleCollapseIsDeferred()` and the 1 s re-check at `reading.js:116-127` are unchanged except for setting `deferralHeld`. |
| FR-006 | test | section-mismatch and narrow-layout tests — green; the guards at `reading.js:112-113` and `:117-118` are untouched. |
| FR-007 | inspection — checked by inspection | `reading.js:170-172` — hidden cancels, visible arms; unchanged by this slice. |
| FR-008 | test + inspection | nine idle tests pinned at 899/900 s; `grep -n IDLE_COLLAPSE_DELAY static/web/reading.js` gives `:65 = 900000` and its one read at `:131`, with no `60000` in the file. |
| FR-009 | inspection — checked by inspection | the event list at `:140` and the two bindings at `:142-143`; the `window` scroll listener at `:1445` saves a results-page snapshot and the `document` keydown at `:1948` handles Escape — both predate the slice and neither reports activity. |
| FR-010 | test | short-drag, drag and dialog tests — green; `reading.js:154-168` restarts when the conditions clear, never from `pointerup`, `dragend` or a click. |
| SC-001 | test | panel-scroll test (red before the fix, green after). |
| SC-002 | test | wheel, rail-activity, focus, drag and dialog tests; keyboard is the inspection row US1/AC3. |
| SC-003 | test | the negative test. |
| SC-004 | test | the drag and dialog tests. |
| SC-005 | test + inspection | the nine rescaled idle tests and the constant grep above. |
| SC-006 | test | short-drag test. |
| SC-007 | test | drag and dialog tests. |
| SC-008 | test | full `tests.e2e.test_reading.ReadingE2ETests`: 82 tests, all slice rows green. One unrelated red — `test_the_panel_shows_its_empty_view_when_no_songbook_exists` — reproduces on unmodified develop and is already carded as ITEM-137. |

## Findings

| # | Type | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | observed consequence | The two new event tests dispatch `Event('scroll')` and `WheelEvent('wheel')` rather than driving hardware through Playwright. A real `scrollTop` write is flushed by Chromium at an arbitrary frame, which under a fake clock landed inside the 899-second wait and restarted the timer; a real `mouse.wheel` was not repeatable under a loaded suite. | left as is: the events are the exact DOM events the listener must catch, the list is asserted to be a real scroller, and `quickstart.md` carries the by-hand thumb check. No requirement names the input device (spec A6). |
| 2 | observed consequence | The dialog test's final pin allows five seconds, and the wheel guard's allows one, because closing a dialog also returns focus to its opener and the faked clock ticks in real time between Playwright calls. The open-at-899-second pins remain exact. | left as is; recorded in `tasks.md` T005/T008. The interval is still 900 s from the last activity, which is what FR-010 asserts. |
| 3 | environment | `manage.py test --exclude-tag=e2e` needs `_static/` collected in a fresh worktree or nine Django tests error on a missing manifest entry; after `collectstatic` the 642-test fast lane has the same 11 pre-existing failures as develop. | left as is; recorded in `quickstart.md` and T012. No application code is involved. |

No `missing`, `partial`, `contradicts` or `unrequested` gap was found. The red tests on the pre-fix
code (`scroll` without capture, short drag without the observer) are this slice's own defects and
are green with the fix; the guards pass on both sides by design.

## Suite

- `tests.e2e.test_reading.ReadingE2ETests` — 82 tests, 81 green; the single red is ITEM-137,
  reproduced on unmodified develop.
- `manage.py test --exclude-tag=e2e` — 642 tests, the same 11 pre-existing failures as develop
  after `collectstatic` (diff of the failure name lists is empty).
