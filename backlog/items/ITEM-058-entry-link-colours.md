---
id: ITEM-058
status: done
title: 'Give the stage entry links a theme-aware colour'
type: chore
priority: P2
effort: S
created: 2026-10-11
updated: 2026-10-11
spec: specs/056-entry-link-colours/spec.md
branch: fix/056-entry-link-colours
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/308
archived_at:
archive_reason:
bump: patch
release_version: 1.3.21
---

# ITEM-058: Give the stage entry links a theme-aware colour

## Summary

The Tata Ibadah stage's entry titles (`.entry__jump` — song and passage links) have no author
colour, so they render in the browser default blue `#0000EE` in both themes: measured 1.98:1 on
the dark canvas where the body text is 16.8:1. Give them a `--link` token — forest green
`#1C5C3C` in light (7.29:1), lifted royal blue `#7C9CF0` in dark (6.97:1) — keeping the
underline.

## Notes

- Owner saw a four-option colour grid (default blue / sage / royal / quiet ink) in both themes
  on the live page (2026-10-11) and chose the green-light + blue-dark combo.
- Scope is exactly `.entry__jump`; the rail logo is an image and other anchors are styled.
- The tokens contrast test gains the pair, so a later palette edit cannot silently break it.

## Acceptance sketch

- Light: entry links render `#1C5C3C`; dark: `#7C9CF0`; both AA on the canvas.
- Underline stays; hover/focus/visited keep the colour; no other anchor changes.

## Links

- Spec: [056 — Give the stage entry links a theme-aware colour](../../specs/056-entry-link-colours/spec.md)
- Related items: ITEM-005 / spec 004 (design tokens), ITEM-056 / spec 054 (the heading the
  links render)
