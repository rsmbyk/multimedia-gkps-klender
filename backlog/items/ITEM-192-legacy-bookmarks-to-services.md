---
id: ITEM-192
status: in-review
title: 'The old bookmarks stand as services'
type: feat
priority: P1
effort: M
created: 2026-11-05
updated: 2026-11-05
spec: 188-legacy-bookmarks-to-services
branch: feat/188-legacy-bookmarks-to-services
pr: 496
issue: 495
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-192: The old bookmarks stand as services

## Summary

The team's song bookmarks stop at the old dock: 157 active, dated lists back to 2024 are unreachable
from the reading pane, the operator dock and the projector. A data migration turns each of them into a
dated Tata Ibadah whose entries are the bookmark's songs, in its order, with its verse numbers — while
the bookmarks themselves stay untouched so the legacy dock keeps working.

## Notes

- Selection, as the owner ruled it: active, dated, and holding at least one song. Deleted bookmarks
  stay deleted; undated ones (`Doding Galangan`, `Lagu Doa Persembahan`) cannot satisfy the
  service/date constraint; empty junk ones carry nothing.
- A service already standing under the same name (case-sensitive) and date never blocks the
  conversion — the bookmark becomes a second service of that name and date, and the standing one is
  left alone. On the local copy: 157 created beside 138 existing, 18 name and date pairs with two.
- No link back to the legacy app, and no idempotence: with duplicates allowed, a second run converts
  again.

## Acceptance sketch

- Every qualifying bookmark has a service under its name and date whose entries equal its items —
  counts and verses, no mismatch — even where one already stood there.
- 157 bookmarks with 1716 items convert; bookmark and item rows unchanged.
- The dock lists the converted services by date, and a song entry opens with its verses.

## Links

- Spec: [188](../specs/188-legacy-bookmarks-to-services/spec.md)
- Related items: ITEM-181 (services and templates), ITEM-189 (the dock's Go To)
