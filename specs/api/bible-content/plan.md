# Plan: API-BIBLE — Bible content REST API

Spec: [`spec.md`](spec.md) (`API-BIBLE`)

## Approach

As-built DRF viewsets with nested serializers, Django filters used by OBS, and
DynamicFields `omit=` on translations/verses.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Models | `multimedia/bible/models.py` |
| API | `multimedia/api/bible/` |
| Tests | `multimedia/bible/tests/test_api.py` |

## Contracts

- Filters: translations by version / abbreviation + book name; verses by
  translation, chapter, verse, and nested abbreviation/book name.
- `omit=` comma-separated field names.

## Risks and rollout

- Documentation-only; write paths for versions/translations/verses are lightly
  tested compared to read/filter paths.

## Non-goals

- OBS browse/history UX; web bible admin.
