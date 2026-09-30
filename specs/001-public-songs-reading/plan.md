# Plan 001: Public song reading + design foundation

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-001
- **Bump:** minor

## Why

The app was built only as an OBS streaming aid. Its `web/` surface is a CRUD editor on
Fomantic UI defaults, client-side fetching, and almost no custom CSS — so there is no reading
experience worth opening for everyday use. This slice begins the shift the owner asked for:
the website itself becomes worth opening to read the Bible or look up a song, not just to run a
service.

This is the first slice: a shared **design foundation** plus the public **song-reading** path.
The Bible reader and the editor/operator redesigns follow in later specs.

## Scope / edges

**In:**

- A reusable design foundation: a Django base template, a CSS `tokens` layer, and a small
  component set (shell, search, list row, book chip, song header, lyric block, breadcrumb,
  empty/error states).
- A **design language defined from scratch**, drifting off Semantic/Fomantic UI, with a palette
  drawn from the GKPS logo's green and blue (used with restraint). Fomantic library files stay in
  the tree until every surface has migrated.
- Application of the shared glossary and naming conventions ([`docs/GLOSSARY.md`](../GLOSSARY.md)).
- Public, server-rendered song reading: home (search + book list) → book index → song list →
  song lyric page.
- Server-side search over songs (title / book number).
- Routing: public reading at `/` and `/songs/...`; the editor moves to `/manage/...`; legacy
  editor paths redirect.
- Mobile-first, accessible markup and contrast.

**Out:**

- Bible reading (next spec).
- Redesigning the editor or OBS operator screens (they adopt the foundation later).
- Authentication / members-only access — reading is public.
- Offline/PWA, UI translation, and printing beyond a simple print stylesheet.

## Approach

Server-render with the Django ORM; no client fetch on read pages. **Drift away from
Semantic/Fomantic UI toward a design language defined from scratch** — a plain-CSS token and
component system (custom properties; no build step), with a palette drawn from the **green and
blue of the GKPS logo** and used sufficiently but not forced. The Fomantic library files stay in
the tree until every surface has migrated, then are removed. Reuse the existing `songs` models;
keep the DRF API untouched for OBS. New code follows [`docs/GLOSSARY.md`](../GLOSSARY.md).

Routes:

| Path | Serves |
| --- | --- |
| `/` | Public home: search + songbook list |
| `/songs/` | All songbooks (book index) |
| `/songs/book/<book_id>/` | Songs within a book |
| `/songs/<song_id>/` | Song detail (lyrics) |
| `/manage/...` | Editor (moved; legacy paths redirect) |
| `/obs/...` | OBS operator UI (unchanged) |

Legacy editor URLs (`/songs/books`, `/songs/books/<id>`, `/songs/songs/<id>`) redirect to their
`/manage/...` equivalents.

## TDD

- **Domain/app tests:** Django test runner (`python manage.py test`), in
  `multimedia/web/tests.py` — URL resolution, view status/context, search filtering, redirects,
  and template-rendering assertions (content present without JS).
- **E2E:** Playwright (Python) driven from Django `LiveServerTestCase`, run under
  `python manage.py test` (`tests/e2e/`), covering the reading flow in a real browser.

## Risks

- **URL restructure** touches existing editor links and any external references. Covered by
  redirects and tests.
- **Versioning resolved:** `VERSION` is `0.5.2` (highest tag in the repo, shared with the parallel
  `develop` line), so this slice's `minor` bump lands as `0.6.0` with no tag collision.
- **Design-foundation scope creep:** bounded to the components listed in the spec for this slice.
