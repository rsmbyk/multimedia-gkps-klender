# Feature Specification: The audio projector screen shows its play/pause control

**Slice**: `specs/156-audio-play-indicator`
**Branch**: `feat/156-audio-play-indicator`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29 — the control hides with the idle chrome)
**Input**: "add play/pause indicator on the audio projector screen" — with a screenshot of `/projector`
showing an audio entry at `0:25 / 5:02` and nothing above the seek bar

## What the projector does today

An audio entry carries its own mark in the markup — `multimedia/web/templates/reading/projector.html:47`:

```html
<span class="screen__audio-play" data-audio-play aria-label="Play audio"></span>
```

and the script wires it up: `media-audio.js` binds `click` on it, toggles its `data-playing` attribute
(`false` while paused, `true` while playing) and its `aria-label` between `Play audio` and `Pause audio`.
So the control exists as an element, a click target and a state.

It paints nothing. Its box, its radius and its two glyphs — the triangle and the pause bars — are
declared in `static/styles/design/components.css:2118` and `:2122–2123`, and the projector page loads
only three stylesheets (`projector.html:20–22`): `fonts.css`, `tokens.css`, `projector.css`.
`projector.css:88` gives the element a background, a colour and a hover tint and stops there — no
width, no height, no radius, no `::before`. An empty `<span>` with `display: block` and `width: auto`
in a column flex container is 0×0.

Measured on the compose page serving `develop` @ `24a6d6d2` (`/projector?service=144`, the audio entry,
1920×1200, dpr 1):

| element | box |
| --- | --- |
| `.screen__audio-player` | 500 × 69.91 at x 710, y 549.05 |
| `.screen__audio-play` | **0 × 0** at x 960, y 549.05 — `display: block`, no `::before` (computed `content: none`) |
| `.screen__audio-seek` | 500 × 6 at y 579.05 |
| `.screen__audio-times` | 87 × 21.91 at x 916.5, y 597.05 |

`document.styleSheets` on that page lists exactly `design/fonts.css`, `design/tokens.css`,
`design/projector.css`. Nothing on the screen says whether the audio is playing.

Two more layers sit between the control and a click, and both would still eat it once the mark is
painted:

1. `.mouse-zones` (`projector.css:427`) is `position: absolute; inset: 0 0 64px; z-index: 2` — three
   transparent zones over the whole screen, the middle one toggling the words. The screen's own
   content has no stacking context above it, so a pointer event at the centre of the projector lands
   on the zone, not on the player.
2. `projector.js:909–921` reserves **any click in windowed mode** for the fullscreen gesture:
   `preventDefault()` and `stopImmediatePropagation()` on the document, in the capture phase. Even a
   painted control would spend its first click entering fullscreen.

Measured on the live route (`preview/measure.py`): the first click on the floor of the audio player
reaches `pointerdown`/`pointerup` but never fires `click`, so `data-playing` stays `false`.

The second half of the defect is the idle rule, `projector.css:95`: `.screen__audio-box.is-idle
.screen__audio-play { opacity: 0; pointer-events: none }`. `audioActivity()` (`projector.js:62`) sets
`is-idle` 3.5 s after playback starts, so even a correctly painted button would disappear at the moment
its state becomes worth reading, and would stop accepting clicks.

## User Scenarios & Testing

### US1 — The audio screen says whether the audio is playing (P1)

**Why this priority**: this is the whole request. An audio entry is the one projection whose content
is otherwise blank — the mark is the only thing on the screen that reports the state, and the operator
standing at the projector cannot tell a playing track from a paused one without walking back to a
laptop.

**Independent Test**: open `/projector` at an audio entry, play it, wait for the chrome to go idle: the
control has gone with it, as the bar dimmed. Move the pointer: the control returns, showing two bars.
Pause it: the same control shows a triangle.

**Acceptance scenarios**

1. **Given** an audio entry is showing and the audio has never played, **When** the screen is looked
   at, **Then** a 48×48 play triangle sits 30px above the seek bar at full opacity.
2. **Given** the audio is playing, **When** the screen is looked at, **Then** the control's mark is two
   bars at the same size and opacity.
3. **Given** the audio is playing and the chrome has settled into its idle state, **When** the screen
   is looked at, **Then** the control is hidden while the seek bar dims to `.52` and the times to `.4`,
   and its 48px of height stays reserved so the bar does not move.
4. **Given** the idle state, **When** the pointer moves or a key is pressed, **Then** the control
   returns at opacity 1 with the mark for the state the audio is in, and the bar and times return with
   it.

### US2 — The control can be clicked (P1)

**Why this priority**: a 0×0 button is not a control. The same rule that gives the mark its size makes
the pointer able to pause the audio on the projector, which today only `Space` can do.

**Independent Test**: click the control on the live projector: the audio starts, and the mark becomes
two bars; click again: it pauses.

**Acceptance scenarios**

1. **Given** an audio entry showing, **When** the control is clicked, **Then** the audio plays and
   `data-playing` reads `true`.
2. **Given** the audio playing, **When** the control is clicked again, **Then** it pauses and
   `data-playing` reads `false`.
3. **Given** the chrome has gone idle while playing, **When** the control is clicked, **Then** the
   click still lands — the idle state does not disable it.
4. **Given** the projector is windowed and not in fullscreen, **When** the control is clicked,
   **Then** the audio toggles and the page does not enter fullscreen; a click anywhere else on the
   screen still enters fullscreen as it does today.

### Edge Cases

- **When** the local companion has no copy of the file, **Then** the audio player stays hidden and the
  missing-file mark shows, exactly as today: no control, no state.
- **When** the track reaches its end, **Then** the audio pauses, so the mark returns to a triangle and
  the control stays visible.
- **When** the screen is left, or the display is turned off, **Then** the control goes with the screen
  and the audio stops, as today.
- **When** the operator prefers reduced motion, **Then** the control has no transition, as the other
  audio chrome already does (`projector.css:98`).
- **When** the audio is paused before it ever started, **Then** the control is visible at full
  opacity — nothing about the idle dimming applies while paused.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The audio screen SHALL paint its play/pause control above the seek bar at 48×48, at full opacity, whenever the audio player is showing. | `projector/R3` (new) |
| FR-002 | The control's mark SHALL follow the audio — a triangle while paused or ended, two bars while playing — drawn with the same geometry and colours the app's own audio player uses. | `projector/R3` (new) |
| FR-003 | The idle state SHALL hide the control the way it dims the rest of the chrome — opacity 0 and no pointer — while its 48px of height stays reserved, and any pointer move or key press SHALL bring it back with the bar and the times. | `projector/R3` (new) |
| FR-004 | Clicking the control SHALL toggle playback, and `Space` SHALL keep toggling it; the control's `aria-label` SHALL keep reading `Play audio` / `Pause audio`. | `projector/R3` (new) |
| FR-005 | A click on the control SHALL reach it: the pointer zones SHALL NOT cover it, and the windowed fullscreen reservation SHALL NOT consume its click. | `projector/R3` (new) |
| FR-006 | Nothing else SHALL change: no other screen, no preview player, no seek-bar or times geometry, no endpoint, no copy, no markup outside the audio line. | `projector/R1`, `projector/R2` |

### Key Entities

- **Play/pause control** — the `<span class="screen__audio-play" data-audio-play>` inside
  `.screen__audio-player`; its `data-playing` attribute is the state the mark reads, written by
  `media-audio.js:update()`.
- **Idle state** — `.screen__audio-box.is-idle`, added by `audioActivity()` 3.5 s after playback starts
  and removed on any pointer or key activity; it dims the seek bar and the times.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | On the live projector at 1920×1200 the control's box is 48×48 (±0.5) with opacity 1 whenever the chrome is up, and opacity 0 with the box unchanged when the chrome settles. | `getBoundingClientRect()`, `opacity` and `pointer-events` read in each state |
| SC-002 | The mark is a triangle while paused and two bars while playing. | the `::before` box of the control at both states |
| SC-003 | A click on the control toggles playback. | `data-playing` read before and after the click, live and in the E2E |
| SC-004 | The seek bar, the times, the player box and every other screen keep their geometry. | the same table as "today", re-read after the change |

## UI/UX

**Live preview**: `http://127.0.0.1:8815/projector?service=144` — `runserver` from this worktree with
`DATABASE_URL` at the compose Postgres, the way an operator would open it; the numbers below are read
off that route by `preview/measure.py` at 1920×1200, dpr 1.

- **Layout / position**: the control is the first child of `.screen__audio-player`'s centred column, so
  it sits on the same axis as the bar and the times — 48px box at x 936→984 (centre 960), y 525.05→573.05,
  with the seek bar 30px below its bottom edge. The cluster moves **24px down** against today, because a
  48px block joins a column that is centred as a whole: seek y 579.05 → **603.05**, times y 597.05 →
  **621.05**, player 69.91px → **117.91px** tall. The player's own width (`min(500px, 60vw)`, x 710→1210)
  does not change.
- **Size / spacing**: circle 48 × 48, `border-radius: 50%`; triangle 12 × 16 (a 12px left border with
  8px transparent top and bottom) at `left: 20px; top: 16px`; the pause mark a 14 × 18 block at
  `left: 17px; top: 15px`, two 5px bars with a 4px gap. The 30px gap between control and bar is the
  existing `margin-top` on `.screen__audio-seek`.
- **Colour / typography**: circle `#514f48`, mark `#ddd8cd`; hover `#656158`; the times keep `#8e887b` at
  16px and the bar keeps `#8e887b` on `#34312b`. No token is introduced — these are the values
  `components.css` already draws for the preview's audio player.
- **States** — all reachable by hand on the live route:
  - **paused / never played** — triangle, opacity 1, bar and times at full strength (0:00 / 5:02 on the
    service this preview names);
  - **playing** — the mark becomes the two bars at the same 48 × 48, opacity 1;
  - **playing, idle (3.5 s in)** — the control **hides**: `.is-idle` on `.screen__audio-box` sets it to
    opacity 0 with `pointer-events: none`, its 48px of height still reserved so the bar holds at
    603.05, while the seek bar dims to `.52` and the times to `.4`;
  - **activity out of idle** — any pointer move or key press removes `.is-idle`: the control returns at
    opacity 1 over 260ms with the mark for the state the audio is in, and the bar and times return;
  - **hover** — `#656158`; **active** — `scale(.94)`, as the video control does;
  - **ended** — pauses, so the triangle returns;
  - **missing file** — the player stays hidden and the missing-file mark shows: no control at all;
  - **prefers-reduced-motion** — no transition on the control, bar or times.
- **Motion**: `background 150ms ease, transform 120ms ease` on the control; nothing else animates.
- **Responsive**: the player is `min(500px, 60vw)`, unchanged; at 1280 wide the control is still 48px
  and the bar 500px, and at 640 wide the bar is 384px with the control unchanged.

## Assumptions

- **The control follows the chrome rather than standing in it.** It hides as the chrome settles and
  returns on any pointer or key activity, dimming being reserved for the bar and the times (owner's
  answer at gate 1, 2026-10-29). The screen therefore settles to the same quiet frame it has today,
  and the control is there the moment an operator reaches for it — which is also when the state is
  worth reading from across the room.
- **Same mark, same colours as the app's audio player.** The triangle/bar glyphs and the `#514f48`
  circle are the ones `components.css` already draws for the preview's player, so the two audio
  surfaces read as one control rather than two designs.
- **48px, not the video control's 58px.** `.screen__audio-play` is 48px in the only rule that ever
  sized it (`components.css:2118`), and the audio player it belongs to is 48px in the preview; the
  video screen's 58px belongs to a control that sits over a full-frame video.
- **The projector gets its own copy of the rules rather than a fourth stylesheet.** `components.css`
  is the reading app's sheet (2,700+ lines of panels, dialogs and rails); linking it on the projector
  to borrow five lines would repaint the whole page. The five lines move into `projector.css`, beside
  the video control that already lives there.
- **The control is a `<span>`, not a `<button>`.** It is one today, and the video control beside it is
  one too; making it focusable would add a second keyboard path beside `Space`. Out of scope.
- **The seek bar stays as unclickable as it is today.** A pointer on the bar still lands on the display
  zone and toggles the words, exactly as before this slice: the box is lifted above the zones with
  `pointer-events: none` and only the control gets `auto`. Scrubbing from the projector is a separate
  request, recorded rather than smuggled in here.
- **Only the audio control is exempted from the fullscreen gesture.** The exemption is keyed on
  `[data-audio-play]`, so every other click that reaches the projected page — the zones, the screen,
  the video control — still enters fullscreen the way it does today.

## Clarifications

### Session 2026-10-29

- Q: Should the control stay at full strength while the seek bar and times dim in the idle state? →
  A: no — it hides and returns with them; the dimming belongs to the bar and the times, the control
  shows and hides (owner, gate 1).
- No other open items. The request named the surface and the thing missing; the defect was reproduced on
  the running page before Specify (0×0 box, three stylesheets, computed `content: none`), and the two
  click layers were read in `projector.css` and `projector.js`. Zero open markers remain.
