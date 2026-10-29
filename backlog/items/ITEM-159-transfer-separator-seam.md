---
id: ITEM-159
status: done
title: 'The Transfers list draws each boundary twice'
type: fix
priority: P2
effort: S
created: 2026-10-28
updated: 2026-10-28
spec: specs/149-transfer-separator-seam/spec.md
branch: fix/149-transfer-separator-seam
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/425
issue: 426
closed_at: 2026-10-28
closed_reason: merged into develop (425)
bump:
release_version:
---

# ITEM-159: The Transfers list draws each boundary twice

## Summary

A Transfers dialog opened from the rail draws two separators where the transfers that finished in
this session end and the older ones begin: the row's own `border-bottom: 1px` and the session
divider's `border-top: 2px` stack 9px apart. The same fault shows at the dialog's edge — the list has
no scroll container, so it runs over the dialog's 22px bottom padding and its last border paints 4px
above the dialog's own border.

The seam becomes one line, and the list becomes the element that scrolls.

## Notes

- Owner report, with a screenshot of `/media-library/` after uploading and opening the dialog from the
  rail button: "why is there multiple consecutive separators here?"
- Reproduced from the screenshot's own pixels: row border at y=496, divider at y=506–507 (2px), 9px
  band between them; the last row's border at y=1020 against the dialog's border at y=1024.
- The divider's rule (when it appears) is untouched — this is a drawing fault, not a grouping one.
- With fifteen rows the unchecked list paints 451px outside the dialog, over the page.

## Acceptance sketch

- The seam paints one 2px `--divider` line, 9px from the text above and 9px below.
- Every other row boundary stays a 1px `--divider` border at its current position.
- A list taller than `max-height: min(86vh, 46rem)` scrolls inside the dialog; the title stays put and
  the last row's border ends the dialog's 22px bottom padding above its border.
- Nothing in the list paints outside the dialog; a short list is unchanged.

## Links

- Spec: [149](../specs/149-transfer-separator-seam/spec.md)
- Related items: ITEM-113 (the media library's transfer plumbing), ITEM-146 (the list's own design pass)
