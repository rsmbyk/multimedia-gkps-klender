# Research: The first sidebar's idle rule, its deferral end and the fifteen-minute wait

**Spec**: `specs/199-sidebar-activity/spec.md`
**Unknowns remaining**: 0

Every decision below was probed in the repo's own Chromium (Playwright 1.47, the version in
`requirements-dev.txt`) before it was written down; the probe that decided it is quoted so a reader
can repeat it. No question was put to the owner at Plan: the three decisions that are the owner's
(the widened scope, the fifteen-minute number, the patch level) were answered at Specify and are
recorded in the spec's Clarifications and A9.

## D001 — `scroll` is observed in the capture phase on both surfaces

- **Decision**: bind the six-name list with `{ capture: true, passive: true }` to `.rail` and
  `#panel`. `scroll` then reaches the panel for any descendant scroller; the five bubbling events
  behave as before.
- **Rationale**: `scroll` fires at its target and does not bubble, so a listener on `#panel` never
  sees `#panelBody`'s scroll — the scroller is a descendant, not the element itself. Capture runs
  from the window down to the target, so the panel's capture listener sees it. The probe:

  ```html
  <div id="panel"><div id="panelBody" style="height:100px;overflow-y:auto">
    <div style="height:2000px">tall</div></div></div>
  <script>
    var log = [], body = document.getElementById('panelBody'), panel = document.getElementById('panel');
    body.addEventListener('scroll', function (e) { log.push(['target', e.eventPhase, e.bubbles]); });
    panel.addEventListener('scroll', function (e) { log.push(['panel-capture', e.eventPhase, e.bubbles]); }, true);
    panel.addEventListener('scroll', function (e) { log.push(['panel-bubble', e.eventPhase, e.bubbles]); });
    body.scrollTop = 120;
  </script>
  ```

  Result: `[['panel-capture', 1, false], ['target', 2, false]]` — capture sees it, bubble does not,
  and the event reports `bubbles: false`. The same probe with a wheel confirmed the pointer path
  (`wheel` is a separate, already-bound event).
- **Alternatives considered**:
  - *Move the listener onto `#panelBody`* — rejected: it hardcodes today's scroller and would miss
    a second one the markup gains later; the spec names the surface, not the element.
  - *Listen for `wheel` only* — rejected: a scrollbar-thumb drag emits no `wheel`, which is the
    exact gesture SC-001 is about, and keyboard scrolling emits none either.
  - *Listen on `document` in capture* — rejected by FR-009: it would make every scroll in the app
    activity, including `#chapters` and the stage.
- **Provenance**: research.

## D002 — the deferral end is a `MutationObserver` plus the existing `focusout`, not a seventh event

- **Decision**: keep a module-scope `deferralHeld`. It is set when a deferral is seen (the
  observer, or the expiry path finding `idleCollapseIsDeferred()` true). A `MutationObserver` on
  `document.body` with `attributes: true, subtree: true, attributeFilter: ['class', 'open']` calls a
  function that, when the four conditions are all false and `deferralHeld` is set, clears the flag
  and calls `scheduleIdleCollapse()`. The panel's `focusout` handler keeps its current restart for
  the focus-leaves case.
- **Rationale**: the four conditions are *state* — `.ui.modal.visible` and `.is-dragging` are
  classes, `dialog[open]` is an attribute — and all three elements live under `document.body`. A
  subtree observer with a two-name filter sees exactly those transitions and nothing else. The
  callback is a microtask, so the restart happens in the same task the class left. Probe: a body
  observer with that filter recorded the class add on a nested element immediately; under
  `page.clock.install` the callback still ran inside the same `evaluate` (the fake clock replaces
  timers, not microtasks), so the E2E's 899/900 s pins are exact rather than poll-slack.
- **Alternatives considered**:
  - *Hook `endDrag` in `static/web/reorder.js`* — rejected: couples two scripts, covers only the
    drag and leaves dialogs and modals behind, and would need the same special case in every future
    deferral source.
  - *Listen for `pointerup`, `dragend` or the dialog's `close` event* — rejected by FR-010/A11: it
    would make an event in `#chapters` (or in a dialog) restart the interval, which is a seventh
    activity event by the back door, and a pointer released over the stage would restart it too.
  - *Poll `idleCollapseIsDeferred()` every 1 s and restart then* — rejected by A10: up to one second
    of slack, which is what the old pins encoded. The poll stays for the expiry path (FR-005), not
    for the end.
- **Provenance**: research.

## D003 — the wait is one constant, 900 000 ms

- **Decision**: `var IDLE_COLLAPSE_DELAY = 900000;` at `static/web/reading.js:64`. Nothing else
  reads it; no setting, query parameter, data attribute or notification is added.
- **Rationale**: 072 put "a new persistent timeout setting or a notification about auto-collapse"
  out of scope, and the owner asked for a number, not a preference. One occurrence makes SC-005's
  grep meaningful and keeps the E2E's fake-clock spans reading directly as the rule. The 720 px
  narrow cut-off is a different number and stays.
- **Alternatives considered**:
  - *A `data-` attribute or a Django setting* — rejected: it would be a second source of truth and
    a surface the spec explicitly excludes.
  - *A per-section delay* — rejected: no requirement distinguishes sections; the collapse outcome
    already does (mini for Alkitab, closed otherwise).
- **Provenance**: owner decision, 2026-11-18 ("also increase the timer to 15 minutes"), recorded in
  spec A12 and the Clarifications.

## D004 — the E2E scrolls with `scrollTop`, and the negative case uses a real second-sidebar scroll

- **Decision**: `document.getElementById('panelBody').scrollTop = 240` drives SC-001; the wheel test
  uses `page.mouse.wheel` over the panel; the negative test sets `#chBody.scrollTop` (asserting it
  moved) and wheels over the stage.
- **Rationale**: `scrollTop` dispatches `scroll` synchronously, with no `wheel`, no pointer and no
  animation frame, which is the defect's exact shape. Probe: after `scrollTop = 200`, a `scroll`
  listener had fired once and a `wheel` listener zero times, before any `run_for`. `#chBody`
  overflows on the Bible chapter page — the existing
  `test_sidebar_click_never_scrolls_the_list` asserts its `scrollTop` can be greater than 0 — so
  the negative test scrolls a list that really moves.
- **Alternatives considered**:
  - *Drag the scrollbar thumb with the mouse* — rejected: overlay scrollbars make the thumb's
    geometry theme- and platform-dependent, and the emitted event is identical to `scrollTop`'s.
    The manual check in `quickstart.md` is where a person can see the thumb move, but the suite
    does not depend on it.
  - *`scrollIntoView`* — rejected: it can animate and its timing depends on the scroll-behaviour
    style; `scrollTop` is one synchronous assignment.
- **Provenance**: research.

## D005 — the deferral-end tests keep the existing fixtures and add one name to the drag fixture list

- **Decision**: `test_short_drag_restarts_sidebar_idle_timeout` joins the `self.idle_drag_entry`
  condition at `tests/e2e/test_reading.py:143`; the drag and dialog tests keep their names and
  reshape their clocks.
- **Rationale**: `ReadingE2ETests.setUp` creates the draggable Tata Ibadah entry only for the test
  name that needs it, because fixtures are committed per test and Playwright runs only after the
  ORM work. A new test needs its name in that list; no other fixture changes.
- **Alternatives considered**: create the entry unconditionally — rejected: it changes every test's
  fixture and the reorder surface for tests that do not drag.
- **Provenance**: research (the existing pattern at lines 143-148).

## Open

None.
