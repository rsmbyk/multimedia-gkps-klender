# Tasks 007: OBS Songs dock and source

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `OBS-SONGS` → NNN 007). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/007-obs-songs-live/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `OBS-SONGS` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/songs/obs-songs-live/tasks.md`)</summary>

# Tasks: OBS-SONGS — OBS Songs dock and source

Spec: [`spec.md`](spec.md) (`OBS-SONGS`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **OBS-SONGS-T1 — Document Songs OBS EARS**
  - Touch: this folder
  - Verify: Align with dock/source JS + Vitest
  - Covers: `OBS-SONGS-AC1`–`AC20`

- [ ] **OBS-SONGS-T2 — Keep Songs OBS Vitest green**
  - Touch: `multimedia/obs/static/obs/songs/**/*.test.js`
  - Verify: `npm test -- songs`
  - Covers: `OBS-SONGS-AC2`, `AC10`–`AC12` (partial)

## Done when

- Spec matches as-built Songs OBS; existing Vitest remains the automated proof.


</details>
