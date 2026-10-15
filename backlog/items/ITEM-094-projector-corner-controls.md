---
id: ITEM-094
status: in-review
title: Quiet controls for the mirrored service projector
type: feat
priority: P1
effort: L
created: 2026-10-14
updated: 2026-10-15
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
- The owner accepted the [single-suggestion Go To preview](../../specs/091-projector-corner/preview-goto-autocomplete.html) and its [Spec 091 amendment](../../specs/091-projector-corner/spec.md#accepted-amendment-one-suggestion-go-to).
- The owner accepted the [two-field search-clear preview](../../specs/091-projector-corner/preview-search-clear.html) and its [Spec 091 amendment](../../specs/091-projector-corner/spec.md#accepted-amendment-projector-search-clear-controls).
- The owner approved the [revised running-text cue preview](../../specs/091-projector-corner/preview-cue-running-text.html) and accepted its [Spec 091 amendment](../../specs/091-projector-corner/spec.md#accepted-amendment-running-untitled-text-cue-labels).
- The owner approved the 550-weight, quieter-resting-label [cue preview](../../specs/091-projector-corner/preview-cue-running-text.html) and accepted its [Spec 091 amendment](../../specs/091-projector-corner/spec.md#accepted-amendment-quieter-corner-cue-typography).
- The owner approved the [shared corner color preview](../../specs/091-projector-corner/preview-cue-state-colors.html) and accepted its [Spec 091 amendment](../../specs/091-projector-corner/spec.md#accepted-amendment-shared-corner-control-colors): cue text, list, next, bait, translation, and keyboard controls share resting, hover, and highlighted colors without keyboard-button fill.
- The owner approved the [Go To motion preview](../../specs/091-projector-corner/preview-goto-morph.html) and accepted its [Spec 091 amendment](../../specs/091-projector-corner/spec.md#accepted-amendment-go-to-morph-animation): G now shares the service list's open/close morph, with a transparent click-intercepting overlay and reduced-motion fallback.
- The owner approved the [chapter-only Go To preview](../../specs/091-projector-corner/preview-goto-chapter-first-verse.html) and accepted its [Spec 091 amendment](../../specs/091-projector-corner/spec.md#accepted-amendment-chapter-only-go-to-opens-its-first-verse): selecting a chapter suggestion opens its first available verse while the suggestion retains the chapter-only label.
- OBS projection sources and old docks are separate surfaces.

## Acceptance sketch

- Current and next entry remain identifiable through passages, songs, texts, rests, and breaks.
- Keyboard and mouse can each navigate, toggle words, and make direct service jumps without relying on the other input.
- Shortcut sheet and entry list intercept outside clicks safely; HUD and pointer inactivity preserve deliberate C hiding.
- The projector text and controls match the approved 1366×768 preview and fit smaller viewports.

## Links

- Spec: [091](../../specs/091-projector-corner/spec.md)
- Related items: ITEM-007 (service entries), ITEM-060 (built-in rests); ITEM-002 concerns the separate OBS projection source.
