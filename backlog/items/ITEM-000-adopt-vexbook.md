---
id: ITEM-000
status: in-review
title: 'Adopt vexbook process at v0.4.0 with full migration'
type: chore
priority: P0
effort: M
created: 2026-09-30
updated: 2026-09-30
spec: 000-multimedia-baseline
branch: chore/adopt-vexbook-v0.4.0
pr: "#252"
archived_at:
archive_reason:
bump: none
release_version:
---

# ITEM-000: Adopt vexbook process at v0.4.0 with full migration

## Summary

Adopt vexbook process at `v0.4.0` into this repo with full migration:
process file set, `VERSION`, adoption ADR, specs `CODE` → `NNN` (`000`–`017`),
backlog `BL-*` → `ITEM-*` (`001`–`010`), vendor rules refresh. Docs/process
only; no behavior change.

## Notes

- Source: vexbook tag `v0.4.0` (local `~/Projects/vexbook`).
- Git model stays Git Flow; SemVer stays locked; `version.js` mirrors `VERSION`.
- Legacy `CODE`/`BL-*` refs preserved in migrated bodies for traceability.
- Follow-up may retire `docs/BACKLOG.md` / `docs/SDD.md` where they conflict
  with `docs/PROCESS.md` (PROCESS wins).

## Acceptance sketch

- Process file set present from `v0.4.0` (PROCESS/KICKOFF/ADOPT/SDD-GATE,
  `_template`s, PR template, ADR template).
- `VERSION` = `0.5.1`; ADR `0001` records decision + mappings.
- `specs/000`–`017` preserve legacy intent verbatim; `specs/README.md` indexes NNN.
- `backlog/board.md` + `ITEM-000`–`010` replace `BL-*` board; Backlog column sorted P0–P3.
- `.cursor/rules/` reference every must-apply doc from PROCESS.
- `pytest` and `npm test` stay green (docs-only).

## Links

- Spec: [000](../../specs/000-multimedia-baseline/spec.md) (baseline; this ITEM covers the whole migration pack)
- Related items: ITEM-001–ITEM-010 (migrated)
- ADR: [0001](../../docs/adr/0001-adopt-vexbook-process.md)
