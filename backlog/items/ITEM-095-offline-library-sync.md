---
id: ITEM-095
status: in-progress
title: Save the public library for offline reading and service projection
type: feat
priority: P1
effort: L
created: 2026-10-15
updated: 2026-10-15
spec: 092
branch: feat/092-offline-library-sync
pr:
archived_at:
archive_reason:
bump: minor
release_version:
---

# ITEM-095: Save the public library for offline reading and service projection

## Summary

Save complete public Bible, song, and Tata Ibadah content plus the two supported shells in the browser. Readers and the service projector can continue offline after an initial visit, while later online checks fetch changed data. In-page reading and per-tab search history use saved content without downloading another HTML page.

## Notes

- [Accepted Spec 092](../../specs/092-offline-library-sync/spec.md) and [status preview](../../specs/092-offline-library-sync/preview.html).
- Keep existing OBS docks, editors, and unrelated pages outside the offline scope.
- Browser history is for end content and searches; each tab keeps its own search state.

## Acceptance sketch

- First completed sync makes included public reading and service projector routes available offline; interrupted sync leaves the previous generation intact.
- Current content loads from saved data immediately and refreshes asynchronously online.
- Direct search URLs, repeat queries, Show more, tab isolation, and Back/Forward honor Spec 092 state rules.

## Links

- Spec: [092](../../specs/092-offline-library-sync/spec.md)
- Related items: ITEM-094 (service projector controls), ITEM-021 (previous search reset rule, revised by this spec).
