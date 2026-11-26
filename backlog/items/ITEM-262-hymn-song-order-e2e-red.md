---
id: ITEM-262
status: backlog
title: 'Hymn song-order E2E expects a different row order'
type: fix
priority: P2
effort: S
created: 2026-11-26
updated: 2026-11-26
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-262: Hymn song-order E2E expects a different row order

## Summary

`tests.e2e.test_reading.ReadingE2ETests.test_hymn_song_order_is_visible_after_browsing_from_home`
expects numeric order; the page renders `['Legacy', 'NKB 2', 'NKB 12A', 'NKB 12B', 'NKB 10',
'NKB 12']` instead of `['NKB 2', 'NKB 10', 'NKB 12', 'NKB 12A', 'NKB 12B', 'Legacy']`. The failure
reproduces on unmodified `origin/develop` `fa452197` under the same command.

## Notes

- Found in spec 245's capability batch; identical on the base with the slice's files unchanged.

## Acceptance sketch

- The assertion and the renderer agree on the hymn row order, with the chosen order recorded.

## Links

- Spec: —
- Related items: ITEM-012 (hymn song order)
