# Spec: APP — Multimedia GKPS Klender (product overview)

| Field | Value |
|-------|--------|
| **Spec ID** | `APP` |
| **Area** | `app` |
| **Status** | `as-built` |
| **Folder** | `specs/app/` |

## Problem / goal

The multimedia team at **GKPS Klender** (Gereja Kristen Protestan Simalungun)
prepares worship content and projects it live with **OBS**. This application is
the single product that stores hymn/bible/tatib content, exposes it over a REST
API, provides browser content-admin UIs, and ships OBS browser docks/sources for
live projection.

This document is the **full app spec**: product intent, surfaces, domains, and
a registry of feature specs. Detailed EARS live in the feature specs below.

## User stories

- **APP-US1:** As a multimedia operator, I want to manage songs, bible passages,
  and tata ibadah in one app, so that worship content is ready before service.
- **APP-US2:** As an OBS operator, I want docks and sources for songs, bible,
  tatib, and a combined project view, so that I can control live projection.
- **APP-US3:** As a developer, I want living specs with stable IDs for each
  capability, so that changes stay anchored to agreed intent.

## Acceptance criteria (EARS)

### Product surfaces

- **APP-AC1:** THE system SHALL expose a REST API under `/api/` for songs,
  bible, tatib, song bookmarks, and song lyric search.
- **APP-AC2:** THE system SHALL expose OBS browser docks and sources under
  `/obs/` for songs, bible, tatib, and project (plus project settings).
- **APP-AC3:** THE system SHALL expose a public web content-admin UI for songs
  and tata ibadah (hub at `/`).
- **APP-AC4:** THE system SHALL expose Django staff admin at `/admin/` for
  domain models (staff login required).
- **APP-AC5:** WHILE product API and content-admin UIs are in use, THE system
  SHALL NOT require end-user login (see `API-ACCESS`). Staff auth applies only
  to `/admin/`.

### Domains

- **APP-AC6:** THE system SHALL persist hymn books, songs, and verses (songs
  domain) and serve them to web and OBS clients.
- **APP-AC7:** THE system SHALL persist bible languages, versions, books,
  translations, and verses and serve them to OBS (and API) clients.
- **APP-AC8:** THE system SHALL persist tata ibadah documents and ordered items
  (TEXT and END_OF_SECTION) and serve them to web and OBS clients.
- **APP-AC9:** THE system SHALL persist song bookmarks (setlists) and ordered
  bookmark items for OBS Songs workflows.
- **APP-AC10:** THE project OBS source SHALL combine songs, bible, and tatib
  BroadcastChannel feeds into one projection surface (`OBS-PROJECT`).

### Process and runtime

- **APP-AC11:** THE project SHALL keep a feature registry of Spec IDs under
  `specs/` and update it when capabilities are added or retired.
- **APP-AC12:** Production hosting SHALL follow `DEPLOY-VERCEL` /
  [`docs/DEPLOY.md`](../../docs/DEPLOY.md); local app runtime SHALL follow
  `DEPLOY-LOCAL` (Docker Compose).
- **APP-AC13:** THE product SHALL expose a single SemVer via
  `multimedia/obs/static/obs/common/version.js` (`APP_VERSION`); OBS docks and
  project settings SHALL display that value through `data-app-version` nodes
  (see [`docs/VERSIONING.md`](../../docs/VERSIONING.md)).

## Feature registry

| Spec ID | Path | Summary |
|---------|------|---------|
| `API-ACCESS` | [`../api/open-access-policy/`](../api/open-access-policy/) | Open product API / web access policy |
| `API-SONGS` | [`../api/songs-content/`](../api/songs-content/) | Songs REST content |
| `API-BIBLE` | [`../api/bible-content/`](../api/bible-content/) | Bible REST content |
| `API-TATIB` | [`../api/tatib-content/`](../api/tatib-content/) | Tatib REST content |
| `API-SEARCH` | [`../api/song-search/`](../api/song-search/) | Song lyric search |
| `SONGS-BM` | [`../songs/song-bookmarks/`](../songs/song-bookmarks/) | Song bookmarks / setlists |
| `OBS-SONGS` | [`../songs/obs-songs-live/`](../songs/obs-songs-live/) | OBS Songs dock + source |
| `OBS-BIBLE` | [`../bible/obs-bible-live/`](../bible/obs-bible-live/) | OBS Bible dock + source |
| `OBS-TATIB` | [`../tatib/obs-tatib-live/`](../tatib/obs-tatib-live/) | OBS Tatib dock + source |
| `OBS-PROJECT` | [`../project/obs-project-projection/`](../project/obs-project-projection/) | Combined OBS projection |
| `WEB-SONGS` | [`../web/songs-content-admin/`](../web/songs-content-admin/) | Web songs admin |
| `WEB-TATIB` | [`../web/tatib-content-admin/`](../web/tatib-content-admin/) | Web tatib admin |
| `WEB-ADMIN` | [`../web/django-staff-admin/`](../web/django-staff-admin/) | Django staff admin |
| `DEPLOY-VERCEL` | [`../deploy/vercel-production/`](../deploy/vercel-production/) | Vercel production |
| `DEPLOY-LOCAL` | [`../deploy/local-compose-runtime/`](../deploy/local-compose-runtime/) | Local Compose runtime |
| `DOCS-SDD` | [`../docs/sdd-adoption/`](../docs/sdd-adoption/) | SDD adoption |
| `TEST-COV` | [`../test/current-coverage/`](../test/current-coverage/) | Test coverage program |

## Out of scope

- Per-plugin versioning (superseded by single SemVer — see
  [`docs/VERSIONING.md`](../../docs/VERSIONING.md)).
- End-user authentication for product API / content admin (intentionally open;
  see `API-ACCESS`).
- Bible or bookmarks browser content-admin UIs (not built; use OBS + `/admin/`).
- Hosting migrations away from Vercel (separate spike).

## Constraints

- Follow [`specs/constitution.md`](../constitution.md) and linked docs.
- Stack: Django 4, DRF, PostgreSQL, WhiteNoise, ES modules + Semantic UI /
  jQuery for OBS and web pages.
- Changelog area labels: [`docs/VERSIONING.md`](../../docs/VERSIONING.md).

## Notes

- Product README surfaces table: [`README.md`](../../README.md).
- This backfill documents **as-built** behavior; future changes update the
  relevant feature spec first, then code/tests.
