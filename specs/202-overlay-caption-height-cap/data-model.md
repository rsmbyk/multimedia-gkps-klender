# Data model: Height-bound song caption type

**Spec**: `specs/202-overlay-caption-height-cap/spec.md`

**No entities.** The slice changes one CSS declaration and the floor computation in a browser
script. No model, migration, fixture, template, storage key or endpoint is touched. The display
state the overlay reads is unchanged; the existing `TataIbadah`, `ServiceEntry`, `Song` and `Verse`
rows the E2E fixtures create are test scaffolding only.

The only shape involved is the type scale:

| Value | Before | After |
| --- | --- | --- |
| Rest (1920×1080) | `clamp(11px, 3.75cqw, 80px)` = 72px | `5cqh` = 54px |
| Floor (1920×1080) | fixed 11px | `stage.clientHeight * 0.02` = 21.6px |
| Shrink step | 6 % of current (`fontSize * 0.94`) | 4 % of rest (`fontSize - rest * 0.04`), 15 steps to the floor |
