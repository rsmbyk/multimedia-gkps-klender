# Implementation Plan: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md` (Accepted, Gate 1 2026-11-19)
**Branch**: `fix/204-dock-entry-open-reset`
**Bump**: `patch` — a defect in shipped behaviour, no new capability, no interface or model change
(declared here for Gate 2; applied pre-merge per VER-04 against the base's `VERSION` at delivery —
`1.34.4` at the branch base `ab46f384`, so `1.34.5` unless a sibling lands first; `CHANGELOG.md`
`[Unreleased]` line in the same commit).
**Preview**: static at `specs/204-dock-entry-open-reset/preview/index.html` — the Gate-1 preview,
the product's own markup, CSS and dock script (byte-identical but for the three drafted lines)
running on five captured services; every state reachable by hand, both behaviours on one page.
The design below follows what was approved.
**Branch base**: `ab46f384` (`origin/develop`, 2026-11-19). The branch was cut at `85319b73` and
fast-forwarded to `ab46f384` before Implement, with no commits of its own: specs 203 (long-word
wrap, `obs-dock.css`) and 205 (re-centring pace, `obs-dock.js`) landed in between, so every line
citation below was re-read against the new tip and the preview's assets re-copied from it. Spec
200's `following` mode and `centreOnOpen` are in the base and are untouched here.
**Card renumber**: the card was drafted as `ITEM-213`; spec 203 landed that ID on `develop` while
this pack was in review, and 214/215 are taken (205's card and a known-red card). The card is now
**`ITEM-216`**, renumbered before the first commit, and every reference in the pack follows it.

## Technical Context

| Field | Value |
| --- | --- |
| Language / stack | Python 3.12, Django 4.0, DRF; server-rendered `reading/obs_dock.html`; vanilla JS `static/web/obs-dock.js`; design CSS `obs-dock.css` + `tokens.css` (neither stylesheet changes) |
| Surfaces | `obs-dock.js`: `entryOverrides` L101, `openService` L418-439 (the reset's home; `replaceChildren` L435, `loadServiceData` L438), its three call sites L392 (`openCursorRow`, picker `Enter`), L1438 (picker click), L2031 (`resumeOnAir`); `loadServiceData` L442-466 and `refreshService` L472-476 and the 10 s timer L2020-2024 (the re-read paths, untouched); `liveEntry` L543, `effectiveOpen` L556-559, `effectiveOpenFor` L563; `toggleBlock` L856-860 (`entryOverrides.set` L861); `renderList` L321, `sync` L1298-1434; `startToggleMorph` L817, `finishToggleMorph` L845 |
| Existing patterns | the page-memory `Map` idiom; one effective-state question read by three painters (crossing settle, `sync` repaint, hand toggle); `openService` as the single explicit-open path; the targeted E2E module shape of `test_obs_dock_follow.py` |
| Storage | none new — `entryOverrides` stays a page-memory `Map`; `gkps-display`, `localStorage`, cookies and the server untouched |
| Testing | Django runner; Playwright (Python) E2E under `tests/e2e/`, tag `e2e`; red-first per TDD against the base `ab46f384`; the preview's three probes as the gate-1 measurement lane |
| Target platform | the dock in OBS's browser source, and any Chromium/Firefox/Safari the operator opens it in |
| Performance goals | none new — one `Map.clear()` per explicit open; no fetch, no layout, no animation added |
| Constraints | the live entry's block stays open (FR-002); crossings keep hand-opened blocks (spec 198 R14); re-reads keep them and land where the operator is (spec 195 R13); an open writes no display state and broadcasts nothing (FR-005); no persistence (FR-006); no new control, copy, colour or motion (A4) |
| Scale / scope | one statement in one script (+ its comment), one new E2E module (~10 tests), two existing modules re-run unchanged, the capability delta in `docs/spec/dock.md`, the card and board row, `VERSION` + changelog at delivery |

## Constitution Check

`CONSTITUTION.md` is absent — SDD-01 makes it optional and never auto-created. The check runs
against the binding constraints the capability specs and `docs/PROCESS.md` impose.

| Constraint | Status | Note |
| --- | --- | --- |
| The display state never reaches the server, and an open writes nothing | pass | the reset touches one in-page `Map`; measured byte-identical state and 0 channel messages across 10 opens |
| A re-read lands where the operator is (`dock/R13`) | pass | the clear sits in `openService`, which no re-read path calls; a hand-opened block survives the `update` message and the timer (measured `[0, 6, 9]` before and after) |
| A hand-opened block survives a crossing (`dock/R14`) | pass | the crossing never opens a service; spec 198's own test is re-run unchanged |
| The live entry is locked open and chevronless (`dock/R14`) | pass | `effectiveOpen` asks `liveEntry()` first, so the clear cannot reach it; measured open, tinted, no chevron |
| No framework, no new dependency | pass | one statement of hand-written JS; no CSS, template or model change |
| Existing accepted numbers undisturbed | pass | row metrics, the 230/400 ms morphs, spec 200's centring and the fluid width all keep their rules |
| Names in repo artifacts | pass | roles only throughout the pack |
| One behaviour truth | pass | the dock's own page is the truth; the preview is static and says what it stubs |
| GIT-06 / GIT-07, VER-03 / VER-04 | pass | nothing committed before Fold; nothing pushed without the owner's word; the patch bump is declared here and applied pre-merge |

Re-checked after Phase 1: pass — Phase 1 added no constraint and changed no row above; the design
is one statement plus a test module, and `contracts/` is `none`.

## Phase 0 — Research

See `research.md` (D001–D008). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no model changes; the override map's lifetime is the only state that moves, and
  the effective-open question is unchanged.
- `contracts/` — **none** (client-only; no endpoint, channel verb, storage key or DOM contract
  changes — stated in `contracts/README.md`).
- `quickstart.md` — the throwaway-database test lane, the preview's three probes, the eight manual
  checks, and what is not yet runnable.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/obs-dock.js` `openService` L418 | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_an_open_starts_every_block_shut_in_another_service` | the clear precedes `replaceChildren` and the load |
| FR-002 | `obs-dock.js` `liveEntry` L543 / `effectiveOpen` L556 (unchanged) | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_the_live_entrys_block_stays_open_when_its_service_is_opened` | open, `aria-current`, no chevron |
| FR-003 (picker click) | `obs-dock.js` L1438 → `openService` | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_an_open_starts_every_block_shut_in_another_service` | the same test drives a click |
| FR-003 (picker `Enter`) | `obs-dock.js` `openCursorRow` L392 | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_the_keyboard_open_resets_like_a_click` | preview evidence: `measurements-enter.json` |
| FR-003 (on-load resume) | `obs-dock.js` `resumeOnAir` L2031 | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_the_on_load_open_keeps_only_the_live_block` | reload with a service on air |
| FR-003 (not a re-read) | `obs-dock.js` `refreshService` L472, timer L2020 (untouched) | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_a_reread_keeps_a_hand_opened_block_open` | the `update` channel message |
| FR-004 | `obs-dock.js` `sync` L1351-1419 (unchanged) | `test` → `tests/e2e/test_obs_dock.py::ObsDockE2ETests::test_open_blocks_survive_crossings_and_forget_on_reload` | existing pin, re-run unchanged |
| FR-005 (no write) | `obs-dock.js` `openService` | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_an_open_writes_no_display_state_and_broadcasts_nothing` | raw bytes + channel listener |
| FR-005 (no motion) | `obs-dock.js` `renderList` L321 / `sync` L1372 | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_an_open_paints_no_morph_in_the_new_list` | rAF sample of `.is-morph` and `scrollTop` |
| FR-006 (page memory) | `obs-dock.js` `entryOverrides` L101 | `test` → `tests/e2e/test_obs_dock.py::ObsDockE2ETests::test_open_blocks_survive_crossings_and_forget_on_reload` | the reload half of the existing pin |
| FR-006 (no new storage) | the slice's diff | `inspection` — the diff adds one `Map.clear()` and a comment; no `localStorage`, `sessionStorage`, cookie or endpoint appears in it | grep the diff for storage APIs |
| SC-001 | `tests/e2e/test_dock_open_reset.py` | `test` → `DockOpenResetE2ETests::test_an_open_starts_every_block_shut_in_another_service` | non-live open count 0 (base: 1) |
| SC-002 | `tests/e2e/test_dock_open_reset.py` | `test` → `DockOpenResetE2ETests::test_reopening_the_same_service_starts_every_block_shut` | base: 1 |
| SC-003 | `tests/e2e/test_dock_open_reset.py` | `test` → `DockOpenResetE2ETests::test_several_hand_opened_blocks_leak_nothing_into_a_shorter_service` | base: `[1, 3]` |
| SC-004 | `tests/e2e/test_dock_open_reset.py` | `test` → `DockOpenResetE2ETests::test_the_live_entrys_block_stays_open_when_its_service_is_opened` | height > 0, chevron count 0 |
| SC-005 | `tests/e2e/test_dock_open_reset.py` + `tests/e2e/test_obs_dock.py` | `test` → `DockOpenResetE2ETests::test_a_reread_keeps_a_hand_opened_block_open` and `ObsDockE2ETests::test_open_blocks_survive_crossings_and_forget_on_reload` | one test per event |
| SC-006 | `tests/e2e/test_dock_open_reset.py` | `test` → `DockOpenResetE2ETests::test_an_open_writes_no_display_state_and_broadcasts_nothing` and `::test_an_open_paints_no_morph_in_the_new_list` | preview: 10 opens, 0 messages, 0 morph frames |
| SC-007 | the six dock modules | `test` → `manage.py test tests.e2e.test_dock_open_reset tests.e2e.test_obs_dock tests.e2e.test_obs_dock_follow tests.e2e.test_dock_keys tests.e2e.test_dock_goto tests.e2e.test_dock_bucket_head multimedia.web.test_obs_dock --keepdb` | red-first on the base; a base-identical red is carded |
| US1/AC1 | `obs-dock.js` `openService` | `test` → `DockOpenResetE2ETests::test_an_open_starts_every_block_shut_in_another_service` | |
| US1/AC2 | `obs-dock.js` `openService` | `test` → `DockOpenResetE2ETests::test_reopening_the_same_service_starts_every_block_shut` | |
| US1/AC3 | `obs-dock.js` `openService` | `test` → `DockOpenResetE2ETests::test_several_hand_opened_blocks_leak_nothing_into_a_shorter_service` | |
| US1/AC4 | `obs-dock.js` `effectiveOpen` | `test` → `DockOpenResetE2ETests::test_the_live_entrys_block_stays_open_when_its_service_is_opened` | |
| US1/AC5 | `obs-dock.js` `liveEntry` | `test` → `DockOpenResetE2ETests::test_a_browsed_service_has_no_open_block_while_another_is_on_air` | |
| US1/AC6 | `obs-dock.js` L392 / L2031 | `test` → `DockOpenResetE2ETests::test_the_keyboard_open_resets_like_a_click` and `::test_the_on_load_open_keeps_only_the_live_block` | one test per path |
| US2/AC1 | `obs-dock.js` `sync` (unchanged) | `test` → `ObsDockE2ETests::test_open_blocks_survive_crossings_and_forget_on_reload` | existing pin |
| US2/AC2 | `obs-dock.js` `refreshService` (unchanged) | `test` → `DockOpenResetE2ETests::test_a_reread_keeps_a_hand_opened_block_open` | |
| US2/AC3 | `obs-dock.js` `entryOverrides` | `test` → `ObsDockE2ETests::test_open_blocks_survive_crossings_and_forget_on_reload` | the reload half |
| US3/AC1 | `obs-dock.js` `renderList` / `sync` | `test` → `DockOpenResetE2ETests::test_an_open_paints_no_morph_in_the_new_list` | |
| US3/AC2 | `obs-dock.js` `openService` | `test` → `DockOpenResetE2ETests::test_an_open_writes_no_display_state_and_broadcasts_nothing` | |
| US3/AC3 | `obs-dock.js` `centreOnOpen` L424 (unchanged) | `test` → `tests/e2e/test_obs_dock_follow.py::ObsDockFollowE2ETests::test_opening_the_service_on_air_enters_following` | existing pin, re-run unchanged |
| Edge: empty service | `obs-dock.js` `openService` / `renderList` | `test` → `tests/e2e/test_dock_open_reset.py::DockOpenResetE2ETests::test_an_empty_service_opens_without_a_block_or_an_error` | added at Implement: the spec's empty-service edge case, green on the base and the slice |

**Verification split**: 30 test · 1 inspection · 0 manual

## Complexity Tracking

none — no constraint is violated, so no justification is owed.

## Project Structure

### Documentation

```
specs/204-dock-entry-open-reset/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  converge.md  fold.md
  contracts/README.md          # none — client-only
  checklists/requirements.md   # reviewer-owned, ticked at gate 2
  preview/                     # index.html + build/capture/probes + fixtures + assets
backlog/items/ITEM-216-dock-entry-open-reset.md
backlog/board.md               # the row moves with the card
docs/spec/dock.md              # R14's delta, written at Fold
CHANGELOG.md  VERSION          # the delivery commit, pre-merge
```

### Source

```
static/web/obs-dock.js                     # +1 statement (and its comment) in openService()
tests/e2e/test_dock_open_reset.py          # new: the reset's own module, ~10 tests
```

### Structure Decision

The reset belongs in `openService()` because that function is the dock's only explicit-open path
and no re-read reaches it (research D001) — placing it in `renderList` or `loadServiceData` would
delete hand-opened blocks every ten seconds. The tests get their own module because the repo puts
one concern per E2E file (spec 197 → `test_dock_bucket_head.py`, spec 200 →
`test_obs_dock_follow.py`), and because a red-first run against the base is then a single module's
output rather than a diff inside spec 198's 1036-line file. No stylesheet, template, model or
storage change is needed, so none is made.
