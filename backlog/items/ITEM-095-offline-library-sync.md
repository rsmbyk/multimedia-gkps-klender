---
id: ITEM-095
status: done
title: Save the public library for offline reading and service projection
type: feat
priority: P1
effort: L
created: 2026-10-15
updated: 2026-10-16
spec: 092
branch: feat/092-offline-library-sync
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/346
archived_at:
archive_reason:
bump: minor
release_version: 1.12.0
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
- Bible sidebar primary and secondary names follow the selected TB/SIM reading edition in online and saved-copy views; mini tiles retain TB book abbreviations, and a full refresh starts in TB.

## Links

- Spec: [092](../../specs/092-offline-library-sync/spec.md)
- Related items: ITEM-094 (service projector controls), ITEM-021 (previous search reset rule, revised by this spec).
