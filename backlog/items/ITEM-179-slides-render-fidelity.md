---
id: ITEM-179
status: done
title: 'A converted deck is drawn in a monospaced face and reflows every slide'
type: fix
priority: P1
effort: M
created: 2026-10-30
updated: 2026-10-30
spec: specs/166-slides-render-fidelity/spec.md
branch: fix/166-slides-render-fidelity
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/469
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/468
closed_at: 2026-10-30
closed_reason: merged into develop (#469)
bump: patch
release_version:
---

# ITEM-179: A converted deck is drawn in a monospaced face and reflows every slide

## Summary

A PowerPoint shown on the projector does not look like the deck. The companion's image carries only
Liberation fonts, so every proportional family the worship decks name — Calibri 630 runs, Calibri Light
through the theme, Britannic Bold 52, Berlin Sans FB Demi 6 — resolves to **Liberation Mono**. Monospaced
advances re-wrap every run, and the composition moves: the cover's title collapses into a 300 × 275 px
column where the deck draws 477 × 199 px, a schedule table's words land up to 250 pt from their place,
and the offering page's band wraps its two amounts and clips the lower one. The image's LibreOffice is
also 7.4 (Debian bookworm, 2022), which keeps wrapping the same tables even once the fonts are there.

## Notes

Measured on the deck the operator reported, `95a90f31…`, converted by the running companion on
2026-10-25 (`derived-slides/95a90f31…-e073f7c4fb0425d1.pdf`). Inside the media container,
`fc-match Calibri` answers `LiberationMono-Regular.ttf`. With LibreOffice 25.2 and the faces mapped to
their metric-compatible equivalents, page 2's table words land on the reference render's own
coordinates (x 641.853496, y 8.777335) and the cover's title ink is 477 × 199 px, one pixel from it.

`Britannic Bold` and `Berlin Sans FB Demi` ship only with Office: the slice makes them suppliable from
a mounted directory rather than shipping them.

The derived PDF is keyed on `libreoffice --version` alone, so a font change without a version change
would leave the old render in place — the identity now covers the fonts too.

## Acceptance sketch

- Every family the decks use resolves to a proportional, metric-compatible face; the build fails on a
  monospaced fallback.
- The image carries LibreOffice 25.2 or newer.
- The reported deck's Calibri and Times New Roman pages land within 1 pt of the reference render; the
  offering page's band holds 5 words with both amounts on their labels' lines.
- A changed LibreOffice or a changed font set produces a new derivative on the next request; an
  unchanged converter still converts once.
- A font dropped into the mounted directory is picked up on the companion's next start.

## Links

- Spec: [166](../specs/166-slides-render-fidelity/spec.md)
- Related items: ITEM-117 (PDF and PowerPoint display), ITEM-118 (the deck's own identity kept)
