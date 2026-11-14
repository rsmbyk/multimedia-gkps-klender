# Implementation Plan: Retired Addresses

**Spec**: `specs/193-legacy-route-retirement/spec.md` (Accepted, Gate 1 2026-11-14)
**Branch**: `feat/193-legacy-route-retirement`
**Bump**: `minor` (1.30.0 → 1.31.0; D009 — the repo's own precedent for a route removal, shown at
Gate 2)
**Preview**: `specs/193-legacy-route-retirement/preview/index.html` — `/obs/blank`'s exact body
(`preview/blank.html`) in a checkerboard, a dark stage and a bright slide

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; Django 4.0 URLconfs (`path`, `re_path`, `RedirectView`, one function view) |
| Existing patterns | `/obs/dock` and `/obs/source/overlay` are hand-written patterns in `multimedia/urls.py`; `multimedia/obs/urls.py` is a four-line `include`; `/search/` → `/search` is the repo's one existing `RedirectView`; `web-home` is the name being dropped |
| Primary dependencies | Django `RedirectView` (`permanent=False`, `query_string=True`); no new package |
| Storage | none — no model, no migration, no stored mapping |
| Testing | Django `TestCase` in `multimedia/web/tests.py` (replacing `LegacyObsRouteCompatibilityTests`); Playwright E2E in `tests/e2e/test_retired_routes.py` (`StaticLiveServerTestCase`, `skipUnless(HAS_PLAYWRIGHT)`) |
| Target platform | the site on Vercel (`DEBUG = False`, `APPEND_SLASH` on) and OBS's embedded Chromium as a browser source |
| Project type | server-rendered Django web app; no build step |
| Performance goals | each retired address costs one URL resolution and one `HttpResponseRedirect` — no query, no template; `/obs/blank` is one small inline-styled document with `Cache-Control: no-store` |
| Constraints | `APPEND_SLASH` is on (`multimedia/settings.py:70`), so both slash forms must be registered or the extra hop is a 301; `MAINTENANCE_MODE` must not affect `/home/`; no live template reverses a `/manage/` name; 76 `reverse('web-home')` call sites must move with the name |
| Scale / scope | 9 exact addresses + the `/manage/` prefix + the `/archive/` namespace + 1 new page; 2 URLconfs and 1 new module |

## Constitution Check

No `CONSTITUTION.md` exists in this repository, so there are no principles to check against (SDD-01
makes it optional and it is never auto-created). Run before Phase 0 — nothing to check.
Re-checked after Phase 1: unchanged, still nothing to check.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Ten decisions: the one table (D001), the uniform 302
(D002), both slash forms (D003), the `/manage/` prefix (D004), `/obs/blank`'s home (D005), the
archive rule (D006), the FR-011 correction (D007), the test split (D008), the bump (D009) and the
verification split (D010).

## Phase 1 — Design

- `data-model.md` — explicitly none: no entities, no stored state.
- `contracts/routes.md` — the one external interface this slice changes: address → status →
  destination, with the query-string and one-hop rules.
- `quickstart.md` — the suite and the `curl` loop that demonstrates every traceability row.

### Design notes

- **One module, one mapping.** `multimedia/retirement.py` holds `RETIRED` (old path without its
  edges, successor; 302), `LEGACY` (three regexes, successor template; 301), the `manage` prefix
  rule, `successor()`, `redirect()`, `routes(prefix)`, `legacy_routes()` and the `archive` view.
  `archive()` unquotes its tail before `successor()`, and `successor()` answers `/` for a path
  carrying a backslash: Chromium reads `/\evil.example` as `//evil.example`, so an archive address
  must never be able to name another host.
  `multimedia/obs/urls.py` and `multimedia/web/urls.py` build their patterns from `routes()` and
  `legacy_routes()`, and `successor()` reads the same two tuples, so the direct route, the legacy
  301s and `/archive/…` cannot disagree; a reviewer reads one module to know the whole retirement.
  Each consumer carries one marked `spec 193` block (FR-010).
- **`obs/urls.py` keeps its mount.** It stays `path('obs/', include('multimedia.obs.urls'))` in the
  root URLconf and becomes a single `retirement.routes('obs')` call, so the `/obs/` retirements are
  one block in the URLconf a reader expects. `/obs/blank` is **not** registered here: it is a live
  surface that outlives the retirement and sits beside `/obs/dock` in `multimedia/urls.py` (D005).
- **`web/urls.py` loses two statements and gains one block.** `path('home/', …)` and
  `path('manage/', include(…))` become `*retirement.routes()`; the `web-home` name disappears and
  its 76 call sites become `web-index`. The `multimedia/web/manage/` package stays in the tree,
  unreachable (spec Assumption).
- **The three legacy `/songs/books*` redirects keep 301 and change targets** (FR-011): they move
  from `RedirectView(pattern_name=…)` lines into `retirement.LEGACY`, a `(regex, destination
  template)` pair each, built by `legacy_routes()` and answered by a three-line
  `HttpResponsePermanentRedirect` view. Their old targets were `/manage/` routes, which this
  release retires; their new ones are `/songs/`, `/songs/book/<id>/`, `/songs/<id>/`. The URL text
  does not change, and `successor()` applies the same regexes so the archive never chains into
  one of them.
- **`/archive/` is one root route** — `re_path(r'^archive(?:/(?P<rest>.*))?$', retirement.archive)`
  — beside `/obs/blank`, both in `multimedia/urls.py` before the two includes. The view strips the
  prefix, calls `successor()`, keeps the query string and answers `HttpResponseRedirect`.
- **The note is one fixed div and one `<style>` in `multimedia/web/templates/reading/obs_blank.html`**,
  reproducing `preview/blank.html` exactly: system-ui 12px/1.4 at 500, `rgba(255,255,255,.2)` and a
  `0 1px 2px rgba(0,0,0,.55)` shadow at rest; on hover `rgba(255,255,255,.95)` on
  `rgba(20,20,18,.82)`, 5px/9px padding, 6px radius, and the anchor revealed. No `{% static %}`, no
  shared stylesheet, no font, no image, no script (FR-006b) — a browser source that cannot load a
  stylesheet still paints the note.
- **`Cache-Control: no-store`** is set in the view, not the template, so it holds whichever template
  engine renders it.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/retirement.py`, `multimedia/web/urls.py` | `test` → `multimedia/web/tests.py::RetiredWebRouteTests::test_home_answers_302_to_the_root` | `/home` and `/home/`; `?from=mail` kept |
| FR-002 | `multimedia/retirement.py`, `multimedia/web/urls.py` | `test` → `RetiredWebRouteTests::test_every_manage_address_answers_302_to_the_root` | `/manage`, `/manage/`, `/manage/songs/`, `/manage/songs/12/` |
| FR-003 | `multimedia/retirement.py`, `multimedia/obs/urls.py` | `test` → `RetiredWebRouteTests::test_each_old_dock_answers_302_to_the_one_dock` | 3 docks × 2 slash forms |
| FR-004 | `multimedia/retirement.py`, `multimedia/obs/urls.py` | `test` → `RetiredWebRouteTests::test_each_old_source_answers_302_to_the_blank_page` | 4 sources × 2 slash forms |
| FR-005 | `multimedia/retirement.py`, `multimedia/obs/urls.py` | `test` → `RetiredWebRouteTests::test_the_old_settings_page_answers_302_to_the_root` | both slash forms |
| FR-006 | `multimedia/urls.py`, `multimedia/web/reading/views.py`, `…/templates/reading/obs_blank.html` | `test` → `RetiredWebRouteTests::test_the_blank_page_is_transparent_and_uncached` | 200, `no-store`, transparent `html`/`body` |
| FR-006a, US1 / AC3 (hover) | `…/templates/reading/obs_blank.html` | `test` → `tests/e2e/test_retired_routes.py::RetiredRoutesE2ETests::test_the_note_is_a_watermark_until_hovered` | computed colour at rest and on hover; anchor hidden → visible |
| FR-006b | `…/templates/reading/obs_blank.html` | `test` → `RetiredWebRouteTests::test_the_blank_page_paints_only_the_note` | 0 `<script`, 0 `<img`, 0 `<link`; only the note's two strings |
| FR-007 | `multimedia/web/urls.py` (reading routes unchanged) | `test` → `RetiredWebRouteTests::test_the_reading_addresses_keep_their_answers` | `/songs/`, `/songs/<song>/`, `/tatib/`, `/tatib/<service>/` → 200 |
| FR-008 | `multimedia/retirement.py::archive`, `multimedia/urls.py` | `test` → `RetiredWebRouteTests::test_the_archive_answers_the_successor_in_one_hop` | `/archive/`, `/archive/home/`, `/archive/manage/songs/12/`, `/archive/songs/`, `/archive/songs/books`, `/archive/obs/songs/source`, `/archive/nowhere/` |
| FR-009 | every redirect above, `permanent=False` | `test` → `RetiredWebRouteTests::test_no_retired_or_archived_address_answers_301` | reads the whole table, not a hand-picked list |
| FR-010 | the `spec 193` blocks in `retirement.py`, `obs/urls.py`, `web/urls.py`, `multimedia/urls.py` | `inspection` — `grep -rn 'spec 193' multimedia`; read the four blocks and name what the next release deletes | no test can prove a deletion surface |
| FR-011 | `multimedia/retirement.py::LEGACY`, `multimedia/web/urls.py` | `test` → `RetiredWebRouteTests::test_the_legacy_song_lists_redirect_to_the_reading_pages` | 301 kept; one hop to `/songs/`, `/songs/book/<id>/`, `/songs/<id>/` |
| US1 / AC1–2, AC4 | `retirement.py`, `obs/urls.py` | `test` → the three dock/source/settings tests above, plus `test_no_old_obs_address_renders_a_page` | 7 of 7 old addresses; no old template in any body |
| US1 / AC3 (legibility) | `preview/index.html` | `inspection` — read the dark and the bright frame; the 20% line is a hint on the dark stage and disappears into the white slide | the trade the owner chose; judged by eye, not by a computed colour |
| US2 / AC1–3 | `retirement.py`, `web/urls.py` | `test` → the `/home/` and `/manage/` tests, plus `test_the_reading_addresses_keep_their_answers` | maintenance switch does not change `/home/` |
| US2 / AC4 | `static/web/editors.js:318-322` | `inspection` — read the two return addresses; neither passes through `/manage/` or `web-home` | no code change; the file already returns to `/songs/` and `/tatib/` |
| US3 / AC1–6 | `retirement.py::archive`, `multimedia/urls.py` | `test` → `test_the_archive_answers_the_successor_in_one_hop` (AC1–5) and `test_no_retired_or_archived_address_answers_301` (AC6) | one hop by construction: `successor()` computes, never follows |
| SC-001 | `multimedia/retirement.py` | `test` → `test_no_old_obs_address_renders_a_page` | 7 of 7 answer 302; 0 render |
| SC-002 | `obs_blank.html` | `test` → `test_the_blank_page_paints_only_the_note` and the E2E note test | one visible text node at rest, 0 script, 0 img, transparent |
| SC-003 | `web/urls.py` | `test` → `test_the_reading_addresses_keep_their_answers` | 4 of 4 answer 200 |
| SC-004 | `retirement.py` | `test` → `test_every_retired_location_resolves_to_a_200` | each `Location` fetched once; 0 chains |
| SC-005 | `retirement.py` | `test` → `test_no_retired_or_archived_address_answers_301` | 0 of the retired and archived answers are 301 |
| US1 on air | an OBS scene holding an old source | `manual` — load each retired source in OBS and watch the program out | no runner watches a stream |
| Production smoke | the deployed site | `manual` — after the release, open `/home/`, `/manage/songs/` and `/obs/bible/source` against production; each lands on the address `contracts/routes.md` names | the Vercel URL is not in the checkout; the owner supplies it |

**Verification split**: 20 test · 3 inspection · 2 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| None — no `CONSTITUTION.md` | — | — |

## Project Structure

### Documentation

```
specs/193-legacy-route-retirement/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/routes.md  checklists/requirements.md  preview/{index,blank}.html
```

### Source

```
multimedia/retirement.py                     new — the table, successor(), redirect(), archive()
multimedia/urls.py                           /obs/blank and /archive/ beside /obs/dock
multimedia/obs/urls.py                       becomes one retirement block
multimedia/web/urls.py                       drops home/ and the manage include; FR-011 targets
multimedia/web/reading/views.py              obs_blank()
multimedia/web/templates/reading/obs_blank.html   new
multimedia/web/tests.py                      RetiredWebRouteTests replaces the legacy class
tests/e2e/test_retired_routes.py             new
static/web/editors.js                        unchanged (inspected)
docs/spec/routing.md                         new at Fold
```

### Structure Decision

`multimedia/retirement.py` sits beside the URLconfs it feeds, not inside `multimedia/obs/` or
`multimedia/web/`: it is read by both, and it is the one file the next release deletes. The blank
page's view and template live with the other OBS surfaces (`multimedia/web/reading/`), which is
where `/obs/dock` and `/obs/source/overlay` already are — that is why it survives the retirement's
deletion. The E2E module lives in `tests/e2e/` with every other browser test; the Django tests stay
in the app's own `tests.py` (repo: tdd, "Location").
