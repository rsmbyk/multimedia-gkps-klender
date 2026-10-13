---
id: ITEM-090
status: done
title: Slimmer, softer scrollbars with no stepper buttons
type: chore
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/087-scrollbar-refinement/spec.md
branch: chore/087-scrollbar-refinement
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/341
archived_at:
archive_reason:
bump: patch
release_version: 1.10.8
---

# ITEM-090: Slimmer, softer scrollbars with no stepper buttons

## Summary

The reading UI's scrollbars carry up/down stepper buttons and a heavier thumb than a passive indicator
needs. Remove the buttons, take the bar from 6px to 5px, and quiet the thumb in both themes.

## Notes

- Real cause, measured on Chromium 145: the shared block sets the **standard** properties
  (`scrollbar-width: thin`, `scrollbar-color`) *and* the `::-webkit-scrollbar*` pseudo-elements. A
  browser that understands the standard properties takes the native path and ignores the
  pseudo-elements, so the native thin bar (10px here, with a stepper glyph above the thumb) is what is
  drawn. A `::-webkit-scrollbar-button` rule therefore does nothing — the selector belongs to a
  pseudo-element the browser is not using. The first draft of this item had that wrong.
- Fix: gate the standard properties behind `@supports not selector(::-webkit-scrollbar)`, so
  Blink/WebKit draw the custom 5px bar (no buttons) and engines without the pseudo-element keep the
  standard thin coloured bar; keep the button suppression as a belt.
- Proposed thumb values: light `#AAA59B → #B4B0A6` (2.25:1 → 1.99:1) and hover `#827D73 → #948F85`;
  dark `#514D45 → #45413A` (2.21:1 → 1.83:1) and hover `#777268 → #65615A`.
- The mini panel and the Tata Ibadah entry list keep hiding their scrollbars.
- Draft only — no implementation until the owner accepts Spec 087.

## Acceptance sketch

- No scrollbar shows an end button.
- The bar is 5px with a transparent track and fully rounded thumb, and the scroller is on the custom
  `::-webkit-scrollbar` path rather than the native one.
- The resting thumb is quieter than today and the hover state still reads clearly, in both themes.

## Links

- Spec: [Spec 087](../../specs/087-scrollbar-refinement/spec.md)
- Preview: [scrollbar comparison](../../specs/087-scrollbar-refinement/preview.html)
- Related items: ITEM-070 (consistent scrollbars — introduced the shared block)
