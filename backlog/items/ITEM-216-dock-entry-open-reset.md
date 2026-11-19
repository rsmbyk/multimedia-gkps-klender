---
id: ITEM-216
status: in-review
title: 'Opening a service starts its entry blocks shut'
type: fix
priority: P1
effort: S
created: 2026-11-19
updated: 2026-11-19
spec: 204
branch: fix/204-dock-entry-open-reset
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/548
issue: 546
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-216: Opening a service starts its entry blocks shut

## Summary

A hand-opened entry block in the OBS dock leaks to the same *position* in the next service the
operator opens — including the same service opened again. The override map is keyed by entry index
and lives for the whole page, while an open rebuilds the list for a different service. Opening a
service should start every block shut, except the live entry's, which stays open.

## Notes

- Reproduced on `develop` (`85319b73`) against the live dock: expand position 4 in service 155
  (12 entries), open service 149 (5 entries) → position 4 stands open there, 70 px tall, untouched.
  Re-opening 155 keeps it open at 126 px. Three hand-opened blocks (1, 3, 8) leak as `[1, 3]` into
  the 5-entry service.
- Cause: `static/web/obs-dock.js` — `entryOverrides` (a page-memory `Map<index, boolean>`) is never
  cleared by `openService()`, and `effectiveOpen()` reads it for whichever service is drawn.
- Spec 198's R14 pins two lifetimes already: a hand-opened block survives a crossing, and nothing
  survives a reload. The open is the third event, and it was left unspecified.
- Out of scope by measurement: switching service mid-crossing produced no scroll jolt
  (scrollTop 0 across 900 ms into a 27-entry list, three attempts).
- Drafted as `ITEM-213`; spec 203 landed that ID on `develop` while the pack was in review, so the
  card renumbered to `ITEM-216` before the first commit (214 and 215 were taken too). Anchor issue
  #546 backfilled at Implement, per the board's tracker-mirror rule.

## Acceptance sketch

- Open another service after expanding a block: no non-live block stands open.
- Re-open the same service: the same.
- The live entry's block stays open when its own service is opened.
- A crossing and a re-read keep hand-opened blocks open (spec 198 / R13 unchanged).

## Links

- Spec: [204](../../specs/204-dock-entry-open-reset/spec.md)
- Related items: [ITEM-208](ITEM-208-dock-entry-toggle.md) (spec 198, the header toggle)
