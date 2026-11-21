# Tasks: the song entry's pickers

**Spec**: `specs/210-song-verse-picker/spec.md` · **Plan**: `./plan.md`
**Verification split**: 40 test · 4 inspection · 0 manual
**Bump**: `patch` (declared at Plan; applied only in the pre-merge delivery commit).

## Phase 1 — Setup

- [x] T001 Confirm the `feat/210-song-verse-picker` worktree is based on current `develop`;
  re-check that spec 210, `reading/R47` and a board card ID are still free across all worktrees.
- [x] T002 Create `tests/e2e/test_song_entry_pickers.py` with a throwaway `gkps210` database
  helper that inherits `DATABASE_URL` from the compose web container at run time; no credential
  value is written into the file.

## Phase 2 — US1 (P1) 🎯 Song search from the first frame

**Goal**: the Song field is searchable without a trigger click and its result list can run past
the modal without resizing it.
**Independent test**: open "+ Song" from a service reached in-page, type `kj 12`, press Enter,
and confirm the hidden song ID and label.

- [x] T003 [P] [US1] Write failing E2E pins for focus on open, query narrowing, keyboard and
  tap selection, Escape, empty result and the fixed-overlay geometry.
- [x] T004 [US1] Focus the search input when the song form renders and keep the typed query
  across focus changes in `static/web/entries.js` and `_entry_form.html`.
- [x] T005 [US1] Keep `placeMenu` as the viewport-capped overlay and remove the 268px
  dialog-bound cap so the list may pass the dialog's bottom edge.
- [x] T006 [US1] Write the picked label and song ID into the form on Enter/tap; verify the
  module is green before leaving the phase.

## Phase 3 — US2 (P1) 🎯 Verse tiles and drag ranges

**Goal**: tick one verse with a click or preview and commit a stretch with one held drag.
**Independent test**: fresh pick starts at verse 1; press tile 2, drag to 5 → `verses=2..5`
  after release, with the values unchanged while held.

- [x] T007 [P] [US2] Write failing E2E pins for five 40px tiles, single click, drag preview
  and commit, collapsed-range summary, All/Clear disabled ends, fresh/edit defaults and the
  same-tile drag edge.
- [x] T008 [US2] Render the tile grid with hidden `name="verses"` ID carriers; keep the
  `{id, number}` fetch contract and the summary's number labels.
- [x] T009 [US2] Add the pointerdown/pointermove/pointerup drag: tint and preview while held,
  commit on release, no anchor mark, keyboard Shift+Arrow kept as the pointerless equivalent.
- [x] T010 [US2] Wire All/Clear disabled states and the collapsed en-dash summary; verify the
  module is green before leaving the phase.

## Phase 4 — US3 (P1) The section follows the song

**Goal**: no unusable verse control for no song, no verses or one verse, and one continuous
reveal when a song arrives.
**Independent test**: no song and no-verses songs measure 0px; a one-verse song shows one inert
tile; a fresh pick reveals in one 200ms curve and instantly under reduced motion.

- [x] T011 [P] [US3] Write failing Django and E2E pins for the server-rendered hidden states,
  the one-verse muted state, the no-verses save refusal and the reveal/reduced-motion curve.
- [x] T012 [US3] Hide the whole Verses section in `_entry_form.html` for no song and for a song
  with no live verses, in the server fragment before script runs.
- [x] T013 [US3] Mute a one-verse song with one inert tile; keep the existing refusal text and
  stale-verse behavior untouched.
- [x] T014 [US3] Add the single 200ms reveal on the product's ease curve with an instant
  reduced-motion branch; verify the pins are green.

## Phase 5 — US4 (P2) A section, not a dropdown

**Goal**: the summary line lives inside the Verses section with a separator, and the soft
trigger collapses only the tiles.
**Independent test**: in the soft-trigger state, the summary is a child of the section, its
bottom border is 1px with an 8px gap, and tapping it leaves the summary visible.

- [x] T015 [P] [US4] Write failing E2E pins for summary placement, separator geometry, no
  chevron/floating verse menu and the soft-trigger collapse.
- [x] T016 [US4] Move the summary line into the section in `_entry_form.html`, add the 1px
  separator and the soft-trigger CSS in `components.css`, and wire the collapse to the tile
  block only. Verify green.

## Phase 6 — Polish and delivery

- [x] T017 Run `multimedia.web.tests`, `multimedia.tatib.tests` and the new E2E module on a
  throwaway database; record any base-level failure separately, never quarantine it silently.
- [x] T018 Re-read every approved preview state against the shipped code and record the
  measured geometry and motion in the spec's `## UI/UX`; regenerate the portable preview only
  if the preview itself changed.
- [x] T019 Fold `reading/R30` (modified: hidden, not disabled), `reading/R43` (modified:
  collapsed ranges, IDs unchanged) and `reading/R47` (new) into `docs/spec/reading.md`, and
  write `fold.md`.
- [x] T020 Converge against the plan's traceability table, appending `converge.md` per pass.
- [ ] T021 Delivery commit: apply `VERSION` 1.35.2 and the `CHANGELOG.md` patch line, attach a
  card to the slice with `In review` and the PR reference; open the PR as a draft. Do not push
  until the owner says so.

## Phase 7 — Convergence

<!-- written by Converge only; absent until it runs -->
