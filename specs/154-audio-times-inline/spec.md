# Feature Specification: An audio preview reads its times as `current / total`

**Slice**: `specs/154-audio-times-inline`
**Branch**: `feat/154-audio-times-inline`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1 and gate 2, 2026-10-29)
**Input**: "move the played timer to beside the total time just like in video \"current / total\"" — with a screenshot of the Preview of an audio entry over `/tatib/144/`

## What the preview does today

An audio entry's Preview is a 620px dialog (`#previewModal`, `.preview.is-audio-preview`) holding a
48px round play button and a timeline: the filename, a 6px seek bar, and under it a line of two
times — `multimedia/web/templates/reading/tatib.html:56`:

```html
<div class="audio-player__times"><span data-audio-elapsed>0:00</span><span data-audio-total>0:00</span></div>
```

`.audio-player__times` (`static/styles/design/components.css:2134`) is
`display: flex; justify-content: space-between; margin-top: 7px; font-size: 12px; color: var(--head-ink)`,
so each span is pushed to its own end of the 504px timeline.

Measured on the compose page serving `develop` @ `24a6d6d2` (`/tatib/144/`, entry `e1`, a 5:02 MP3,
headed Chromium 1440×900, dpr 1):

| element | box |
| --- | --- |
| `#previewModal` | x 410→1030, 620×125 |
| `.preview__audio .audio-player` | x 436→1004, 568×69 |
| `.audio-player__timeline` | x 500→1004, 504px wide |
| `.audio-player__seek` | x 500→1004, y 445.5, 504×14 |
| `[data-audio-elapsed]` | x 500→523.8, 23.8×18 at y 466.5 |
| `[data-audio-total]` | x 980.2→1004, 23.8×18 at y 466.5 |

The two numbers therefore sit **456.4px apart**, each flush with an end of the bar, and the played
time — the number an operator actually watches — is the one at the far left, reading as a caption for
the play button rather than for the bar.

The split also removes the separator from the text: the two spans are adjacent with no text between
them, so the line's accessible text is `0:000:10` (measured in the E2E's own DOM, a 10-second file) —
two numbers with nothing saying how they relate.

The projector's own audio bar already prints the pair inline:
`multimedia/web/templates/reading/projector.html:47` renders
`<span data-audio-elapsed>0:00</span> / <span data-audio-total>0:00</span>` inside
`.screen__audio-times` (`static/styles/design/projector.css:94`). The reading surface is the one that
deviates from the shape the product already uses when the times are read as one value.

## User Scenarios & Testing

### US1 — The played time sits beside the total (P1)

**Why this priority**: it is the report. A played time detached from its total is read as two labels,
not as `current / total`, and it is the one number the operator glances at while an offertory track
runs.

**Independent Test**: open the Preview of an audio entry and read the line under the seek bar: one
line, `0:00 / 5:02`, both numbers together at the bar's right end.

**Acceptance scenarios**

1. **Given** an audio entry whose file the local companion serves, **When** its Preview is opened,
   **Then** the times line reads `current / total` — the played time, a separator, the total — with
   the two numbers on one line, 5px either side of the separator.
2. **Given** the same Preview, **When** the times line is measured against the seek bar, **Then** the
   group's right edge is the bar's right edge (±1px) and the played time starts in the bar's right
   half — it is no longer at the bar's left end.
3. **Given** a playing file, **When** the audio advances or the bar is seeked, **Then** both numbers
   keep updating in place and the line does not move: no reflow, no width change of the pair beyond
   the digits' own.

### US2 — The shape matches the projector's own bar (P2)

**Why this priority**: the product already states how a current/total pair reads on the projector; a
second shape on the reading side is how two surfaces drift apart.

**Independent Test**: put the projector's `.screen__audio-times` and the preview's
`.audio-player__times` side by side: same order, same separator, same reading.

**Acceptance scenarios**

1. **Given** both surfaces, **When** their text is read, **Then** both are `current / total` — the
   played time first, a slash, the total — and neither is reversed.
2. **Given** the projector, **When** this slice ships, **Then** nothing about it changes: its times
   line keeps its own font size, colour, margin and left alignment.

### Edge Cases

- **When** the file's duration is unknown (metadata not yet loaded, `0:00 / 0:00`), **Then** the pair
  keeps the same shape and the same right alignment.
- **When** the duration runs past an hour, **Then** the pair reads as `clock()` already prints it —
  minutes are not wrapped (`62:03`) — and it stays on one line, right-aligned.
- **When** the companion cannot serve the file, **Then** the player is not shown at all
  (`.preview__audio-unavailable`), and nothing about that state changes.
- **When** the viewport narrows and the dialog shrinks to `calc(100vw - 32px)`, **Then** the pair
  stays right-aligned under the bar and does not overlap the play button.
- **When** the theme is dark, **Then** the pair keeps `var(--head-ink)` and reads at the same weight.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An audio Preview's times SHALL read `current / total` on one line: the played time, a separator, the total, in that order. | `new: reading` → R27 |
| FR-002 | The pair SHALL be right-aligned to the seek bar's right edge, and the played time SHALL NOT sit at the bar's left end. | `new: reading` → R27 |
| FR-003 | Both numbers SHALL keep updating in place as the audio plays and as it is seeked, with no positional change of the line. | `reading/R24` (the list holds still) applied to the player's own line |
| FR-004 | Nothing else SHALL change: the dialog's 620px width, the 48px play button, the filename line, the 6px bar, the 7px gap above the times line, the 12px type, `var(--head-ink)`, the unavailable and empty states, and the projector's own bar. | `new: reading` → R27 |

### Key Entities

- **The times line** — `.audio-player__times`: the flex row under the seek bar holding the two
  `[data-audio-elapsed]` / `[data-audio-total]` spans that `static/web/media-audio.js:37` rewrites on
  every `timeupdate`. It has no state of its own; it mirrors the audio element.
- **Clock string** — `clock()` (`media-audio.js:24`): `Math.floor(seconds / 60) + ':' + ss`, hours
  deliberately not split. Unchanged.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The times line reads one grouped `current / total` pair, right-aligned under the bar. | Live preview, 1440×900: elapsed x 941.9→965.7, separator x 970.7→975.2, total x 980.2→1004 — one line, 5px either side of the slash, the pair's right edge on the seek bar's (1004 = 1004) |
| SC-002 | The played time no longer starts at the bar's left end. | The elapsed span's left edge moves x 500 → x 941.9, in the bar's right half (the bar runs x 500→1004) |
| SC-003 | The suite can see the shape, so it cannot regress silently. | `tests/e2e/test_audio_display.py::test_preview_times_read_current_over_total_beside_the_bar` asserts the text shape and the pair's geometry at rest and after a seek — red on `develop`'s markup (`0:000:10`, 456.4px apart), green here |
| SC-004 | Nothing else on the dialog moves. | The same probe before and after: dialog 620×125, player 568×69, seek 504×14, all boxes and y positions identical |

## UI/UX

Live preview at **http://localhost:8814/tatib/144/** (slice worktree, `runserver 0.0.0.0:8814`), open
entry `e1`'s Preview, 1440×900, dpr 1. The preview is the change itself on
`feat/154-audio-times-inline`, so a click runs the product's own markup, CSS and `media-audio.js`
against the real local companion (`127.0.0.1:63174`); the companion's allowlist carries
`http://localhost:8814` for the review window only.

Before · after, measured on develop @ `24a6d6d2` and on this branch, same viewport and entry:

| element | before | after |
| --- | --- | --- |
| `#previewModal` | x 410→1030, 620×125 | x 410→1030, 620×125 |
| `.audio-player` | x 436→1004, 568×69 | x 436→1004, 568×69 |
| `.audio-player__seek` | x 500→1004, 504×14 at y 445.5 | x 500→1004, 504×14 at y 445.5 |
| `[data-audio-elapsed]` | x 500→523.8, 23.8×18 at y 466.5 | **x 941.9→965.7**, 23.8×18 at y 466.5 |
| `.audio-player__separator` | — | **x 970.7→975.2, ≈4.5px** |
| `[data-audio-total]` | x 980.2→1004 | x 980.2→1004 (unmoved) |
| the pair's text | `0:00` … `5:02`, 456.4px apart | `0:00 / 5:02`, 62.1px wide, ending on the bar's edge |

- **Layout / position**: the times line's children are `played`, `separator`, `total`, in that order,
  laid out by `display: flex; justify-content: flex-end`. The pair's right edge is the seek bar's right
  edge (x 1004).
- **Size / spacing**: `gap: 5px` on both sides of the separator — 5px from the played time to the
  slash, 5px from the slash to the total. The line's own box is unchanged (x 500→1004, 504×18 at
  y 466.5, 7px under the bar).
- **Colour / typography**: unchanged — 12px, `var(--head-ink)` (rgb(100, 99, 87) in light), inherited
  family; the separator is the same ink and size as the numbers.
- **States**: idle `0:00 / 5:02` · playing (`0:01 / 5:02` after a second) · seeked · ended
  (`5:02 / 5:02`) — in all three the pair's box is identical at x 941.9→1004, y 466.5: the played time
  grows leftwards, the total stays put · unknown duration `0:00 / 0:00` · past an hour (`62:03`) ·
  unavailable (player hidden — unchanged) · dark theme (`var(--head-ink)` = rgb(156, 154, 145), same
  12px) · narrow viewport (below).
- **Motion**: none added; the line does not animate or reflow as the digits change.
- **Responsive**: at 420×820 the dialog is 382px wide at x 19 (Chrome's own cap on the `min()` rule),
  the seek bar runs x 103→381 (278px), and the pair sits x 318.9→381 — right edge on the bar's, 232px
  clear of the play button's 48px column. Proportions hold: the pair keeps its 5px gaps and its one
  line.
- **Not changed**: the projector's `.screen__audio-times` (`projector.css:94`) — it already reads
  `current / total`.

## Assumptions

- **The pair is right-aligned under the bar, not left-aligned** — every video player the report points
  at ("just like in video") puts `current / total` at the bar's right end; left would leave the times
  floating away from the total's old position.
- **A plain `/` is the separator**, with 5px either side — the projector's own line uses ` / `, so the
  product already has this shape.
- **The separator is a real text node, not a generated pseudo-element** — a screen reader should read
  `0:00`, `slash`, `5:02` rather than run the two numbers together.
- **The line stays a flex row of spans** — `media-audio.js:39` writes `textContent` into the two spans
  by selector, so the markup change must leave both selectors in place and must not depend on the
  children's order or count.
- **The times line stays under the bar** — moving it onto the bar's own row was not asked for and would
  change the dialog's height.

## Clarifications

### Session 2026-10-29

No `[NEEDS CLARIFICATION]` markers were raised: the request names the target shape and the screenshot
names the surface. The three defaults a reader might not predict — side, separator and alignment — are
recorded in **Assumptions** above.
