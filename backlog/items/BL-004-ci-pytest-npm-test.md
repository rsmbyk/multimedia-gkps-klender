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
