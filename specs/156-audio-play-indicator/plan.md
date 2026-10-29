# Implementation Plan: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`
**Branch**: `feat/156-audio-play-indicator`
**Bump**: `patch`
**Preview**: live — `http://127.0.0.1:8815/projector?service=144`, measured by
`specs/156-audio-play-indicator/preview/measure.py` (see `quickstart.md`)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS (`static/styles/design/projector.css`) and one early return in `static/web/projector.js`; no Python, template, model or migration change |
| Primary dependencies | none added — the existing `.screen__audio-play` element, its `data-playing` attribute and `media-audio.js`'s `attach()` |
| Storage | none |
| Testing | Playwright (Python) E2E through `StaticLiveServerTestCase`: two cases added to `tests/e2e/test_audio_display.py`, driving its existing fake companion |
| Target platform | the projector page in every engine the app supports; `::before`, flexbox and `getComputedStyle` only, all already used there |
| Project type | server-rendered Django app, no build step; WhiteNoise serves a collected `static/` in production |
| Performance goals | no request added, no layout shift, no new compositing layer beyond the one the video box already creates |
| Constraints | the projector keeps its three stylesheets; the mouse zones keep their 40/20/40 split; the fullscreen gesture keeps working everywhere outside the control; the bar and times keep their geometry and dimming |
| Scale / scope | 1 CSS block (5 rules) + 1 restored idle rule, 1 JS guard line, 2 E2E tests |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check is not applicable. The
repo's standing constraints hold: no new dependency, no inline style, no token literal that the projector
does not already carry, no change to the media companion, and the page's three-stylesheet budget kept.

Re-checked after Phase 1: pass. The slice stores nothing, adds no route, and touches no surface other
than the audio screen and the one page-level click guard.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** The six decisions are: geometry into `projector.css` (D001),
stacking above the zones (D002), the fullscreen exemption (D003), the glyph port (D004), hide-not-dim
under idle (D005, owner), and the E2E harness (D006).

## Phase 1 — Design

- `data-model.md` — the two view entities (the control, the chrome state) and their invariants.
- `contracts/` — `none`: no interface is exposed; the page's response and the companion's routes are
  unchanged.
- `quickstart.md` — how to run, measure, test and read the diff.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/projector.css` (`.screen__audio-play`) | `test` → `tests/e2e/test_audio_display.py::AudioDisplayE2ETests::test_projector_audio_control_is_painted_and_toggles` | box ≥ 44px, measured 48 × 48 |
| FR-002 | `static/styles/design/projector.css` (`::before`, `[data-playing="true"]::before`) | `test` → `test_projector_audio_control_hides_as_the_chrome_settles_and_returns` | `border-left` 12px (triangle) → 0px with a 14×18 block (bars) |
| FR-003 | `projector.css` (`.is-idle .screen__audio-play`), `projector.js` (`audioActivity`) | `test` → `test_projector_audio_control_hides_as_the_chrome_settles_and_returns` | opacity 0 + `pointer-events: none` at idle, 48px box kept, back to 1 on `pointermove` |
| FR-004 | `static/web/media-audio.js` (unchanged), the control's click binding | `test` → both new cases click the control; the existing `test_projector_space_navigation_and_reset` covers `Space` | `aria-label` toggle already asserted by `media-audio.js`'s `update()` |
| FR-005 | `projector.css` (`.screen__audio-box` z-index/pointer-events), `projector.js:909` guard | `test` → the clicks in both new cases would be swallowed without both halves | measured before the fix: pointer reached the control, `click` never fired |
| FR-006 | the diff scope itself | `inspection` — `git diff --stat` shows `projector.css`, `projector.js`, `test_audio_display.py` only; every other screen's CSS is untouched | |
| SC-001 | `preview/measure.py` + the E2E | `test` | 48 × 48 ± .5, opacity 1 / 0, all three viewports |
| SC-002 | `preview/measure.py` + the E2E | `test` | `::before` box at both states |
| SC-003 | the E2E clicks | `test` | `data-playing` flips true → false |
| SC-004 | `preview/measure.py` | `inspection` — compare the "today" table with the measured player/bar/times boxes | the cluster drops 24px by design; width and height of the bar are unchanged |
| US1/AC1–AC4 | `projector.css`, `preview/measure.py` | `test` | AC1's 30px gap is read from `measure.py` (see SC-004) |
| US2/AC1–AC4 | `projector.js`, `media-audio.js` | `test` | each case's assertions follow a real pointer click; AC4 is the windowed case |
| Edge: missing file | `projector.js:renderAudioScreen` (unchanged) | `test` → existing `test_missing_audio_states` | player stays hidden |
| Edge: ended | `media-audio.js` (unchanged) | `inspection` — `ended` runs the same `update()` that writes `data-playing`, so the mark returns to the triangle | |
| Edge: reduced motion | `projector.css:110` | `inspection` — the `prefers-reduced-motion` rule lists `.screen__audio-play` | |
| Edge: other viewports | `preview/measure.py` | `inspection` — 1280 and 640 runs, both in `quickstart.md` | |

**Verification split**: 11 test · 5 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | | |

## Project Structure

### Documentation

```
specs/156-audio-play-indicator/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/none.md  checklists/requirements.md  preview/measure.py
```

### Source

```
static/styles/design/projector.css   the control's box, mark, states; the box above the zones
static/web/projector.js              one early return in the fullscreen click guard
tests/e2e/test_audio_display.py      two cases
backlog/items/ITEM-169-audio-play-indicator.md   the card
backlog/board.md                     the card's row
```

### Structure Decision

No new directory or module: the control belongs to the projector's own stylesheet, beside the video
control it mirrors, and the guard belongs to the listener that already owns the page's click policy. The
test lives in the module that already builds an audio service and its fake companion.
