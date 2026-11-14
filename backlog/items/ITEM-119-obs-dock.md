---
id: ITEM-119
status: done
title: 'OBS dock: run Service Entries with one state for dock, projector, and overlay'
type: feat
priority: P1
effort: L
created: 2026-10-19
updated: 2026-10-21
spec: specs/119-obs-dock/spec.md
branch: feat/obs-dock
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/367
issue:
closed_at: 2026-10-21
closed_reason: merged into develop (PR #367)
bump: minor
release_version: 1.20.0
---

# ITEM-119: OBS dock — one state for dock, projector, and overlay

## Summary

Give the operator one dock inside OBS that picks a Tata Ibadah, browses it, and runs it,
while a fixed-URL projector page and a caption overlay browser source render the same
browser-local state. Closing or opening any surface catches up to what is on air; the
old per-service projector windows, their beat reaper, and the "one Tata Ibadah per
browser" step-aside go away.

## Notes

The owner settled the model across the interactive mockup (v1–v70, October 2026): one
dock drives both the projector and the overlay; the projector's URL moves to
`/projector` with `?service=<id>` as an act of projection; the dock lives at
`/obs/dock` and the overlay at `/obs/source/overlay`; hide (reversible pause) and
release (Stop project) are distinct verbs; the overlay caption is Source Sans 3 at the
measured broadcast proportions; the projector keeps CMG Sans with Source Sans 3 as its
bundled fallback and balanced wrapping on its screen lines.

## Acceptance sketch

- The dock runs a service end to end: picker → runner, entry-click projects, screens and
  baits step, TB/SIM flips both surfaces, hide/show resumes in place.
- `/projector` follows the dock and adopts `?service=<id>` without navigating; the
  overlay captions the same screen and is control-free.
- Every surface catches up after all were closed; many tabs agree; Stop project releases
  everything and the button flips back to Project.
- Fonts are bundled; the projector renders CMG Sans (Source Sans 3 fallback) with
  balanced wrapped rows; media entries and legacy pages are unchanged.

## Links

- Spec: [119](../../specs/119-obs-dock/spec.md)
- Preview: [mockup v70](../../specs/119-obs-dock/preview/dock-preview.html)
- Related items: [ITEM-002](./ITEM-002-projection-controls.md),
  [ITEM-007](./ITEM-007-service-entries.md),
  [ITEM-094](./ITEM-094-projector-corner-controls.md)
