# Contracts: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`

none — the slice adds no HTTP endpoint, message, persisted state or external interface. It consumes
the projector's existing screen data (`text`, `voice`, `mark`, `words`) and changes only how the
browser paints one row; the projector payload, the `editor:saved` event and the overlay's
localStorage state keep their present shapes.
