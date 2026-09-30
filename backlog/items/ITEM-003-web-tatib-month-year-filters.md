---
id: ITEM-003
status: ready
title: 'Wire web tatib calendar to month/year API filters'
type: feat
priority: P1
effort: S
created: 2026-07-10
updated: 2026-09-30
spec: 012-web-tatib-admin
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 
---

# ITEM-003: Wire web tatib calendar to month/year API filters

## Summary

Migrated from `BL-003` with no behavior change.

## Notes

- Vexbook status: `ready` (legacy mapped per ADR 0001).
- Type `feat` / priority `P1` / effort `S` carried from legacy item.
- Spec: [012](../../specs/012-web-tatib-admin/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [012](../../specs/012-web-tatib-admin/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-003`

---

> Migrated from `BL-003` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-003 — Wire web tatib calendar to month/year API filters

| Field | Value |
|-------|--------|
| **ID** | `BL-003` |
| **Status** | `ready` |
| **Priority** | `P1` |
| **Size** | `S` |
| **Area** | `web` |
| **Owner** | |

## Problem / why

`WEB-TATIB` documents an as-built quirk: the month calendar UI requests
`is_active=true&has_date=true` but does **not** send `month`/`year`, even though
`API-TATIB` supports those filters. Operators may think they are filtering by
month when they are not.

## Outcome

Calendar selection drives `month`/`year` (and documented behavior matches the
UI), or the UI is clarified if product chooses not to filter by month.

## Acceptance sketch

- WHEN a month is selected, THE list request SHALL include the corresponding
  `month`/`year` **or** the UI SHALL not imply month filtering (product choice).
- Update `WEB-TATIB` spec if behavior changes.
- TDD: Vitest and/or pytest as appropriate.

## Links

| Kind | Ref |
|------|-----|
| Spec | `WEB-TATIB-AC3`, `API-TATIB-AC3` |
| Notes | Honest quirk called out in web tatib plan/spec |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from `WEB-TATIB` as-built notes |
