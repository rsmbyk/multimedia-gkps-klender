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
