# Tasks 013: Django staff admin

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Docs-only legacy migration (CODE `WEB-ADMIN` → NNN 013). No behavior change. -->

## Checklist

- [x] Spec Accepted by the project owner (adopt with full migrate)
- [x] Branch from the current base (`chore/adopt-vexbook-v0.4.0`)
- [x] Red — domain/app tests (paths): N/A (docs-only; existing suite is proof)
- [x] Green — implementation (paths): `specs/013-web-django-admin/{plan,spec,tasks}.md`
- [x] Red — E2E (paths, or N/A in spec out-of-scope): N/A
- [x] Green — E2E: N/A
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`none`)
- [x] If bump is not `none`: N/A
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Legacy `WEB-ADMIN` intent preserved verbatim in `spec.md`
- [x] Existing `pytest` / `npm test` unaffected (docs-only)
- [x] Board, tasks, and version (if any) are complete in this PR

<details>
<summary>Legacy tasks (verbatim from `specs/web/django-staff-admin/tasks.md`)</summary>

# Tasks: WEB-ADMIN — Django staff admin

Spec: [`spec.md`](spec.md) (`WEB-ADMIN`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **WEB-ADMIN-T1 — Document staff admin EARS**
  - Touch: this folder
  - Verify: Align with `multimedia/*/admin.py`
  - Covers: `WEB-ADMIN-AC1`–`AC6`

- [ ] **WEB-ADMIN-T2 — Manual smoke (optional)**
  - Touch: `/admin/`
  - Verify: Login required; models listed for songs/bible/tatib/bookmarks
  - Covers: `WEB-ADMIN-AC1`–`AC2`

## Done when

- Spec matches as-built Django admin registrations.


</details>
