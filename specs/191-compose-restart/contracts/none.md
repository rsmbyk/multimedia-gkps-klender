# Contracts: Stack Restart Policy

**Slice**: `specs/191-compose-restart` · **Phase 1** · **Written**: 2026-11-14

**None.** The slice changes no external interface: no HTTP route, no CLI contract, no API payload,
no launcher sub-command. The `docker compose` command surface keeps its exact shape — the only
change is that containers the daemon restarts now come back on their own.

Recorded as an explicit `none` rather than silently absent (SDD-12).
