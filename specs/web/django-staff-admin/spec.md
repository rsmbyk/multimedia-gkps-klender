# Spec: WEB-ADMIN — Django staff admin

| Field | Value |
|-------|--------|
| **Spec ID** | `WEB-ADMIN` |
| **Area** | `web` |
| **Status** | `as-built` |
| **Folder** | `specs/web/django-staff-admin/` |

## Problem / goal

Staff maintainers need a login-gated Django admin for domain models (songs,
bible, tatib, bookmarks), especially where no public web content-admin exists
(bible, bookmarks).

## User stories

- **WEB-ADMIN-US1:** As a staff user, I want `/admin/` login, so that anonymous
  visitors cannot use Django admin.
- **WEB-ADMIN-US2:** As a maintainer, I want registered models with search and
  filters, so that I can find and edit content efficiently.
- **WEB-ADMIN-US3:** As a maintainer, I want autocomplete on related fields
  where configured, so that large FK lists stay usable.

## Acceptance criteria (EARS)

- **WEB-ADMIN-AC1:** THE system SHALL serve Django admin at `/admin/`.
- **WEB-ADMIN-AC2:** WHEN an unauthenticated user accesses `/admin/`, THE
  system SHALL require authentication (staff login).
- **WEB-ADMIN-AC3:** THE admin SHALL register songs models: `Language`, `Book`,
  `Song` (list filter `book`; search book/title/number fields), `Verse`
  (filter `song__book`; autocomplete `song`; search lyric + song fields).
- **WEB-ADMIN-AC4:** THE admin SHALL register bible models: `Language`,
  `Version`, `Book`, `BookTranslation` (search `translation`; filter
  `version`), `Verse` (autocomplete `book_translation`; search title/text;
  filter version/book/chapter).
- **WEB-ADMIN-AC5:** THE admin SHALL register tatib models: `TataIbadah`
  (search name; readonly `created_at`; filter `is_active`), `TataIbadahItem`
  (autocomplete tatib; search tatib name/text; filter `item_type`).
- **WEB-ADMIN-AC6:** THE admin SHALL register bookmark models: `SongBookmark`
  (search name; readonly `created_at`), `SongBookmarkItem` (autocomplete
  bookmark+song; search bookmark/song fields; readonly `created_at`).

## Out of scope

- Public web content admin for songs/tatib (`WEB-SONGS`, `WEB-TATIB`).
- Custom admin actions / import-export beyond as-built ModelAdmin config.
- Automated pytest coverage of admin (explicitly out of `TEST-COV`).

## Constraints

- Related: `API-ACCESS` (staff-only exception), domain `API-*` / `SONGS-BM`.
- Admin modules: `multimedia/*/admin.py`.

## Notes

- Bible and bookmarks have no public web CRUD UI — admin (+ OBS/API) is the
  operator path.
