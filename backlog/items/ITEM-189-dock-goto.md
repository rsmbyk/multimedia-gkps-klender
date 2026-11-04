---
id: ITEM-189
status: in-review
title: 'The dock can put a passage or a song on air — the Go To, shared by every surface'
type: feat
priority: P1
effort: L
created: 2026-11-03
updated: 2026-11-04
spec: specs/185-dock-goto/spec.md
branch: feat/185-dock-goto
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/491
issue:
archived_at:
archive_reason:
bump:
release_version:
---

# ITEM-189: The dock can put a passage or a song on air — the Go To, shared by every surface

## Summary

The projector has a Go To: `G` opens a search, a passage or a song is chosen, and it paints over the
service until the operator goes back. The dock — the surface the operator actually runs a service
from inside OBS — has no such thing, so an unplanned song or a verse means leaving the dock for the
projector window, and the caption overlay never learns about it at all.

The request: bring the Go To into the dock, with **one** Go To state synced between the dock, the
projector and the overlay, living exactly as long as the Tata Ibadah projection state does (spec 184:
it ends with the browser session, not before).

## Notes

- The blocker is architectural, not cosmetic: `gkps-display` names a service and a screen, and both
  readers rebuild that screen from the service's own page — the projector from its islands, the
  overlay from `/projector?service=<id>`. A song outside the Tata Ibadah has no index in that
  pointer.
- The content already exists: `/projector/goto/index/`, `/chapter/<book>/<chapter>/`,
  `/song/<id>/` (spec 136), and the lookup is a pure function over the index, already shared as
  `static/web/projector-library.js`.
- The projector's Go To is page-local today (`detour`, `returnScreen`, the cue's "back to …"),
  which is why the dock cannot see it and the overlay keeps painting the service underneath it.
- The display state's shape is pinned in `docs/spec/display-state.md` R1 and spec 119's domain
  rules; this slice extends it and states the delta.

## Acceptance sketch

- From the dock's runner, `G` (or the head's control) opens a find row; typing a reference and
  pressing Enter puts that passage or song on air on the projector and on the overlay.
- The dock marks that it is off the service and its transport steps the goto; Back puts the service
  back exactly where it stood, edition included.
- The projector's own `G` writes the same state, so a goto started there shows in the dock and on
  the overlay, and a goto started in the dock shows on the projector's cue.
- A browser restart leaves every surface idle — the goto dies with the session, like the service.

## Links

- Spec: [185](../specs/185-dock-goto/spec.md)
- Related items: ITEM-119 (the display state, spec 119), ITEM-146 (the Go To index and
  fetch-on-selection, spec 136), ITEM-188 (the session boundary, spec 184)
