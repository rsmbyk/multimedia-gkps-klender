---
id: ITEM-006
status: backlog
title: 'Vitest for OBS display navigation and end-marker paths'
type: test
priority: P2
effort: M
created: 2026-07-10
updated: 2026-09-30
spec: 007-obs-songs-live
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 
---

# ITEM-006: Vitest for OBS display navigation and end-marker paths

## Summary

Migrated from `BL-006` with no behavior change.

## Notes

- Vexbook status: `backlog` (legacy mapped per ADR 0001).
- Type `test` / priority `P2` / effort `M` carried from legacy item.
- Spec: [007](../../specs/007-obs-songs-live/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [007](../../specs/007-obs-songs-live/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-006`

---

> Migrated from `BL-006` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-006 — Vitest for OBS display navigation and end-marker paths

| Field | Value |
|-------|--------|
| **ID** | `BL-006` |
| **Status** | `idea` |
| **Priority** | `P2` |
| **Size** | `M` |
| **Area** | `test` |
| **Owner** | |

## Problem / why

OBS live specs note thin or missing Vitest for display.js navigation / END
logic (songs), activate rules on tatib `item_type` / end markers, and related
paths that are easy to regress during dock refactors.

## Outcome

Isolatable tests for the highest-risk display navigation and end-marker
behaviors called out in `OBS-SONGS` / `OBS-TATIB` notes.

## Acceptance sketch

- Prioritize songs last-lyric / last-verse / refuse-activate-on-END and tatib
  EOS activate refusal / empty post behavior.
- Prefer unit-style tests over brittle full Semantic UI snapshots (`TEST-COV`).

## Links

| Kind | Ref |
|------|-----|
| Spec | `OBS-SONGS`, `OBS-TATIB`, `TEST-COV` |
| Related | `BL-005` |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from OBS as-built Vitest gap notes |
