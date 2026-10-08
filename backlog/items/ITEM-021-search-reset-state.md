---
id: ITEM-021
status: in_progress
title: 'Clear remembered search when the home is reset'
type: fix
priority: P1
effort: S
created: 2026-10-07
updated: 2026-10-07
spec: specs/019-search-reset-state/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-021: Clear remembered search when the home is reset

## Summary

Resetting to the empty search home should clear the remembered result URL and scroll offset. Sidebar browsing without a reset must keep the existing restore-last-results behavior.

## Notes

- `#searchHome` and `#searchResults` are intentional conditional regions in one shell, not duplicate pages.
- Owner decision: reset means a fresh `/home/` landing with no query; the search-field × remains a clear-input action that retains displayed results.

## Acceptance sketch

- Reset home clears the remembered result and scroll keys; rail Search stays on the empty home.
- Sidebar browsing preserves remembered search and scroll until reset.

## Links

- Spec: [019 — Clear remembered search when the home is reset](../../specs/019-search-reset-state/spec.md)
- Related items: ITEM-005 (public site revamp), ITEM-006 (sidebar editors)
