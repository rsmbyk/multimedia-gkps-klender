# Tasks: Spec-Driven Development adoption

Spec: [`spec.md`](spec.md) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **T1 — Write `docs/SDD.md`**
  - Touch: `docs/SDD.md`
  - Verify: phases, when-to-use, layout, EARS, TDD relationship documented

- [x] **T2 — Add Cursor rule and AGENTS pointer**
  - Touch: `.cursor/rules/sdd.mdc`, `AGENTS.md`
  - Verify: rule is alwaysApply; AGENTS has Specs (SDD) section

- [x] **T3 — Scaffold `specs/` + templates + constitution**
  - Touch: `specs/README.md`, `specs/constitution.md`, `specs/_templates/*`
  - Verify: templates are copyable; constitution links existing docs

- [x] **T4 — Record this adoption as an example spec tree**
  - Touch: `specs/docs/sdd-adoption/*`
  - Verify: spec / plan / tasks present and consistent with the change

- [x] **T5 — Changelog Unreleased bullet**
  - Touch: `CHANGELOG.md`
  - Verify: `[docs]` bullet under `## Unreleased`

## Done when

- All acceptance criteria in `spec.md` are met.
- No product test changes required (docs/tooling only).
- Ready for Conventional Commit on `chore/spec-driven-development`.
