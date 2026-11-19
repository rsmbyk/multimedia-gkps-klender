---
id: ITEM-207
status: done
title: "The dock's pinned bucket head leaves a 4px gap under the toolbar"
type: fix
priority: P2
effort: S
created: 2026-11-16
updated: 2026-11-17
spec: specs/197-dock-bucket-head-pin/spec.md
branch: fix/197-dock-bucket-head-pin
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/529
issue: 528
closed_at: 2026-11-17
closed_reason: merged into develop (PR #529)
bump: patch
release_version:
---

# ITEM-207: The dock's pinned bucket head leaves a 4px gap under the toolbar

## Summary

Scrolling the dock picker pins each age bucket's head, but not to the top: the head's box starts 4px below
the scroller's top edge, because that 4px is the scroll body's `padding-top` and the head's `top: 0` resolves
inside it. The row above keeps painting in the band, so the head reads as floating instead of pinned. The fix
moves the strip's ownership to the head — the picker body carries no top padding and the head's own 14px top
padding is the sky above the label — so the label stays at the same height at rest and pinned, and the head's
foot does not move.

## Notes

- Reported on `/obs/dock` at 449×604, dark theme, with a screenshot: "the pinned date group headers are not
  perfectly pinned to the toolbar (there is a small gap between it and the toolbar)" (2026-11-16).
- The band is silent at many offsets — a row's padding is the same `--rail-bg` as the head — and shows only
  where a row's glyphs or a badge cross it. Both cases are the same defect.
- Measured before/after: head box top 68.00 → 64.00px with the scroller at 64.00px; row pixels in the strip
  up to 9,715 at 4× over 514 offsets → 0; hit test at scroller top + 2px `BUTTON.servicerow` → `H3`. The
  label sits 14.00px under the divider in both states (it is 78.00px from the viewport top either way), and
  the head's foot is 100.52px on both, so no other box in the list moves.
- A first shape (`top: -4px` on the head, reserve 37 → 33px) was retracted at preview: it kept the label at
  78.00px at rest and moved it to 74.00px when pinned, which the owner saw as the pinned header sitting
  differently from the rest one.
- The owner asked for the air between buckets to grow slightly: `#pickBody section + section { padding-top:
  12px }`, so the next label sits 26.00px below the previous group's last row (10.00px on develop). Carried by
  the section, it scrolls away and never enters the pin.

## Acceptance sketch

- At every scroll offset where a bucket head is pinned, nothing but the head paints between the divider and
  its label, at 320–2560px and in both themes.
- At `scrollTop` 0 the picker looks exactly as it does today.
- The air above the next bucket's label is 26px (from 10px), and it scrolls away without moving the pin.
- Walking the picker's cursor never parks a row under the pinned head.
- The runner's pinned entry and next band answer as they do today.

## Links

- Spec: [197](../specs/197-dock-bucket-head-pin/spec.md)
- Related items: ITEM-177 (spec 164 — the fluid dock this picker belongs to), ITEM-191 (spec 187 — the
  keyboard grammar that scrolls the cursor into view), ITEM-168 (spec 151 — the rail's marks, untouched).