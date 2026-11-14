---
id: ITEM-199
status: done
title: "The old addresses answer the new app"
type: feat
priority: P1
effort: S
created: 2026-11-14
updated: 2026-11-15
spec: specs/194-legacy-route-retirement/spec.md
branch: feat/194-legacy-route-retirement
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/514
issue: 513
closed_at: 2026-11-15
closed_reason: merged into develop (PR #514)
bump: minor
release_version:
---

# ITEM-199: The old addresses answer the new app

## Summary

This release replaces three OBS docks and four overlay sources with one dock and one
overlay, and closes the back office that `/manage/` served. Every old address is still in a scene
file, a bookmark or a habit, and until now each one answered 200 with a page the release no longer
maintains — the worst case being a browser source opened live, painting a half-loaded old overlay
over the stream. The direction (2026-11-14, chat): the old docks go to the one dock, the old
overlays to a page that paints only one corner note, `/home/` and `/manage/` to `/`, and the old version is
reachable through one `/archive/` namespace for exactly one release.

## Notes

- `/songs/` and `/tatib/` were named in the request but are **not** retired: both are rail
  destinations in the shipped app (`base.html:104`, `:120`) and `static/web/editors.js:318-322`
  returns to them after a save. Retiring them would remove the hymn and service readers; the owner
  chose to keep them at the first gate of the slice.
- The old version cannot be archived as running code: 0.7.0's views read columns its migrations
  dropped (`songs.0015` removed `Book.lang`). The archive is therefore a redirect table, not a copy
  — `/archive/<old path>` answers the live page that replaced it, in one hop.
- Every answer is a 302 — the archive and the retired addresses alike. The owner asked whether an
  old address could be used again later; the honest answer is "on the server yes, in a browser that
  already cached a 301 no", so this release claims nothing permanent and when the archive is
  withdrawn next release each address is decided between a 301 and reuse.
- `multimedia/obs/` (564K of old docks and overlays) and `multimedia/web/manage/` become
  unreachable here and are deleted with the archive, not before.

## Acceptance sketch

- Every old OBS address (`/obs/{bible,songs,tatib}/dock`, `/obs/{bible,songs,tatib}/source`,
  `/obs/project/source`, `/obs/project/settings`), with and without a trailing slash, answers 302:
  docks → `/obs/dock`, sources → `/obs/blank`, settings → `/`.
- `/obs/blank` answers 200 with a transparent page carrying one corner note — `Old OBS source` at
  20% white, `Switch to /obs/source/overlay` on hover — no script, no image; `no-store` on it.
- `/home/` and every `/manage/…` address answer 302 to `/`.
- `/songs/` and `/tatib/` answer exactly as today.
- `/archive/…` answers 302 to the successor of the address it names, one hop, nothing rendered.

## Links

- Spec: [194](../specs/194-legacy-route-retirement/spec.md)
- Related items: ITEM-196 (spec 192, the companion page — the slice that moved `VERSION` to 1.30.0),
  ITEM-181 (spec 167, Tata Ibadah templates), ITEM-002 (projection source as display + controls —
  the demand the old `/obs/project/settings` answered)
