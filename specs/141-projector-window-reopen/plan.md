# Implementation Plan: a closed projector window can be reopened at the screen on air

**Spec**: `specs/141-projector-window-reopen/spec.md`
**Branch**: `feat/141-projector-window-reopen`
**Bump**: `patch`
**Preview**: `specs/141-projector-window-reopen/preview/preview.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 · Django 4.0 templates · ES5-style browser JS (`static/web/display.js`) · CSS (`static/styles/design/components.css`) |
| Primary dependencies | none added — Django's template engine, the existing display module, the existing design tokens |
| Storage | `localStorage['gkps-display']`, read only by this slice (spec 119) |
| Testing | Playwright (Python) E2E via `StaticLiveServerTestCase`; `tests/e2e/test_projector.py` |
| Target platform | desktop browsers; the control is a desktop control (≥721 px), like the Project control |
| Project type | server-rendered Django web app, no build step |
| Performance goals | no request added; the click opens a page that already exists and paints it from the stored state |
| Constraints | the state is browser-local and shared by every tab; the reading pane is swapped in place, so handlers stay delegated; no new route, no server state |
| Scale / scope | 1 template, 1 JS module, 1 stylesheet block, 7 E2E tests |

## Constitution Check

No `CONSTITUTION.md` exists, and SDD-01 makes it optional and never auto-created. The check is
therefore not applicable; the repo's own rules (delegated handlers, tokens, the 720 px breakpoint)
are honoured as constraints above.

Re-checked after Phase 1: pass — no principle to violate, and no dependency, route or stored value
is added.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity change; the display state the control reads and the DOM contract it
  joins.
- `contracts/` — `none` (no endpoint, payload, template variable or stored value).
- `quickstart.md` — the preview server, the E2E command, and how to see it in the running app.

The design in one paragraph: the template gains a second button in the existing `.read__project`
group — `data-project-window`, `data-projector-url="{% url 'web-projector' %}"`, `aria-label`/`title`
"Open projector window", an inline "pop out" glyph. `components.css` gives it the group's box at
34 × 34 with no padding, hides it by default, draws it only under
`.read__project[data-displaying="true"]` inside `@media (min-width: 721px)`, and lets the Tata Ibadah
group wrap inside its pane. `display.js` gains one branch in its delegated click listener: for
`[data-project-window]`, guard on the live state, then open the named window with an empty URL and
fill it only when it is blank; for the existing toggle nothing changes.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/templates/reading/tatib.html`, `static/web/display.js`, `components.css` | `test` → `tests/e2e/test_projector.py::ProjectorE2ETests::test_the_reopen_control_appears_only_while_the_service_is_on_air` | drawn only while this service is on air |
| FR-002 | `static/web/display.js` | `test` → `…::test_reopening_returns_the_window_to_the_screen_on_air` and `…::test_reopening_writes_no_display_state` | bare `/projector`, no adoption |
| FR-003 | `static/web/display.js` | `test` → `…::test_an_open_projector_window_is_focused_not_reloaded` | token survives; no second popup |
| FR-004 | `static/web/display.js` (release path unchanged) | `test` → `…::test_stop_projecting_still_releases_with_the_control_present` | Stop and a closed window keep spec 119 |
| FR-005 | `tatib.html`, `components.css` | `inspection` — the button's 34 × 34 box, 15 px glyph and "Open projector window" name; the show rule inside `@media (min-width: 721px)` | the phone half is also covered by SC-006's test |
| FR-006 | `components.css` | `test` → `…::test_the_project_group_stays_inside_the_pane` | 1440/1280 × media/no media |
| SC-001 | `display.js` | `test` → `…::test_reopening_returns_the_window_to_the_screen_on_air` | active screen index 4 |
| SC-002 | `display.js` | `test` → `…::test_reopening_writes_no_display_state` | `gkps-display` identical, `at` included |
| SC-003 | `display.js` | `test` → `…::test_an_open_projector_window_is_focused_not_reloaded` | `window` token + focus |
| SC-004 | `components.css` | `inspection` — computed box, colours and outline on the preview and in the app | numbers in `spec.md` §UI/UX |
| SC-005 | `components.css` | `test` → `…::test_the_project_group_stays_inside_the_pane` | group right ≤ pane right |
| SC-006 | `components.css` | `test` → `…::test_the_reopen_control_is_not_drawn_on_a_phone` | 425 px, with and without media |

**Verification split**: 10 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/141-projector-window-reopen/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/none.md  checklists/requirements.md
  preview/preview.html
```

### Source

```
multimedia/web/templates/reading/tatib.html      + one button in .read__project
static/web/display.js                            + one delegated branch and the open/focus helper
static/styles/design/components.css              + the icon button, its visibility gate, the group wrap
tests/e2e/test_projector.py                      + seven tests in ProjectorE2ETests
```

### Structure Decision

No new file in the product: the control belongs to the group the template already draws, the state
already has one writer module, and the stylesheet already owns the group's box. A separate script or
a new partial would add a second reader of `gkps-display` for one act.
