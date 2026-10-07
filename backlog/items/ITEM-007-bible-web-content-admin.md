---
id: ITEM-007
status: backlog
title: 'Bible web content-admin UI'
type: feat
priority: P3
effort: L
created: 2026-07-10
updated: 2026-09-30
spec: 008-obs-bible-live
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 
---

# ITEM-007: Bible web content-admin UI

## Summary

Migrated from `BL-007` with no behavior change.

## Notes

- Vexbook status: `backlog` (legacy mapped per ADR 0001).
- Type `feat` / priority `P3` / effort `L` carried from legacy item.
- Spec: [008](../../specs/008-obs-bible-live/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [008](../../specs/008-obs-bible-live/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-007`

---

> Migrated from `BL-007` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-007 — Bible web content-admin UI

| Field | Value |
|-------|--------|
| **ID** | `BL-007` |
| **Status** | `idea` |
| **Priority** | `P3` |
| **Size** | `L` |
| **Area** | `web` |
| **Owner** | |

## Problem / why

Bible content is editable via API and Django staff admin only. `APP` /
`API-BIBLE` / `OBS-BIBLE` note there is no public browser content-admin like
songs/tatib.

## Outcome

A web UI (or an explicit decision to keep admin-only) for maintaining bible
structure/content without relying solely on `/admin/`.

## Acceptance sketch

- If built: follow `WEB-SONGS` / `WEB-TATIB` patterns; new Spec ID (e.g.
  `WEB-BIBLE`); register in `APP` / `specs/README.md`.
- Open-access policy (`API-ACCESS`) applies unless a future auth spec lands.

## Links

| Kind | Ref |
|------|-----|
| Spec | `APP` out of scope today; `API-BIBLE`, `WEB-ADMIN` |
| Related | `BL-008` |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from APP / bible out-of-scope notes |
