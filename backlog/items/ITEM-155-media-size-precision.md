---
id: ITEM-155
status: ready
title: 'A media size reads in the unit that still shows its number'
type: fix
priority: P1
effort: S
created: 2026-10-28
updated: 2026-10-28
spec: specs/145-media-size-precision/spec.md
branch: feat/145-media-size-precision
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-155: A media size reads in the unit that still shows its number

## Summary

The New media card always prints megabytes with one decimal, so every file under 50,000 bytes reads
`0.0 MB` — a chosen JPEG in the screenshot read `Image · 0.0 MB`. The Media Library and the transfer rail
use a second formula that rounds kilobytes to a whole number, so a file under 500 bytes reads `0 KB` and a
12,345-byte file loses 346 bytes. Owner report: *"the size calculator should detect to the smallest
precisions (what does it means 0.0 MB? no size?)"*.

One label replaces both formulas: the largest decimal unit in which the value is at least 1, one decimal
only when it adds something, and the unit promoted rather than printing `1000`.

## Notes

- Measured on the branch: 12,345 B reads `0.0 MB` in the card and `12 KB` in the library; 512 B reads
  `0 KB` there.
- `fmt` in `media-handoff.js` is defined and never called; the slice deletes it instead of keeping it in
  step.
- The byte count is unchanged everywhere — this is a label, not a stored number.
- Implemented and converged on `feat/145-media-size-precision`; the card waits at `Ready` because the
  board has no `In progress` column and no PR exists until the push is authorised.

## Acceptance sketch

- `512 B` · `2 KB` · `12.3 KB` · `1 MB` · `200 MB`; no non-empty file reads zero.
- The card, the library row and the library Total print the same string for the same file.
- Typography and spacing of the line are unchanged.

## Links

- Spec: [145](../specs/145-media-size-precision/spec.md)
- Preview: [live, `http://127.0.0.1:8821/tatib/149/`](../specs/145-media-size-precision/preview/README.md)
