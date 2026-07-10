# BL-001 — Shared OBS SemVer footer and version constant

| Field | Value |
|-------|--------|
| **ID** | `BL-001` |
| **Status** | `ready` |
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
