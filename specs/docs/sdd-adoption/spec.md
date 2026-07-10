# Spec: Spec-Driven Development adoption

## Problem / goal

Product work was guided by TDD, Git Flow, and deploy docs, but there was no
shared place to capture *intent* before coding. Agents and humans could drift
from the real goal. This change adopts lightweight, docs-native SDD so specs
live in-repo and drive plan → tasks → implementation.

## User stories

- As a maintainer, I want a documented SDD workflow and `specs/` layout, so that
  new features start from agreed acceptance criteria.
- As an agent, I want a Cursor rule and constitution that point at those docs, so
  that I do not skip Specify / Plan / Tasks on in-scope work.

## Acceptance criteria (EARS)

- THE repository SHALL document SDD in `docs/SDD.md` and link it from
  `AGENTS.md`.
- THE repository SHALL provide `specs/constitution.md`, `specs/README.md`, and
  copyable templates under `specs/_templates/`.
- THE repository SHALL include an always-applied Cursor rule
  `.cursor/rules/sdd.mdc` that summarizes SDD and points at `docs/SDD.md`.
- WHEN product behavior changes under SDD, THE workflow SHALL still require TDD
  for implementation tasks (SDD does not replace TDD).
- THE adoption SHALL NOT require installing Spec Kit, OpenSpec, or other SDD
  CLIs.

## Out of scope

- Backfilling specs for existing product features
- Installing or configuring third-party SDD toolchains
- Changing Git Flow, SemVer, deploy, or TDD mechanics beyond cross-links

## Constraints

- Follow [`specs/constitution.md`](../../constitution.md) once added; until then
  follow existing `docs/TDD.md`, `docs/GIT_FLOW.md`, and `docs/DEPLOY.md`.
- Docs / tooling only — no product behavior change; no new tests required.

## Notes

- Example folder for this adoption: `specs/docs/sdd-adoption/` (this tree).
