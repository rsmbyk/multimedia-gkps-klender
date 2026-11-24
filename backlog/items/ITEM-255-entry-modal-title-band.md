---
id: ITEM-255
status: in review
title: 'Large entry dialogs lost their title band'
type: fix
priority: P1
effort: S
created: 2026-11-24
updated: 2026-11-24
spec: 240-entry-modal-title
branch: fix/240-entry-modal-title
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-255: Large entry dialogs lost their title band

## Summary

New text, Edit text and New media opened in the 840×760 dialog with the title painted
at the dialog's own top-left corner: no 26px/20px inset and no divider. Spec 226 moved
those declarations from `.editor__title` to `.editor__head`, but the entry form has no
header row. Restore the band for headerless large forms without touching the verse
header's single rule or the compact dialogs.

## Notes

One scoped selector in `static/styles/design/components.css` plus its narrow override;
no template, script, endpoint or model change. The live preview, before/after numbers
and the new E2E module live in the spec pack. The card closes on the slice PR, not in a
follow-up board PR.

## Acceptance sketch

- At 1440×900 the title text starts 26px from the dialog's left and 21px from its top,
  the band is 72.5px tall, and one 1px rule sits under it in all three large dialogs.
- At 390×844 the band is `16px 18px`, text 18px/17px, the 1px rule stays and the page
  behind gains no scrollbar.
- Verse Create/Edit keep spec 226's one head rule; passage, song and media Edit keep
  the compact 480px dialog with their divided title.

## Links

- Spec: [240-entry-modal-title](../specs/240-entry-modal-title/spec.md)
- Related items: ITEM-241 (spec 226, the change that exposed this)
