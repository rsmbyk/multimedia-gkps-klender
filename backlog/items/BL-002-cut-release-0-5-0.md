# BL-002 — Cut first SemVer release 0.5.0

| Field | Value |
|-------|--------|
| **ID** | `BL-002` |
| **Status** | `done` |
| **Priority** | `P0` |
| **Size** | `M` |
| **Area** | `docs` |
| **Owner** | |

## Problem / why

Production is still on the legacy `0.4.x` scheme. The first release under the
new single-SemVer docs is planned as `0.5.0` (finalize Unreleased, tag on
`main`, shared version UI).

## Outcome

`release/0.5.0` (or equivalent) lands on `main` tagged `v0.5.0`, changelog
section finalized, version constant/footer match.

## Acceptance sketch

- Follow [`docs/VERSIONING.md`](../../docs/VERSIONING.md) and
  [`docs/GIT_FLOW.md`](../../docs/GIT_FLOW.md) release checklist.
- Prefer `BL-001` done (or bundled) so the footer is not still per-app.

## Links

| Kind | Ref |
|------|-----|
| Spec | `DEPLOY-VERCEL`, `APP` |
| Related | `BL-001` |
| Notes | Changelog `## Unreleased` on `develop` |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from versioning / Git Flow docs |
| 2026-07-10 | Cutting `release/0.5.0` (bundled with `BL-001`) |
