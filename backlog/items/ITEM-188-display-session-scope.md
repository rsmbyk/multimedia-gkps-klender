---
id: ITEM-188
status: in_review
title: 'The active Tata Ibadah survives a browser restart'
type: fix
priority: P1
effort: M
created: 2026-11-03
updated: 2026-11-03
spec: specs/184-display-session-scope/spec.md
branch: fix/184-display-session-scope
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/488
issue: 489
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-188: The active Tata Ibadah survives a browser restart

## Summary

The display state — which Tata Ibadah is on air and at which screen — is kept in
`localStorage['gkps-display']` with no session boundary. Closing the browser or OBS and opening it
again therefore repaints the previous service: the OBS caption overlay comes back with the last
liturgy or lyric on screen, the projector back on that screen, and the dock's picker still wearing
the "On screen" pill before the operator has chosen anything.

Spec 119 made this deliberate — "State survives every surface closing — the display ends only by
`release`" — but it also means the state survives the browser itself. The operator should find
every surface idle at the start of a browser session and light it up only when they choose to.

## Notes

- On air today is one object in `localStorage`: `{service, screen, on, translation, at}`, written by
  the dock (`static/web/display.js`) and the projector (`static/web/projector.js`), read by the
  overlay (`static/web/obs-overlay.js`) and by every reading page.
- The containment must not reach the server: the public site is no-login and the state is the
  operator's own.
- Within one browser session nothing changes: any surface opened or reloaded still catches up to
  what is on air.
- Spec 119's "closing every surface changes nothing" is the contract this slice revises; the exact
  boundary is a Clarify question.

## Acceptance sketch

- Open a service, put it on air, then close every surface and reopen the browser on the same
  profile: the overlay paints nothing, the projector is blank, the dock's control reads "Display
  this service", and no picker row wears "On screen".
- In a live session, opening a second surface still catches up, and hiding/releasing still reaches
  every surface.
- Whatever marks the session carries no service or screen, and no display state is sent to the
  server.

## Links

- Spec: [184](../specs/184-display-session-scope/spec.md)
- Related items: ITEM-119 (the display state, spec 119), ITEM-150 (reopening the projector window,
  spec 141)
