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
