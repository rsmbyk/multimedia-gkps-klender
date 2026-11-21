# Data Model: a checkout made on Windows starts the stack

**Slice**: `specs/216-windows-checkout-start` · **Phase 1** · **Written**: 2026-11-21

**None.** The slice adds one build step to the `Dockerfile`, one line to a new `.gitattributes`, and
changes the report path of the two launchers. There are no entities, no models, no migrations and no
stored state; nothing the running app reads or writes changes shape.

Deliberately not modelled (SDD-23: Fold cannot invent intent): `docs/spec/local-stack.md` gains two
behaviour requirements (`R4`, `R5`), which is Fold's bookkeeping, not a data change.
