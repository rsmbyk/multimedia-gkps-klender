---
id: ITEM-176
status: in-review
title: 'Closing the file picker closes the New media dialog'
type: fix
priority: P1
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/163-media-dialog-file-picker-cancel/spec.md
branch: fix/163-media-dialog-file-picker-cancel
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/462
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-176: Closing the file picker closes the New media dialog

## Summary

The New media form's file input sits inside the editor dialog, and the browser fires `cancel` at that
input when the person closes the picker without choosing. The dialog's own `cancel` listener
(`static/web/media-entry.js:19`) treats every `cancel` that reaches it as its Escape, so the bubbling
input event dismisses the whole form. Everything typed into it goes too.

## Notes

The same event fires when the person re-picks the file they already chose — the browser reports that as
`cancel`, not `change` — so the dialog also closes on a re-pick.

Reproduced on the slice's own server (`/tatib/149/`, 1440×900, Chromium): the dialog closes 248ms after
the input's `cancel` and the form is discarded. Escape on the dialog itself fires `cancel` at the
dialog, which is the path the listener was written for.

## Acceptance sketch

- Dismissing the picker leaves the New media dialog open, on its tab, with its chosen file, its title
  and its Save state unchanged.
- Escape on the dialog still closes it, with the same 150ms motion; the other editor forms are
  untouched.

## Links

- Spec: [163](../specs/163-media-dialog-file-picker-cancel/spec.md)
- Related items: ITEM-107 (the New media modal's layout), ITEM-157 (media size precision)
