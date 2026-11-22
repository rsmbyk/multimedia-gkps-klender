---
id: ITEM-235
status: done
title: 'The search landing opens without its input focused'
type: fix
priority: P2
effort: S
created: 2026-11-22
updated: 2026-11-22
spec: 220-initial-search-focus
branch: fix/220-initial-search-focus
pr: 579
issue: 578
closed_at: 2026-11-22
closed_reason: merged into develop (PR #579)
bump: patch
release_version:
---

# ITEM-235: The search landing opens without its input focused

## Summary

When the empty search landing opens, focus stays on the page rather than the search field, so
starting a search requires a click. Focus the field only on the landing; keep the compact search
field unfocused while results are open.

## Notes

- In scope: the empty landing at `/` or `/search`, including the fresh landing opened by the Search rail.
- Out of scope: a direct or restored results view, its compact search field, and reading pages.

## Acceptance sketch

- Opening the empty search landing puts focus in its search field; typing can start a query without a preceding click.
- Opening or restoring search results does not move focus into the compact search field.
- Opening a reading page does not auto-focus the search field.

## Links

- Spec:
- Related items:
