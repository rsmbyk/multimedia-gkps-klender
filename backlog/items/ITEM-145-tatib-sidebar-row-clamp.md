---
id: ITEM-145
status: done
title: 'A Tata Ibadah sidebar row is three lines, ellipsized'
type: feat
priority: P2
effort: S
created: 2026-10-26
updated: 2026-10-26
spec: specs/135-tatib-sidebar-row-clamp/spec.md
branch: feat/135-tatib-sidebar-row-clamp
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/400
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/399
closed_at: 2026-10-26
closed_reason:
bump: patch
release_version:
---

# ITEM-145: A Tata Ibadah sidebar row is three lines, ellipsized

## Summary

A service-order row in the reading sidebar is capped by content, not by height: untitled text
entries get their first two body lines, songs get a heading plus a `Bait …` line, and every label is
cut at 60 characters with no ellipsis. A 64-character song title therefore wrapped to two lines and
looked like a three-line row, and a 61-character title lost its tail silently.

The cap is the row's height instead: three visual lines of the entry's own text, in every kind —
text, media, passage, song (the `Bait …` line counted, leaving two for the heading) and the legacy
rows — with an ellipsis when the row does not show all of it.

## Notes

- Owner request: remove the 60-character cap; cap at three visual lines; ellipsize the end.
- The 60-character cut lives in `multimedia/web/reading/views.py` (`_tatib_stage`), applied after the
  label is built, and again on the legacy row's first line with a literal `…`.
- `static/web/offline-render.js` renders the same rows from the saved library and must match.

## Acceptance sketch

- A row whose text is longer than three visual lines shows three, ending in `…`.
- A 64-character title is shown whole when it fits in three lines, with no silent cut.
- A song row with a long title spends two lines on the heading and shows its `Bait …` line third.
- The saved copy of the page draws the same rows.

## Links

- Spec: [135](../specs/135-tatib-sidebar-row-clamp/spec.md)
- Related items: ITEM-122 (saved-page parity)
