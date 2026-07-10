# Specs

Living specifications for this project. Process: [`docs/SDD.md`](../docs/SDD.md).
Spec IDs: see [Spec ID conventions](#spec-id-conventions) below.

| Path | Purpose |
|------|---------|
| [`constitution.md`](constitution.md) | Project-wide guardrails (points at `docs/`) |
| [`app/`](app/) | **APP** — full product overview and feature registry |
| [`_templates/`](_templates/) | Starter `spec.md` / `plan.md` / `tasks.md` |
| `<area>/<feature>/` | One folder per capability or change |

## Spec ID conventions

| Kind | Pattern | Example |
|------|---------|---------|
| Spec | `<CODE>` | `OBS-SONGS`, `API-SONGS`, `APP` |
| User story | `<CODE>-US<n>` | `OBS-SONGS-US1` |
| Acceptance criterion | `<CODE>-AC<n>` | `OBS-SONGS-AC3` |
| Task | `<CODE>-T<n>` | `OBS-SONGS-T2` |

- Codes are stable once published.
- Numbers restart per spec.
- OBS live surfaces: **`OBS-` first**, then domain (`OBS-SONGS`, …).
- Full rules: [`docs/SDD.md`](../docs/SDD.md#spec-ids).

## Feature registry

| Spec ID | Path | Status | Summary |
|---------|------|--------|---------|
| `APP` | [`app/`](app/) | as-built | Full product overview |
| `API-ACCESS` | [`api/open-access-policy/`](api/open-access-policy/) | as-built | Unauthenticated product API / web |
| `API-SONGS` | [`api/songs-content/`](api/songs-content/) | as-built | Songs books / songs / verses REST |
| `API-BIBLE` | [`api/bible-content/`](api/bible-content/) | as-built | Bible langs / versions / books / verses REST |
| `API-TATIB` | [`api/tatib-content/`](api/tatib-content/) | as-built | Tata ibadah + items REST |
| `API-SEARCH` | [`api/song-search/`](api/song-search/) | as-built | Song lyric phrase search |
| `SONGS-BM` | [`songs/song-bookmarks/`](songs/song-bookmarks/) | as-built | Song setlists (API + OBS) |
| `OBS-SONGS` | [`songs/obs-songs-live/`](songs/obs-songs-live/) | as-built | OBS Songs dock + source |
| `OBS-BIBLE` | [`bible/obs-bible-live/`](bible/obs-bible-live/) | as-built | OBS Bible dock + source |
| `OBS-TATIB` | [`tatib/obs-tatib-live/`](tatib/obs-tatib-live/) | as-built | OBS Tatib dock + source |
| `OBS-PROJECT` | [`project/obs-project-projection/`](project/obs-project-projection/) | as-built | Combined OBS projection |
| `WEB-SONGS` | [`web/songs-content-admin/`](web/songs-content-admin/) | as-built | Browser songs content admin |
| `WEB-TATIB` | [`web/tatib-content-admin/`](web/tatib-content-admin/) | as-built | Browser tatib content admin |
| `WEB-ADMIN` | [`web/django-staff-admin/`](web/django-staff-admin/) | as-built | Django `/admin/` staff UI |
| `DEPLOY-VERCEL` | [`deploy/vercel-production/`](deploy/vercel-production/) | as-built | Vercel + Neon production |
| `DEPLOY-LOCAL` | [`deploy/local-compose-runtime/`](deploy/local-compose-runtime/) | as-built | Docker Compose local runtime |
| `DOCS-SDD` | [`docs/sdd-adoption/`](docs/sdd-adoption/) | active | SDD process adoption |
| `TEST-COV` | [`test/current-coverage/`](test/current-coverage/) | active | Current-state test coverage |

## Starting a new change

1. Pick a new Spec ID (add a row to the registry and to [`app/spec.md`](app/spec.md)).
2. Copy `_templates/` into `specs/<area>/<short-feature-name>/`.
3. Fill `spec.md` (with `CODE-US*` / `CODE-AC*`) → human OK → `plan.md` → OK → `tasks.md` → OK.
4. Implement tasks with TDD; keep the spec updated if intent shifts.

`<area>` should align with changelog labels when possible (`songs`, `bible`,
`api`, `web`, `deploy`, `docs`, …).
