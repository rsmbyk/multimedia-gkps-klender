# Data Model: the runtime entrypoint survives the bind mount

**Slice**: `specs/217-entrypoint-shadowed` · **Phase 1** · **Written**: 2026-11-21

**None.** The slice moves one file inside the image and changes one `Dockerfile` line. No entities, no
models, no migrations, no stored state.

Deliberately not modelled: `docs/spec/local-stack.md`'s `R4` is rewritten by Fold — bookkeeping
against a requirement that already exists, not a data change (SDD-23).
