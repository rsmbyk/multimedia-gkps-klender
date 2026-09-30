# Tasks 012: Web tatib content admin

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `WEB-TATIB` → NNN 012). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/012-web-tatib-admin/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [ ] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [ ] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `WEB-TATIB` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [ ] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/web/tatib-content-admin/tasks.md`)</summary>

# Tasks: WEB-TATIB — Tatib content admin (web)

Spec: [`spec.md`](spec.md) (`WEB-TATIB`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **WEB-TATIB-T1 — Document web tatib admin EARS**
  - Touch: this folder
  - Verify: Align with web tatib JS + Vitest
  - Covers: `WEB-TATIB-AC1`–`AC10`

- [ ] **WEB-TATIB-T2 — Keep reorder Vitest green**
  - Touch: `multimedia/web/static/web/tatib/items/reorder.test.js`
  - Verify: `npm test -- reorder`
  - Covers: `WEB-TATIB-AC9`

## Done when

- Spec matches as-built web tatib admin; Vitest remains the proof.


</details>
