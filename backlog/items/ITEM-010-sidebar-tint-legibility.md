---
id: ITEM-010
status: in_review
title: 'Higher-legibility selected sidebar tint'
type: chore
priority: P2
effort: S
created: 2026-10-06
updated: 2026-10-06
spec: specs/009-sidebar-tint-legibility/spec.md
branch: feat/009-sidebar-tint-legibility
pr: 266
archived_at:
archive_reason:
bump: patch
release_version: 0.11.2
---

# ITEM-010: Higher-legibility selected sidebar tint

## Summary

Use the accepted light-theme selected-row tint `#B9D7C9` for improved near-black text contrast. Keep Spec 008's dark-theme selection unchanged.

## Notes

- Owner accepted the color after reviewing the light/dark preview on 2026-10-06.
- Contrast: `10.71:1` with light-theme `--ink` (`#1F1F1D`), or `13.63:1` with pure black.
- The live home-to-sidebar browser check confirmed the selected mint remains visible against the rail surface.

## Acceptance sketch

- All selected sidebar row types use `#B9D7C9` with readable near-black text.
- Dark-theme selection and unrelated row states remain unchanged.
- Live light-theme selection remains perceptibly distinct from the rail surface.

## Links

- Spec: [`specs/009-sidebar-tint-legibility/spec.md`](../../specs/009-sidebar-tint-legibility/spec.md)
- Related item: ITEM-009
