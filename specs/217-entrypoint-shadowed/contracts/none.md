# Contracts: the runtime entrypoint survives the bind mount

**Slice**: `specs/217-entrypoint-shadowed` · **Phase 1** · **Written**: 2026-11-21

**None.** No HTTP route, no API payload, no launcher argument, no compose key: the container's command
surface (`CMD`), the two launchers and `docker-compose.yml` are all untouched. The only path that
changes is inside the image.

Recorded as an explicit `none` rather than silently absent (SDD-12).