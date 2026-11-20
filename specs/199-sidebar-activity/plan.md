# Implementation Plan: The first sidebar counts the scroll it promised, and a deferral gives its interval back

**Spec**: `specs/199-sidebar-activity/spec.md`
**Branch**: `fix/199-sidebar-activity`
**Bump**: `patch` (1.33.0 → 1.33.1)
**Preview**: n/a — the slice moves nothing on screen; spec `## UI/UX` records the reason (no control,
no label, no colour, no number the operator can see).

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Vanilla ES5 JavaScript in `static/web/reading.js`; Python 3.12 only in the E2E module. Django templates, CSS, models and views untouched |
| Primary dependencies | none added; the slider uses the DOM APIs the file already uses (`addEventListener`, `setTimeout`, `MutationObserver`) |
| Storage | none — no model, no migration, no request, no `localStorage` key; the delay is a script constant |
| Testing | Playwright (Python) E2E through Django's `StaticLiveServerTestCase`, with `page.clock.install` for the fifteen-minute spans — the repo's user-visible acceptance harness |
| Target platform | Chromium at ≥ 720 px wide (the narrow drawer arms no timer and is asserted unchanged); light and dark share the code path |
| Project type | Server-rendered Django page with one behaviour script; the slice touches that script and its E2E |
| Performance goals | no per-frame work; one `MutationObserver` on `document.body` limited to `class` and `open` attributes, and six listeners per surface as today |
| Constraints | exactly six activity events, two surfaces; `scroll` in capture; the 720 px cut-off, the three eligibility guards and the 1 s expiry poll stay; the deferral end restarts at the moment it clears; one constant, no setting |
| Scale / scope | ~15 lines changed or added in one script; 4 new E2E tests and 9 existing idle E2E tests scaled (one module) |

## Constitution Check

No `CONSTITUTION.md` exists at the repo root (SDD-01: the constitution is optional and never
auto-created), so this table has no principles to check against. The repo's standing constraints
still apply and are met: no person's name in the artifacts, no secret, no new dependency, no
capability invented beyond spec 072's sentence.

Re-checked after Phase 1: pass — the design adds one platform observer and no dependency; the
activity list stays closed at six, the deferral end is read from the condition itself, and nothing
in the design needs the second sidebar, the stage, a dialog or a modal to become an activity
surface.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entities: the slice changes *when* one timer restarts, nothing is stored
  or transmitted. The two invariants (one pending timer; a held deferral gives a full interval) are
  recorded there because they are checkable, not because they are modelled.
- `contracts/` — `none`: the reading page exposes no interface of its own; the behaviour is
  internal DOM wiring with no request, response or event contract crossing the process boundary.
- `quickstart.md` — how to run the E2E module, which five tests to read first, and the one manual
  look at the constant.

### Decisions carried into the design

- **D001 — one closed event list, bound in capture on both surfaces.** `['pointerdown',
  'pointermove', 'keydown', 'focusin', 'wheel', 'scroll']` is written once; the loop binds each name
  to `.rail` and `#panel` with `{ capture: true, passive: true }`. Capture changes nothing for the
  five events that already bubble and is the whole fix for `scroll`, which never reaches a bubble
  listener on the panel because the scroller (`#panelBody`) is a descendant.
- **D002 — the deferral end is observed, not listened for.** A `MutationObserver` on
  `document.body` (`attributes: true, subtree: true, attributeFilter: ['class', 'open']`) plus the
  existing `focusout` handler. A module-scope `deferralHeld` is set when the observer or the expiry
  path sees a deferral, and cleared — with `scheduleIdleCollapse()` — the first time the four
  conditions are all false. The observer callback is a microtask, so the restart lands in the same
  task the class or attribute left; the 1 s expiry poll stays as the spec's backstop, not as the
  mechanism.
- **D003 — the delay is one constant.** `IDLE_COLLAPSE_DELAY = 900000` at `reading.js:64`, read
  only by `scheduleIdleCollapse`. No setting, query parameter, data attribute or notification; the
  720 px cut-off is untouched.
- **D004 — the test scrolls with `scrollTop`.** `#panelBody.scrollTop = 240` dispatches the same
  synchronous `scroll` a scrollbar-thumb drag emits, with no `wheel` and no pointer, which is
  exactly the defect's shape. The thumb itself is not a stable test target (overlay scrollbars),
  and it would prove no more than the event does.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `tests/e2e/test_reading.py` — `test_panel_scroll_restarts_sidebar_idle_timeout` | `test` | scroll at 30 s; open at 899 s, mini at 900 s. Red on `develop` (collapses at 60 s) |
| US1/AC1 (by hand) | the live reading page at 1280 px — `#panelBody`'s scrollbar | `manual` — drag the thumb, then read `scrollTop > 0` and `html[data-nav]` still `open`; the fifteen-minute span itself is not waited | proves a real thumb emits the event the test synthesises |
| US1/AC2 | same module — `test_panel_wheel_restarts_sidebar_idle_timeout` | `test` | wheel at 40 s after a pointer move at 30 s, so only the wheel can explain the 899 s pin; guard, green on both |
| US1/AC3 | `static/web/reading.js` — the six-name list and its two bindings | `inspection` — `keydown` is still in the list and still bound to `#panel`; a key that scrolls also emits the `scroll` US1/AC1 pins | no separate test: `keydown` is the pre-existing path, and focusing the list to isolate it would arm the focus deferral |
| US1/AC4 | browser behaviour + `scheduleIdleCollapse` | `inspection` — the handler runs only on an event; Chromium emits no `scroll` when `scrollTop` is already at a limit | nothing to assert that a missing event did not restart |
| US2/AC1 | `tests/e2e/test_reading.py` — `test_short_drag_restarts_sidebar_idle_timeout` | `test` | drag at 14:00, release at 14:05; open at release + 899 s, closed at + 900 s. Red on `develop` |
| US2/AC2 | `tests/e2e/test_reading.py` — `test_drag_defers_sidebar_idle_collapse_then_restarts` | `test` | drag held past 900 s; after release open at 899 s, closed at 900 s (pins moved from 59/60 s) |
| US2/AC3 | `tests/e2e/test_reading.py` — `test_dialog_defers_sidebar_idle_collapse_then_restarts` | `test` | dialog held past 900 s; close, then 899/900 s — the focus return and the `[open]` removal now agree |
| US2/AC4 | the same drag and dialog tests | `test` | both now measure from the moment the interaction ends, with no poll second in the span |
| US3/AC1 | `tests/e2e/test_reading.py` — `test_second_sidebar_and_stage_activity_does_not_restart_sidebar_idle_timeout` | `test` | `#chBody` scrolled (asserted > 0) at 30 s; open at 899 s, mini at 900 s |
| US3/AC2 | the same test | `test` | a wheel at stage coordinates (≈ 900, 450 at 1280 px) at 30 s; same pins |
| US3/AC3 | the dialog test | `test` | typing is not separately sent; the dialog is open across the expiry and the panel stays open |
| US3/AC4 | `tests/e2e/test_reading.py` — `test_narrow_layout_keeps_matching_sidebar_open` | `test` | 390 px, drawer open, `#chBody` scrolled once (asserted > 0), 900 s elapsed, still open |
| FR-001 | `static/web/reading.js` — the event list and loop | `test` → panel scroll, wheel, rail activity and the negative test | six names, two surfaces; no seventh |
| FR-002 | same — `capture: true` on the panel binding | `test` → `test_panel_scroll_restarts_sidebar_idle_timeout` | the probe in `research.md` shows capture sees the descendant scroll and bubble does not |
| FR-003 | `static/web/reading.js` — the `focusout` handler | `test` → `test_sidebar_timeout_waits_while_filter_has_focus` | unchanged; a focus that leaves restarts, an inner move does not |
| FR-004 | `static/web/reading.js` — no listener outside the two surfaces | `test` → the negative test | `#chBody` and stage wheel restart nothing |
| FR-005 | `static/web/reading.js` — `idleCollapseIsDeferred` + the 1 s poll | `test` → the drag and dialog tests | deferral itself does not restart |
| FR-006 | `static/web/reading.js` — `scheduleIdleCollapse` guards | `test` → `test_sidebar_for_other_section_stays_open_when_stage_is_bible`, `test_narrow_layout_keeps_matching_sidebar_open` | wide, `open`, matching section |
| FR-007 | `static/web/reading.js` — `visibilitychange` pair | `inspection` — the hidden branch still cancels and the visible branch still arms | not changeable in Chromium's E2E without CDP overrides |
| FR-008 | `static/web/reading.js:64` | `test` → `test_matching_idle_bible_sidebar_collapses_to_mini` at 899/900 s | 900 000 ms; the 720 px cut-off is untouched |
| FR-009 | `static/web/reading.js` — one list, two `addEventListener` calls | `inspection` — no `document`/`window` activity listener; widening the surface is a visible edit | grep: the six names occur once |
| FR-010 | `static/web/reading.js` — `deferralHeld` + observer + expiry branch | `test` → the short-drag, drag and dialog tests | restart at the condition clearing, not on a poll tick |
| SC-001 | panel scroll | `test` → `test_panel_scroll_restarts_sidebar_idle_timeout` | |
| SC-002 | wheel, pointer, keyboard, focus | `test` → wheel, rail activity and focus tests | keyboard is inspection (US1/AC3) |
| SC-003 | second sidebar and stage | `test` → the negative test | |
| SC-004 | deferral | `test` → drag and dialog tests | |
| SC-005 | 899/900 s everywhere; one constant | `test` → the nine scaled tests; `inspection` → `grep -n IDLE_COLLAPSE_DELAY static/web/reading.js` returns the declaration and its one read, and no `60000` remains | |
| SC-006 | short drag | `test` → `test_short_drag_restarts_sidebar_idle_timeout` | |
| SC-007 | interaction ends → full interval | `test` → drag and dialog tests | |
| SC-008 | everything else | `test` → full `tests/e2e/test_reading.py` | no control, class or template added |

**Verification split**: 26 test · 5 inspection · 1 manual

## Risks and their handling

- **The observer is too broad.** `class` churn elsewhere on the page could look like a deferral
  ending. The filter is `['class', 'open']`, the callback only acts on a `deferralHeld` that was
  set by the four conditions themselves, and a class change that leaves all four false while nothing
  was held does nothing. A theme switch touches `<html>`, outside the observed subtree; the reorder
  morph changes no class but `is-dragging`, which is the one being watched.
- **A drag added and cleared inside one task.** The observer then sees only the final state, and no
  timer task could have run between the two, so the old deadline is the correct one — this is not a
  gap, and real drags span input tasks.
- **The 1 s poll and the observer both restart.** If the timer expired while deferred, the poll may
  fire just after the observer already restarted; `scheduleIdleCollapse` cancels the previous timer
  first, so the later call can only push the deadline by its own arm, not shorten it. The pins would
  catch a regression: `test_drag_defers…` asserts 899 s open.
- **A future second rail scroller.** Already covered by the capture binding; no code change, noted
  in the script's comment.
- **Fifteen minutes makes the collapse rare in a service** (A12). Deliberate; no test asserts the
  old rhythm, and the single manual row checks the thumb's event, not the elapsed span.

## Project Structure

### Documentation

```
specs/199-sidebar-activity/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  checklists/requirements.md
```

### Source

```
static/web/reading.js          # the constant, the six-name list, capture binding, deferral observer
tests/e2e/test_reading.py      # 3 new tests, 9 idle tests scaled, drag/dialog pins reshaped
```

### Structure Decision

Both files already exist and already own this behaviour: `reading.js` holds `scheduleIdleCollapse`
and the activity wiring, and `tests/e2e/test_reading.py` holds every idle test at
`ReadingE2ETests`. No module is split out: the deferral observer needs `idleCollapseIsDeferred`
and `scheduleIdleCollapse`, both closed over by the same IIFE, and extracting them would create a
second place to keep the activity list honest.
