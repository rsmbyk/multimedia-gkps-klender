---
id: ITEM-126
status: done
title: 'A saved hymn song page never shows the song sort control'
type: fix
priority: P2
effort: S
created: 2026-10-24
updated: 2026-10-24
spec: specs/125-saved-song-sort-parity/spec.md
branch: fix/125-saved-song-sort-parity
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/374
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-126: A saved hymn song page never shows the song sort control

## Summary

Opening a hymn-book song from the reading sidebar paints the saved page first, and that page offers the
song sort control beside "Filter songs…" although the server page hides it — a hymn book keeps number
order (spec 011). The online update then hides the control, so it flashes for roughly 220 ms and the song
filter jumps 339 px → 293 px → 339 px under the pointer. The saved renderer decides the control from the
section alone; the server decides it from the book's hymn flag. This slice makes the saved render follow
the server's rule and pins both the parity and the transient in browser tests.

## Notes

- Reported from `/songs/139/` with the sort control visible beside the song filter while the "Saved copy"
  badge was shown.
- A second saved/server difference was found in the same comparison and deliberately kept out of scope:
  the `/songs/` list page's saved render omits the disabled "+ Add song" button the server renders.

## Acceptance sketch

- Opening a hymn-book song from the sidebar never shows the sort control, online or offline, and the song
  filter keeps one width on that route.
- The saved and server song pages agree on the control's hidden state for hymn and non-hymn routes.
- An ordinary songbook's song page still offers the control before and after the online update.

## Links

- Spec: [`specs/125-saved-song-sort-parity/spec.md`](../specs/125-saved-song-sort-parity/spec.md)
- Related items: ITEM-122 (saved reading parity), ITEM-011 (hymn song order, spec 011)
