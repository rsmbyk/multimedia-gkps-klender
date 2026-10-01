# Plan 003: Maintenance page at the site root

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-004
- **Bump:** minor

## Why

The public home is served at `/` (spec 001). While the site is still being
prepared, the owner wants `/` to show a short "under maintenance" notice instead
of the reading home, and the current home to remain reachable at a temporary URL
for the people who need it.

The switch must be reversible without a code change, so it is gated by a
`MAINTENANCE_MODE` setting rather than hardcoded.

## Scope / edges

**In:**

- A `MAINTENANCE_MODE` boolean setting read from the environment
  (`MAINTENANCE_MODE`).
- `/` serves the maintenance page when maintenance is on: HTTP **503** with a
  `Retry-After` header, `noindex`.
- `/` serves the real home when maintenance is off.
- The existing `HomeView` mounted at `/home/`, still named `web-home`, so header
  links and search resolve to the real home.
- A maintenance template in the project design language (no Fomantic, no search
  form).
- Tests (`multimedia/web/tests.py`) and the E2E reading flow updated to the
  temporary URL, plus one E2E for the maintenance page.
- Docs: `docs/ARCHITECTURE.md` URL roots; an additive note on spec 001; glossary
  terms for **Maintenance page** / **Temporary home**.

**Out:**

- Global maintenance middleware (only `/` is gated; `/songs/`, `/manage/`,
  `/admin/`, `/api/`, and `/obs/` stay up).
- A `MAINTENANCE_ALLOWLIST` or per-route config.
- Any i18n framework — copy is a single template.
- Deploy/env wiring beyond documenting the variable (set in Vercel; see
  [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md)).

## Approach

1. **`multimedia/settings.py`** — add
   `MAINTENANCE_MODE = config('MAINTENANCE_MODE', default=<proposed>, cast=bool)`.
2. **`multimedia/web/views.py`** — an `IndexView` (subclass of `HomeView`) whose
   `get` returns the maintenance response when `settings.MAINTENANCE_MODE` is
   true, otherwise falls through to the home.
3. **`multimedia/web/urls.py`** — mount the real home at `home/` under the name
   `web-home`, and the `IndexView` at `''` under a new name `web-index`.
4. **Template** `multimedia/web/templates/reading/maintenance.html` — logo,
   heading, a short body in Indonesian + English, `noindex`, styled by
   `styles/design/`.
5. **Tests** — unit tests in `multimedia/web/tests.py` with
   `override_settings(MAINTENANCE_MODE=True/False)`; update
   `tests/e2e/test_reading.py` to open `reverse('web-home')` and add a
   maintenance-page E2E.
6. **Docs** — ARCHITECTURE URL roots, spec 001 additive note, glossary rows.

## TDD

- **Domain/app tests:** `multimedia/web/tests.py` — a `MaintenanceModeTests`
  class: `/` is 503 + `Retry-After` and hides search when on; `/` is the home
  when off; `/home/` is the home either way; `/songs/`, `/manage/` stay 200.
- **E2E (Playwright):** `tests/e2e/test_reading.py` — existing flows navigate to
  the temporary home; one added test asserts `/` shows the maintenance notice.
  Skips cleanly when the browser is unavailable (no browser in this environment;
  verified by hand instead).

## Risks

- **E2E breakage at `/`.** The existing E2E opens `'/'`; with maintenance on it
  must point at the temporary URL. Handled in the same PR.
- **`MAINTENANCE_MODE` default.** Proposed `default=True` so the notice is live
  as asked; setting `MAINTENANCE_MODE=False` restores the home. If the owner
  prefers a safe-by-default toggle, flip the default and set it in Vercel.
- **SEO.** A 503 with `Retry-After` keeps search engines retrying rather than
  indexing the notice; the page also carries `noindex`. The temporary home
  (`/home/`) is not canonical while maintenance is on.
- **Accidental scope creep into a full maintenance mode.** Only `/` is gated; a
  site-wide switch would be a separate spec.
- **Temporary URL name.** `/home/` is proposed (English paths per
  [`docs/GLOSSARY.md`](../../docs/GLOSSARY.md)); `/beranda/` is the Indonesian
  alternative.

## Owner decisions (resolved at Accept)

1. Temporary URL: `/home/`.
2. `MAINTENANCE_MODE` default: `True` (notice live now; set `False` to restore).
3. Copy: Indonesian with a short English line.
