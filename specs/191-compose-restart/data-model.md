# Data Model: Stack Restart Policy

**Slice**: `specs/191-compose-restart` · **Phase 1** · **Written**: 2026-11-14

**None.** The slice adds two `restart:` keys to `docker-compose.yml`. There are no entities, no
models, no migrations, no stored state, and no files on disk beyond the compose file itself.

Deliberately not invented (SDD-23: Fold cannot invent intent): no capability data changes —
`docs/spec/local-stack.md` gains a behaviour requirement (R3), which is Fold's bookkeeping, not a
data change.
