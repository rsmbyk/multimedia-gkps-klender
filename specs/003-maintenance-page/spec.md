# Spec: Maintenance page at the site root

- **ID:** 003
- **Status:** Accepted
- **Item:** ITEM-004
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

While the public site is still being prepared, the site root `/` shows a short
maintenance notice, and the current reading home stays reachable at a temporary
URL. The notice is switchable through `MAINTENANCE_MODE` so it can be turned off
without a code change.

This conditionally supersedes the spec 001 home scenario when maintenance is on.
Only `/` is gated; the editor, API, OBS surfaces, and the rest of public reading
are untouched.

## Scope

### In scope

- `MAINTENANCE_MODE` boolean setting (env `MAINTENANCE_MODE`).
- `/` serving the maintenance page (HTTP 503, `Retry-After`, `noindex`) when on,
  and the real home when off.
- The real home at `/home/`, still named `web-home`.
- A design-language maintenance template.
- Unit tests + E2E updates.
- Docs: `docs/ARCHITECTURE.md`, an additive note on spec 001, glossary rows.

### Out of scope

- Site-wide maintenance (middleware, allowlists, per-route rules).
- Gating `/songs/`, `/manage/`, `/admin/`, `/api/`, `/obs/`.
- An i18n framework.
- Deploy/env wiring beyond documenting `MAINTENANCE_MODE`.

## Domain rules

- **One switch.** Maintenance behavior is controlled only by
  `MAINTENANCE_MODE`; no other state changes which response `/` gives.
- **Only the root is gated.** `/` alone reflects maintenance; every other route
  behaves exactly as before.
- **The real home keeps its name.** The temporary URL is mounted under the
  existing `web-home` url name, so header brand/search links resolve to the real
  home, not the notice.
- **Honest HTTP.** The maintenance response is `503 Service Unavailable` with a
  `Retry-After` header, and carries `noindex`; it is not a `200`.
- **No dead controls.** The notice does not render the song search form (it
  would submit back to `/`).

## Acceptance scenarios

### Scenario: Maintenance is on

- **Given** `MAINTENANCE_MODE` is on
- **When** I open `/`
- **Then** I get a `503` response
- **And** the body shows the maintenance notice
- **And** the response has a `Retry-After` header and a `noindex` directive
- **And** the song search form is not present

### Scenario: The real home stays reachable

- **Given** `MAINTENANCE_MODE` is on
- **When** I open `/home/`
- **Then** I get the reading home (`200`) with the search field and book list
- **And** its brand and search links point at `/home/`, not `/`

### Scenario: Maintenance is off

- **Given** `MAINTENANCE_MODE` is off
- **When** I open `/`
- **Then** I get the reading home (`200`) with the search field and book list

### Scenario: Other surfaces are unaffected

- **Given** either maintenance state
- **When** I open `/songs/`, `/manage/`, or an API/OBS route
- **Then** it responds as before, not with the maintenance notice

### Scenario: Reader still browses and reads (E2E)

- **Given** the temporary home `/home/`
- **When** a reader browses books and opens a song
- **Then** the lyrics render as in spec 001

## Traceability

- Domain/app tests: `multimedia/web/tests.py` — `MaintenanceModeTests`
  (`test_root_shows_maintenance_when_on`,
  `test_root_shows_home_when_off`,
  `test_temporary_home_serves_home_when_on`,
  `test_other_surfaces_unaffected`).
- E2E: `tests/e2e/test_reading.py` — existing flows moved to the temporary home,
  plus `test_maintenance_notice_at_root`. Skips cleanly without a browser.
- Implementation: `multimedia/settings.py`, `multimedia/web/views.py`,
  `multimedia/web/urls.py`,
  `multimedia/web/templates/reading/maintenance.html`, `docs/ARCHITECTURE.md`,
  `docs/GLOSSARY.md`, `specs/001-public-songs-reading/spec.md`.

> **Verified:** `multimedia.web` suite green (17 tests, 4 new) in the project
> image. Live check on the running stack: `/` → `503` + `Retry-After: 3600` +
> `noindex` and no search form; `/home/` → `200` with search; `/songs/` → `200`.
> E2E updated and declares a maintenance test, but skips here (no browser
> binary) — run `playwright install chromium` to execute it.
