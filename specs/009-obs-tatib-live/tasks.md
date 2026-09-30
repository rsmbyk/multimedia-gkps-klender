# Tasks 009: OBS Tatib dock and source

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `OBS-TATIB` → NNN 009). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/009-obs-tatib-live/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `OBS-TATIB` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/tatib/obs-tatib-live/tasks.md`)</summary>

# Tasks: OBS-TATIB — OBS Tatib dock and source

Spec: [`spec.md`](spec.md) (`OBS-TATIB`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **OBS-TATIB-T1 — Document Tatib OBS EARS**
  - Touch: this folder
  - Verify: Align with tatib dock/source JS + Vitest
  - Covers: `OBS-TATIB-AC1`–`AC17`

- [ ] **OBS-TATIB-T2 — Keep Tatib OBS Vitest green**
  - Touch: `multimedia/obs/static/obs/tatib/**/*.test.js`
  - Verify: `npm test -- tatib`
  - Covers: `OBS-TATIB-AC2`, `AC13` (partial)

## Done when

- Spec matches as-built Tatib OBS; Vitest remains the automated proof.


</details>
