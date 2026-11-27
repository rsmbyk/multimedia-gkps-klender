# Feature Specification: refit the projector words when fullscreen changes the stage

**Slice**: `specs/247-projector-fullscreen-fit`
**Branch**: `fix/247-projector-fullscreen-fit`
**Created**: 2026-11-27
**Status**: Accepted
**Input**: "the projector page does not update the font sizes when switching between full screen and windowed"
**Demand**: `ITEM-264` (card opened at delivery)
**Capability**: `projector/R14` — modified block, not a new requirement

The projector fits every screen of words to the stage it will rest in. The fit is recomputed
when the window is resized, when the bundled faces arrive and when a header is rewritten, but a
fullscreen transition is not one of its triggers. With the F key, a mouse zone or F11 the stage
grows, while the active screen keeps the size it was fitted to in the windowed stage: the words
stay small and the new space above and below them is empty. This slice adds the missing trigger —
`fullscreenchange` for the page's own gesture, and `(display-mode: fullscreen)` for the browser's
own F11 — and re-fits the screen on the stage on the next frame, after the new geometry is laid
out.

## Scope

### In scope

- The inline font size of the words (`screen__lines`) and heading (`screen__head`) on the active
  service screen, and the remembered fit for the screens either side.
- A Go To detour's own words when it is the screen on the stage.
- Both directions: entering and leaving fullscreen, by F key, mouse zone or browser F11.

### Out of scope

- The cue, HUD, key sheet and media-player font sizes — unchanged.
- The fit algorithm, its 2–200px range, the morph, the media (`T`, fit and pan) rules and the
  audio/video takeover — unchanged.
- Server, schema and endpoint behaviour — unchanged.

## User Scenarios & Testing

### US1 — Fullscreen refits the words on the stage (P1)

**Why this priority**: it is the reported symptom — words at the windowed size with a much
bigger empty stage after the operator goes fullscreen.

**Independent Test**: grow the stage by 200px, send the fullscreen signals without a window
resize, and read the active screen's computed font size before and after.

**Acceptance scenarios**

1. **Given** a text screen fitted at a 1376×804 stage to `87px` **When** a fullscreen transition
   grows the stage to 1376×1004 and no `resize` event arrives **Then** its words are fitted to
   `93px`, its heading to `57.4772px`, and its remembered fit names the new stage.
2. **Given** that same screen in fullscreen **When** the transition ends and the stage returns to
   1376×804 **Then** its words return to `87px` and its heading to `53.769px`.
3. **Given** a Go To detour showing on the stage **When** a fullscreen transition arrives **Then**
   the detour's own words are re-fitted, not the service screen hidden behind it.
4. **Given** the stage does not change size **When** a fullscreen signal arrives **Then** the
   screen keeps its size and no visible change occurs.

### US2 — The other fit paths and the rest of the projector survive (P2)

**Why this priority**: the change adds a trigger; it may not change the answer any existing path
gives or the behaviour of the controls around the stage.

**Independent Test**: replay the existing resize-driven fit and the fullscreen gesture probe on
the same service and compare the settled sizes.

**Acceptance scenarios**

1. **Given** a browser that does send `resize` on fullscreen **When** the viewport goes from
   1440×900 to 1920×1080 and back **Then** the words settle at `109px` and `87px` as before,
   with no second or conflicting fit.
2. **Given** F11, which produces no `fullscreenElement` and no `fullscreenchange` **When** the
   display-mode query changes **Then** the words are re-fitted on the next frame.
3. **Given** the F key, the mouse zones, the cue and the shortcuts sheet **When** fullscreen is
   entered or left **Then** every one keeps its present behaviour.

### Edge Cases

- **When** both `fullscreenchange` and `resize` arrive for one transition **Then** both fits read
  the same settled stage and agree; the second is a no-op against the remembered key.
- **When** the stage has no text screen (image, audio, video, PDF or blank) **Then** nothing is
  fitted and no error is raised.
- **When** a browser does not implement `matchMedia` **Then** the `fullscreenchange` and `resize`
  paths still run.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A `fullscreenchange` event SHALL re-fit the screen on the stage (the Go To detour when one is up, otherwise the active service screen) on the next animation frame. | `projector/R14` |
| FR-002 | A change in `(display-mode: fullscreen)` SHALL re-fit the same screen, covering the browser's own fullscreen control, which emits no `fullscreenElement`. | `projector/R14` |
| FR-003 | The re-fit SHALL read the stage after the transition has laid it out and SHALL update the remembered fit key, so the arriving size is the size a resize gives for the same stage. | `projector/R14` |
| FR-004 | The screens either side SHALL be re-fitted in idle time after a transition, as they are after a resize. | `projector/R14` |
| FR-005 | Every existing fit trigger — arrival, jump, resize, bundled faces and header rewrite — SHALL keep its present behaviour, as SHALL all cue, key-sheet and media-screen behaviour. | `projector/R14` |
| FR-006 | No endpoint, schema, permission, CSS or control change is made. | `projector/R14` |

### Key Entities

- **Active screen** — the service screen on the stage, or the Go To detour while one is up; the
  node whose head and lines carry the fitted font sizes.
- **Fit key** — `stage.clientWidth × stage.clientHeight` plus the head text, line count and body
  length; the remembered value that makes a second fit at the same stage a no-op.
- **Fullscreen signal** — one of `fullscreenchange` (F key and mouse zone), a `change` on the
  `(display-mode: fullscreen)` media query (browser F11), or `resize`; each asks for the same
  re-fit, never a different size.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A stage change with no resize re-fits the active words. | `preview/probe.py`: base stays `87px` at both 804 and 1004; slice `87px → 93px → 87px`. |
| SC-002 | The heading follows the same fit. | `53.769px → 57.4772px → 53.769px` in the same probe. |
| SC-003 | The re-fit answers the same size a resize would. | CDP resize probe on the slice: `1440×900 → 87px`, `1920×1080 → 109px`, back to `87px`. |
| SC-004 | Nothing outside the words moves. | URL stays `/projector?service=144`, `data-current-screen=0`, body text unchanged in every probe reading. |

## UI/UX

Live preview of the real code path: `http://127.0.0.1:8771/projector?service=144` (slice
worktree, served with `manage.py runserver 0.0.0.0:8771 --noreload`, 1440×900 at 1×). The change
is applied in that worktree and left uncommitted for the gate. The comparison surface is the
compose server at `http://127.0.0.1:63404/projector?service=144`; both serve byte-identical
`projector.js` before the slice edit (verified by `git diff develop..origin/develop` on that path).
All numbers are from `preview/probe.py` unless marked otherwise.

- **Layout / position**: stage `1376×804` windowed → `1376×1004` in the modelled fullscreen, back
  to `1376×804`; the URL and `data-current-screen=0` are unchanged throughout.
- **Size / spacing**: active lines `87px → 93px → 87px` on the slice, `87px → 87px → 87px` on
  the base; heading `53.769px → 57.4772px → 53.769px` against base `53.769px` throughout;
  remembered fit key `1376x804|…` → `1376x1004|…` → `1376x804|…` on the slice, never changing
  on the base.
- **Colour / typography**: no colour, weight, line-height or face changes; the existing
  heading/body ratio (1 ÷ golden ratio) is preserved by `setSize`.
- **States**: windowed · fullscreen by F key / mouse zone · fullscreen by F11 · returned to
  windowed · no text screen · Go To detour · both signals in one transition.
- **Motion**: no new animation; the re-fit runs in one `requestAnimationFrame` after the signal,
  before the next paint; the existing 240ms arrival morph is untouched.
- **Responsive**: the same fit rule applies at every stage size; the CDP resize check at
  `1920×1080` gives `109px` on the slice, matching the base.

## Assumptions

- "Full screen" covers all three operator paths named in Clarify — F key, mouse zone and F11 —
  and the words stay at the windowed size with empty space above and below in each.
- A browser may change the stage without delivering `resize` on those transitions; the missing
  signal, not the fit algorithm, is the defect. Both remaining signals are explicit triggers now.
- `(display-mode: fullscreen)` follows F11 on Chromium and Firefox; where a browser reports no
  such change, the existing `resize` path still covers it. Safari is not verified here.
- The fix is applied in the worktree before gate 1 so the live URL is the preview; the code stays
  uncommitted until Fold, and the probe keeps the base numbers for the red half of the evidence.
- The comparison server serves local `develop` at `43f0c957`, nine commits behind the slice's base
  `origin/develop` at `abdb28fd`; the projector fit files are identical at both refs, so the base
  reading is a valid control.
- Demand is `ITEM-264`: the next free card ID on `origin/develop` and every local branch at the
  time the branch was cut. It is opened at delivery, following the recent slices' practice.

## Clarifications

### Session 2026-11-27

- Q: Which font sizes stay unchanged when switching full screen ↔ windowed? → A: The projected
  words and heading — the fitted text screens (not the cue, key sheet or media controls).
- Q: How do you switch the projector into full screen? → A: All of the F key, the mouse zones and
  F11.
- Q: What happens to the words after fullscreen? → A: They stay the same size, with lots of empty
  space in fullscreen.
- Zero `[NEEDS CLARIFICATION]` markers remain.
