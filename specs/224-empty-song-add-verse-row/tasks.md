# Tasks: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md`
**Plan**: `specs/224-empty-song-add-verse-row/plan.md`
**Verification split: 14 test · 5 inspection · 5 manual**

## Phase 1 — Setup

- [X] T001 [P] Create `multimedia/web/reading/test_verse_add_gate.py` with its own `Book`/`Song`
  fixtures (`TestCase`, `reverse('web-song', …)`) and a helper that counts `[data-add-verse]` and
  `.verse-add` in the rendered response.
- [X] T001B [P] Create `tests/e2e/test_song_empty_placement.py` with `StaticLiveServerTestCase`,
  an empty ordinary song and an empty `TataIbadah`, and a helper that opens both routes and reads
  the top of `.entry__empty-title`. No product file changes.

## Phase 2 — Foundational: red before the template edit

Run against the throwaway `gkps224` database before `song.html` is touched, so each case fails for
its own reason (TDD-02).

- [X] T002 [P] [US1] Write `test_empty_song_has_no_after_verse_row` (FR-001, US1 AC1, AC5, SC-001):
  a song with no verses has zero `.verse-add` wrappers; include a fixture whose only verse is
  soft-deleted.
- [X] T003 [P] [US1] Write `test_empty_song_has_one_add_verse_button` (FR-002, US1 AC1, SC-001):
  the same page has exactly one `[data-add-verse]`, inside `.entry__empty`.
- [X] T004 [P] [US1] Write `test_song_with_verses_keeps_its_single_add_row` (FR-003, US1 AC3,
  SC-002): a song with three verses has one `.verse-add` after the last `p.v` and no invitation.
- [X] T004B [P] [US2] Write `test_empty_song_title_matches_the_tata_ibadah_title` (FR-006, US2 AC1,
  SC-005): at 1440×900 the two `.entry__empty-title` tops differ by at most 1px.
- [X] T004C [P] [US2] Write `test_empty_song_title_matches_the_tata_ibadah_title_at_900x700`
  (US2 AC2, SC-005): the same assertion at 900×700.
- [X] T005 Run the three template cases and the two geometry cases on the unmodified product;
  record the red output in `analysis.md`. The failures must be an element count and a y-gap, not
  an import or DB error.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: an empty song paints one `Add verse`, the one in its invitation.
**Independent test**: T002 and T003 go green; T004 and the existing verb cases stay green.

- [X] T006 [US1] Make FR-001 pass: in `multimedia/web/templates/reading/song.html:45`, change
  `{% if can_edit_verses %}` to `{% if can_edit_verses and verse_rows %}`. No other line changes.
- [X] T006B [US2] Make FR-006 pass: add the three scoped `.read[data-kind="song"]:has(.entry__empty)`
  rules next to the Tata Ibadah block in `static/styles/design/components.css`, with
  `padding-top: 0`; no global selector, token or animation changes.
- [X] T007 Re-run T002–T004, T004B, T004C and the existing `VerseVerbTests` cases; all are green.

## Phase 4 — Polish and regression

- [X] T008 [P] Re-run `preview/probe.py` against the live worktree and record SC-003's before/after
  boxes in `analysis.md` (manual): invitation title moves y=205.9 → 253.9, surviving button stays
  111.8×38 at x=1060.1, with-verses row stays 520×38 at x=856, y=681.3; compare it with the
  Tata Ibadah title at y=253.5.
- [X] T008B [US2] `manual` — measure both empty routes at 390×844 in the live probe; record the
  5.5px residual and the taller song header in `converge.md`.
- [X] T009 `inspection` — read the whole diff: one template condition, three song-empty-only CSS
  rules, two small test modules; no JS, view, endpoint, copy or permission change; hymn and
  restricted gating still present; every new selector contains `:has(.entry__empty)`.
- [X] T010 `inspection` — Fold modifies `reading/R40` in place with the new gate, its empty-song
  scenario and the shared empty-state position; move the capability header's `last folded` and
  prepend the slice to `slices`.
- [X] T011 `manual` — click through the live empty page's invitation button and save a first verse
  (SC-004), then the with-verses page; record the observation in `converge.md`.
- [X] T012 [Convergence] Compare the code against every traceability row by its declared method and
  append `## Phase 1: Convergence` to `converge.md` with evidence.

## Phase 5 — Delivery

- [X] T013 `VERSION` 1.36.9 → 1.36.10 and one `### Fixed` line under `## [Unreleased]` in
  `CHANGELOG.md`, applied at delivery and re-checked against `origin/develop` for a claimed number.
- [X] T014 Delivery on the owner's word: open the PR as a draft against `develop` with `Refs #590`,
  move `ITEM-239` to `In review` and then pre-merge `Done` (`closed_reason`, board row, `bump`),
  push, mark ready. No follow-up board PR.

## Closing note

Filled in by Converge/Fold with the actual merge SHA and PR number.
