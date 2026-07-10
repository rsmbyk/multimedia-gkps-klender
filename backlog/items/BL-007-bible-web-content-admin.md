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
