---
id: ITEM-205
status: in-progress
title: 'A saved change reaches the on-air surfaces'
type: fix
priority: P1
effort: S
created: 2026-11-15
updated: 2026-11-15
spec: 195
branch: fix/195-hotfix-batch
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-205: A saved change reaches the on-air surfaces

## Summary

Editing the on-air Tata Ibadah's entries leaves the OBS overlay painting the old entries. The projector re-reads on the `update` message, but the overlay (and the dock) fetch each service's screens once and cache them for the whole session, so even a delivered re-read request repaints the stale data (seen on production, 2026-11-15).

## Notes

- `obs-overlay.js` and `obs-dock.js` both hold a per-service cache with no invalidation; the overlay hears `update` but re-paints from the cache.
- Whether the re-read request can reach the overlay at all depends on where it is edited — same browser (the channel carries it) or a separate OBS browser (nothing carries it) — decided at Clarify.

## Acceptance sketch

- With a service on air, editing its entries (add, edit, reorder, delete) repaints the overlay with the new words.
- The dock's step list and the projector agree with the overlay.

## Links

- Spec:
- Related items:
