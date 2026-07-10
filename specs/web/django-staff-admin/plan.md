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
