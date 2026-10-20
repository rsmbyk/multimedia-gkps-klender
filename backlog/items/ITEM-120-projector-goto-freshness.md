---
id: ITEM-120
status: in_progress
title: 'Refresh projector Go To data while online'
type: fix
priority: P1
effort: M
created: 2026-10-20
updated: 2026-10-20
spec: specs/120-projector-goto-freshness/spec.md
branch: fix/120-projector-goto-freshness
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.19.2
---

# ITEM-120: Refresh projector Go To data while online

## Summary

Go To reads the committed saved Bible/song library. A changed server song title was absent from online suggestions until library sync or page reload. Make online suggestions settle on current data while preserving offline lookup.

## Acceptance sketch

- Changed Bible and song records appear in online Go To without reloading.
- Saved suggestions remain usable if offline or sync fails.
- Older lookups cannot overwrite a newer query or disturb projection.

## Links

- Spec: [120](../../specs/120-projector-goto-freshness/spec.md)
- Related: Spec 119 (public reading navigation).
