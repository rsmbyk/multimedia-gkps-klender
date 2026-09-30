---
id: ITEM-002
status: backlog
title: Projection source as display + controls
type: feat
priority: P1
effort: L
created: 2026-09-30
updated: 2026-09-30
spec:
branch:
pr:
archived_at:
archive_reason:
bump: minor
release_version:
---

# ITEM-002: Projection source as display + controls

## Summary

The OBS projection source (`/obs/project/source`) currently only **displays** text and offers a few
keyboard shortcuts. Make it also provide **on-screen controls**, so the operator can drive the
service from the projection window itself without switching to the dock — and without the control
UI distracting from, or being captured with, the projected text.

## Notes

- Today: `multimedia/obs/static/obs/project/source/display.js` renders song lyrics, service items,
  and Bible passages from BroadcastChannel subjects; `controls.js` binds `1`/`2`/`3` and
  `left`/`right`/`space` against the last active app.
- Key constraints:
  - The control UI must be **unobtrusive** — hidden until intent (hover/focus/interact), auto-hide
    — so the projected text stays clean.
  - It must not be **captured** by OBS when hidden; separate the control layer from the display
    layer.
  - Decide the control model first: which controls, for which app (songs / service order / Bible),
    and how "active app" is chosen.
- Shares the design language with the public web redesign (ITEM-001), but is a separate concern.

## Acceptance sketch

- Operator can drive the active app from the projection window.
- Controls never obscure the text and are absent from the OBS capture while hidden.
- Behavior is documented in the glossary terms (Projection, Source, Dock, Control message).

## Links

- Spec: —
- Related items: ITEM-001 (design language), ITEM-000 (process adoption)
