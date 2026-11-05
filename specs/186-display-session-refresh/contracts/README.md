# Contracts: a surface re-reads the session it is showing

**Spec**: `specs/186-display-session-refresh/spec.md`

## Interfaces exposed by this slice

`none` — no endpoint, no storage key and no channel message is added (FR-004). The only new name is
internal to the state module: `window.gkpsDisplay.reread()`, the module's own act, which the module
also binds to `focus`, `visibilitychange` and `pageshow`. A subscriber that renders on notification
needs nothing else.

## Not exposed

The triggers, the compare and the notify all stay inside `static/web/display.js`. The projector's
`rereadSession()` is private to `projector.js`. The channel's message types and the stored shape are
exactly what spec 185 left them.
