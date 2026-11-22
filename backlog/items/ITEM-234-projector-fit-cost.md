---
id: ITEM-234
status: in-review
title: 'A text screen arrives late while the entries beside it arrive at once'
type: fix
priority: P1
effort: S
created: 2026-11-22
updated: 2026-11-22
spec: 219
branch: fix/219-projector-fit-cost
pr: 576
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-234: A text screen arrives late while the entries beside it arrive at once

## Summary

The owner's report, 2026-11-22: "in projector, when you are advancing to a text entry, or a screen of
the same text entry, there is a delay of the text showing. you can clearly feel it as it is not as
fast as the other entries/screens." A second report followed with a screenshot of three overlapping
texts: "then screen goes weird when you hold down left/right keys."

The projector fits a screen's words by walking the font size down from 200 px one pixel at a time,
asking after each whether the words still fit; every question forces a layout of the page, which
holds every screen of the service. So an advance into a screen of words costs 130–280 layout reads
before the browser can paint it, and the cost grows with the body: a short lyric settles high, a text
entry comes down furthest. Two further defects sit on top: the fit runs *after* the arrival morph has
started, so it measures the words 14 px lower than they come to rest — the same screen was fitted to
131 px on an advance and 135 px on a resize — and the arrival animation is stalled by the work while
it plays.

## Notes

- Held keys: each move starts a 240 ms crossfade and a repeat arrives every ~35 ms, so the crossfades
  stack — measured 7 screens painted at once on `develop`, 64 frames of 122 carrying an overlap. A
  move that arrives mid-morph now cuts, leaving 1 screen painted and 1 overlapping frame.

- Measured on the local service **Ibadah Minggu** (171 screens, 126 carrying words) at 1440 × 900:
  a word-bearing screen costs 14.5 ms median and 59 ms worst on `develop`, a blank one 1.0–1.8 ms.
- 19 of 60 screens are fitted to a different size on an advance than on a resize on `develop`.
- A single-screen text whose body cannot fit at any size is cut one character at a time: 2 992 ms for
  a 400-row body, 3 711 characters kept.

## Acceptance sketch

- A screen either side of the one showing is fitted before it is asked for, so a paced advance costs
  no fitting at all.
- The fit measures the screen at rest, so an advance and a resize agree on every screen.
- The largest fitting size is unchanged, and the single-screen cut keeps the same rows and characters.
- A screen that was not fitted ahead of time is still fitted correctly on arrival.
- A held arrow key paints one screen at a time, and a single move still crossfades.

## Links

- Spec: `specs/219-projector-fit-cost/spec.md`
- Related items: ITEM-031 (spec 031, one-screen fitted text), ITEM-060 (built-in projection breaks)
