# Plan 013: Django staff admin

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `WEB-ADMIN` from `specs/web/django-staff-admin/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/web/django-staff-admin/{spec,plan,tasks}.md` into `specs/013-web-django-admin/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/web/django-staff-admin/plan.md`)</summary>

# Plan: WEB-ADMIN — Django staff admin

Spec: [`spec.md`](spec.md) (`WEB-ADMIN`)

## Approach

Document as-built `ModelAdmin` registrations. No new admin features in this
backfill.

## Touch points

| Area | Files / modules |
|------|-----------------|
| URL | `multimedia/urls.py` → `admin/` |
| Admin | `multimedia/{songs,bible,tatib,bookmarks}/admin.py` |

## Contracts

- Staff auth required.
- Search/filter/autocomplete as listed in ACs.

## Risks and rollout

- Documentation-only; no admin automated tests today.

## Non-goals

- Building bible/bookmarks public web UIs.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `WEB-ADMIN` — intended; follow-up may update them.
