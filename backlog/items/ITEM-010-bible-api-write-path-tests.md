---
id: ITEM-010
status: backlog
title: 'Expand bible API write-path test coverage'
type: test
priority: P2
effort: S
created: 2026-07-10
updated: 2026-09-30
spec: 003-api-bible-content
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 
---

# ITEM-010: Expand bible API write-path test coverage

## Summary

Migrated from `BL-010` with no behavior change.

## Notes

- Vexbook status: `backlog` (legacy mapped per ADR 0001).
- Type `test` / priority `P2` / effort `S` carried from legacy item.
- Spec: [003](../../specs/003-api-bible-content/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [003](../../specs/003-api-bible-content/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-010`

---

> Migrated from `BL-010` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-010 — Expand bible API write-path test coverage

| Field | Value |
|-------|--------|
| **ID** | `BL-010` |
| **Status** | `idea` |
| **Priority** | `P2` |
| **Size** | `S` |
| **Area** | `test` |
| **Owner** | |

## Problem / why

`API-BIBLE` plan notes write paths for versions/translations/verses are lightly
tested compared to read/filter paths used by OBS.

## Outcome

Pytest coverage for representative create/update/delete (and uniqueness) on
versions, translations, and verses, without changing product behavior.

## Acceptance sketch

- Extend `multimedia/bible/tests/test_api.py` (or equivalent).
- Align with `API-BIBLE` / `TEST-COV-AC12`.

## Links

| Kind | Ref |
|------|-----|
| Spec | `API-BIBLE`, `TEST-COV` |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from `API-BIBLE` plan risks |
