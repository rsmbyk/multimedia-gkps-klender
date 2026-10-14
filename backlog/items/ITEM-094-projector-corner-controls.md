---
id: ITEM-094
status: in-review
title: Quiet controls for the mirrored service projector
type: feat
priority: P1
effort: L
created: 2026-10-14
updated: 2026-10-14
spec: 091
branch: feat/091-projector-corner
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/346
archived_at:
archive_reason:
bump: minor
release_version: 1.11.0
---

# ITEM-094: Quiet controls for the mirrored service projector

## Summary

The hall projector mirrors the operator's laptop. Show the current and next service positions in a quiet corner, and let the operator navigate or jump without displaying the editor. Keyboard-only and mouse-only operation must both be complete for ordinary service projection.

## Notes

- The [approved preview](../../specs/091-projector-corner/preview.html) and [gallery](../../specs/091-projector-corner/preview-gallery.html) record the visual decisions.
- The Draft includes projector header/body fitting, keyboard navigation, entry and library finds, the service list, mouse zones, and unobtrusive inactivity behavior.
- OBS projection sources and old docks are separate surfaces.

## Acceptance sketch

- Current and next entry remain identifiable through passages, songs, texts, rests, and breaks.
- Keyboard and mouse can each navigate, toggle words, and make direct service jumps without relying on the other input.
- Shortcut sheet and entry list intercept outside clicks safely; HUD and pointer inactivity preserve deliberate C hiding.
- The projector text and controls match the approved 1366×768 preview and fit smaller viewports.

## Links

- Spec: [091](../../specs/091-projector-corner/spec.md)
- Related items: ITEM-007 (service entries), ITEM-060 (built-in rests); ITEM-002 concerns the separate OBS projection source.
