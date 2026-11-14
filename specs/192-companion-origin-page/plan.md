# Implementation Plan: The companion's page manages this computer's origins

**Spec**: `specs/192-companion-origin-page/spec.md`
**Branch**: `feat/192-companion-origin-page`
**Bump**: `minor` — a new operator capability: the companion's configuration page (VER-10; from
1.29.1 → 1.30.0, applied in the delivery commit per VER-04)
**Preview**: `specs/192-companion-origin-page/preview/` — functional page mock; accepted at Gate 1

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0 (tests), stdlib `http.server` for the companion |
| Primary dependencies | none added — fontconfig (`fc-list`) already ships in the media image |
| Storage | `index.sqlite3` `settings` table (existing) — key `origins`, JSON array (D001) |
| Testing | Django test runner (`manage.py test`); companion exercised through real HTTP against a spawned server; Playwright (Python) drives the served page; a PATH-stubbed `docker` drives `up.sh` |
| Target platform | the operator's Docker Compose stack (Windows/macOS/Linux launchers; the OBS laptop is the reference machine) |
| Project type | Django monorepo with a stdlib-HTTP local companion service |
| Performance goals | none new — the enforcement check is an in-memory set membership per request |
| Constraints | the companion serves loopback only; no new dependencies; the page must work with an empty recorded set; `.env` loses its required variable |
| Scale / scope | one page, five config endpoints, an enforcement change, compose/docs/test cleanup, launcher font listing |

## Constitution Check

`CONSTITUTION.md` does not exist in this repository (SDD-01: optional, never auto-created) —
nothing to check against. Re-checked after Phase 1: n/a.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the recorded origin set, the read-only local seeds, the computed fonts view
- `contracts/companion-http.md` — page + config endpoints + refusal payload + web surfacing
- `quickstart.md` — run the tests, start the stack, open the page

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 page served always | `multimedia/local_media.py` (`do_GET '/'`), `multimedia/companion_page.html` | `test` → `multimedia/test_local_media.py::test_page_served_with_empty_recorded_set` | Host loopback, no Origin needed |
| FR-001 shows recorded/seeds/fonts | page JS (`companion_page.html`) + `GET /v1/origins`, `GET /v1/fonts` | `test` → `multimedia/test_local_media.py::test_page_endpoints_shape` | endpoint shapes per contract |
| FR-002 add/edit/delete + validation | `LocalLibrary` origin methods + `/v1/origins` POST/PUT/DELETE | `test` → `multimedia/test_local_media.py::test_origin_add_validates`, `…::test_origin_edit_delete_renumbers`, `…::test_origin_duplicate_refused`, `…::test_origins_persist_across_restart` | persistence = restart of the library object on the same root |
| FR-002 page CRUD drives it | `companion_page.html` JS | `test` → `tests/e2e/test_companion_page.py` (Playwright against the spawned companion) | add/edit/delete through the real page |
| FR-003 per-request enforcement | `MediaHandler._allowed()` + `LocalLibrary.allowed_origins()` | `test` → `multimedia/test_local_media.py::test_enforcement_sees_recorded_set_without_restart` | recorded set added at runtime passes immediately |
| FR-003 refusal names the page | 403 payload in `_reply`/`do_OPTIONS`/`do_GET`/`do_POST`/`do_DELETE` | `test` → `multimedia/test_local_media.py::test_refused_request_names_the_page` | payload text + no CORS header |
| FR-004 config auth | `_config_allowed()` | `test` → `multimedia/test_local_media.py::test_config_surface_host_and_origin_rules` | loopback Host; absent/own Origin; no token; foreign Host refused |
| FR-005 fonts view | `GET /v1/fonts` (fc-list per directory) + page section | `test` → `multimedia/test_local_media.py::test_fonts_view_lists_directories_and_counts` (injected fake lister) · `inspection` — the page section renders the payload rows | zero-found said outright |
| FR-006 no origin configuration at start | `docker-compose.yml`, `.env.example`, `README.md`, `docs/local-media-companion.md`, `docs/ARCHITECTURE.md` | `test` → `tests/test_docker_compose.py::test_media_companion_allowlist_uses_local_seeds_only`, `…::test_env_example_carries_no_origin_variable`, `…::test_no_operator_origin_variable_remains` | rewritten from today's guard tests |
| FR-006 launchers origin-free | `docker/up.sh`, `docker/up.ps1` | `inspection` — neither script reads or prompts for any origin variable | they never did; the slice adds none |
| FR-007 launcher names mounted dirs | `docker/up.sh` (count + paths + zero-found), `docker/up.ps1` (same) | `test` → `tests/test_launcher_fonts.py` (subprocess, PATH-stubbed docker) · `inspection` — the PowerShell twin carries the same lines | spec 182's skip naming stays |
| FR-008 web surfaces the reason | `static/web/media-library.js` (`refresh`/`setStatus`), media library template | `inspection` — the failure path stores the payload message and the popup renders it · `manual` — on the obs laptop: unrecorded origin → the picker's status shows the refusal line | the manual row is the acceptance evidence the spec names |
| SC-001 fresh computer to working setup | composed run | `manual` — fresh checkout without `.env`: stack starts, page renders empty, one added origin lets the production picker connect | the OBS laptop scenario |
| SC-002 set survives restarts | `LocalLibrary` persistence | `test` → `…::test_origins_persist_across_restart` (rebuild the library object on the same root) | |
| SC-003 boundary + explanation | enforcement + payload | covered by the FR-003 rows | |
| SC-004 stored origins exact | `parse_allowed_origins` on the stored list | covered by the FR-002 rows (validation) | |
| SC-005 rename completion | repo-wide | superseded — the variable is removed entirely; verified by the FR-006 tests | |
| SC-006 no origin config at start | compose + launchers | covered by the FR-006 rows | |
| SC-007 launcher names what it mounts | launchers | covered by the FR-007 rows | |
| US1/AC1–3 | as FR-001 | | |
| US2/AC1–5 | as FR-002 | | |
| US3/AC1–4 | as FR-003, FR-008 | | |
| US4/AC1–3 | as FR-006, FR-007 | | |
| US5/AC1–3 | as FR-005 | | |

**Verification split**: 9 test · 3 inspection · 2 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| (none) | | |

## Project Structure

### Documentation

```
specs/192-companion-origin-page/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/companion-http.md  checklists/requirements.md  preview/
```

### Source

```
multimedia/local_media.py          # page route, config endpoints, runtime enforcement, refusal payload
multimedia/companion_page.html     # the configuration page (new)
multimedia/test_local_media.py     # companion tests (new cases)
static/web/media-library.js        # refusal surfacing in the status popup
static/styles/design/components.css  # (only if the popup reason needs a style hook)
docker-compose.yml                 # local seeds only; guard removed
docker/up.sh  docker/up.ps1        # font listing + font source labels
.env.example  README.md  docs/local-media-companion.md  docs/ARCHITECTURE.md
tests/test_docker_compose.py       # rewritten origin assertions
tests/test_launcher_fonts.py       # new launcher harness
tests/e2e/test_companion_page.py   # new Playwright page test
```

### Structure Decision

The page lives in the `multimedia` package (not `static/`): the companion container bakes the
package and must serve the page without the Django static pipeline, and one file keeps the page
self-contained. The origin store lives on `LocalLibrary` because both consumers (handler,
transfer manager) already hold it.
