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
