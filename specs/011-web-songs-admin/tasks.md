# Tasks 011: Web songs content admin

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `WEB-SONGS` → NNN 011). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/011-web-songs-admin/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `WEB-SONGS` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/web/songs-content-admin/tasks.md`)</summary>

# Tasks: WEB-SONGS — Songs content admin (web)

Spec: [`spec.md`](spec.md) (`WEB-SONGS`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **WEB-SONGS-T1 — Document web songs admin EARS**
  - Touch: this folder
  - Verify: Align with web songs JS + Vitest path/chunk tests
  - Covers: `WEB-SONGS-AC1`–`AC10`

- [ ] **WEB-SONGS-T2 — Keep web Vitest contracts green**
  - Touch: `multimedia/web/static/web/**/*.test.js`
  - Verify: `npm test -- api-paths lyric-chunks`
  - Covers: `WEB-SONGS-AC4`–`AC6`, `WEB-SONGS-AC10`

## Done when

- Spec matches as-built web songs admin; Vitest contracts remain the proof.


</details>
