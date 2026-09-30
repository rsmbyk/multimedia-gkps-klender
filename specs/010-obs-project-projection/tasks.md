# Tasks 010: Combined OBS projection

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `OBS-PROJECT` → NNN 010). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/010-obs-project-projection/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `OBS-PROJECT` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [ ] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/project/obs-project-projection/tasks.md`)</summary>

# Tasks: OBS-PROJECT — Combined OBS project projection

Spec: [`spec.md`](spec.md) (`OBS-PROJECT`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **OBS-PROJECT-T1 — Document project OBS EARS**
  - Touch: this folder
  - Verify: Align with project source/settings JS + Vitest
  - Covers: `OBS-PROJECT-AC1`–`AC11`

- [ ] **OBS-PROJECT-T2 — Keep project Vitest green**
  - Touch: `multimedia/obs/static/obs/project/**/*.test.js`
  - Verify: `npm test -- project`
  - Covers: `OBS-PROJECT-AC3`, `AC11` (partial)

## Done when

- Spec matches as-built project projection; Vitest remains the automated proof.


</details>
