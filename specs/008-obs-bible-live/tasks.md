# Tasks 008: OBS Bible dock and source

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `OBS-BIBLE` → NNN 008). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/008-obs-bible-live/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `OBS-BIBLE` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/bible/obs-bible-live/tasks.md`)</summary>

# Tasks: OBS-BIBLE — OBS Bible dock and source

Spec: [`spec.md`](spec.md) (`OBS-BIBLE`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **OBS-BIBLE-T1 — Document Bible OBS EARS**
  - Touch: this folder
  - Verify: Align with bible dock/source JS + Vitest
  - Covers: `OBS-BIBLE-AC1`–`AC17`

- [ ] **OBS-BIBLE-T2 — Keep Bible OBS Vitest green**
  - Touch: `multimedia/obs/static/obs/bible/**/*.test.js`
  - Verify: `npm test -- bible`
  - Covers: `OBS-BIBLE-AC2`, `AC10`, `AC8` (partial)

## Done when

- Spec matches as-built Bible OBS; Vitest remains the automated proof.


</details>
