---
id: ITEM-057
status: done
title: 'Give each entry a containing box with centred words and equal add-row gaps'
type: chore
priority: P2
effort: M
created: 2026-10-11
updated: 2026-10-11
spec: specs/055-contained-entry-box/spec.md
branch: fix/055-contained-entry-box
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/309
archived_at:
archive_reason:
bump: patch
release_version: 1.3.22
---

# ITEM-057: Give each entry a containing box with centred words and equal add-row gaps

## Summary

The owner's four rules for the service pane, to hold in every condition: the top and bottom gaps
must include the control buttons, the gaps must look equal, the texts/words must be centred
vertically, and the buttons stay floating at the entry's top-right. The approved model: every
entry with controls is a **containing box** (min-height 52px = 8 + 36 + 8) whose words are
centred; every revealed add row keeps **8px** to the boxes above and below; the start bar
collapses and reveals like the other rows; the section-break divider takes the same box.

## Notes

- Reviewed live on `/tatib/142/` in preview rounds of 2026-10-11 (injected CSS, repo untouched);
  owner OKed with "proceed".
- Supersedes spec 053's 44px band. On a tall entry the floating controls overlay its first
  line(s) while shown — the approved trade for no reserved band.
- The start bar is a preceding sibling, so CSS cannot reveal it: `entries.js` gains the sync and
  `tatib.html` wraps the buttons in `.entry__start-inner` (the `.entry__add-inner` pattern).
- Measured in the preview: rest rhythm 12px uniform; revealed 8/8 in every case; centring exact
  on 52px boxes; touch shows bar and rows outright.

## Acceptance sketch

- At rest: bar and rows 0px tall; entry boxes 12px apart, uniformly.
- Revealed row: buttons 8px from the box above and 8px from the box below, always.
- Words centred in the box; controls wholly inside it, floating at the top-right.
- Divider: 52px box, rule centred, note under it; no oscillation on hover.

## Links

- Spec: [055 — Give each entry a containing box with centred words and equal add-row gaps](../../specs/055-contained-entry-box/spec.md)
- Related items: ITEM-054 / spec 052 (resting space), ITEM-055 / spec 053 (the band this
  replaces), ITEM-039 / spec 037 (the neighbouring rows), ITEM-032 / spec 030 (the start bar)
