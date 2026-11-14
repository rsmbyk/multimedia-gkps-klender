# Implementation Plan: the dock's Go To — one detour state, three surfaces

**Spec**: `specs/185-dock-goto/spec.md`
**Branch**: `feat/185-dock-goto`
**Bump**: `patch` — 1.26.2 → 1.26.3. Twenty-three of the repo's twenty-six plans take `patch`,
and the two neighbours that touched this same state (183, 184) are `patch`; the Go To already
exists on the projector, so this extends one surface and shares one pointer rather than adding a
capability nobody had.
**Preview**: `specs/185-dock-goto/preview/` — `index.html` (the dock's states) and `sync.html`
(the three surfaces following one state), both self-contained and opened directly.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript, ES5-era IIFEs in `static/web/` (no build step); Python 3.12 / Django 4.0 for the template that carries the new control. No view or model changes. |
| Primary dependencies | none new. `static/web/projector-library.js` (the lookup, already shipped), the three existing `/projector/goto/*` payloads, `localStorage`, `BroadcastChannel`, `static/web/display-session.js` (spec 184). |
| Storage | `localStorage['gkps-display']`, one new field (`goto`). No new key, no server state, no migration. |
| Testing | Django's test runner for any view-level regression, and Playwright (Python) E2E under `tests/e2e/` — the repo's harness for user-visible behaviour. |
| Target platform | OBS's Chromium (CEF) dock panel at 320 / 400 / 520 px wide; projector and caption overlay at 1920 × 1080. |
| Project type | Django app, server-rendered templates plus vanilla JS modules; no bundler. |
| Performance goals | Typing in the band: 0 requests (FR-005). One selection: 1 request (SC-001). A verse step inside the loaded chapter: 0; a chapter crossing: 1. One state change reaches every surface in one channel message (US2/AC1). The index is 29 KB gzipped, read once per dock page (US1/AC1). |
| Constraints | No new endpoint, no new storage key (FR-013). The state stays a pointer — no verse text or lyric in it (FR-001, SC-005). The projector's detour look and its `G` panel stay as they are (FR-010). The dock's transport bar stays one 40 px line with its chips and arrows centred (UI/UX). The session stamp is inherited, not re-implemented (FR-003). |
| Scale / scope | 4 user stories, 19 functional requirements, 6 success criteria, 15 acceptance scenarios. The slice touches 4 JS modules, 1 stylesheet, 1 template, and adds 2 E2E modules. |

## Constitution Check

The repo carries no `CONSTITUTION.md`; the standing principles are the ones its own documents
declare — `AGENTS.md`, `docs/PROCESS.md`, and the capability files under `docs/spec/`.

| Principle | Status | Note |
| --- | --- | --- |
| The display state is browser-local and never server state (`docs/spec/display-state.md`) | pass | `goto` is one more field in the same object; nothing crosses the network but the pointer. |
| One state, one channel: surfaces catch up rather than keep private copies (`display-state` R1) | pass | The projector's private `detour` is retired; `detour` survives only as a payload cache keyed by the state (D007). |
| No new endpoint; content is fetched from what exists (spec 136) | pass | FR-013. |
| The session bounds the state's life (spec 184) | pass | No new mechanism: `GKPSDisplaySession.owns()` already gates `read()`. |
| Behaviour is recorded in a capability file at Fold | pass | `display-state/R2` added; `projector/R1` and `R5`, `overlay/R1` modified; `docs/spec/dock.md` created (D010). |
| Previews are built from the product's own components | pass | Both pages link `static/styles/design/*` and carry the dock's real markup; the sync page paints with the projector's and overlay's own rules. |
| Tests prove user-visible behaviour through the repo's Playwright harness | pass | Two E2E modules; the verification split below is 37 test · 3 inspection · 0 manual. |
| No personal names in repo artifacts | pass | Roles only. |

Re-checked after Phase 1: **pass** — no violation needs the Complexity Tracking table.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Ten decisions; the two that shape the code are
D001 (the return place is not duplicated in `goto`) and D007 (the projector's `detour` becomes a
cache, not memory).

## Phase 1 — Design

- `data-model.md` — the `goto` entity (song and passage), the band's query state, the block's
  rows, and the invariants the state must hold.
- `contracts/` — `display-state.md`: the stored shape, the verbs and the one new channel message;
  `README.md` names what is exposed and what stays internal.
- `quickstart.md` — the stack, the two preview probes, and the targeted E2E runs.

## Traceability

Components are the preview's: the head's control, the band, the layer, the block, the transport.
`tests/e2e/test_dock_goto.py` owns the dock's own behaviour; `tests/e2e/test_goto_shared_state.py`
owns agreement between surfaces.

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/display.js` (`read`, `write`) | `test` → `tests/e2e/test_goto_shared_state.py::test_the_stored_state_carries_no_verse_words` | shape asserted field-by-field; no text in it |
| FR-002 | `static/web/display.js` (`show`, `hide`, `release`, `flip`, `goTo`, `back`) | `test` → `tests/e2e/test_dock_goto.py::test_show_ends_the_goto_and_flip_names_what_is_on_air` | |
| FR-003 | `static/web/display.js` (`read` → `GKPSDisplaySession.owns`) | `test` → `tests/e2e/test_goto_shared_state.py::test_restart_paints_no_goto` | inherits 184 |
| FR-004 | `multimedia/web/templates/reading/obs_dock.html`, `static/web/obs-dock.js` (`openFind`) | `test` → `tests/e2e/test_dock_goto.py::test_g_opens_the_band_and_the_picker_has_no_goto` | |
| FR-005 | `static/web/obs-dock.js` (`refreshFind`), `static/web/projector-library.js` | `test` → `tests/e2e/test_dock_goto.py::test_typing_makes_no_request` | request counter |
| FR-006 | `static/web/obs-dock.js` (`chooseFind`) | `test` → `tests/e2e/test_dock_goto.py::test_choosing_fetches_once_and_steps_stay_local` | |
| FR-007 | `static/web/obs-dock.js` (`renderBlock`), `static/styles/design/obs-dock.css` | `test` → `tests/e2e/test_dock_goto.py::test_the_block_replaces_the_service_rows` | |
| FR-008 | `static/web/display.js` (`back`), `static/web/projector.js` (`render`) | `test` → `tests/e2e/test_dock_goto.py::test_back_restores_the_service_screen_and_edition` | |
| FR-009 | `static/web/display.js` (`show`, `moveTo`), `static/web/obs-dock.js` (row click) | `test` → `tests/e2e/test_dock_goto.py::test_a_block_row_moves_the_goto_and_show_ends_it` | |
| FR-010 | `static/web/projector.js` (`openDetour`, `renderDetour`, `renderDetourCue`) | `test` → `tests/e2e/test_goto_shared_state.py::test_the_dock_follows_a_goto_started_on_the_projector` | |
| FR-011 | `static/web/obs-overlay.js` (`sync`, `modelOf`, `plate`) | `test` → `tests/e2e/test_goto_shared_state.py::test_the_overlay_paints_each_goto_kind` | |
| FR-012 | `static/web/projector.js` (media owner check in `render`) | `test` → `tests/e2e/test_goto_shared_state.py::test_a_goto_stops_a_playing_recording` | |
| FR-013 | `static/web/display.js`, `multimedia/web/reading/goto.py` | `inspection` — diff shows no new route, no new key, and every fetch carries `cache: 'no-store'` | |
| FR-014 | `static/web/projector.js`, `static/web/obs-overlay.js` (first paint), `static/web/obs-dock.js` (`sync`) | `test` → `tests/e2e/test_goto_shared_state.py::test_a_surface_opened_mid_goto_catches_up` | |
| FR-015 | `static/web/obs-dock.js` (`stepUnit`, `flipEdition`, `blankBtn`) | `test` → `tests/e2e/test_dock_goto.py::test_the_transport_steps_the_goto_not_the_service` | |
| FR-016 | `static/web/obs-dock.js` (`chooseFind` adopting the browsed service) | `test` → `tests/e2e/test_dock_goto.py::test_a_goto_can_start_with_nothing_on_air` | |
| FR-017 | `static/web/obs-dock.js` (`renderList`), `obs-dock.css` | `inspection` — with a goto up, no `.entryrow` carries `aria-current` and no pill is drawn | |
| FR-018 | `static/web/obs-dock.js` (`openFind`, `closeFind`), `obs-dock.css` (`.findscrim`) | `test` → `tests/e2e/test_dock_goto.py::test_the_layer_closes_on_escape_click_and_empty_backspace` | |
| FR-019 | `static/web/obs-dock.js` (`sync` → `switchBtn.disabled`), `obs-dock.css` | `test` → `tests/e2e/test_dock_goto.py::test_switch_service_is_disabled_while_a_goto_is_up` | |
| SC-001 | `tests/e2e/test_dock_goto.py` | `test` — the request counter around typing, choosing and stepping | notes: measured in one walk |
| SC-002 | `tests/e2e/test_dock_goto.py` | `test` — the Back comparison | |
| SC-003 | `tests/e2e/test_goto_shared_state.py` | `test` — the three readouts compared at every step | |
| SC-004 | `tests/e2e/test_goto_shared_state.py` | `test` — restart walk | |
| SC-005 | `tests/e2e/test_goto_shared_state.py` | `test` — read of the stored JSON | |
| SC-006 | `tests/e2e/test_dock_goto.py` | `test` → `test_the_same_lookup_answers_both_surfaces` | |
| US1/AC1 | `static/web/obs-dock.js` (`openFind`) | `test` → `test_g_opens_the_band_and_the_picker_has_no_goto` | |
| US1/AC2 | `static/web/obs-dock.js` (`refreshFind`) | `test` → `test_typing_makes_no_request` | |
| US1/AC3 | `static/web/obs-dock.js` (`chooseFind`, `apply`) | `test` → `test_choosing_fetches_once_and_steps_stay_local` | |
| US1/AC4 | `static/web/obs-dock.js` (`closeFind`), `obs-dock.css` | `test` → `test_the_layer_closes_on_escape_click_and_empty_backspace` | |
| US1/AC5 | `static/web/obs-dock.js` (`refreshFind`) | `test` → `test_no_match_says_so_and_enter_does_nothing` | |
| US2/AC1 | `static/web/display.js` (channel), all three readers | `test` → `test_the_three_surfaces_agree_at_every_step` | |
| US2/AC2 | `static/web/obs-dock.js` (`stepUnit`) | `test` → `test_the_transport_steps_the_goto_not_the_service` | |
| US2/AC3 | `static/web/projector.js`, `static/web/obs-overlay.js`, `static/web/obs-dock.js` (`sync`) | `test` → `test_a_surface_opened_mid_goto_catches_up` | |
| US2/AC4 | `static/web/projector.js` (`render` → cue) | `test` → `test_the_dock_follows_a_goto_started_on_the_projector` | |
| US3/AC1 | `static/web/display.js` (`back`) | `test` → `test_back_restores_the_service_screen_and_edition` | |
| US3/AC2 | `static/web/obs-dock.js` (`renderBlock`, `renderList`) | `test` → `test_the_block_replaces_the_service_rows` | |
| US3/AC3 | `static/web/obs-dock.js` (`renderList`) | `inspection` — the block is the list's only content, and Back restores the service rows unhighlighted | |
| US4/AC1 | `static/web/display.js` (`read`) | `test` → `test_restart_paints_no_goto` | |
| US4/AC2 | `static/web/display.js` (`release`) | `test` → `test_release_ends_the_goto` | |
| US4/AC3 | `static/web/display.js` (`hide`), readers | `test` → `test_hide_during_a_goto_keeps_the_place` | |

**Verification split**: 37 test · 3 inspection · 0 manual.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| No violation | — | — |

## Project Structure

### Documentation

```
specs/185-dock-goto/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/
```

### Source

```
static/web/display.js        the goto's verbs, the shape, the one new message
static/web/obs-dock.js       the head's control, the band, the layer, the block, the transport
static/web/projector.js      the detour read from the state; `detour` becomes a payload cache
static/web/obs-overlay.js    the goto painted as a caption or a plate
static/styles/design/obs-dock.css   the band, the layer, the block, the disabled switch
multimedia/web/templates/reading/obs_dock.html   one control in the runner's head
tests/e2e/test_dock_goto.py         the dock's own behaviour
tests/e2e/test_goto_shared_state.py agreement between the three surfaces
```

### Structure Decision

The four modules are the ones the state already runs through, so the slice adds no file to
`static/web/`: `display.js` is the only writer of `gkps-display`, and the three readers each own
their own painting. The dock's new parts live in `obs-dock.js` and `obs-dock.css` beside the
runner they belong to; the template gains one button. The Go To's payloads and lookup are reused
verbatim — no server code, no new module, no new dependency.
