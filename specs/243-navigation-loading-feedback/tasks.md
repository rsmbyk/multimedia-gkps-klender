# Tasks — spec 243

**Spec**: `specs/243-navigation-loading-feedback/spec.md` · **Plan**: `plan.md`

## Setup

- [X] T001 Confirm the slice worktree at `~/Projects/multimedia-gkps-klender-243` on `fix/243-navigation-loading-feedback`, based on `origin/develop` at `14af227a`.
- [X] T002 Recheck the next free numbers: `ITEM-258` and `reading/R61`; plan bump `patch` against specs 240–242.
- [X] T003 Place the Phase 0 research note at `specs/243-navigation-loading-feedback/research.md`; full citations stay in `preview/loading-patterns-research.md`.

## Foundational — failing tests first (TDD-02)

- [X] T004 Write the failing test for `US1/AC1` in new `tests/e2e/test_navigation_pending.py`: a delayed rail click locks that rail item dim-only and bars the top edge of the first- and second-level sidebars.
- [X] T005 Write the failing test for `US1/AC2–AC4`: list-only chapter/songbook fetches leave the stage with no `aria-busy`, bar or placeholder, and the displayed passage is unchanged.
- [X] T006 Write the failing tests for `US2/AC1–AC3`: song, verse/passage and service writes set stage busy, run the stage bar and show the three distinct placeholder anatomies with sidebar-seeded title data.
- [X] T007 Write the failing test for `US2/AC4`: placeholder `.read` origin equals the real `.read` at 1440px (x=520, y=218) and uses 18px horizontal padding at ≤720px.
- [X] T008 Write the failing test for `US2/AC5`: settlement clears `aria-busy`, the stage bar and the placeholder.
- [X] T009 Write the failing tests for `US3/AC1–AC3`: write→write cancels the first; write→list keeps the first and adds a list bar; list→write cancels the list.
- [X] T010 Write the failing test for `US3/AC4`: a cancelled item unlocks and can be activated again.

## US1 — List-only fetches leave the reading page alone

- [X] T011 Make T004–T005 pass in `static/web/reading.js` by adding the pending state at `navigate()` and mapping `opts.kind`/clicked source to list-only vs stage-write.
- [X] T012 Add the dim-only item lock in `static/styles/design/components.css`: rail icon visible at opacity 0.45, row opacity 0.58, `aria-disabled="true"`; no spinner, label, edge fill or ring marker.
- [X] T013 Add the 3px section bar to `#panel`, `#chapters` and `.stage` in `static/web/reading.js` / `components.css`, positioned at `top: 0` of each root and shown only for sections the fetch will update.

## US2 — Stage writes get a layout-matched placeholder

- [X] T014 Make T006–T008 pass by building the three placeholder layouts in `static/web/reading.js` with the product's `read__*`, `v` and `tatib__item` classes, seeded from `data-name` / chapter text / rail label.
- [X] T015 Give the placeholder the real stage padding (`var(--stage-pad-top)`, `clamp(24px, 5vw, 64px)`, 18px at ≤720px) so its content origin matches the real `.read`.
- [X] T016 Add the pre-rendered polite `role="status"` live region and `aria-busy` on `.stage` only for writes; announce one opening and one settlement message without moving focus.

## US3 — Supersede by stage-write class

- [X] T017 Make T009–T010 pass by replacing `pendingNavigation` queueing with cancel/coexist by stage-write class, releasing the cancelled item immediately and keeping the full-page fallback busy until unload.
- [X] T018 Confirm by inspection that pending state exists only in `navigate()` and all settlement paths (success, failure, supersede, unload) clear or hand off correctly.

## Polish and verification

- [X] T019 Re-run `tests/e2e/test_navigation_pending.py` and the sibling `tests/e2e/test_navigation_freshness.py`; both green, with the rail-to-page path still in-page and server-current.
- [X] T020 Run `collectstatic --noinput` and `multimedia.web.tests` with a throwaway DB; the two failures reproduce unchanged on base `14af227a`.
- [X] T021 Drive the accepted preview file at `preview/index.html` and record the final measured bar offsets, lock opacities and placeholder origins in `preview/probe14.py` output.
- [X] T022 Analyze: write `analysis.md` with artifact SHAs, metrics, findings and history (Analyze stage).
- [X] T023 Converge: compare the present code with the traceability table and append `converge.md`.
- [X] T024 Fold: add `reading/R61` to `docs/spec/reading.md` and record `fold.md`.
- [X] T025 Open `ITEM-258`, move the board row and deliver the patch bump in `VERSION` / `CHANGELOG.md` with the card closed in the same PR.

## Late asks after gate 2 (in-slice extensions)

- [X] T026 Match the song placeholder to the real header: displayed number in the eyebrow, displayed title case, no section bar above the numbered verses.
- [X] T027 Fall back to the selected songbook name in the eyebrow when a song row has no number code.
- [X] T028 Disable the sidebar row's edit/delete/add controls for the same period as the row lock, and restore them on settlement.

**TDD checkpoint**: no production edit before T004–T010 have been watched fail for the expected reason.

## Phase 1: Convergence

- 1 of 1 pass — consolidated 15-test run green on the build; same command red on base `14af227a` (10 failures, 1 error, 4 passes). `converge.md` records the rows and dispositions.

Merged into `develop` via PR #624 on 2026-11-26.
