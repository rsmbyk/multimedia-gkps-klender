# Fold: the overlay's text wraps inside the box that owns it

**Slice**: `specs/183-overlay-text-wrap` · **Capability**: [`docs/spec/overlay.md`](../../docs/spec/overlay.md)
· **Date**: 2026-11-02 · **Version**: 1.26.1 (`bump: patch`)

## Capabilities touched

| Capability | Operations | Before → after |
| --- | --- | --- |
| `overlay` | `modified` R2 (a song screen paints the caption), `modified` R3 (a passage screen paints a quotation card), `modified` R4 (a liturgy screen paints a script panel) | 8 requirements → 8 requirements; each modified block gains one sentence and one scenario |

The header moves `last folded` to 2026-11-02 and prepends `183-overlay-text-wrap` to the slice list.

## What changed in each block

- **R2** — the caption now carries the requirement that a lyric line wider than its box breaks at its own edge, keeps
  its centring and its balanced lines, and grows the block taller by the rows added. Scenario: a 66-character run draws
  5 rows in 1728 × 403.19 with no ink past the box (2,035.20 px past it before this slice).
- **R3** — a kicker, a title or a verse line wider than the card's content box breaks at that edge. Scenario: a
  126-character verse title draws 3 rows under the reference, the card 1728 × 364.03, nothing past it (207.39 px
  before).
- **R4** — a turn or a title wider than the panel's content box breaks at that edge. Scenario: the reported body draws
  3 rows inside the panel with nothing past it (710.45 px before), a marked row wraps its words column under the mark's
  column, and a 64-character entry title still measures one row because the panel grows to hold it.

## What was read and left untouched

- **R1** (paints from the display state, no control), **R5** (a speaker mark's own column), **R6** (blank, media, break
  and released paint nothing), **R7** (arrival, exit and the morph), **R8** (the edition flip) — read against the
  working tree; **no behaviour change**, and none is folded. The mark keeps its `white-space: nowrap` by its own
  declaration, which R5 already states.

## Not folded

None. No gap was accepted: `converge.md` **pass 2** is the pass this fold rests on, and pass 1 (the narrow scope) is
recorded there as superseded rather than folded.

## Note on the mechanism

The capability file records behaviour, not the sheet's shape, so it does not name the declaration. The implementation
is one inherited `overflow-wrap: break-word` on `.obs-overlay__stage`; the reason it sits there rather than on each
element is in `research.md` D002, with the scope reversal that moved it.
