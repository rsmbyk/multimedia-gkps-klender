# Plan: API-ACCESS — Open product access policy

Spec: [`spec.md`](spec.md) (`API-ACCESS`)

## Approach

Document the as-built open-access policy. No code changes in this backfill.
Other API/web/OBS specs link here for auth assumptions.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Settings | `multimedia/settings.py` (`REST_FRAMEWORK`) |
| Router | `multimedia/api/routers.py` (`OptionalTrailingSlashRouter`) |
| URLs | `multimedia/urls.py` — `/api/`, `/admin/`, web routes |
| Tests | `multimedia/*/tests/test_api.py` unauthenticated cases |

## Contracts

- Unauthenticated AllowAny for product API.
- Staff auth only for `/admin/`.
- Optional trailing slash on API routes.

## Risks and rollout

- Risks: Deploying publicly without network controls exposes write APIs —
  accepted as-built; call out in ops notes if needed.
- Documentation-only backfill.

## Non-goals

- Adding authentication.
- Changing CSRF or session settings.
