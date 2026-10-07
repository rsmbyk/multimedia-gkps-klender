---
id: ITEM-004
status: ready
title: 'CI for pytest and npm test'
type: chore
priority: P1
effort: M
created: 2026-07-10
updated: 2026-09-30
spec: 017-test-coverage
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 
---

# ITEM-004: CI for pytest and npm test

## Summary

Migrated from `BL-004` with no behavior change.

## Notes

- Vexbook status: `ready` (legacy mapped per ADR 0001).
- Type `chore` / priority `P1` / effort `M` carried from legacy item.
- Spec: [017](../../specs/017-test-coverage/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [017](../../specs/017-test-coverage/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-004`

---

> Migrated from `BL-004` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-004 — CI for pytest and npm test

| Field | Value |
|-------|--------|
| **ID** | `BL-004` |
| **Status** | `ready` |
| **Priority** | `P1` |
| **Size** | `M` |
| **Area** | `test` |
| **Owner** | |

## Problem / why

`TEST-COV` explicitly left CI / GitHub Actions out of scope. Suites exist
locally (pytest on Compose Postgres, Vitest) but PRs have no automated gate.

## Outcome

A GitHub Actions (or equivalent) workflow runs `pytest` and `npm test` on PRs
into `develop` (and/or `main`), with Postgres available for FTS search tests.

## Acceptance sketch

- PR checks run Python and JS suites.
- Song search FTS tests can pass (Postgres service in CI).
- Document how CI relates to local `docs/TDD.md` workflow.
- Update `TEST-COV` / add a small `test` or `docs` spec note if needed.

## Links

| Kind | Ref |
|------|-----|
| Spec | `TEST-COV` (out-of-scope CI → bring in scope) |
| Notes | Prefer existing pytest/Vitest stack; ask before large CI frameworks |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from `TEST-COV` out of scope |
