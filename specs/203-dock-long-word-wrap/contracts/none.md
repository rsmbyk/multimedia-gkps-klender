# Contracts: A long word wraps in the dock runner

**Spec**: `specs/203-dock-long-word-wrap/spec.md`

`none` — the dock page is server-rendered HTML whose only external surfaces (`/obs/dock`, the static
stylesheet it links, the projector library it fetches) keep their existing contract. This slice changes a
stylesheet's text breaking: no endpoint, no event, no storage key, no message between surfaces is added,
changed or removed. The display state, the go to and the transport keys are untouched.
