# Tasks 015: Local Compose runtime

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `DEPLOY-LOCAL` → NNN 015). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/015-deploy-local/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `DEPLOY-LOCAL` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/deploy/local-compose-runtime/tasks.md`)</summary>

# Tasks: DEPLOY-LOCAL — Local Docker Compose runtime

Spec: [`spec.md`](spec.md) (`DEPLOY-LOCAL`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **DEPLOY-LOCAL-T1 — Document local Compose EARS**
  - Touch: this folder
  - Verify: Align with README + `docker-compose.yml` + `.env.example`
  - Covers: `DEPLOY-LOCAL-AC1`–`AC6`

- [ ] **DEPLOY-LOCAL-T2 — Manual smoke (optional)**
  - Touch: Compose stack
  - Verify: `docker compose up` → http://127.0.0.1:63404/ (published port moved
    by spec [018](../018-local-compose-ports/spec.md); see `.env` `WEB_PORT`)
  - Covers: `DEPLOY-LOCAL-AC4`

## Done when

- Spec matches as-built local runtime docs.


</details>
