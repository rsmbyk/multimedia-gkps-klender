# Feature Specification: a slot states the kind it resolves to

**Slice**: `specs/213-slot-kind-badge`
**Branch**: `feat/213-slot-kind-badge`
**Created**: 2026-11-21
**Status**: Accepted (owner, gate 1, 2026-11-21)
**Input**: "can you add a modifier on the fill-in and choice icons on the service entry page so that we
know what kind of entry is the fill-in and choice is" — owner. The shape was answered in the same
session: *"how about adding a modifier at the corner of fill-in and choice mark?"* (owner, 2026-11-21).

## What the page does today

On a template's page every entry states its kind in the left gutter, and the two *slot* kinds — a
fill-in and a choice, spec 167 — state only that they are a place to fill: which of the two the row is
(a `+` or a `◎`), never which kind the operator will fill it with.

| measured on `/tatib/151/` (template *111ojo*, six slots), 1440 × 900, 400px reading pane | value |
| --- | --- |
| a slot row's mark — `.slot__mark` | **20 × 20px** at `left: 24px`, vertically centred; a 20-viewBox dashed rounded rect (`stroke-dasharray: 2.8 2.4`) with a `+` glyph (fill-in) or a target pair (choice) |
| a passage / song row's mark — `.entry__kind-icon` | **20 × 20px** at `left: 24px` — the *same seat*, carrying that kind's own glyph (spec 144) |
| a media row's mark — `.entry__media-icon` | **42 × 42px** chip at `left: 13px`, with a per-family glyph |
| the resolved kind, in words — `.slot__kind` | `11.5px/600`, uppercase, `letter-spacing: .08em`, `--head-ink` — `Fill-in · Song`, `Choice · Passage`, `Choice · Song`, `Choice · Text`, `Choice · Media` |
| a slot row's own padding | `padding-left: 64px` (the title column every other entry starts at) |
| the mark's glyphs available to the page | a note (song), an open book (passage) — spec 144 marked those two kinds and no others; media wears its family chip and a text row carries no mark at all (spec 144 FR-004) |

So a reader who scans the gutter can tell a song row from a prayer by its glyph, and cannot tell a
*song fill-in* from a *passage fill-in* at all.

## User Scenarios & Testing

### US1 — A slot's mark names the kind it resolves to (P1)

**Why this priority**: this is the request. The page is read at a glance while a service is prepared;
which kind a slot will become should be known before its words are, the way a song row's note is.

**Independent Test**: with the change applied, each of the six slot rows on `/tatib/151/` paints a
corner badge on its mark, and the badge differs between a song slot, a passage slot, a media slot and a
text slot.

**Acceptance scenarios**

1. **Given** a template carrying a fill-in whose kind is song, **When** its page is drawn, **Then** the
   row's mark carries a badge whose glyph is the song mark.
2. **Given** a template carrying a choice whose kind is passage, **When** its page is drawn, **Then**
   the row's mark carries the passage badge — a different mark from the song slot's.
3. **Given** the four kinds on one page, **When** the gutter is scanned without reading the
   `Fill-in · Song` line, **Then** the four badges are told apart.
4. **Given** any slot row, **When** it is drawn, **Then** the mark still reads as a slot: the dashed
   frame is unchanged and the row's own `+` or `◎` is still on the mark.

### US2 — The kind mark's own language, at a slot's scale (P1)

**Why this priority**: the badge sits in a 20px seat beside real `.entry__kind-icon` marks; a badge
drawn in a foreign stroke language or a second colour reads as an alien mark on the same rail.

**Independent Test**: compare the badge's computed stroke width, colour and box against
`.entry__kind-icon` on the same page.

**Acceptance scenarios**

1. **Given** a song slot and a song entry side by side, **When** the two marks are compared, **Then**
   both carry the same note glyph, the entry's in the seat's full 20px and the slot's in the badge.
2. **Given** the hover fill, **When** a slot row is pointed at, **Then** the badge and its backing
   stay legible — the badge does not composite into the fill.
3. **Given** the two themes, **When** the page is drawn, **Then** the badge's glyph holds the contrast
   the stage's own meta text holds on `--canvas`.

### US3 — The page's rhythm and text column are untouched (P2)

**Why this priority**: specs 055, 140, 143 and 144 fixed the stage's geometry as a contract — 56px
boxes, one left rail, the title column at 64px. A badge that moves a row or narrows the title column
breaks them.

**Independent Test**: measure every `.tatib__item`'s top, the title's first-line x, and the page's
scroll height before and after.

**Acceptance scenarios**

1. **Given** a slot row, **When** the badge is drawn, **Then** the row's box height is unchanged and
   the title's first line still starts at the same x.
2. **Given** `prefers-reduced-motion`, **When** the row is drawn, **Then** nothing is animated.
3. **Given** a 400px reading pane, **When** the badge is drawn, **Then** no rows move and no title
   wraps that did not wrap before.

### Edge Cases

- **When** a slot's resolved kind is text — the one kind with no glyph anywhere in the product —
  **Then** the badge carries a mark of its own rather than an empty disc. *(Recorded assumption.)*
- **When** a slot is a choice with no options (`No options yet`), **Then** the row still carries its
  kind badge; the badge states the kind, not the row's readiness.
- **When** a slot's row is hovered, focused or is the origin of an open modal, **Then** the mark keeps
  its badge; it is decorative and takes no pointer.
- **When** a legacy slot has no `fill_kind` (a stored row the four kinds cannot explain), **Then** the
  mark is drawn without a badge, exactly as it is today.
- **When** the row renders inside the **Use template** dialog, **Then** it carries no badge, because it
  carries no mark: the dialog's slot row (`.g-row--slot`) is a label, a title, a value and an action,
  and the served markup contains no `.slot__mark` in it at all. The dialog's own kind marks sit on its
  muted *fixed* rows, which are ordinary entries and already carry spec 144's marks.
- **When** the row renders in the sidebar's contents list, **Then** it carries no badge — `#chList`
  paints no kind mark of any kind today (no `.slot__mark`, no `.entry__kind-icon`), and spec 144's
  FR-008 keeps those surfaces on their own anatomy.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A fill-in or choice row on a template's page SHALL carry a badge on its mark naming the kind the slot resolves to. | `reading/R35` (modified) |
| FR-002 | The badge SHALL differ per kind — song, passage, media and text each paint a different mark, drawn in the mark's own stroke language. | `reading/R35` (modified) |
| FR-003 | The mark SHALL keep the slot's own identity: the dashed frame and the row's `+` or `◎` are unchanged by the badge. | `reading/R35` (modified) |
| FR-004 | The badge SHALL be `aria-hidden`, and the row's accessible name SHALL be unchanged — the kind is already stated in words by the row's own label. | `reading/R35` (modified) |
| FR-005 | The badge SHALL add no height and move no title: a slot row's box and every other block's top SHALL be unchanged. | `reading/R35` (modified) |
| FR-006 | The badge SHALL remain legible on `--canvas` and on the hover fill, in both themes, at the stage's own meta-text contrast. | `reading/R35` (modified) |
| FR-007 | A slot whose stored kind cannot be read SHALL draw the mark without a badge, never a broken or empty one. | `reading/R35` (modified) |

### Key Entities

- **Kind badge** — a small mark at the slot mark's corner, drawn from the entry's `fill_kind`, on the
  same 20px mark the passage and song rows use. Server-rendered: the kind is known when the page is
  drawn, so no script injects it.
- **Slot mark** — the existing `.slot__mark`: a 20px dashed rounded frame with the row's own `+` or
  `◎` inside (`_slot_mark.html`), unchanged by this slice apart from the badge.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Every slot row on a template's page is badged | on `/tatib/151/`: six badges, one per slot; a service's page carries none; the number matches the slots and not the entries |
| SC-002 | The four kinds are told apart | the four badges' `data-kind-badge` values, and their rendered glyph paths, are pairwise different |
| SC-003 | The mark keeps its identity | the dashed frame's computed `stroke-dasharray` and the row's own `+`/`◎` path are unchanged before and after |
| SC-004 | Nothing moves | every `.tatib__item`'s top, every title's first-line x, and the page's scroll height, before and after |
| SC-005 | Reachable-free | the badge is `aria-hidden="true"`; the row's accessible name is byte-identical before and after |

## UI/UX

Measured on the live slice server (`http://127.0.0.1:8777/tatib/151/`, template *111ojo*, six slots)
at 1440 × 900 with both sidebars open — a 400px reading pane — in both themes, at 1× and on the
preview page `specs/213-slot-kind-badge/preview/compare.html`, whose A/B/C columns are the real rows
cloned from the served page.

**Adopted: B — a 13px disc overhanging the mark's bottom-right corner, carrying a 10px glyph.**

| | value |
| --- | --- |
| the mark, unchanged | **20 × 20px** at `left: 24px`; the dashed frame draws at **14.8 × 14.8** (a 20-unit viewBox rect at 2.6) |
| the badge | **13 × 13px** disc, `right: -4px; bottom: -3px` — it overhangs the mark's box by **4px** right and **3px** bottom |
| the glyph | **10 × 10px**, drawn on a 12-unit viewBox at `stroke-width: 1.6` |
| the disc's fill | `--canvas` — light `#F7F5F1`, dark `rgb(20, 19, 15)` |
| the glyph's colour | `--head-ink` — light `rgb(100, 99, 87)`, dark `rgb(156, 154, 145)` |
| contrast | **5.57:1** light · **6.59:1** dark on the disc — the stage's own meta-text figure, and the `slot__kind` label's |
| gap to the row's kind label | **16px** (badge right edge 1015, label left 1030) |
| the four glyphs | a beamed note (song) · an open book (passage) · a framed play mark (media) · three text lines (text) |
| the mark keeps its own glyph | `stroke-dasharray: 2.8 2.4` and the `+` / `◎` path are byte-identical to the pre-change page |
| nothing moves | all six rows' `y` and `height`, every title's `x` (1030 / 1063), and the page's scroll height (**2278px**) are identical with the badge drawn and with it suppressed |

- **Size, and why 13 and not 11 or 15.** The three candidates were built and compared on real 1× pixels
  magnified 8×: at **11px** (glyph 8.5) the mark is an unnamed blob, at **13px** (glyph 10) it reads as
  a note, at **15px** (glyph 11.5) it is unmistakable but the disc is wider than the 14.8px dashed
  frame it sits on and eats its whole corner. **B is the smallest size that reads**, and the owner chose
  it on that basis.
- **The disc is the canvas, and on a pointed-at row it repaints the row's own tint.** A disc of plain
  `--canvas` on the row's `--icon-hover-bg` fill reads as a hole punched in the row — measured and
  seen at 8×. The badge therefore lays the same `--icon-hover-bg` gradient over its canvas in the
  row's four fill states (`:hover`, `.is-modal-origin`, `:focus`, `:has(:focus)`), so the two composite
  to the same value by construction rather than by a second hand-matched colour. The glyph's contrast
  does not change on the fill.
- **States**: at rest · hovered · `.is-modal-origin` · keyboard focus · both themes · a slot with no
  options (`No options yet`) · a slot with no title.
- **Motion**: none.
- **Responsive**: nothing in the badge is width-dependent. At the 400px pane the badge stays inside the
  row (its right edge is 15px clear of the row's own edge) and the title column is untouched.
- **The coupling to avoid**: `.slot__mark > svg` is the *frame* selector. It was `.slot__mark svg`
  (descendant), which would have stretched the badge's own glyph to the full 20px box — the change is
  a `>` so the frame keeps its rule and the badge carries its own size.

## Assumptions

- **The surface is the template's page.** The request names the service entry page and the six slot
  rows are drawn there; the Use template dialog and the sidebar are marked as open questions above
  rather than silently included.
- **The badge is a corner modifier, not a replacement.** The owner's shape keeps the mark's frame and
  inner glyph and adds the kind at a corner; the `Fill-in · Song` line stays, so nothing loses its
  words.
- **A text slot gets its own mark.** Text is the one kind with no glyph in the product today; the badge
  set needs one, drawn in the same language rather than left blank.
- **Server-rendered.** `fill_kind` is already resolved for the row (`views.py` `slot_kind`), so the
  badge is markup, not script — the same reason spec 144's marks are server-rendered.
- **Legacy rows degrade quietly.** A slot with no readable `fill_kind` draws today's mark.

## Clarifications

### Session 2026-11-21

- Q: What should the fill-in/choice mark become — the kind inside the frame, the kind taking the whole
  seat, or fill-in-vs-choice made obvious? → A: **a modifier at the corner of the mark**, keeping the
  mark itself (owner).
- Q: Which badge size? → A: **B, 13px disc with a 10px glyph**, chosen from three candidates built on
  the real rows and shown side by side at 1× plus their 1× pixels at 8× (owner, 2026-11-21). A (11px)
  was built first and rejected on legibility; C (15px) was the clearest but eats the dashed frame's
  corner.
- Q: Does the **Use template** dialog's slot row carry the badge? → **No, and the question is moot**:
  that row has no mark at all (`.g-row--slot` is label, title, value and action; the served dialog
  contains no `.slot__mark`). Answered by inspection of the served markup, not by preference.
- Q: Does the sidebar's contents list carry the badge? → **No**: `#chList` paints no kind mark of any
  kind today, and spec 144's FR-008 keeps those surfaces on their own anatomy. Answered by inspection.
