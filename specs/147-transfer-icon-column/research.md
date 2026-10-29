# Research — a transfer row's icon column

**Spec**: `specs/147-transfer-icon-column/spec.md` · **Date**: 2026-10-28

## The mechanism

`components.css:2752-2753`:

```css
.media-transfers__row  { display: flex; align-items: center; gap: 12px; padding: 13px 4px; border-bottom: 1px solid var(--divider); }
.media-transfers__mark { width: 32px; text-align: center; color: var(--focus); font-size: 22px; }
```

`.media-transfers__mark` is a flex item, so `width: 32px` is its **flex base**, not its size: the item
is `flex: 0 1 auto`, and its automatic minimum (`min-width: auto`) is its content's min-content width —
the 21px SVG (`components.css:2796`, `.media-transfers__mark svg { width: 21px; height: 21px }`).

When a name's single line is wider than the row, the flex line is short by that overflow and the mark
is the only item that can give it up: `main` has `min-width: 0` and its `strong` is `nowrap` +
`text-overflow: ellipsis`, so at the moment of measurement `main` was already at its share and the
mark went from 32px to its floor.

Measured on the live page (9 rows, 580px dialog, 1920px window):

| | mark widths | glyph spread | name spread | row height | truncating |
| --- | --- | --- | --- | --- | --- |
| shipped | 32 / 21 / 22.75px | 5.5px | 11.0px | 72px (one value) | 2 |

The glyph's 5.5px is half the mark's 11px loss because `text-align: center` re-centres the 21px SVG
inside the narrowing box — which is why the icon column looks ragged by half of what the words do.

## The candidates, measured, not argued

Each was injected into the live page over the shipped stylesheet and measured with the same script.

| Candidate | `mark` widths | glyph spread | name spread | height | verdict |
| --- | --- | --- | --- | --- | --- |
| a. `.media-transfers__mark { flex: none }` | 32px | 0.0px | 0.0px | 72px | **chosen** |
| b. `.media-transfers__mark { min-width: 32px }` | 32px | 0.0px | 0.0px | 72px | works; leaves the item growable |
| c. `.media-transfers__row { display: grid; grid-template-columns: 32px minmax(0,1fr) }` | 32px | 0.0px | 0.0px | 72px | works; three declarations and a new layout model |
| d. `.media-transfers__mark { flex-shrink: 0 }` | 32px | 0.0px | 0.0px | 72px | works; grow still allowed |

**Why a, and not the other three.** All four produce the same pixels today, so the choice is about
what the declaration says. A column that must be 32px wide is neither shrinkable nor growable, and
`flex: none` states exactly that in one token; `min-width` and `flex-shrink` each fix one direction
and leave the other open, so a future glyph or label wider than 32px would silently widen the column
again — the same class of bug, arriving from the other side. The grid in (c) is the shape
`.service-media__row` already uses, and it would be the right answer if the row were being redrawn;
here it re-derives `align-items`, the divider and the gap for a result the one-line fix already
reaches, and a slice should not redraw a row to change one column's width.

**On `width` versus `flex-basis`.** No change to `width` is needed: `flex: none` sets the basis to
`auto`, which resolves to the declared `width: 32px`. Keeping `width` and adding the lock is what
makes the diff one declaration.

## What the fix changes besides the column

With the mark pinned, the whole deficit lands on `main` — the name column becomes the 482px the
layout always reserved (`534 − 8 padding − 32 mark − 12 gap`) instead of borrowing 11px from the
icon. So the truncation point moves left by 11px on the long rows and the ellipsis appears slightly
sooner; the count of truncating rows is unchanged (2 of 9), and the row height stays 72px.

## How it is proved

- **Unit level**: nothing. There is no domain rule here — the behaviour is layout.
- **Browser level**: Playwright, in the file the surface already uses
  (`tests/e2e/test_media_library.py`), reusing the companion stub from
  `test_sidebar_transfer_session_shows_active_then_finished` (it routes `http://127.0.0.1:63174/**`
  to a JSON payload and the page draws rows from it). The assertions are the measurements above:
  `getBoundingClientRect().left` on every `svg` and every `strong`, plus `scrollWidth > clientWidth`
  and the row's height.
- **Why not a CSS-string assertion**: a test that greps `components.css` for `flex: none` proves the
  text was typed, not that a glyph sits on a line — the same reason spec 142 verified with boxes
  rather than with rules.

## Unknowns remaining: 0

The two open questions at the start — whether the mark could be pinned without moving the text of
the rows that already fit, and whether `main` would then overflow the dialog — were both answered by
the measurement above: the seven short rows are byte-identical to their shipped positions (glyph
702.5, text 741.0), and the long rows' `strong` reports `clientWidth` 482 ≤ `scrollWidth`.
