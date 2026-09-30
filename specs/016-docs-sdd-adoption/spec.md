# Spec: SDD adoption notes

- **ID:** 016
- **Status:** Accepted
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none
- **Legacy:** `DOCS-SDD` migrated from `specs/docs/sdd-adoption/` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`)

## Intent

Migrated as-built from legacy `DOCS-SDD` with no behavior change. Original
problem/goal and acceptance criteria are preserved verbatim below for
traceability. New work uses Given / When / Then in this file going forward.

## Scope

### In scope

- Preserve legacy `DOCS-SDD` intent (spec/plan/tasks) under the vexbook `NNN` layout.
- Keep legacy `CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*` refs readable for traceability.

### Out of scope

- Behavior changes (none in this migration).
- Retiring legacy `CODE` cross-refs in code/tests (follow-up if wanted).

## Domain rules

- This migration is docs-only (`bump: none`).
- If future behavior changes this area, update this `NNN` spec first per `docs/PROCESS.md`.

## Acceptance scenarios

### Scenario: legacy intent preserved

- **Given** the legacy spec at `specs/docs/sdd-adoption/`
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

## Migrated as-built (verbatim from `specs/docs/sdd-adoption/spec.md`)

# Spec: DOCS-SDD — Spec-Driven Development adoption

| Field | Value |
|-------|--------|
| **Spec ID** | `DOCS-SDD` |
| **Area** | `docs` |
| **Status** | `active` |
| **Folder** | `specs/docs/sdd-adoption/` |

## Problem / goal

Product work was guided by TDD, Git Flow, and deploy docs, but there was no
shared place to capture *intent* before coding. Agents and humans could drift
from the real goal. This change adopts lightweight, docs-native SDD so specs
live in-repo and drive plan → tasks → implementation.

## User stories

- **DOCS-SDD-US1:** As a maintainer, I want a documented SDD workflow and
  `specs/` layout, so that new features start from agreed acceptance criteria.
- **DOCS-SDD-US2:** As an agent, I want a Cursor rule and constitution that
  point at those docs, so that I do not skip Specify / Plan / Tasks on in-scope
  work.

## Acceptance criteria (EARS)

- **DOCS-SDD-AC1:** THE repository SHALL document SDD in `docs/SDD.md` and link
  it from `AGENTS.md`.
- **DOCS-SDD-AC2:** THE repository SHALL provide `specs/constitution.md`,
  `specs/README.md`, and copyable templates under `specs/_templates/`.
- **DOCS-SDD-AC3:** THE repository SHALL include an always-applied Cursor rule
  `.cursor/rules/sdd.mdc` that summarizes SDD and points at `docs/SDD.md`.
- **DOCS-SDD-AC4:** WHEN product behavior changes under SDD, THE workflow SHALL
  still require TDD for implementation tasks (SDD does not replace TDD).
- **DOCS-SDD-AC5:** THE adoption SHALL NOT require installing Spec Kit,
  OpenSpec, or other SDD CLIs.
- **DOCS-SDD-AC6:** THE repository SHALL define stable Spec IDs
  (`CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*`) in `docs/SDD.md` and
  `specs/README.md`.

## Out of scope

- Installing or configuring third-party SDD toolchains
- Changing Git Flow, SemVer, deploy, or TDD mechanics beyond cross-links
- (Historical) Product feature backfill was deferred here; see `APP` and the
  feature registry for the later as-built backfill.

## Constraints

- Follow [`specs/constitution.md`](../../constitution.md) and linked docs.
- Docs / tooling only for the original adoption — no product behavior change.

## Notes

- Example folder for this adoption: `specs/docs/sdd-adoption/` (this tree).
- Product overview: [`APP`](../../app/spec.md).

