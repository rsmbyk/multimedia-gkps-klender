---
id: ITEM-190
status: done
title: 'A surface that outlives its browser session keeps painting the display'
type: fix
priority: P1
effort: S
created: 2026-11-04
updated: 2026-11-04
spec: specs/186-display-session-refresh/spec.md
branch: fix/186-display-session-refresh
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/492
issue:
archived_at:
archive_reason:
bump: patch
release_version: 1.26.4
closed_at: 2026-11-04
closed_reason: merged into develop (PR #492)
---

# ITEM-190: A surface that outlives its browser session keeps painting the display

## Summary

Spec 184 bounded the display state to the browser session: `read()` refuses a state whose `session` stamp does not
match the browser's marker. That refusal happens when a surface **reads**, and an open surface only reads again when
something writes. The marker is a session cookie, so a browser restart (or a cleared jar) drops it while `localStorage`
survives — and a dock or projector tab that outlived the restart keeps painting the display every other surface now
refuses.

Seen live while reviewing the dock's Go To (spec 185): the dock marked a service on screen, the overlay's diagnostic
read `session REFUSED` for the same stored state, and a freshly loaded dock page painted nothing.

## Notes

- Measured, `/obs/dock` on the worktree server, 2026-11-04: after the marker was cleared, `gkpsDisplay.read()` returned
  `{service: null, on: false}` while the dock still drew 1 live row and its eye still read `Hide words`; a fresh dock
  page drew 0 and read `Display this service`; the overlay refused the state.
- The overlay already re-reads on `visibilitychange` and `focus` (`obs-overlay.js:305-308`) — the shape of the fix, and
  proof that it is two surfaces missing a trigger rather than a new mechanism.
- Spec 184's own scenario says "the dock marks no service as on screen" after a restart; this is that scenario, reached
  through a tab that never reloaded.
- Stacked on `feat/185-dock-goto`: spec 185 rewrites `display.js` and the dock's paint, so this branch is cut from it
  rather than from `develop`.

## Acceptance sketch

- With a service on air, clearing the session marker and focusing the tab leaves the dock painting nothing, without a
  reload; the projector the same.
- A focus with the state unchanged repaints nothing.
- No new storage key, channel message, verb or timer.

## Links

- Spec: [186](../specs/186-display-session-refresh/spec.md)
- Related items: ITEM-188 (the session boundary, spec 184), ITEM-189 (the dock's Go To, spec 185)
