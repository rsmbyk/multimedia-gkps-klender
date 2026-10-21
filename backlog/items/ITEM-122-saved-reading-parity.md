---
id: ITEM-122
status: in_review
title: 'Match saved reading views to refreshed pages'
type: fix
priority: P1
effort: M
created: 2026-10-21
updated: 2026-10-21
spec: specs/122-saved-reading-parity/spec.md
branch: fix/122-saved-reading-parity
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/370
archived_at:
archive_reason:
bump: patch
release_version: 1.20.1
---

# ITEM-122: Match saved reading views to refreshed pages

## Summary

Saved-library navigation briefly shows incorrect labels, headings, hymn references, and action markup before an online refresh. Match the first saved render to the direct server page across reading routes, including offline use.

## Acceptance sketch

- Song and empty Tata Ibadah sidebar opens match the corresponding reload immediately.
- Offline saved views retain the same meaningful markup.

## Links

- Spec: [122](../../specs/122-saved-reading-parity/spec.md)
- Related items: ITEM-119, ITEM-121
