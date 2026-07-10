# Production deploy

This is the **runbook for the current production setup**. Follow it before
changing hosting, `vercel.json`, static-file settings, or production env vars.

Hosting migrations (leaving Vercel, zero-config Django, etc.) are **out of
scope** here — treat those as a separate spike with an explicit rollback plan.

## Current production

| Piece | Value |
|-------|--------|
| Host | **Vercel** (Python serverless) |
| Database | **PostgreSQL** via `DATABASE_URL` (e.g. Neon) |
| Git branch | **`main`** only |
| How code reaches `main` | Git Flow **`release/*`** or **`hotfix/*`** (merge commit) — see [`GIT_FLOW.md`](GIT_FLOW.md) |
| App entry | `multimedia/wsgi.py` — callable **`app`** (alias of Django `application`) |
| Python | **3.12** (`.python-version` and `vercel.json` `runtime`) |

Vercel should track **`main`** as the production branch. Preview deploys from
other branches are optional; do not treat them as production.

## How requests reach Django

Production depends on root [`vercel.json`](../vercel.json):

1. **Legacy `builds`** — `@vercel/python` builds `multimedia/wsgi.py` as the
   serverless function (`maxLambdaSize` `50mb`, `runtime` `python3.12`).
2. **`routes`** — every path `/(.*)` is sent to that WSGI entry.

That wiring is what makes Django handle `/`, `/obs/...`, `/api/...`, and static
URLs through the app.

### Do not remove this casually

In `0.4.16` we deleted `vercel.json` to silence the legacy-`builds` warning and
rely on Vercel “zero-config” Django detection. The **build succeeded** but
**no function was routed**, so every URL returned Vercel’s platform **404** with
**no Django / machine logs**. Restoring `vercel.json` (`0.4.17`) fixed it.

Until a deliberate, tested migration exists:

- Keep `vercel.json` with `builds` + `routes` pointing at `multimedia/wsgi.py`
- Keep the WSGI module exporting **`app`**
- Expect Vercel’s **legacy builds warning** — cosmetic; prefer a working site

## Environment variables (Vercel)

Set these in the Vercel project (**Settings → Environment Variables**), at least
for **Production**. Local Docker uses [`.env.example`](../.env.example) and a
compose-injected Postgres URL — do not point local `.env` at Neon.

### Required

| Variable | Notes |
|----------|--------|
| `DATABASE_URL` | Postgres URL (Neon or other). Must be reachable from Vercel. |
| `DJANGO_SECRET_KEY` | Long random secret. Required whenever the app loads (no random fallback). |
| `DJANGO_DEBUG` | `False` in production. Settings refuse `True` when `VERCEL` is set. |

### Recommended for a custom domain

| Variable | Notes |
|----------|--------|
| `DJANGO_ALLOWED_HOSTS` | Your domain(s), comma-separated. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Full origins, e.g. `https://your-domain.example`. |

### Automatic on Vercel

When `VERCEL` is set, [`multimedia/settings.py`](../multimedia/settings.py):

- Appends `.vercel.app` and `VERCEL_URL` to `ALLOWED_HOSTS`
- Appends `https://{VERCEL_URL}` to `CSRF_TRUSTED_ORIGINS` when `VERCEL_URL` is present

Missing hosts historically produced Django **400 Bad Request** on `*.vercel.app`.

## Static files on Vercel

On Vercel (`VERCEL` set):

- `STATICFILES_STORAGE` = WhiteNoise **compressed** storage (**not** the
  manifest variant)
- `WHITENOISE_USE_FINDERS` = `True` — serve from app/`STATICFILES_DIRS` at
  runtime without requiring a successful `collectstatic` into `_static`

Elsewhere (local / non-Vercel), the project still uses
`CompressedManifestStaticFilesStorage` and `STATIC_ROOT` = `_static`.

Do **not** reintroduce a Vercel `build.sh` / `collectstatic` step unless you
have verified it on a preview deploy. A failing static build previously broke
production deploys even when the app code was fine.

## Release → deploy checklist

1. Cut and merge a Git Flow **`release/*`** or **`hotfix/*`** into **`main`**
   (merge commit). Tag `vX.Y.Z` when shipping a version — see
   [`VERSIONING.md`](VERSIONING.md) (single SemVer from `0.5.0`).
2. Confirm Vercel starts a **Production** deployment from `main`.
3. Wait for the deployment to succeed (build log green).
4. Smoke-test (below).
5. Hard-refresh / clear cache on each OBS browser source after a frontend or
   template change — OBS caches aggressively.

## Post-deploy smoke checklist

Use the production origin (custom domain or `*.vercel.app`):

- [ ] `/` loads (not Vercel platform 404, not Django 400/500)
- [ ] A known API path responds (e.g. an authenticated or public list you use)
- [ ] One OBS dock HTML loads (e.g. `/obs/songs/dock`)
- [ ] Static asset from that page loads (CSS/JS — no widespread 404s)
- [ ] If you changed OBS JS/CSS/templates: hard-refresh docks/sources in OBS

If you see a **Vercel 404** with an empty runtime log, suspect routing /
`vercel.json` first — not application code.

If you see Django **400**, check `ALLOWED_HOSTS` / custom domain env vars.

If you see Django **500**, check Vercel function logs (database, secret, import
errors).

## Landmines (read before changing prod)

| Change | Risk |
|--------|------|
| Delete or empty `vercel.json` | Platform 404; Django never runs |
| Remove `builds` / `routes` for “modern” config without a tested replacement | Same |
| Rename/remove WSGI `app` | Function may not bind |
| Force zero-config Django without verifying this repo layout | Undetected missing function |
| Set `DJANGO_DEBUG=True` in production | Settings raise on Vercel; security risk elsewhere |
| Omit `DJANGO_SECRET_KEY` | App fails to start (no random fallback) |
| Break `DATABASE_URL` | 500s on every DB hit / startup ImproperlyConfigured |
| Re-add failing `collectstatic` build step | Deploy fails before traffic moves |
| Deploy product work from a branch other than `main` | Bypasses Git Flow; easy to lose track of what’s live |

## Known cosmetic issue

Vercel may warn that **`builds` in `vercel.json` is legacy** and overrides some
project settings. That warning is **expected** with the current working config.
Do not “fix” it by deleting `vercel.json` without a full preview + production
validation plan.

## Future work (not this runbook)

Possible later spikes (each needs its own plan and rollback):

- Migrate off legacy `builds` to a supported Vercel Python/Django shape that
  still routes to `multimedia/wsgi.py`
- Move hosting (container platform, VM, etc.)
- Automate smoke checks in CI after `main` deploys

Until then, **prefer documenting and freezing** this setup over drive-by cleanup.
