# Implementation Plan: one keyboard grammar for the dock and the projector

**Spec**: `specs/187-keyboard-parity/spec.md`
**Branch**: `feat/187-keyboard-parity`
**Bump**: `minor` — 1.26.4 → 1.27.0. The slice adds user-visible capability that did not exist on the
dock (a `K` sheet, a `G` on the picker, a held `Esc`, a fetch guard) and changes what the projector's
sheet shows; the two neighbouring slices that only moved state (183, 184) took `patch`, and this one
does not.
**Preview**: `specs/187-keyboard-parity/preview/` — `index.html`, the dock's sheet and the go to
standing alone, self-contained and probe-driven; `projector-sheet/` — the living projector sheet's
before and after, captured from the running page.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript, ES5-era IIFEs in `static/web/` (no build step); Python 3.12 / Django 4.0 for the two templates; no model or view changes. |
| Primary dependencies | none new. `static/web/projector-library.js` (`lookup`, `movePassage`, `fetchChapter`) already loaded by the dock's band; `static/web/display.js`; `localStorage`; `BroadcastChannel`; `static/web/display-session.js`. |
| Storage | `localStorage['gkps-display']`, unchanged in shape — only the allowance that `goto` may stand beside `service: null` (contract `display-state.md`). No new key, no server state. |
| Testing | Playwright (Python) E2E under `tests/e2e/` through `StaticLiveServerTestCase`; the preview's `probe.py` for the sheet's static numbers. |
| Target platform | OBS's Chromium (CEF) dock at 320 / 400 / 520 px wide and 520–1200 px tall; projector and overlay at 1920 × 1080 and 1280 × 720. |
| Project type | Django app, server-rendered templates plus vanilla JS modules; no bundler. |
| Performance goals | A verse step inside a loaded chapter: 0 requests. A chapter or book crossing: exactly 1. Opening the sheet: 0. Typing in a band: 0. One state write reaches every surface in one channel message. |
| Constraints | No new endpoint and no new storage key. The dock's transport stays one 40 px line. The projector's sheet keeps its labels, chords and type scale; only grouping, column and frame change. Every control in the dock stays `tabindex="-1"` so the panel holds the keyboard. One row per direction, the projector's wording where shared. |
| Scale / scope | 11 user stories, 15 functional requirements, 12 success criteria, 44 acceptance scenarios. The slice touches 4 JS modules, 2 templates, 2 stylesheets, and adds 2 E2E modules (plus 2 extended). |

## Constitution Check

The repo carries no `CONSTITUTION.md`; the standing principles are the ones its own documents declare —
`AGENTS.md`, `docs/PROCESS.md`, and the capability files under `docs/spec/`.

| Principle | Status | Note |
| --- | --- | --- |
| One browser-local display state, written by the dock, read by the others (`docs/spec/display-state.md`) | pass | No second state; a service-less go to is the same object with `service: null` (D005). |
| One channel; a reader re-reads rather than trusting the payload | pass | No new message type; readers learn to paint a `goto` without a `service`. |
| No new endpoint; content comes from what exists (spec 136) | pass | Chapter/song payloads and the index are spec 185's routes. |
| The session bounds the state's life (spec 184) | pass | Every write still stamps `session`; nothing else changes. |
| The dock's keyboard lives on the panel, every control `tabindex="-1"` | pass | The sheet's controls join that rule; the band's field is the one element that takes the focus, and FR-015 says so. |
| The projector's sheet is grouped by subject and must not clip (projector R9, R12) | justified | R9's fixed 677 px frame is superseded: the moved media groups make the left column the tallest (835.5 px at 1080p), and 720p scrolls instead of clipping. Recorded as FR-014 and folded into `projector/R9`, `R12`. |
| Previews are built from the product's own components | pass | The dock's sheet is drawn from the product's tokens, `obs-dock.css` and the sheet's own markup; the projector's before/after are the living page with its DOM moved. |
| Tests prove user-visible behaviour through the repo's Playwright harness | pass | Two new modules and two extended; the split below is 25 test · 2 inspection · 0 manual. |
| No personal names in repo artifacts | pass | Roles only. |

Re-checked after Phase 1: **pass** — the one justified row is the sheet's frame, and Complexity
Tracking carries it.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Eleven decisions; the three that shape the code are D001
(the band keeps the keyboard by asking for it), D002 (stepping is the library's own move) and D005 (a
go to with no service).

## Phase 1 — Design

- `data-model.md` — the display state with a service-less go to, the go to entity, the dock's
  shortcut table, the band's query state, and the invariants.
- `contracts/` — `display-state.md` (the delta to spec 185's contract) and `keyboard.md` (the one
  grammar both surfaces answer to); `README.md` names them and what stays internal.
- `quickstart.md` — the worktree stack, the preview build/probe, and the targeted E2E runs.

## Traceability

Components name the file that owns the behaviour; `tests/e2e/test_dock_keys.py` and
`test_projector_keys.py` are new, the other two are extended. Every row also names the story scenarios
it answers.

| Requirement | Component / file | Verified by | Covers |
| --- | --- | --- | --- |
| FR-001 | `static/web/obs-dock.js` (`onKey` Esc branch, a 900 ms timer, release/blur cancel) | `test` → `tests/e2e/test_dock_keys.py::test_a_tap_of_escape_does_nothing_and_a_hold_returns_to_the_picker` | US1/AC1-3, US1/AC4-5 |
| FR-002 | `static/web/obs-dock.js` (`onKey` picker branch, `openFind`) | `test` → `tests/e2e/test_dock_keys.py::test_g_opens_the_band_on_the_picker` | US2/AC1, US2/AC5 |
| FR-003 | `static/web/display.js` (`gotoOf`, `goTo`, `stepGoto`, `hide`, `resume`, `flip`, `back`) | `test` → `tests/e2e/test_goto_shared_state.py::test_a_picker_go_to_writes_no_service_and_back_idles` | US2/AC2-3 |
| FR-004 | `static/web/obs-dock.js` (`chooseFind`, `renderBlock`), `obs_dock.html` | `test` → `tests/e2e/test_dock_keys.py::test_the_picker_go_to_stands_alone_and_back_returns_to_the_picker` | US2/AC2-4 |
| FR-005 | `static/web/obs-dock.js` (`stepUnit`, `edgeOf`, a `requestPassage` twin) + `static/web/projector-library.js` (`movePassage`, `fetchChapter`) | `test` → `tests/e2e/test_dock_keys.py::test_the_go_to_steps_like_the_projectors_chords` | US3/AC1-4 |
| FR-006 | `static/web/obs-dock.js` (`onKey` picker branch) | `test` → `tests/e2e/test_dock_keys.py::test_the_picker_moves_on_up_and_down_only` | US4/AC1-3 |
| FR-007 | `static/web/obs-dock.js` (`setKeysOpen`), `obs_dock.html` (`.keysheet`), `obs-dock.css` | `test` → `tests/e2e/test_dock_keys.py::test_k_opens_the_sheet_and_the_picker_group_rides_with_the_view` | US5/AC1-3 |
| FR-008 | `obs_dock.html` (the sheet's groups), `obs-dock.css` | `test` → `tests/e2e/test_dock_keys.py::test_k_opens_the_sheet_and_the_picker_group_rides_with_the_view` (the product's rows) · `specs/187-keyboard-parity/preview/probe.py` (the design's rows and order) | US5/AC4, US9/AC3 |
| FR-009 | `static/web/obs-dock.js` (`gotoBusy` around `fetchGoto` and the passage step) | `test` → `tests/e2e/test_dock_keys.py::test_no_key_changes_what_is_on_air_while_a_go_to_fetches` | US6/AC1-3 |
| FR-010 | `static/web/projector.js` (`onKey`: `ctrlKey \|\| metaKey`, the meta return moved) | `test` → `tests/e2e/test_projector_keys.py::test_meta_and_control_are_the_same_modifier` | US7/AC1-3 |
| FR-011 | `static/web/projector.js` (`renderDetour`), `static/web/obs-overlay.js` (`sync`, `plate`) | `test` → `tests/e2e/test_goto_shared_state.py::test_the_overlay_paints_a_service_less_go_to` | US2/AC2, US2/AC5 |
| FR-012 | `static/web/obs-dock.js` (`edgeOf`, `stepUnit` plain/shift/ctrl branches) | `test` → `tests/e2e/test_dock_keys.py::test_home_and_end_act_on_the_bait_or_entry` | US8/AC1-5 |
| FR-013 | `multimedia/web/templates/reading/projector_controls.html` (group merge and order) | `test` → `tests/e2e/test_projector_keys.py::test_the_sheet_carries_one_display_group_and_one_find_group` | US9/AC1-2, US9/AC4 |
| FR-014 | `projector_controls.html` (media groups and columns), `static/styles/design/projector.css` (`.sheet` height) | `test` → `tests/e2e/test_projector_keys.py::test_audio_and_video_are_one_group_in_the_left_column` | US10/AC1-5 |
| FR-015 | `static/web/obs-dock.js` (`focusPanel`, `window` focus, `visibilitychange`, `focusin`, `pointerdown`) | `test` → `tests/e2e/test_dock_keys.py::test_the_band_keeps_the_keyboard_when_the_window_returns` | US11/AC1-5 |
| SC-001 | `tests/e2e/test_dock_keys.py` | `test` — 300 ms tap moves nothing, 1000 ms hold shows the picker | US1 |
| SC-002 | `tests/e2e/test_goto_shared_state.py` | `test` — `localStorage['gkps-display']` carries `service: null` plus the goto | US2 |
| SC-003 | `tests/e2e/test_dock_keys.py` | `test` — request counter: 1 / 1 / 0 across `Shift+→`, `Ctrl+→`, a plain step | US3 |
| SC-004 | `tests/e2e/test_goto_shared_state.py` | `test` — six chords compared on both surfaces, same place | US3 |
| SC-005 | `tests/e2e/test_dock_keys.py` | `test` — `←` `→` `PgUp` `PgDn` move 0 rows; `↑`/`↓` move 1 and clamp | US4 |
| SC-006 | `tests/e2e/test_dock_keys.py` | `test` — `K` opens on both views, `Esc` closes, a click on the frame never acts on a control | US5 |
| SC-007 | `tests/e2e/test_dock_keys.py` | `test` — 10 keys and 3 clicks change nothing during a delayed fetch | US6 |
| SC-008 | `tests/e2e/test_projector_keys.py` | `test` — `⌘+→` lands where `Ctrl+→` lands; `⌘+T` flips nothing | US7 |
| SC-009 | `tests/e2e/test_goto_shared_state.py` | `test` — the overlay's plate and the projector's detour for a service-less go to; `Back` idles both | US2 |
| SC-010 | `tests/e2e/test_dock_keys.py` | `test` — the live row against the service's own ends, in a text entry and in a bait | US8 |
| SC-011 | `tests/e2e/test_projector_keys.py` | `test` — the three columns' headings in order and the sheet's box at 1080p | US10 |
| SC-012 | `tests/e2e/test_dock_keys.py` | `test` — blur/refocus leaves `activeElement` on `#findInput`; typing appends; `Esc` returns it to the panel | US11 |
| FR-013 (no label or chord changed) | `projector_controls.html` | `inspection` — the diff shows moved `<section>`s and one `<h3>`, and no `.fn` or `.k` change | US9/AC4 |
| FR-014 (no label or chord changed) | `projector_controls.html` | `inspection` — the same diff; one duplicate `Play/Pause` row removed with its heading | US10/AC5 |

**Verification split**: 25 test · 2 inspection · 0 manual.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| The dock mirrors the projector's `unitBoundary` and `requestPassage` instead of sharing a module | The two scripts are separate closures over different models (`stops`/`entries` against `screens`/`entries`); the slice's ask is behaviour, not a refactor of the projector's tested core | Extracting the arithmetic into `projector-library.js` would change the projector's core beyond the request, and one shared table would still need the two models |
| The projector's sheet frame leaves its fixed 677 px | The owner's media move makes the left column the tallest (835.5 px at 1080p); a fixed frame would clip the sixth group at every window size | Keeping 677 px and clipping, or shrinking the rows/headings, both break a rule the owner set |

## Project Structure

### Documentation

```
specs/187-keyboard-parity/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/  projector-sheet/
```

### Source

```
static/web/obs-dock.js          the sheet, the held Esc, the picker's G, the go-to chords, Home/End, the guard, the band's focus
static/web/display.js           a go to may stand with service: null
static/web/projector.js         ⌘ as Ctrl; the sheet's regrouping; the service-less detour
static/web/obs-overlay.js       painting a service-less go to
multimedia/web/templates/reading/obs_dock.html        the sheet's five groups and its picker group
multimedia/web/templates/reading/projector_controls.html  Display absorbs Find and Fullscreen; Find reordered; media groups merged and moved
static/styles/design/obs-dock.css    the sheet, its caps, its scrollbar
static/styles/design/projector.css   the sheet's frame follows its tallest column
tests/e2e/test_dock_keys.py     new
tests/e2e/test_projector_keys.py new
tests/e2e/test_dock_goto.py     extended: the picker's go to, the guard
tests/e2e/test_goto_shared_state.py extended: a service-less go to across surfaces
tests/e2e/test_obs_dock.py      extended: the picker's narrowed keys
tests/e2e/test_projector.py     extended: the sheet's groups and frame
```

### Structure Decision

The dock's sheet lives in `obs_dock.html` with its rules in `obs-dock.css`, beside the dock it belongs
to; the projector's sheet stays in `projector_controls.html` and `projector.css`. The two share a
grammar (`contracts/keyboard.md`), not a component: the dock's sheet is one column inside a 384 px
panel, the projector's is three columns at 1095 px, and neither can render the other's layout. The
preview keeps its own folder and its captured data, as spec 185 established.
