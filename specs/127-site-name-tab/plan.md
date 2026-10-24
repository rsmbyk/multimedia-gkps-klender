# Implementation Plan: The tab names the site, and the index's tab stops at the name

**Spec**: `specs/127-site-name-tab/spec.md`
**Branch**: `fix/127-site-name-tab`
**Bump**: `patch`
**Preview**: `specs/127-site-name-tab/preview/` — no mockup; the tab is browser chrome, and the note records
why

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 / Django 4.0 (view context + template defaults); vanilla browser JavaScript (ES5 style, no build step) in `static/web/offline-render.js` and `static/web/reading.js` |
| Primary dependencies | none added — string edits only |
| Storage | none — no model, migration, payload or IndexedDB schema change |
| Testing | Django test runner (`multimedia/web/tests.py`); Playwright (Python) E2E for the saved-versus-server parity already in `tests/e2e/` |
| Target platform | browsers served by the reading shell (`/`, `/home/`, `/search`, `/bible/…`, `/songs/…`, `/tatib/…`, `/media-library/`), desktop viewport |
| Project type | server-rendered Django templates with vanilla JS; the saved renderer builds the same page in the browser from the synced library |
| Performance goals | none — the strings are built while the page is already being rendered |
| Constraints | the title is produced by three places (server `<title>`, `offline-render.js`, `reading.js`); they must agree or the tab changes name mid-session, which is what spec 122 fixed for other fields |
| Scale / scope | 12 title strings in one view module, 7 template defaults, 5 browser strings, 1 unit test class extended, 4 E2E assertions updated |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| n/a | n/a | no `CONSTITUTION.md` exists in this repo (checked 2026-10-24) — nothing to check against |

Re-checked after Phase 1: n/a — still no constitution file.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entity, field, relationship, migration or payload changes`
- `contracts/` — `none — the change is the text of an existing response element; it exposes no request, response, event, function or payload contract`
- `quickstart.md` — how to serve the branch and what to read in the browser

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/reading/views.py` (`HomeView`, `SearchView`'s no-query branch), `templates/reading/home.html`, `base.html`'s default, `static/web/offline-render.js` `homePage()` | `test` → `ReadingViewTests::test_the_index_tab_names_the_site_and_stops_there`; `manual` → the same three routes read in a browser | `/` and `/home/` share `HomeView`; `/search` without `q` returns the landing |
| FR-002 | `multimedia/web/reading/views.py` (`SearchView`, `BibleView`, `SongListView`, `SongBookView`, `SongDetailView`, `TatibView`, `media_library`), the six template defaults | `test` → `test_a_section_landing_puts_the_site_name_last`, the updated chapter/song title assertions | one suffix, one rule |
| FR-003 | same files | `test` → the existing per-route title assertions (chapter, song, service labels) | the leading text is untouched by construction — only the suffix changes |
| FR-004 | `static/web/offline-render.js` (`common()`, `homePage()`, `listPage()`, the search results document) | `test` → `tests/e2e/test_saved_render_parity.py` (updated expectation) | saved and server titles compared on every route the class covers |
| FR-005 | `static/web/reading.js` (`syncVisibleBibleTitle`) | `test` → `tests/e2e/test_reading.py`'s edition-switch title assertions (updated) | the tab follows the edition |
| FR-006 | untouched markup: `base.html`'s rail labels and the home logo's `alt`, the search field's label, every heading | `inspection` — `grep -rn "GKPS Klender" multimedia/web/templates` shows only the ones this slice edits as titles | a rename of the visible page would be a different change |
| SC-001 | index routes | `manual` → `quickstart.md` step 2 | exact string, nothing after it |
| SC-002 | every other route | `manual` → `quickstart.md` step 3 | one line per route |
| SC-003 | saved renderer | `test` → the parity regression | equal titles |
| SC-004 | untouched fields | `test` → the full `multimedia.web` suite, re-run unchanged | 43 tests at the last local run |
| US1/AC1–AC6 | views + templates | `test` → the title assertions for chapter, song, service, landings, results, media library | one per route |
| US2/AC1–AC4 | `HomeView`, `IndexView`, maintenance template | `test` → the index test; `inspection` → the maintenance template already carries the name | maintenance is a 503 branch of the same view |
| US3/AC1–AC3 | `offline-render.js`, `reading.js` | `test` → the parity and edition-switch assertions | saved pages are the server page's copy (spec 122) |

**Verification split**: 10 test · 1 inspection · 2 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/127-site-name-tab/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/reading/views.py                  # 12 page_title strings
multimedia/web/templates/reading/base.html       # the <title> default
multimedia/web/templates/reading/*.html          # 6 block-title defaults
static/web/offline-render.js                     # 4 saved-render strings
static/web/reading.js                            # the in-place title update
multimedia/web/tests.py                          # 2 new pins, 3 updated expectations
tests/e2e/test_reading.py                        # 6 updated assertions
tests/e2e/test_offline_library.py                # 1 updated expectation
tests/e2e/test_saved_render_parity.py            # 1 updated expectation
docs/spec/reading.md                             # R1's tab scenario, new R3
specs/README.md                                  # the spec index row
backlog/items/ITEM-129-site-name-tab.md  backlog/board.md
VERSION  CHANGELOG.md                            # patch bump
```

### Structure Decision

No new module, template, CSS, asset or fixture: the slice replaces the site-name token in strings that
already exist, and pins the two shapes — index alone, every other page appended — where the titles are
already asserted.
