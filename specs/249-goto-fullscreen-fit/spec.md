# Feature Specification: refit the Go To detour on a stage resize

**Slice**: `specs/249-goto-fullscreen-fit`
**Branch**: `fix/249-goto-fullscreen-fit`
**Created**: 2026-11-27
**Status**: Accepted
**Input**: "i just tested it again, and it does not work for goto"
**Demand**: `ITEM-265` (card opened at delivery)
**Capability**: `projector/R14` — modified block, regression note on spec 247's fix

Spec 247 taught the projector to re-fit the screen on the stage on `fullscreenchange` and on a
`(display-mode: fullscreen)` change. A Go To detour is on the stage but is not one of the service
screens `render()` fits, and `fitNeighbours()` deliberately skips it. A geometry change delivered
as a window `resize` — the browser's own fullscreen control (F11), or a page fullscreen whose
`fullscreenchange` arrives before the viewport grows — therefore leaves the detour's words at the
windowed size while the stage behind them is bigger. This slice makes the resize path fit the
screen that is actually on the stage, so the detour follows the same geometry as a service screen.

## Scope

### In scope

- The Go To detour's fitted words and heading when the stage size changes through `resize`.
- Both orderings: `resize` alone (F11) and `fullscreenchange` followed by `resize` (F key/zone on a
  browser that reports the signal before the new viewport).
- Returning to the old stage size, and the detour's remembered fit key following it.

### Out of scope

- Service-screen fitting, the fit walk, typography, CSS, controls and endpoints — unchanged.
- The `document.fonts.ready` path, which still clears the detour's key without fitting it while a
  detour is up; recorded as a known gap below.
- The cue, HUD, key sheet and media-player sizes.

## User Scenarios & Testing

### US1 — A Go To detour follows the stage (P1)

**Why this priority**: the owner retested spec 247 with a Go To on screen and the words still did
not change size; this is the reported defect.

**Independent Test**: open a passage Go To, change the viewport from 1440×900 to 1920×1080, read
the detour's computed font size before, during and after.

**Acceptance scenarios**

1. **Given** a passage Go To on the stage fitted at `87px` on a 1376×804 stage **When** a resize
   grows the stage to 1856×984 **Then** the detour's words are fitted to `109px` and its key names
   the new stage.
2. **Given** that detour in the grown stage **When** the viewport returns to 1440×900 **Then** its
   words return to `87px` and the key returns to `1376x804|…`.
3. **Given** a `fullscreenchange` signal arrives before the resize **When** the stage grows
   **Then** the detour still ends at the new stage's fit — the signal's earlier frame does not win.
4. **Given** no Go To detour **When** a resize arrives **Then** service screens fit exactly as
   before and no extra work is visible.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The window `resize` path SHALL fit the screen on the stage — the Go To detour when one is up, otherwise the active service screen — after the existing render. | `projector/R14` |
| FR-002 | A resize following a `fullscreenchange` that was delivered before the viewport grew SHALL leave the detour fitted to the grown stage. | `projector/R14` |
| FR-003 | The detour's remembered fit key SHALL follow both directions of the resize, so the returned size equals the original. | `projector/R14` |
| FR-004 | Service screens, their neighbour fits, the cue, the controls and all other geometry paths SHALL keep their present behaviour. | `projector/R14` |
| FR-005 | No endpoint, schema, permission, CSS or template change is made. | `projector/R14` |

### Key Entities

- **Go To detour** — the `.projector-detour` section on the stage while `detour` is set; its own
  head, lines and fit key, separate from the service screens behind it.
- **Resize path** — the `window` `resize` listener that calls `render(true)`, which fits only
  service screens, plus the new stage-screen fit.
- **Stage key** — `stage.clientWidth × stage.clientHeight` plus the detour's head and body, which
  makes a second fit at the same size a no-op.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A resize with a detour on stage re-fits the detour. | `preview/probe.py`: base `87 → 87 → 87`, slice `87 → 109 → 87` with stage 804 → 984 → 804. |
| SC-002 | The earlier fullscreen signal cannot freeze the detour. | Same probe with `fullscreenchange` dispatched before the viewport change: base `87 → 87 → 87`, slice `87 → 109 → 87`. |
| SC-003 | Nothing outside the detour's words changes. | URL, detour `is-active`, service screens and controls unchanged in every reading. |

## UI/UX

Live preview of the real code path: `http://127.0.0.1:8772/projector?service=144` (slice worktree,
`manage.py runserver 0.0.0.0:8772 --noreload`, 1440×900 at 1×). Comparison surface: the compose
server at `http://127.0.0.1:63404/projector?service=144`, which serves the merged spec-247 build.
Numbers are from `preview/probe.py`.

- **Layout / position**: stage `1376×804 → 1856×984 → 1376×804`; viewport `1440×900 →
  1920×1080 → 1440×900`; the detour stays active and the URL stays `/projector?service=144`.
- **Size / spacing**: detour lines `87px → 109px → 87px` on the slice, flat `87px` on the base,
  in both the resize-only and signal-first orderings; fit key `1376x804|…` → `1856x984|…` →
  `1376x804|…` on the slice, unchanged on the base.
- **Colour / typography**: no face, weight, colour, line-height or heading ratio changes; the
  existing size search writes the same inline properties.
- **States**: resize alone · `fullscreenchange` then resize · return to windowed · no detour.
- **Motion**: no new animation; the detour re-fit runs in the same next-frame callback spec 247
  uses, before the next paint.
- **Responsive**: the same fit rule applies at every stage size; the probe measures both 1376×804
  and 1856×984.

## Assumptions

- "Does not work for goto" means the projected words of a passage Go To detour; the earlier
  Clarify session established that the projected words/heading are the surface in question.
- F11's geometry change reaches the page as `resize`; on a page gesture the browser may send
  `fullscreenchange` first and `resize` second, so both orderings are covered.
- The compare server serves the merged spec-247 build (`c72b5ee3`); the slice is based on that same
  commit, so the only source difference is the resize handler.
- The production change is already in the worktree as the gate-1 preview, uncommitted.
- `ITEM-265` and version `1.37.6` are the next free IDs at the time the branch was cut; both are
  rechecked before delivery.
- Known gap left open: the bundled-faces-ready path clears the detour's key but does not fit the
  detour while it is up. Not the reported trigger; recorded rather than widened into this slice.

## Clarifications

### Session 2026-11-27

- Q: Which state fails after the owner's retest? → A: Go To — the detour's words stay at the
  windowed size when the stage changes.
- Earlier session answers still stand: the projected words/heading are the surface, and the F key,
  mouse zones and F11 are the operator paths.
- No unanswered questions and zero `[NEEDS CLARIFICATION]` markers.
