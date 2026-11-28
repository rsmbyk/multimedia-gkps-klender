# Contracts: refit the Go To detour on a stage resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md`

none — the slice adds one call inside the projector's existing `resize` listener. It exposes no
HTTP endpoint, message, storage key or DOM attribute to another component; the browser's `resize`
event and the inline `font-size` are interfaces this file already owns.

## Not exposed

The fit key stays an internal cache, the projection channel messages are unchanged, and the
Go To fetch endpoints keep their existing contracts.
