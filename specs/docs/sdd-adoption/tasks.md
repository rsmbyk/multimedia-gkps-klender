# Tasks: DOCS-SDD — Spec-Driven Development adoption

Spec: [`spec.md`](spec.md) (`DOCS-SDD`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **DOCS-SDD-T1 — Write `docs/SDD.md`**
  - Touch: `docs/SDD.md`
  - Verify: phases, when-to-use, layout, EARS, TDD relationship documented
  - Covers: `DOCS-SDD-AC1`, `DOCS-SDD-AC4`, `DOCS-SDD-AC5`

- [x] **DOCS-SDD-T2 — Add Cursor rule and AGENTS pointer**
  - Touch: `.cursor/rules/sdd.mdc`, `AGENTS.md`
  - Verify: rule is alwaysApply; AGENTS has Specs (SDD) section
  - Covers: `DOCS-SDD-AC1`, `DOCS-SDD-AC3`

- [x] **DOCS-SDD-T3 — Scaffold `specs/` + templates + constitution**
  - Touch: `specs/README.md`, `specs/constitution.md`, `specs/_templates/*`
  - Verify: templates are copyable; constitution links existing docs
  - Covers: `DOCS-SDD-AC2`

- [x] **DOCS-SDD-T4 — Record this adoption as an example spec tree**
  - Touch: `specs/docs/sdd-adoption/*`
  - Verify: spec / plan / tasks present and consistent with the change
  - Covers: `DOCS-SDD-AC2`

- [x] **DOCS-SDD-T5 — Changelog Unreleased bullet**
  - Touch: `CHANGELOG.md`
  - Verify: `[docs]` bullet under `## Unreleased`
  - Covers: `DOCS-SDD-AC1`

- [x] **DOCS-SDD-T6 — Spec ID conventions**
  - Touch: `docs/SDD.md`, `specs/README.md`, templates
  - Verify: `CODE` / `CODE-US*` / `CODE-AC*` / `CODE-T*` documented
  - Covers: `DOCS-SDD-AC6`

## Done when

- All acceptance criteria in `spec.md` are met.
- No product test changes required (docs/tooling only).
