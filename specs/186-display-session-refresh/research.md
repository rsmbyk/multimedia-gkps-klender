# Research: a surface re-reads the session it is showing

**Spec**: `specs/186-display-session-refresh/spec.md`
**Unknowns remaining**: 0

## D001 — The module owns the compare and the notify

- **Decision**: `display.js` exports `reread()`: it calls the existing `read()`, compares the result
  with the state it holds, and only on a difference replaces it, re-syncs the page's own controls
  (`syncButton`) and notifies the subscribers. The triggers (`focus`, `visibilitychange` when
  visible, `pageshow` when restored) are bound once, inside the module.
- **Rationale**: the dock renders from `subscribe(sync)`, so a notify is already how it repaints
  (`obs-dock.js:1287`). Putting the trigger in each surface would let a reader that renders on
  notification — and a future one — drift out of the rule, and would repaint surfaces that have
  nothing to change.
- **Alternatives considered**: a `setInterval` poll (repaints forever for a condition that changes
  once per browser session); a listener in each surface (three copies, and the dock's own copy would
  have to duplicate the compare).
- **Provenance**: research.

## D002 — The projector gets its own re-read, because it does not load `display.js`

- **Decision**: `projector.js` binds the same three triggers to `rereadSession()`, which reads the
  same key through its own `read()` and repaints silently (`render(true)`).
- **Rationale**: the projector page loads `display-session.js` and `projector.js` only — it has
  carried its own read/write pair since spec 119 (`projector.js:466-490`). Loading `display.js` there
  would give the page a second writer and its project-button hooks for nothing.
- **Alternatives considered**: adding `display.js` to the projector page (a second writer on the same
  key, for one function); leaving the projector out (US1/AC4 and SC-002 would be false).
- **Provenance**: research.

## D003 — The compare is the whole object, by value

- **Decision**: compare `JSON.stringify(read())` with `JSON.stringify(state)`. The object is seven
  scalars and an optional pointer; a field-by-field comparison would be the same work, spelled out.
- **Rationale**: the shape is flat and small (spec 185's `read()`), and `read()` returns a fresh
  object, so a value comparison is exact. A key-order change is impossible: both sides come from the
  same literal in the same module.
- **Alternatives considered**: comparing `at` only (a write that ends a go to but keeps `at` equal is
  impossible — every write renews it — but a *restored* state could share it; and `at` alone would
  miss `on`).
- **Provenance**: research.

## D004 — `pageshow` is listened to only when the page was restored

- **Decision**: the `pageshow` handler acts when `event.persisted` is true.
- **Rationale**: a normal load already reads at boot; a back/forward-cache restore does not re-run the
  boot path, and is exactly the case where the cookie may have gone while the page sat in the cache.
- **Alternatives considered**: acting on every `pageshow` (a duplicate read on every load, harmless
  but pointless).
- **Provenance**: research.

## Open

<!-- empty: Phase 0 is finished -->
