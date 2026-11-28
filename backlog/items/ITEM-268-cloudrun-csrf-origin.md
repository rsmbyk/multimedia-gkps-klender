---
id: ITEM-268
status: done
title: 'Cloud Run writes pass CSRF'
type: fix
priority: P0
effort: S
created: 2026-11-28
updated: 2026-11-28
spec: specs/251-cloudrun-csrf-origin/spec.md
branch: fix/251-cloudrun-csrf-origin
pr: 644
issue: 643
closed_at: 2026-11-28
closed_reason: merged into develop (PR #644)
bump: patch
release_version:
---

# ITEM-268: Cloud Run writes pass CSRF

## Summary

Every add, edit and delete on the two live sites returns a Django CSRF 403. Cloud Run ends TLS before
the request reaches gunicorn, and no proxy-scheme setting tells Django that the request was HTTPS, so
the browser's HTTPS Origin is compared with an http:// host. Reading works; no write reaches its view.

## Notes

- Measured on both live services on 2026-11-28: a valid CSRF cookie/token with `Origin: https://<host>`
  gives 403; the same POST with `Origin: http://<host>` gives 404 from the nonexistent target. The
  failure is the scheme decision, not the token, the view or the database.
- Fix: `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` in `multimedia/settings.py`.
- Regression: `tests/test_cloudrun_csrf.py` — a real CSRF middleware request in Cloud Run shape,
  red (403) before the setting and green (200) after; a negative case keeps CSRF enforced.
- Deployment is a separate step: the setting only helps after both Cloud Run services are redeployed.

## Acceptance sketch

- A Cloud Run-shaped HTTPS POST reaches the view; without the proxy header the same POST is still 403.
- After deployment, the nonexistent-PK probe answers 404 on production and staging, not 403.
- Local Compose over plain HTTP is unchanged.

## Links

- Spec: [251](../../specs/251-cloudrun-csrf-origin/spec.md)
- Related items: [ITEM-113](ITEM-113-media-library-share-csrf.md) (a different CSRF cookie issue).
