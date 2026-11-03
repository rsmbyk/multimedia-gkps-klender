# Implementation Plan: the active Tata Ibadah lasts only the browser session

**Spec**: `specs/184-display-session-scope/spec.md`
**Branch**: `fix/184-display-session-scope`
**Bump**: `patch`
**Preview**: `n/a — no appearance changes; the live walkthrough is the app restarted (spec §UI/UX)`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 · Django 4.0 · browser JavaScript (plain IIFEs, no build step) |
| Primary dependencies | none new — Django, Django REST Framework, WhiteNoise, Playwright for the E2E |
| Storage | `localStorage['gkps-display']` (the state) + a `gkps-session` session cookie (the marker) |
| Testing | Django `LiveServerTestCase` + Playwright (Python); existing `test_obs_*`, `test_projector`, `test_reading` suites |
| Target platform | Chromium-family browsers and OBS's embedded CEF; the four server-rendered surfaces |
| Project type | server-rendered web application, no client build |
| Performance goals | no measurable cost: one cookie string read per state read, one write per mint |
| Constraints | state never reaches the server; no appearance change; spec 119's in-session rule kept (owner, Clarify 2026-11-03) |
| Scale / scope | one operator browser at a time; the stored object is under 100 bytes |

## Constitution Check

`CONSTITUTION.md` does not exist in this repository and is never auto-created (SDD-01). There is no
principle set to check against.

Re-checked after Phase 1: nothing to re-check — no constitution, no principle added.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the display state (with `session`) and the session marker, their validation and
  invariants.
- `contracts/none.md` — no external interface; the internal seam between the four surfaces is
  recorded there.
- `quickstart.md` — the throwaway database, the test commands, and the by-hand restart walkthrough.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/display-session.js` (`owns`), `static/web/display.js`, `static/web/projector.js`, `static/web/obs-overlay.js` | `test` → `tests/e2e/test_display_session.py::test_a_state_from_an_earlier_session_paints_nothing` | a foreign stamp reads as no state |
| FR-002 | `static/web/obs-overlay.js` (`readState`, `sync`), `templates/reading/obs_overlay.html` | `test` → `…::test_first_paint_never_shows_a_prior_session_state` | a `MutationObserver` installed from document start counts plates added |
| FR-003 | `static/web/display-session.js` (`stamp`), `display.js`/`projector.js` (`write`) | `test` → `…::test_the_state_carries_the_session_of_its_writer` | stamp equals the cookie after every write |
| FR-004 | `static/web/display.js`, `static/web/projector.js`, `static/web/obs-overlay.js` (unchanged verbs) | `test` → `…::test_a_reload_inside_the_session_keeps_the_display`, `…::test_every_surface_closed_and_reopened_keeps_the_display`; plus the existing `test_obs_dock`, `test_obs_overlay`, `test_projector` suites | catch-up and every verb unchanged |
| FR-005 | `static/web/display-session.js` (the value minted), `display.js` (write) | `test` → `…::test_the_marker_carries_no_display_data` | the cookie holds one opaque id; no service/screen text |
| FR-006 | `static/web/display-session.js` (the in-page fallback) | `test` → `…::test_a_surface_without_cookie_storage_still_paints` | `document.cookie` is blanked by an init script; the page still paints, a reload starts idle |
| FR-007 | `static/web/display.js` (`hide`, `release`), `static/web/projector.js` (`toggleWords`) | `test` → existing `tests/e2e/test_obs_overlay.py::test_hide_empties_the_overlay_and_nothing_is_focusable`, `tests/e2e/test_projector.py::test_stop_projecting_still_releases_with_the_control_present` | the two stop verbs are untouched |
| FR-008 | `static/web/display-session.js` (`owns`) | `test` → `…::test_a_state_with_a_foreign_stamp_reads_as_no_state` | hand-set value, no transition involved |
| FR-009 | `static/web/display-session.js` (`owns`), three readers | `test` → `…::test_a_state_written_before_this_slice_reads_as_no_state` | a state with no `session` |
| FR-010 | `static/web/display-session.js` (`stamp`: write, then re-read) | `test` → `…::test_two_surfaces_minting_together_agree_on_one_session` | best effort on the interleaving; the invariant is deterministic |
| SC-001 | the three surfaces | `test` → `…::test_a_browser_restart_ends_the_session` | a real `launch_persistent_context` restart; 0 overlay children, 0 pills, projector not showing |
| SC-002 | `static/web/obs-overlay.js` | `test` → `…::test_first_paint_never_shows_a_prior_session_state` | 0 plates attached from document start |
| SC-003 | `static/web/display.js` and the channel | `test` → `…::test_every_surface_closed_and_reopened_keeps_the_display`; the existing suites | spec 119 kept inside the session |
| SC-004 | `static/web/display-session.js` | `test` → `…::test_the_marker_carries_no_display_data` | one opaque value; no display text |
| SC-005 | `display.js::read`, `obs-overlay.js::readState` | `test` → `…::test_a_state_with_a_foreign_stamp_reads_as_no_state` | both readers return the empty state |
| US1/AC1 | the three surfaces | `test` → `…::test_a_browser_restart_ends_the_session` | every surface idle after a restart |
| US1/AC2 | `static/web/obs-overlay.js` | `test` → `…::test_first_paint_never_shows_a_prior_session_state` | never a frame |
| US1/AC3 | `static/web/display.js` (`show`) | `test` → existing `tests/e2e/test_obs_dock.py` projection cases | the first act still works |
| US2/AC1 | `static/web/obs-overlay.js` (`sync`), `display.js` (channel) | `test` → existing `tests/e2e/test_obs_overlay.py::test_a_liturgy_text_wears_a_plate_with_its_title_and_quieter_leader_lines` | catch-up on open |
| US2/AC2 | the dock + overlay | `test` → `…::test_a_reload_inside_the_session_keeps_the_display` | the overlay never blanks |
| US2/AC3 | `localStorage` + the cookie | `test` → `…::test_every_surface_closed_and_reopened_keeps_the_display` | the owner's answer, proven |
| US2/AC4 | `display.js`, `projector.js` verbs | `test` → existing `test_obs_overlay` hide/flip and `test_obs_dock` step cases | hide, show, flip, step, release |
| Assumption — OBS restart | OBS's own CEF | `manual` — open OBS with the dock and the overlay added, project a service, quit OBS, start it again; both surfaces are idle | CEF does not persist session cookies (research D008); OBS cannot be driven from this suite |

**Verification split**: 22 test · 0 inspection · 1 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| (none) | — | — |

## Project Structure

### Documentation

```
specs/184-display-session-scope/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/none.md  checklists/requirements.md
  preview/ — not created: the spec records `n/a — no appearance changes`
backlog/items/ITEM-188-display-session-scope.md   the card, at the repo's board
```

### Source

```
static/web/display-session.js   new — the marker: current, stamp, owns
static/web/display.js           read() validates; write() stamps (the dock and every reading page)
static/web/projector.js         read() validates; write() stamps (its own store)
static/web/obs-overlay.js       readState() validates (listen-only)
multimedia/web/templates/reading/base.html          + display-session.js
multimedia/web/templates/reading/obs_dock.html      + display-session.js
multimedia/web/templates/reading/projector.html     + display-session.js
multimedia/web/templates/reading/obs_overlay.html   + display-session.js
tests/e2e/test_display_session.py   new — the boundary, both directions
```

### Structure Decision

The rule lives in one new file beside the existing state module rather than in each surface, because
the three readers must answer identically and drift between copies is the failure mode this slice
exists to prevent. The four templates load it immediately before their surface script; no build
step, no template context, no server change. The test module sits in `tests/e2e/` with the other
browser suites because the behaviour is only observable across pages and across a browser restart.
