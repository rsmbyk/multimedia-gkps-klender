---
id: ITEM-008
status: backlog
title: 'Bookmarks web content-admin UI'
type: feat
priority: P3
effort: L
created: 2026-07-10
updated: 2026-09-30
spec: 006-songs-bookmarks
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 
---

# ITEM-008: Bookmarks web content-admin UI

## Summary

Migrated from `BL-008` with no behavior change.

## Notes

- Vexbook status: `backlog` (legacy mapped per ADR 0001).
- Type `feat` / priority `P3` / effort `L` carried from legacy item.
- Spec: [006](../../specs/006-songs-bookmarks/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [006](../../specs/006-songs-bookmarks/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-008`

---

> Migrated from `BL-008` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-008 — Bookmarks web content-admin UI

| Field | Value |
|-------|--------|
| **ID** | `BL-008` |
| **Status** | `idea` |
| **Priority** | `P3` |
| **Size** | `L` |
| **Area** | `web` |
| **Owner** | |

## Problem / why

Song bookmarks are managed from OBS + API + Django admin. There is no public
web content-admin for setlists (`SONGS-BM` / `APP` out of scope).

## Outcome

A web UI for bookmark CRUD/reorder (or an explicit keep-OBS-only decision).

## Acceptance sketch

- If built: reuse songs/tatib web patterns; Spec ID e.g. `WEB-BOOKMARKS`; link
  `SONGS-BM` API contracts.
- Do not invent auth unless `API-ACCESS` is superseded.

## Links

| Kind | Ref |
|------|-----|
| Spec | `SONGS-BM`, `APP`, `WEB-ADMIN` |
| Related | `BL-007` |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from SONGS-BM / APP out-of-scope notes |
