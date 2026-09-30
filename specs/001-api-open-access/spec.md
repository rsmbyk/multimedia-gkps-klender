# Spec: Open product API and web access

- **ID:** 001
- **Status:** Accepted
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none
- **Legacy:** `API-ACCESS` migrated from `specs/api/open-access-policy/` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`)

## Intent

Migrated as-built from legacy `API-ACCESS` with no behavior change. Original
problem/goal and acceptance criteria are preserved verbatim below for
traceability. New work uses Given / When / Then in this file going forward.

## Scope

### In scope

- Preserve legacy `API-ACCESS` intent (spec/plan/tasks) under the vexbook `NNN` layout.
- Keep legacy `CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*` refs readable for traceability.

### Out of scope

- Behavior changes (none in this migration).
- Retiring legacy `CODE` cross-refs in code/tests (follow-up if wanted).

## Domain rules

- This migration is docs-only (`bump: none`).
- If future behavior changes this area, update this `NNN` spec first per `docs/PROCESS.md`.

## Acceptance scenarios

### Scenario: legacy intent preserved

- **Given** the legacy spec at `specs/api/open-access-policy/`
- **When** comparing with this `NNN` pack
- **Then** problem/goal, user stories, and acceptance criteria are preserved verbatim below

### Scenario: suite stays green

- **Given** docs-only migration
- **When** running `pytest` and `npm test`
- **Then** existing suites pass with no behavior change

## Traceability

- Domain/app tests: existing `pytest` suite (`multimedia.settings_test`) and Vitest suite — no new tests for migration.
- E2E: N/A (docs-only migration).
- Implementation: this migration (adopt PR).

---

## Migrated as-built (verbatim from `specs/api/open-access-policy/spec.md`)

# Spec: API-ACCESS — Open product access policy

| Field | Value |
|-------|--------|
| **Spec ID** | `API-ACCESS` |
| **Area** | `api` |
| **Status** | `as-built` |
| **Folder** | `specs/api/open-access-policy/` |

## Problem / goal

Worship operators and OBS browser sources need frictionless access to content
APIs and content-admin pages on a trusted network / deployment. The product
intentionally leaves the REST API and public web templates unauthenticated.
Staff Django admin remains the only login-gated surface.

## User stories

- **API-ACCESS-US1:** As an OBS dock, I want to call `/api/` without credentials,
  so that browser sources work without login flows.
- **API-ACCESS-US2:** As a content editor, I want to use the web songs/tatib
  admin without signing in, so that preparation stays fast during service setup.
- **API-ACCESS-US3:** As a maintainer, I want staff-only `/admin/` for sensitive
  model editing, so that Django admin is not anonymously writable.

## Acceptance criteria (EARS)

- **API-ACCESS-AC1:** THE product REST API SHALL NOT require authentication for
  documented CRUD and search endpoints under `/api/`.
- **API-ACCESS-AC2:** WHEN an unauthenticated client lists or mutates documented
  API resources, THE system SHALL allow the request (subject to validation),
  returning normal success status codes (e.g. 200/201/204).
- **API-ACCESS-AC3:** THE web content-admin pages under `/`, `/songs/…`, and
  `/tatib/…` SHALL be reachable without login.
- **API-ACCESS-AC4:** THE Django admin at `/admin/` SHALL require staff
  authentication.
- **API-ACCESS-AC5:** API routers SHALL accept optional trailing slashes
  (`/?`) for registered endpoints.
- **API-ACCESS-AC6:** WHEN product behavior changes, related feature specs SHALL
  reference this policy rather than inventing a conflicting auth model.

## Out of scope

- Designing or implementing end-user auth / OAuth / API keys.
- CSRF hardening redesign for anonymous browser writes.
- Network-level access control (VPN, IP allowlists) — ops concern outside app.

## Constraints

- Follow [`specs/constitution.md`](../../constitution.md).
- DRF settings today set filter backends only; no
  `DEFAULT_PERMISSION_CLASSES` lock-down (`multimedia/settings.py`).
- Related: `APP`, `TEST-COV` (auth assertions), all `API-*` / `WEB-*` / `OBS-*`.

## Notes

- Asserted by pytest: `test_unauthenticated_can_*` in songs/bible/tatib/bookmarks
  API tests; trailing slash on songs books.
- Intentional long-term policy unless a future spec supersedes this one.

