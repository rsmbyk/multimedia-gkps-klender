# Tasks 016: SDD adoption notes

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `DOCS-SDD` → NNN 016). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/016-docs-sdd-adoption/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `DOCS-SDD` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [ ] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/docs/sdd-adoption/tasks.md`)</summary>

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


</details>
