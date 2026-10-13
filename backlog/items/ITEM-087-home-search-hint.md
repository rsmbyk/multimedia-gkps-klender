---
id: ITEM-087
status: done
title: Refresh the home search helper line
type: chore
priority: P3
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/084-home-search-hint/spec.md
branch: chore/084-home-search-hint
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/338
archived_at:
archive_reason:
bump: patch
release_version: 1.10.5
---

# ITEM-087: Refresh the home search helper line

## Summary

The home's helper line reads `Try Matius 5:13, KJ 152, or pengampunan dosa`. The owner wants the two
examples the congregation actually reaches for: `Try Yoh 3:16 or HAL 411`.

## Notes

- Both new examples were run against the local stack: `Yoh 3:16` returns the Yohanes 3:16 reference and
  `HAL 411` returns its song, so the line advertises nothing empty.
- The old copy is asserted in five places (one unit test, four E2E assertions).
- Draft only — no implementation until the owner accepts Spec 084.

## Acceptance sketch

- The landing home reads `Try Yoh 3:16 or HAL 411`.
- Both examples return results.
- The line stays hidden while results are on screen.

## Links

- Spec: [Spec 084](../../specs/084-home-search-hint/spec.md)
- Preview: [home hint preview](../../specs/084-home-search-hint/preview.html)
- Related items: ITEM-064 (public site revamp — introduced the line)
