# Plan 011: Web songs content admin

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `WEB-SONGS` from `specs/web/songs-content-admin/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/web/songs-content-admin/{spec,plan,tasks}.md` into `specs/011-web-songs-admin/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/web/songs-content-admin/plan.md`)</summary>

# Plan: WEB-SONGS — Songs content admin (web)

Spec: [`spec.md`](spec.md) (`WEB-SONGS`)

## Approach

As-built Django TemplateViews + axios ES modules talking to `API-SONGS`. Hymn
books are UI-restricted; API may still allow writes.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Views/URLs | `multimedia/web/songs/` |
| Templates | `multimedia/web/templates/songs/` |
| JS | `multimedia/web/static/web/songs/`, `api-paths.js` |
| Tests | `api-paths.test.js`, `lyric-chunks.test.js` |

## Contracts

- Path helpers in `api-paths.js` must stay aligned with `/api/songs/…`.
- Lyric chunk pairing for preview.

## Risks and rollout

- Documentation-only; no pytest for page auth (open by policy).

## Non-goals

- Changing hymn-book write policy on the API.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `WEB-SONGS` — intended; follow-up may update them.
