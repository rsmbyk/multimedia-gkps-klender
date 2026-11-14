---
id: ITEM-129
status: done
title: 'Name the site in the tab, and stop the index tab at the name'
type: fix
priority: P2
effort: S
created: 2026-10-24
updated: 2026-10-24
spec: specs/127-site-name-tab/spec.md
branch: fix/127-site-name-tab
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/378
issue:
closed_at:
closed_reason:
bump: patch
release_version: 1.20.5
---

# ITEM-129: Name the site in the tab, and stop the index tab at the name

## Summary

Every reading page's browser tab names the site `GKPS Klender`, while the rest of the application — the
site root's `index.html`, the maintenance notice, the manage and Tata Ibadah pages — already calls it
`Multimedia GKPS Klender`. The index's tab then spends its width on a trailing tagline
(`GKPS Klender — Search Alkitab, Kidung, and Tata Ibadah`), truncated to `GKPS Klender — Sea…` in the
vertical tab strip the request's screenshot shows.

## Notes

- The title is written in three places that must agree: the Django view context and template defaults, the
  saved renderer (`static/web/offline-render.js`), and the in-place update in `static/web/reading.js`.
- The index's title — `/`, `/home/`, and `/search` with no query — becomes the site name alone; every other
  reading page appends ` — Multimedia GKPS Klender`.
- Nothing visible moves: headings, the search field's accessible name, the logo's `alt` and the rail's
  labels keep `GKPS Klender`.

## Acceptance sketch

- `/`, `/home/` and `/search` read exactly `Multimedia GKPS Klender`.
- A Bible chapter, song, Tata Ibadah service, section landing, results page and the Media Library end with
  ` — Multimedia GKPS Klender`, their leading text unchanged.
- A page rendered from the saved library carries the same title as the server page, and an in-place Bible
  edition switch does not rename the tab.

## Links

- Spec: [127](../../specs/127-site-name-tab/spec.md)
- Related items: ITEM-127 (spec 126), ITEM-122 (spec 122)
