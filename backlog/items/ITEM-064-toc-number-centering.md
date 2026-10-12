---
id: ITEM-064
status: done
title: 'Center entry numbers vertically in the Tata Ibadah contents list'
type: chore
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: 063
branch: chore/062-toc-number-centering
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/316
archived_at:
archive_reason:
bump: patch
release_version: 1.6.1
---

# ITEM-064: Center entry numbers vertically in the Tata Ibadah contents list

## Summary

The contents list aligns each row on its first text baseline, so on multi-line
entries (a quoted text, or a song with its `Bait …` line) the entry number sits at
the top. Center the number vertically on the whole row so the numbering column
reads evenly; the text keeps its current alignment.

## Notes

- Owner approved the alignment preview on 2026-10-12; spec accepted on 2026-10-12 (drafted as 062, renumbered to 063 after #315 took 062).
- Rows share `.songrow` with the songbook song list; that list is not changed.
- The drag copy (`.reorder__ghost`) is built outside `#chList` and must match.

## Acceptance sketch

- One-, two-, and three-line rows: the number's vertical center matches the row's.
- Text position, row height, padding, and drag-handle space are unchanged.
- Hover, selected, filtering, drag copy, and both themes keep the centered number.

## Links

- Spec: [063](../../specs/063-toc-number-centering/spec.md)
- Preview: [alignment preview](../../specs/063-toc-number-centering/preview.html)
- Related items: ITEM-048, ITEM-062
