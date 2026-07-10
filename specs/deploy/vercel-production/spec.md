# Spec: DEPLOY-VERCEL — Vercel production hosting

| Field | Value |
|-------|--------|
| **Spec ID** | `DEPLOY-VERCEL` |
| **Area** | `deploy` |
| **Status** | `as-built` |
| **Folder** | `specs/deploy/vercel-production/` |

## Problem / goal

Production must reliably serve Django (API, web, OBS pages, static) on Vercel
with Neon/`DATABASE_URL`, without regressing to platform 404s from broken
routing.

## User stories

- **DEPLOY-VERCEL-US1:** As a maintainer, I want `main` deploys on Vercel to
  reach Django WSGI, so that all app URLs work in production.
- **DEPLOY-VERCEL-US2:** As an operator, I want static assets and OBS pages
  served from the same origin, so that docks/sources keep working after deploy.
- **DEPLOY-VERCEL-US3:** As a maintainer, I want unsafe debug disabled on
  Vercel, so that production is not left in DEBUG mode.

## Acceptance criteria (EARS)

- **DEPLOY-VERCEL-AC1:** Production SHALL deploy from Git branch `main` via
  Vercel with PostgreSQL `DATABASE_URL` (e.g. Neon).
- **DEPLOY-VERCEL-AC2:** THE root `vercel.json` SHALL keep legacy `builds` +
  `routes` sending `/(.*)` to `multimedia/wsgi.py` exporting callable `app`.
- **DEPLOY-VERCEL-AC3:** THE project SHALL NOT remove that `vercel.json` wiring
  without a tested migration plan (prior removal caused platform 404s with no
  Django logs).
- **DEPLOY-VERCEL-AC4:** WHEN `VERCEL` is set, THE settings SHALL append
  `.vercel.app` / `VERCEL_URL` to `ALLOWED_HOSTS` and trusted CSRF origins as
  documented in [`docs/DEPLOY.md`](../../../docs/DEPLOY.md).
- **DEPLOY-VERCEL-AC5:** WHEN `VERCEL` is set, THE settings SHALL refuse
  `DJANGO_DEBUG=True`.
- **DEPLOY-VERCEL-AC6:** WHEN `VERCEL` is set, static files SHALL be served via
  WhiteNoise finders (no fragile collectstatic-only build step as the sole
  strategy).
- **DEPLOY-VERCEL-AC7:** Required production env vars SHALL include
  `DATABASE_URL`, `DJANGO_SECRET_KEY`, and `DJANGO_DEBUG=False` (plus
  recommended host/CSRF vars for custom domains).

## Out of scope

- Migrating off Vercel / zero-config Django experiments (separate spike).
- Local Compose runtime (`DEPLOY-LOCAL`).
- Silencing the legacy-builds warning without a tested replacement.

## Constraints

- Follow [`docs/DEPLOY.md`](../../../docs/DEPLOY.md) and constitution deploy
  rules.
- Related: `APP`, `DEPLOY-LOCAL`, Git Flow release path to `main`.

## Notes

- Incident history: `0.4.16` removed `vercel.json` → 404s; `0.4.17` restored.
