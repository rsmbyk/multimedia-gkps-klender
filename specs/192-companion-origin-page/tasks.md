# Tasks: The companion's page manages this computer's origins

**Spec**: `specs/192-companion-origin-page/spec.md`
**Plan**: `specs/192-companion-origin-page/plan.md`
**Verification split**: 9 test · 3 inspection · 2 manual

## Phase 1 — Setup

- [x] T001 Confirm the slice worktree carries the spec pack (`specs/192-companion-origin-page/`) and no stray files; `.env` gitignored status unchanged.

## Phase 2 — Foundational (runtime origins store + enforcement)

- [x] T002 [P] [F] failing tests: `multimedia/test_local_media.py` — library origin store (add validates the exact-origin rules, duplicate refused, edit/delete renumber, persisted to the `settings` table and reloaded on a rebuilt library)
- [x] T003 [F] implement `LocalLibrary.recorded_origins()/allowed_origins()/add_origin()/update_origin()/remove_origin()` with in-memory list + `settings` persistence (`multimedia/local_media.py`)
- [x] T004 [P] [F] failing test: `_allowed()` accepts a runtime-recorded origin and the env seeds without a restart; refusal payload names the page and carries no CORS header
- [x] T005 [F] wire `_allowed()`/`_reply` to the runtime set and the new 403 message; drop the frozen `MediaHandler.origins`/`TransferManager.app_origins` capture in favour of the library (both files)

## Phase 3 — US1 (P1) 🎯 MVP: the page is served

**Goal**: with no `.env`, `http://127.0.0.1:63174/` renders with the empty state, the seeds and the fonts.
**Independent test**: spawn the companion with no recorded set; GET `/` returns the page; `GET /v1/origins` returns `{"recorded": [], "seeds": […]}`.

- [x] T006 [P] [US1] failing test: `GET /` serves the page on a loopback Host with an empty recorded set; foreign Host or foreign Origin → 403 (the page's own origin and an absent Origin pass)
- [x] T007 [US1] implement `_config_allowed()` and the `/` route serving `multimedia/companion_page.html` (the file added in this task; self-contained, app design tokens, FR-002's grammar in its JS)
- [x] T008 [P] [US1] failing test: `/v1/origins` GET and `/v1/fonts` GET shapes per `contracts/companion-http.md` (fonts with an injected fake lister)
- [x] T009 [US1] implement the two GET endpoints (fonts: one full `fc-list` pass grouped per mounted directory + operator dir, launcher labels honoured, zero-found said outright)

## Phase 4 — US2 (P2): add / edit / delete on the page

**Goal**: the operator reworks the recorded set from the page; persistence across restarts.
**Independent test**: Playwright drives the served page — add (invalid then valid), edit inline, delete; the set survives a companion restart.

- [x] T010 [P] [US2] failing test: config endpoints POST (400 rule / 409 duplicate / 200), PUT (404 out-of-range), DELETE — through real HTTP
- [x] T011 [US2] implement POST/PUT/DELETE `/v1/origins` (`multimedia/local_media.py`)
- [x] T012 [P] [US2] failing Playwright test: `tests/e2e/test_companion_page.py` — the served page: add (rule named under the form), duplicate refused, inline edit (Confirm/Discard, outside-press discards), delete renumbers, reload shows the persisted set
- [x] T013 [US2] make the Playwright test pass (page JS against the real endpoints; the mock's grammar, production copy)

## Phase 5 — US3 (P2): enforcement + refusal surfacing

**Goal**: only seeds ∪ recorded may use the companion; the web app says why.
**Independent test**: with only staging recorded, a production-origin request is refused with the page-naming payload; the local web app works with nothing recorded.

- [x] T014 [US3] enforcement is covered by T004/T005 — extend the test: local seeds pass with an empty recorded set (`multimedia/test_local_media.py`)
- [x] T015 [US3] `static/web/media-library.js`: keep the failure message and render it in the status popup (template hook if needed); bare `Unavailable` stays when no message

## Phase 6 — US4 (P3): the stack needs no origin configuration

**Goal**: fresh checkout, no `.env`: plain compose and both launchers start everything; no origin anywhere.
**Independent test**: the rewritten compose tests + the launcher harness run without any origin input.

- [x] T016 [P] [US4] failing tests: `tests/test_docker_compose.py` — compose media env is the local seeds only (`:?` guard gone), `.env.example` carries no origin variable, no `GKPS_MEDIA_PRODUCTION_ORIGIN` in compose/`.env.example`/README/the two docs
- [x] T017 [US4] edit `docker-compose.yml` (local seeds only), `.env.example`, `README.md` (first-time section), `docs/local-media-companion.md` (steps 2–3 become: start the stack, open the page; volume note gains the recorded origins), `docs/ARCHITECTURE.md` (allowlist paragraph), the launcher pair stays origin-free (nothing to remove — verify)

## Phase 7 — US5 (P3): fonts view + launcher listing

**Goal**: the page shows what the converter sees; the launcher names what it mounts.
**Independent test**: the launcher harness output carries count + paths (+ labels env); the fonts endpoint test shapes the page rows.

- [x] T018 [P] [US5] failing test: `tests/test_launcher_fonts.py` — `docker/up.sh` with stubbed docker prints the count line, each mounted path, and the zero-found line; the override carries the font source labels
- [x] T019 [US5] implement the font listing (count + indented paths + zero-found) and the `GKPS_MEDIA_FONT_LABELS` env in `docker/up.sh` and `docker/up.ps1` (same transcript in both)
- [x] T020 [US5] the page's fonts section renders `/v1/fonts` (covered by T008/T013; the section is part of the page file from T007)

## Phase 8 — Polish

- [x] T021 Run the full touched suites (`multimedia.test_local_media`, `tests.test_docker_compose`, `tests.test_launcher_fonts`, `tests.e2e.test_companion_page`) green; repo-wide grep: no `GKPS_MEDIA_PRODUCTION_ORIGIN` anywhere
- [x] T022 Docs pass: README first-time flow, `docs/local-media-companion.md` (setup steps, volume note, refusal message), `docs/ARCHITECTURE.md` (runtime allowlist) — consistent with the served page's copy

## Phase 9 — Convergence

Converged 2026-11-14. Capability fold: `media-library` gains R5 (the companion's page: origins,
enforcement, refusal surfacing, fonts view); `local-stack` R1 modified (starts with no `.env`) and
R2 modified (the launcher names what it mounts and passes the on-disk sources as labels). Docs
reconciled: README first-time flow, `docs/local-media-companion.md`, `docs/ARCHITECTURE.md`,
`.env.example`. Checklist 18/18 ticked. Version 1.29.1 → 1.30.0 (minor, per the card's `bump`).
Full touched suites green — 46 companion tests, 10 compose, 3 launcher harness, 1 companion-page
Playwright — plus `tests.e2e.test_media_library` 45/46, the one failure
(`test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`, a 20px vs 12px spacing measurement)
reproducing identically on unmodified `origin/develop` and therefore not this slice's.
