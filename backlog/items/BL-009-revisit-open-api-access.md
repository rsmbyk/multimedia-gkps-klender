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
