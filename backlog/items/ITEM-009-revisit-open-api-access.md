---
id: ITEM-009
status: backlog
title: 'Harden or revisit open product API access'
type: idea
priority: P2
effort: L
created: 2026-07-10
updated: 2026-09-30
spec: 001-api-open-access
branch:
pr:
archived_at:
archive_reason:
bump: none
release_version: 
---

# ITEM-009: Harden or revisit open product API access

## Summary

Migrated from `BL-009` with no behavior change.

## Notes

- Vexbook status: `backlog` (legacy mapped per ADR 0001).
- Type `idea` / priority `P2` / effort `L` carried from legacy item.
- Spec: [001](../../specs/001-api-open-access/spec.md).

## Acceptance sketch

See legacy acceptance sketch preserved below.

## Links

- Spec: [001](../../specs/001-api-open-access/spec.md)
- Related items: ITEM-000 (adopt)
- Legacy: `BL-009`

---

> Migrated from `BL-009` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`).
>
> Legacy `BL-*` status/priority/size preserved below for traceability.

# BL-009 — Harden or revisit open product API access

| Field | Value |
|-------|--------|
| **ID** | `BL-009` |
| **Status** | `idea` |
| **Priority** | `P2` |
| **Size** | `L` |
| **Area** | `api` |
| **Owner** | |

## Problem / why

`API-ACCESS` documents intentional unauthenticated CRUD for product API and
content-admin UIs. That is fine on a trusted network but risky if the
deployment is publicly writable. Ops notes call this out as accepted as-built.

## Outcome

Either keep open access with documented network controls, or introduce an
agreed auth/permission model and update `API-ACCESS` + dependent specs.

## Acceptance sketch

- Product decision first; do not silently lock down APIs.
- IF auth is added, THEN update `API-ACCESS`, `TEST-COV`, web/OBS clients, and
  deploy docs.

## Links

| Kind | Ref |
|------|-----|
| Spec | `API-ACCESS` |
| Notes | Long-term policy unless a future spec supersedes |

## History

| Date | Note |
|------|------|
| 2026-07-10 | Seeded from `API-ACCESS` risks |
