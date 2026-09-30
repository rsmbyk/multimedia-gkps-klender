---
id: ITEM-005
status: ready
title: 'Vitest for project hotkeys 1/2/3 and mutual mute'
type: test
priority: P2
effort: S
created: 2026-07-10
updated: 2026-09-30
spec: 010-obs-project-projection
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 
---

# ITEM-005: Vitest for project hotkeys 1/2/3 and mutual mute

## Summary

Migrated from `BL-005` with no behavior change.

## Notes

- Vexbook status: `ready` (legacy mapped per ADR 0001).
- Type `test` / priority `P2` / effort `S` carried from legacy item.
- Spec: [010](../../specs/010-obs-project-projection/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [010](../../specs/010-obs-project-projection/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-005`

---

> Migrated from `BL-005` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-005 — Vitest for project hotkeys 1/2/3 and mutual mute

| Field | Value |
|-------|--------|
| **ID** | `BL-005` |
| **Status** | `ready` |
| **Priority** | `P2` |
| **Size** | `S` |
| **Area** | `test` |
| **Owner** | |

## Problem / why

`OBS-PROJECT` notes that controls `1`/`2`/`3` and mutual-mute status behavior
lack Vitest coverage today, while format and colour storage are covered.

## Outcome

Isolatable Vitest coverage for last-active control posting, keys 1/2/3
rebroadcast, and forcing other apps inactive when one becomes active.

## Acceptance sketch

- Cover `OBS-PROJECT-AC4`, `AC7`–`AC9` as far as isolatable without full OBS.
- Follow TDD; keep mocks consistent with existing project tests.

## Links

| Kind | Ref |
|------|-----|
| Spec | `OBS-PROJECT`, `TEST-COV-AC20` |
| Notes | Called out in `OBS-PROJECT` Notes |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from `OBS-PROJECT` Vitest gaps |
