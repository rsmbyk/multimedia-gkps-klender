---
id: ITEM-260
status: done
title: 'Search and Media Library rail fetches show pending state'
type: feat
priority: P1
effort: M
created: 2026-11-26
updated: 2026-11-26
spec: 245-rail-fetch-feedback
branch: fix/245-rail-fetch-feedback
pr: 627
issue: 626
closed_at: 2026-11-26
closed_reason: merged into develop (PR #627)
bump: patch
release_version:
---

# ITEM-260: Search and Media Library rail fetches show pending state

## Summary

The Search and Media Library rail tiles did not show the pending state the other rail and sidebar
fetches show. Make both fetch in place, lock the clicked tile, bar the reading stage and seed a
placeholder from the destination's own markup. Direct Media Library loads show a loading count and
spinner until the companion and references settle.

## Notes

- New `reading/R62` extends `reading/R61`; spec 245's accepted preview is `preview/combined.html`.
- The Media Library companion's local allow-list accepts port 8787 through
  `preview/media-override.yml`; tracked Compose configuration is unchanged.
- Push-step red attribution is recorded in spec 245's `converge.md`, pass 11.

## Acceptance sketch

- Clicking either rail tile while its response is delayed locks only that tile and bars the stage.
- The placeholder matches the destination layout: Search results/home or the library's grouped file
  rows, with no old search shell showing beneath it.
- Settlement clears lock, bar, `aria-busy` and placeholder; a later stage write supersedes it.

## Links

- Spec: [245-rail-fetch-feedback](../specs/245-rail-fetch-feedback/spec.md)
- Related items: ITEM-258 (the rail/sidebar pending-state rule)
