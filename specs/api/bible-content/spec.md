# Spec: API-BIBLE — Bible content REST API

| Field | Value |
|-------|--------|
| **Spec ID** | `API-BIBLE` |
| **Area** | `api` |
| **Status** | `as-built` |
| **Folder** | `specs/api/bible-content/` |

## Problem / goal

OBS Bible dock/source and API consumers need structured access to languages,
versions, books, book translations, and verses (including nested filters and
optional field omission used by OBS).

## User stories

- **API-BIBLE-US1:** As an OBS Bible dock, I want to filter translations and
  verses by version/book/chapter, so that I can load a passage quickly.
- **API-BIBLE-US2:** As a client, I want `omit=` on translation/verse payloads,
  so that responses stay small for projection UIs.
- **API-BIBLE-US3:** As a maintainer, I want CRUD on bible domain models via
  REST, so that content can be seeded and corrected without only using admin.

## Acceptance criteria (EARS)

- **API-BIBLE-AC1:** THE system SHALL expose CRUD at `/api/bible/langs`,
  `/api/bible/versions`, `/api/bible/books`, `/api/bible/translations`, and
  `/api/bible/verses`.
- **API-BIBLE-AC2:** WHEN an unauthenticated client lists versions, THE system
  SHALL return HTTP 200 (`API-ACCESS`).
- **API-BIBLE-AC3:** WHEN a client POSTs a language and a book (with
  `testament` and `number_of_chapters`), THE system SHALL return HTTP 201 for
  each valid create.
- **API-BIBLE-AC4:** WHEN a client filters translations by `version` or by
  `version__abbreviation` and `book__name`, THE system SHALL return matching
  `BookTranslation` rows.
- **API-BIBLE-AC5:** WHEN a client GETs verses with
  `book_translation` and `chapter` (and optionally `verse`), THE system SHALL
  return matching verses.
- **API-BIBLE-AC6:** WHEN a client passes `omit=field1,field2` on translations
  or verses, THE system SHALL omit those keys from the JSON response
  (`DynamicFieldsMixin`).
- **API-BIBLE-AC7:** THE system SHALL enforce unique
  `(version, book, translation)` for book translations and unique
  `(book_translation, chapter, verse)` for verses.
- **API-BIBLE-AC8:** THE system SHALL restrict `testament` to `old` or `new`.

## Out of scope

- Bible OBS dock UX (`OBS-BIBLE`).
- Bible web content-admin UI (does not exist).
- Import pipelines / seeder behavior details (`DEPLOY-LOCAL` notes seeders).

## Constraints

- Open access: `API-ACCESS`. Models: `multimedia/bible/models.py`.
- Related: `OBS-BIBLE`, `WEB-ADMIN`, `TEST-COV`.

## Notes

- Pytest: `multimedia/bible/tests/test_api.py`.
