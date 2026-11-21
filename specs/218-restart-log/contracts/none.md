# Contracts: a dead companion says why

**Slice**: `specs/218-restart-log` · **Phase 1** · **Written**: 2026-11-21

**None.** No HTTP route, no API payload, no launcher argument: both launchers keep their command
contract, their default command and their exit status. The only addition is text on stderr.

Recorded as an explicit `none` rather than silently absent (SDD-12).
