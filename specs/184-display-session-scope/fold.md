# Fold: the active Tata Ibadah lasts only the browser session

**Spec**: `specs/184-display-session-scope/spec.md`
**Date**: 2026-11-03
**Folded by**: the slice, at Converged.

## Capabilities touched

| Capability | Operation | Before | After |
| --- | --- | --- | --- |
| `display-state` | `added` — the capability file is created | 0 requirements, no file | 1 requirement (`R1`), `docs/spec/display-state.md` |

## The delta

- **added `display-state/R1`** — the display state carries the session that wrote it and is read only
  while that session is live; a state from an earlier session is no state, on every surface, from its
  first paint. The marker is a cookie with no expiry carrying no display data. Inside one session
  catch-up and live updates are unchanged, and closing every surface does not end the display
  (spec 119, kept). Four scenarios: a browser starts again · a state with no stamp · every surface
  closes inside one session · the browser cannot hold a cookie.

## Files

- `docs/spec/display-state.md` — created; header `last folded` 2026-11-03, `slices`
  `184-display-session-scope`.

## Not folded — accepted gaps

- None. The one manual verification (an OBS restart) is a method, not a behaviour: the behaviour it
  checks is folded as R1's first scenario.

## Untouched capabilities

`overlay` (R1 paints from the display state), `projector` (R2 renders its own response) and `reading`
(R16 the reopen control) keep their text: this slice changes the state's lifetime, not what any of
them paints or how it is driven.
