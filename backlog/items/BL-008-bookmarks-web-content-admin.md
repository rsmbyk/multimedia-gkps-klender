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
