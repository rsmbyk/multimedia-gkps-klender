# Converge: reopening the projector window

**Slice**: `specs/141-projector-window-reopen`
**Pass 1 — 2026-10-27**

## What was checked

| Row | Method | Evidence |
| --- | --- | --- |
| FR-001 | test | `test_the_reopen_control_appears_only_while_the_service_is_on_air` — off air, on air, a second tab, hidden, released |
| FR-002 | test | `test_reopening_returns_the_window_to_the_screen_on_air` (`/projector` with no query, screen 4) and `test_reopening_writes_no_display_state` (stored JSON identical, `at` included) |
| FR-003 | test | `test_an_open_projector_window_is_focused_not_reloaded` — the window token survives and no second window appears |
| FR-004 | test | `test_stop_projecting_still_releases_with_the_control_present`; `test_closing_the_projector_window_leaves_the_display_alone` still green |
| FR-005 | inspection | markup in `multimedia/web/templates/reading/tatib.html` (34 × 34 box, 15 px glyph, `aria-label`/`title` "Open projector window"), the rule inside `@media (min-width: 721px)` in `components.css`; measured 34 × 34 in the app |
| FR-006 | test | `test_the_project_group_stays_inside_the_pane` (1440 and 1280, with and without media) |
| SC-001 | test | the reopened window reports `data-current-screen="4"` |
| SC-002 | test | `localStorage['gkps-display']` deep-equal before and after the press |
| SC-003 | test | `window.__gkpsReopenToken` still `'kept'`; `context.pages` unchanged |
| SC-004 | inspection | measured: 34 × 34, radius 9 px, glyph `#646357`, hover `#1F1F1D` / `#1C5C3C` / `rgba(31,31,29,.08)` |
| SC-005 | test | group right ≤ pane right at 1440 (spill −119.6 px) and 1280 (0 px, group 240 px wrapped) |
| SC-006 | test | at 425×900 both controls measure 0 × 0 |

**Suites run**: `tests/e2e/test_projector` — 62 tests, OK (7 new). `tests/e2e/test_reading` — 86
tests, 85 OK; the one failure is the known red test ITEM-137 (`test_the_panel_shows_its_empty_view_when_no_songbook_exists`,
the songbook empty-view copy from spec 129), reproduced identically in a `develop` checkout, so it is
not this slice's.

**Preview against the app**: the numbers the approved preview measured are the numbers the running
page returns — group 280.4 px and header 69.2 px at 1440×900; group 240 px, spill 0, header 111.2 px
at 1280×800; control 34 × 34; the phone draws only Media files (90.7 px). No divergence.

## Findings

| # | Type | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | missing | The projector page never finished adopting the stored service: `static/web/projector.js` assigned `savedScreensSignature` — a variable spec 136 removed when the offline library went — under `'use strict'`, so `adoptService` threw at that line before `done`. Evidence: the console reported `ReferenceError: savedScreensSignature is not defined`, the reopened page showed service 144 at screen 0 with `data-showing="false"`, and the fetched screens were already in the stage. After removing the dead assignment, the reopened window lands on screen 4 with the words up. | Fixed in this pass: the assignment is deleted (dead — nothing reads it). Code at fault, so it became a task (T006's scope) rather than a spec conflict. It restores spec 119's adoption behaviour that FR-002 depends on; `docs/spec/projector.md` is unchanged because no behaviour changed — the defect was that behaviour not working. |
| C2 | note | The capability file's R14 named only the Project control at the phone width; the new control must be covered by that rule. | Folded: R14's sentence now names both controls, and R15 states it again where the control is defined. |

No `contradicts` or `unrequested` gaps: every requirement and success criterion has its row, and
each row was checked by the method it declared.

## Outcome

Converged on pass 1, with C1 fixed and C2 folded. One pre-existing defect was found by this slice and
repaired; it is reported in the closing report as a card candidate if the owner wants it tracked
separately.

## History

- **2026-10-27 — pass 1** on the implemented slice: all 12 traceability rows checked by their declared
  method, both suites run, C1 found and fixed, C2 folded. 0 CRITICAL, 0 remaining gaps: converged.
