---
id: ITEM-074
status: in_review
title: Scroll Preview text with arrow keys
type: fix
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/071-preview-keyboard-scroll/spec.md
branch: fix/071-preview-keyboard-scroll
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/324
archived_at:
archive_reason:
bump: patch
release_version: 1.6.8
---

# ITEM-074: Scroll Preview text with arrow keys

## Summary

Clicking a long Preview's text leaves focus on the dialog, so ArrowUp and ArrowDown cannot scroll its body. Focus the scrollable body after a non-interactive text click while preserving control focus and modal dismissal.

## Notes

- Separate from the proposed unified Text entry and three-way screen-mode switch.
- The shared Preview dialog covers Text, Single-screen Text, passage, and song entries.

## Acceptance sketch

- Clicking text in an overflowing Preview allows native ArrowUp and ArrowDown scrolling without moving the page behind it.
- Clicking a break button or song tab preserves that control's focus and behavior.
- Escape and backdrop dismissal still restore focus to the Preview opener.

## Links

- Spec: [Spec 071](../../specs/071-preview-keyboard-scroll/spec.md)
