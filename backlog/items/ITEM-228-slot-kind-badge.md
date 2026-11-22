---
id: ITEM-228
status: done
title: 'A fill-in and a choice state the kind they resolve to'
type: feat
priority: P2
effort: S
created: 2026-11-21
updated: 2026-11-21
spec: 213
branch: feat/213-slot-kind-badge
pr: 563
issue: 562
closed_at: 2026-11-21
closed_reason: merged into develop (PR #563)
bump: patch
release_version: 1.36.6
---

# ITEM-228: A fill-in and a choice state the kind they resolve to

## Summary

A template's fill-in and choice rows wear a dashed slot mark whose inner glyph says only *which of the
two* the row is — a `+` for a fill-in, a `◎` for a choice. The gutter therefore never says which kind
the operator will fill it with, while the song and passage rows beside it put their own glyph in that
same 20px seat. The request: hang a modifier on the slot mark that names the kind — a badge at its
corner, so the frame keeps saying "a place to fill" and the corner says "song", "passage", "media" or
"text".

## Notes

- Measured on `/tatib/151/` (template *111ojo*, six slots) at a 1440px window: `.slot__mark` is
  **20 × 20** at `left: 24px`, vertically centred (`generate.css`, the `#read` block); the resolved kind
  is printed as `slot__kind` — 11.5px/600 uppercase `--head-ink` letter-spaced `.08em` — reading
  `Fill-in · Song`, `Choice · Passage`, `Choice · Song`, `Choice · Text`, `Choice · Media`.
- The mark's own glyph is `_slot_mark.html`: a 20-viewBox dashed rounded rect (`stroke-dasharray:
  2.8 2.4`) with `M10 6.8v6.4M6.8 10h6.4` for a fill-in and a target pair for a choice. It is
  `aria-hidden`.
- That seat is the page's kind column: `.entry__kind-icon` is 20px at `left: 24px` (spec 144, passage
  and song), and `.entry__media-icon` is a 42px chip at `left: 13px`. A slot borrows the 20px seat.
- The kind's own glyph language is 24-viewBox, 1.8 stroke, round caps: a note, an open book. Only
  passage and song have glyphs today (spec 144 marked those two kinds and no others); media's mark is
  the chip, and a text row is unmarked by design (spec 144 FR-004).
- `fill_kind` is one of `SlotKind`'s four values and is already resolved for the row (`slot_kind` in
  `views.py`), so the badge needs no new query.
- `docs/spec/reading.md` R35 states an option row carries "its mark in the gutter"; the option rows on
  `/tatib/151/` carry none. Out of scope here — recorded, not fixed.

## Acceptance sketch

- A fill-in or choice row's mark carries a corner badge naming the kind: song, passage, media or text.
- The badge is legible at the 400px reading pane in both themes and on the hover fill, and adds no
  height of its own.
- The four kinds are told apart without reading the `Fill-in · Song` line.

## Links

- Spec: `specs/213-slot-kind-badge/spec.md`
- Related items: ITEM-160 (the passage and song kind mark, spec 144), ITEM-181 (the fill-in and choice
  kinds, spec 167)
