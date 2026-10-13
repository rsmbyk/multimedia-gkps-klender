---
id: ITEM-086
status: in-review
title: Match the translation switch hover to the screen-mode switch
type: chore
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/083-language-switch-hover/spec.md
branch: fix/083-language-switch-hover
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/337
archived_at:
archive_reason:
bump: patch
release_version: 1.10.4
---

# ITEM-086: Match the translation switch hover to the screen-mode switch

## Summary

The TB/SIM translation switch darkens its text under the pointer while the Multi-line / Single-screen
switch fills the hovered option. Make both answer the pointer the same way.

## Notes

- Two instances share `.read__lang`: the reading header (anchors) and the entry form's passage picker
  (buttons).
- The fill is `--icon-hover-bg` with `--ink` text, as `.screen-mode button:hover:not([aria-pressed="true"])`
  already uses; the selected option must not take it, or it would cover the switch's thumb.
- Draft only — no implementation until the owner accepts Spec 083.

## Acceptance sketch

- Hovering an unselected TB or SIM fills it like an unselected screen-mode option.
- Hovering the selected one changes nothing.
- The header and the modal behave identically.

## Links

- Spec: [Spec 083](../../specs/083-language-switch-hover/spec.md)
- Preview: [switch comparison](../../specs/083-language-switch-hover/preview.html)
- Related items: ITEM-082 (unified Text screen mode — the switch being matched)
