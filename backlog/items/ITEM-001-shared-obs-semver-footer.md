---
id: ITEM-001
status: done
title: 'Shared OBS SemVer footer and version constant'
type: feat
priority: P0
effort: M
created: 2026-07-10
updated: 2026-09-30
spec: 007-obs-songs-live
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 0.5.0
---

# ITEM-001: Shared OBS SemVer footer and version constant

## Summary

Migrated from `BL-001` with no behavior change.

## Notes

- Vexbook status: `done` (legacy mapped per ADR 0001).
- Type `feat` / priority `P0` / effort `M` carried from legacy item.
- Spec: [007](../../specs/007-obs-songs-live/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [007](../../specs/007-obs-songs-live/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-001`

---

> Migrated from `BL-001` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-001 — Shared OBS SemVer footer and version constant

| Field | Value |
|-------|--------|
| **ID** | `BL-001` |
| **Status** | `done` |
| **Priority** | `P0` |
| **Size** | `M` |
| **Area** | `project` |
| **Owner** | |

## Problem / why

[`docs/VERSIONING.md`](../../docs/VERSIONING.md) plans one shared OBS footer and
one JS-readable SemVer constant. Templates may still show divergent per-app
version strings from the `0.4.x` scheme. Needed before / as part of the first
`0.5.0` release.

## Outcome

All OBS pages show a single app version from one constant; old per-app hardcoded
strings are removed.

## Acceptance sketch

- One JS-readable constant is the source of truth for the product SemVer.
- Shared footer on OBS pages reads that constant.
- No divergent per-app version strings remain in OBS templates.

## Links

| Kind | Ref |
|------|-----|
| Spec | Update `OBS-*` / `APP` as needed when implementing |
| Notes | [`docs/VERSIONING.md`](../../docs/VERSIONING.md) “UI display (planned)” |
| Related | `BL-002` (cut `0.5.0`) |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from versioning docs |
| 2026-07-10 | Implemented on `release/0.5.0` (`version.js` + `data-app-version`) |
