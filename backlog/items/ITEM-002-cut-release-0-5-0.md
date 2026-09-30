---
id: ITEM-002
status: done
title: 'Cut first SemVer release 0.5.0'
type: chore
priority: P0
effort: M
created: 2026-07-10
updated: 2026-09-30
spec: 000-multimedia-baseline
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 0.5.0
---

# ITEM-002: Cut first SemVer release 0.5.0

## Summary

Migrated from `BL-002` with no behavior change.

## Notes

- Vexbook status: `done` (legacy mapped per ADR 0001).
- Type `chore` / priority `P0` / effort `M` carried from legacy item.
- Spec: [000](../../specs/000-multimedia-baseline/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [000](../../specs/000-multimedia-baseline/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-002`

---

> Migrated from `BL-002` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

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
