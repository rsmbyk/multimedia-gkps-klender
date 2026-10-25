---
id: ITEM-138
status: in-review
title: 'A text entry opens in the media modal''s large frame'
type: chore
priority: P2
effort: S
created: 2026-10-25
updated: 2026-10-25
spec: specs/133-text-modal-large-frame/spec.md
branch: feat/133-text-modal-large-frame
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/394
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/393
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-138: A text entry opens in the media modal's large frame

## Summary

`+ Text` and `+ Media` sit side by side and open the same dialog, but one drew 480×495 and the other
840×760. Every text form — create and edit — now opens in that 840×760 frame with the same title band,
gutters and action row, and its Text box fills the height the frame leaves instead of sitting in a
131px hole. The frame belongs to the dialog, not to a kind's script: the form says
`data-editor-size="large"` and the stylesheet keys on that.

While measuring it, the dialog turned out to be laid out in document coordinates, so a scrolled page
moved it: a 760px frame on a service scrolled 74px opened at y = −4 and clipped its title band. The
dialog is now `position: fixed`, which centres it on the window at any scroll position and leaves the
date popover resolving inside it.

## Notes

- The media create dialog's values are the reference and are unchanged: 840×760, `20px 26px` title band
  at 21px, 788px fields at x=326, action row `14px 26px 20px` with no divider.
- Passage, song and media-edit forms keep the compact 480px dialog.
- Below 650px the gutters fall to 18px and the title band to `16px 18px`.
- The switch, its help line and the Save guard are untouched; `entries.js` was not edited.

## Acceptance sketch

- At 1440×900 `+ Text` and `+ Media` measure the same box, title band, field gutter, field width, action
  row and Save x.
- The Text box ends 14px above the action row: 419px on create, 507px on edit, 227px at 1280×600.
- At 390×844 the frame is 352×760 with 18px gutters and no document scroll.
- An entry's Edit opened on a page scrolled to the bottom is centred on the window.
- `multimedia.web` green; the new browser module green; the switch and Save-guard modules re-run
  unchanged.

## Links

- Spec: [133](../specs/133-text-modal-large-frame/spec.md)
- Related items: ITEM-133 (the empty service's add tiles, the same stage), ITEM-122 (saved-page parity)
