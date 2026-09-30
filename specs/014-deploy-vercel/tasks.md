# Tasks 014: Vercel production

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `DEPLOY-VERCEL` → NNN 014). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/014-deploy-vercel/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `DEPLOY-VERCEL` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/deploy/vercel-production/tasks.md`)</summary>

# Tasks: DEPLOY-VERCEL — Vercel production hosting

Spec: [`spec.md`](spec.md) (`DEPLOY-VERCEL`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **DEPLOY-VERCEL-T1 — Document production EARS from deploy runbook**
  - Touch: this folder
  - Verify: Align with `docs/DEPLOY.md` + `vercel.json`
  - Covers: `DEPLOY-VERCEL-AC1`–`AC7`

- [ ] **DEPLOY-VERCEL-T2 — Treat vercel.json changes as high-risk**
  - Touch: `vercel.json`, `multimedia/wsgi.py`
  - Verify: Any change has explicit tested plan / rollback
  - Covers: `DEPLOY-VERCEL-AC2`–`AC3`

## Done when

- Spec matches production runbook; agents link here before deploy edits.


</details>
