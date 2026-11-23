# Tasks: A song opened from the sidebar can edit its verses

**Spec**: `specs/230-song-verse-script-boot/spec.md`
**Plan**: `specs/230-song-verse-script-boot/plan.md`
**Verification split**: 16 test · 5 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 Confirm the slice worktree is on `fix/230-song-verse-script-boot` from `origin/develop`
  `623d9d4d`, and that the preview server on port 8771 serves this tree. No repo setup change.

## Phase 2 — Foundational

- [X] T002 Add `tests/e2e/test_song_verse_script_boot.py`: a `StaticLiveServerTestCase` with a
  non-hymn `Book`, a `Song` with two live verses, a Playwright Chromium page at 1440×900, and a
  `_reach_song_from_sidebar()` helper that clicks `/songs/`, `web-book`, then `web-song` without
  a reload. Record the script-node count and page errors from the page.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: after reaching a song by sidebar clicks, its Add and Edit verse controls open the
editor exactly as they do on a direct load.

**Independent test**: three clicks from `/` to `/songs/<pk>/`, then Add verse opens `New verse`.

- [X] T003 [P] [US1] Write the failing E2E
  `...::test_add_verse_opens_from_sidebar` (US1/AC1, FR-003, SC-001, SC-006): dialog opens with
  `New verse`, one editor request, no page errors; run it red on the unmodified templates.
- [X] T004 [P] [US1] Write the failing E2E `...::test_edit_verse_opens_from_sidebar`
  (US1/AC2, FR-004, SC-002): `Edit verse 1` opens; run it red.
- [X] T005 [P] [US1] Write the failing E2E `...::test_script_boots_at_shell_load`
  (US1/AC4, FR-002, SC-003): one `songs_verse.js` node at `/` and one on the navigated page, with
  the script's resource entry present before the swap; run it red.
- [X] T006 [US1] In `multimedia/web/templates/reading/base.html`, add
  `<script src="{% static 'web/songs_verse.js' %}"></script>` beside `reorder.js` (FR-001).
- [X] T007 [US1] Remove the `<script src>` from `multimedia/web/templates/reading/song.html`
  (FR-002); keep the surrounding markup byte-identical.
- [X] T008 [US1] Run the three E2E cases green and re-run `preview/probe.py`, comparing its
  before/after numbers with the spec's `## UI/UX`.

## Phase 4 — US2 (P1)

**Goal**: a direct song load keeps working and has exactly one script include.

**Independent test**: open `/songs/<pk>/` directly; Add and Edit both open, one script node.

- [X] T009 [P] [US2] Write the failing E2E
  `...::test_direct_load_still_opens_both_dialogs` (US1/AC3, US2/AC1, FR-005, SC-004, SC-006):
  one script node, both dialogs open, no page errors; run it red on the unmodified templates if
  the include count differs, then green after T006/T007.
- [X] T010 [US2] Confirm US2/AC3 in `test_add_verse_opens_from_sidebar`: one `/editor/verse/new/`
  request and one open dialog per click (no double binding).
- [X] T011 [US2] Re-run `tests/e2e/test_verse_modal_header.py` to catch a shared-editor
  regression from the extra script load; record the result.

## Phase 5 — Polish

- [X] T012 [P] Inspect the diff: only the two template lines, the new E2E module and the spec
  pack change; no CSS, script body, endpoint or permission rule is touched (FR-006, US1/AC5).
- [X] T013 [P] Inspect `preview/probe.py` boxes: 111.765625×38 at x=900, y=681.34375 in both
  trees, Δ0.00px (SC-005).
- [X] T014 [P] At Fold, add `reading/R55` to `docs/spec/reading.md` with the rule that a script
  owning controls on a swapped-in page is booted by the shell (FR-007).

## Phase 6 — Delivery (after Fold)

- [X] T015 Apply `bump: patch` (VERSION 1.36.15 → 1.36.16) and the changelog line immediately
  before the merge, with `ITEM-245` moved to Done in the same commit.

## Phase 7 — Convergence

<!-- written by Converge only; absent until it runs -->
