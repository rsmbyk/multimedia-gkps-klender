# Contracts: earlier top pin for the live header

**Spec**: `specs/248-dock-top-pin-early/spec.md`

none — the slice changes no HTTP endpoint, message shape, storage schema or public JS API. The top
pin's slot and the covered-row class are internal DOM state in `static/web/obs-dock.js` and
`static/styles/design/obs-dock.css`; the dock's click contract on the pinned copy stays the centre
act (R15), already owned by `docs/spec/dock.md`.
