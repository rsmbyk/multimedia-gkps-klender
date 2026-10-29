# Feature Specification: a preview's play shortcut paints nothing on the dialog's edge

**Slice**: `specs/159-preview-body-ring`
**Branch**: `fix/159-preview-body-ring`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29)
**Input**: the owner's report — *"why is there that ring on the edge of the modal when you play/pause the audio or song with space key"* — and card ITEM-165.

## What the page does today

`.preview__body` is the Preview dialog's scroll region and it carries `tabindex="0"`
(`multimedia/web/templates/reading/_preview_modal.html:11`), so `showModal()` hands it DOM focus the
moment the dialog opens whenever it is the dialog's first focusable element. It draws its keyboard
indicator with

```css
.preview__body:focus { outline: none; }
.preview__body:focus-visible { outline: 2px solid var(--focus); outline-offset: -2px; }
```

(`static/styles/design/components.css:2093`), where `--focus` is `#1C5C3C` — `rgb(28, 92, 60)`
(`tokens.css:40`).

The space shortcut is a separate listener (`static/web/preview.js:579–592`): it calls
`preventDefault()` and `player.toggle()`, and touches focus not at all. But space is still a key
press, and the browser treats keyboard input as "the keyboard is in use": an element that already
held focus becomes `:focus-visible`, and the ring is painted on it.

In audio and video previews there is no head and no foot, `.preview` has `padding: 0`, and the body
is laid out over the dialog's whole box — measured on the live page, dialog and body both
**920 × 852 at (296, 24)**. So an inset ring on the body is indistinguishable from a border on the
modal: the owner's 1920 × 1200 screenshot shows a 2px `rgb(28, 92, 60)` band at x 618–1537,
y 351–961, one pixel inside the card's own edge.

Measured on the compose page at 1.22.10, `/tatib/144/`, 1512 × 900, audio entry `e1` and video entry
`e26`:

| step | body matches `:focus-visible` | computed outline |
| --- | --- | --- |
| opened with the pointer | false | `none 0px` |
| one space press | **true** | `solid 2px -2px rgb(28, 92, 60)` |
| a second space press | true | unchanged |
| a click inside the body | true | unchanged |
| opened with Enter | true | `solid 2px -2px rgb(28, 92, 60)` |

The click inside the body cannot clear it: the click handler calls `content.focus()`
(`preview.js:470–474`), which is a no-op on an element that already holds focus, so the browser's
keyboard mark survives until focus actually moves. Reaching the body with Tab sets the same ring
(verified: one Tab from the opener on entry `e6`, ring `solid 2px -2px rgb(28, 92, 60)`) — that is
the state the rule exists for, and it is the one spec 071 bought when it made the body focusable so
the arrow keys could scroll it.

## User Scenarios & Testing

### US1 — A key that operates the player leaves no mark on the dialog (P1)

**Why this priority**: it is the reported defect, it reproduces on every space press, and the ring
outlives the key — so the operator reads a border the dialog does not have, or believes something
is selected.

**Independent Test**: on the live page, open an audio preview and a video preview with the pointer,
press space twice, and sample `:focus-visible` plus the body's computed outline after each press:
no indicator at any point, and the player toggles each time.

**Acceptance scenarios**

1. **Given** an audio preview opened with the pointer, **When** space is pressed, **Then** the player
   toggles and nothing is painted on the body or on the dialog's edge.
2. **Given** a video preview opened with the pointer, **When** space is pressed twice, **Then** the
   player toggles twice and nothing is painted on the body or on the dialog's edge.
3. **Given** a preview opened from the keyboard — which paints the ring as it opens — **When** space is
   pressed, **Then** the player toggles and that ring is gone, with no other indicator drawn in its place.
4. **Given** a body whose ring is showing because the reader Tabbed to it, **When** space is pressed,
   **Then** the player toggles and the ring is suppressed; the reader's next Tab draws it again.

### US2 — A reader who arrives by keyboard still sees the indicator (P2)

**Why this priority**: the ring is not the defect. It is the scroll region's keyboard indicator, and
a fix that deletes it makes the dialog look like it holds no focusable content to anyone who never
touches the pointer.

**Independent Test**: on the live page, open a preview with the pointer and press Tab until the body
holds focus; the 2px `--focus` ring is drawn as it is today, and the arrow keys scroll a body that
overflows.

**Acceptance scenarios**

1. **Given** any preview, **When** the reader reaches the body with Tab, **Then** the body draws its
   `2px` `--focus` ring at offset `-2px`, as it does today.
2. **Given** a text preview whose body overflows, **When** the body holds focus and ArrowDown is
   pressed, **Then** it scrolls, and at the bottom edge the key is swallowed — spec 071's guard,
   unchanged.

### Edge Cases

- **When** a preview has no space shortcut — image, PDF — **Then** nothing about it changes: the body
  keeps focusing on open and keeps its ring under keyboard navigation.
- **When** the focus ring is showing because the reader Tabbed to the body, **Then** pressing space
  still toggles the player and the ring is suppressed, and the reader's next Tab draws it again — the
  body keeps focus throughout, so a key delays the indicator, never the focus itself.
- **When** the pointer clicks inside the body, **Then** the body still takes focus quietly, as today.
- **When** the seek bar holds focus, **Then** space is still left to the seek control, not the player.
- **When** Escape is pressed, **Then** the dialog closes as it does today, ring or no ring.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A key that operates a preview's player SHALL leave no focus indicator on the preview's body, and therefore none on the dialog's edge — including clearing one the dialog drew as it opened. | `new: reading` → R27 |
| FR-002 | The body's keyboard indicator SHALL remain available: reachable by Tab, `2px` solid `--focus` at offset `-2px`, unchanged in geometry and colour from today. | `new: reading` → R27 |
| FR-003 | The body SHALL keep the behaviour it was made focusable for: arrow keys scroll a body that overflows, and the edge guard at its top and bottom still swallows them. | `new: reading` → R27 |
| FR-004 | Nothing else changes: the player's toggle, the seek bar, the header tabs, the pointer click that focuses the body, Escape, and the image and PDF previews' behaviour. | `new: reading` → R27 |

### Key Entities

- **Preview body** — the dialog's `tabindex="0"` scroll region, `preview__body`. Holds focus on open
  whenever it is the dialog's first focusable element; carries the ring that this slice concerns.
- **Play/pause shortcut** — the space listener on the dialog, `preview.js:579–592`, one per audio and
  video preview. Toggles the player and owns no focus.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | On the live page, a pointer-opened audio preview and a pointer-opened video preview show no focus indicator on the body after one space press or after two. | `preview/probe.py`: `:focus-visible` false and computed outline `none 0px` after every press |
| SC-002 | The player toggles on every space press, in both previews. | the same probe reads `audio.paused` / `video.paused` before and after each press |
| SC-003 | Reaching the body with Tab still draws the ring, at `2px` `rgb(28, 92, 60)`, offset `-2px`. | the same probe, one Tab from the opener |
| SC-004 | Apart from the ring, the dialog is unchanged: same box, same padding, same controls, same copy. | screenshot diff of the preview against 1.22.10 at 1512 × 900 |

## UI/UX

**Static preview at `specs/159-preview-body-ring/preview/preview.html`** (regenerate with
`build_preview.py`; the stylesheets are frozen at `24a6d6d2`). Three panels over one real dialog —
`Now`, `A`, `B` — each with both open paths, both entries, and a live readout of `:focus-visible`,
the computed outline and both boxes. Read in headless Chromium at 1512 × 900, and cross-checked
against the live compose page (`/tatib/144/`, entries `e1` and `e26`) and the owner's 1920 × 1200
screenshot.

| state | Now | **A — adopted** | *(B — not adopted)* |
| --- | --- | --- | --- |
| pointer open | none | none | none |
| pointer open + space | **ring** | none | none |
| keyboard open | ring | ring | **none** |
| keyboard open + space | ring | **none** | none |
| Tab to the body | ring | ring | ring |
| click in the body, then space | ring | none | none |

- **Layout / position**: the body is the dialog's box at every width — video **920 × 852 at (296, 24)**
  and audio **620 × 256 at (446, 322)** in a 1512 × 900 window; **920 × 881 at (500, 159)** and
  **620 × 256 at (650, 472)** at 1920 × 1200; **384 × 607** and **384 × 248** at a 420px window, where
  Chrome's own dialog rule caps the 388px the stylesheet asks for. The ring is drawn inset, so on the
  modal's edge it reads as a 2px border one pixel inside the card.
- **Size / spacing**: `outline-width: 2px`, `outline-offset: -2px`; the ring moves no layout — it is an
  outline, not a border. Body padding unchanged: `22px` (video), `28px 26px` (audio), `16px` and
  `24px 20px` at a 420px window.
- **Colour / typography**: `--focus` = `#1C5C3C` = `rgb(28, 92, 60)`; no typography is involved.
- **States**: the six rows above, plus the body's own — it has no hover, active or disabled state, before
  or after. Every row is reachable by hand in the preview.
- **Motion**: none; the ring is not animated and appears at once.
- **Responsive**: unchanged — video `min(920px, 100vw − 32px)`, audio `min(620px, 100vw − 32px)`.

**Adopted: A.** The ring shows while the dialog holds focus and no shortcut has been used; the first
space press takes it away, and any Tab clears the suppression so the indicator returns. B was rejected:
it removes the indicator from the reader who arrived by keyboard, which is the state the rule exists
for.

## Assumptions

- **The shortcut keeps owning no focus.** Toggling playback is its whole job, so the fix may not be
  met by moving focus to the play button — that would leave a ring, merely a smaller one, and would
  take the arrow-key scrolling away from the body.
- **The ring is not narrowed to bodies that scroll.** Today every preview body draws it; deciding
  that a non-scrolling body needs no indicator is a different change and stays out of this slice.
- **The image and PDF previews are untouched.** They carry the same body rule and have no space
  shortcut, so nothing in this slice moves them.
- **The capability number is R27, provisional.** `reading` folds through R26 as of 2026-10-28; other
  slices in flight may claim R27 first, and the number is re-checked when this one folds.

## Clarifications

### Session 2026-10-29

No open items — zero markers remain.

- **Q**: a preview opened from the keyboard paints the body's ring before any key is pressed. Does that
  state keep the ring (**panel A**), or paint no ring at all until the reader reaches the body with Tab
  (**panel B**)?
  → **A: keep it, and the first space press takes it away.** Answered by the owner after opening
  `preview/preview.html` and driving both panels by hand — the first answer, *"previews"*, picked
  neither panel and was asked again rather than guessed at.
- **Re-checked against the whole spec.** The answer contradicts nothing: US1 scenario 3 already held
  that a space press leaves nothing painted, and A is the reading of it that keeps US2's indicator for
  the keyboard reader. FR-001 now says *leave*, not merely *paint*, so the ring the dialog draws as it
  opens is covered; US1 scenario 4 and the Tab edge case state the Tab-reinstates-it rule that A needs.
- No question was skipped, so no assumption was written in place of an answer.
