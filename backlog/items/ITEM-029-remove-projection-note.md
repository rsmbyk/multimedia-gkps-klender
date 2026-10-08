---
id: ITEM-029
status: in_review
title: 'Remove the projection status note'
type: fix
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/027-remove-projection-note/spec.md
branch: fix/027-remove-projection-note
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.0.1
---

# ITEM-029: Remove the projection status note

## Summary

Remove the danger-coloured status line that appears beneath the Project / Stop projecting controls.
It reads like an error but only narrates the display lifecycle — the Update acknowledgement ("The
display is re-reading this Tata Ibadah.") and the window-gone notice ("The projector window is gone,
so the display stopped."). The actions behind it stay: Update still re-reads, and closing the
projector window still stops the display.

## Notes

- The note is `data-project-note` / `.read__project-note`, filled by `say()` in `static/web/display.js`.
- It shares nothing with other status copy, so removal is self-contained.
- Distinct from ITEM-023 / spec 021 (which hid a lock explanation); this is plain lifecycle narration.

## Acceptance sketch

- No status line renders under the Project / Stop projecting controls, in any state.
- Pressing Update still makes the display re-read the page, with no note.
- Closing the projector window still stops the display and returns the button to "Project", with no note.

## Links

- Spec: [027 — Remove the projection status note](../../specs/027-remove-projection-note/spec.md)
- Related items: ITEM-020 (projection button styles), ITEM-028 (live projection editing)
