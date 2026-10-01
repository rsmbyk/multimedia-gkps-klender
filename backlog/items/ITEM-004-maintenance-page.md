---
id: ITEM-004
status: in_review
title: Maintenance page at the site root
type: feat
priority: P1
effort: M
created: 2026-10-01
updated: 2026-10-01
spec: ../specs/003-maintenance-page/spec.md
branch: feat/003-maintenance-page
pr:
archived_at:
archive_reason:
bump: minor
release_version: 0.7.0
---

# ITEM-004: Maintenance page at the site root

## Summary

The public home lives at `/`. While the site is still being prepared, the owner
wants `/` to show a short "under maintenance" notice instead of the reading
home, and the current home to stay reachable at a temporary URL (`/home/`) for
the people who need it.

The change is gated by a `MAINTENANCE_MODE` setting (env `MAINTENANCE_MODE`) so
it can be turned off without a code change. Only `/` is affected; `/songs/`,
`/manage/`, `/admin/`, `/api/`, and `/obs/` keep working.

## Notes

- `index.html` in `web/templates/` is the **editor** landing at `/manage/`
  (`web-root`), not the public home. "Index url" here means the site root `/`
  (`HomeView`, url name `web-home`).
- Keep the url name `web-home` on the real home so header links and search keep
  working; `/` gets its own view/name.
- The maintenance page should use the project's design language
  (`static/styles/design/`), not Fomantic, and must not link into the search
  form (which would bounce back to `/`).
- Copy proposed (adjustable): Indonesian primary with a short English line.
- `bump: minor` — a backward-compatible capability (maintenance mode) plus a new
  route.

## Acceptance sketch

- With maintenance on, `GET /` returns **503** with a `Retry-After` header and
  the maintenance copy; it does not show the search form.
- The real home is reachable at `/home/` and still works (browse, search).
- With maintenance off, `/` shows the real home again.
- `/songs/`, `/manage/`, `/admin/`, `/api/`, `/obs/` are unaffected either way.

## Links

- Spec: [`specs/003-maintenance-page/spec.md`](../specs/003-maintenance-page/spec.md)
- Supersedes (conditionally): spec 001 home scenario
- Related items: ITEM-001 (public reading home)
