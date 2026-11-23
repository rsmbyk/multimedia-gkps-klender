# Tasks: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md` · **Plan**: `plan.md`

## Phase 1 — Setup

- [x] T001 Confirm the worktree is on `feat/225-open-created-songbook-song`, cut from `develop`.
- [x] T002 Confirm the live dev server on `127.0.0.1:8768` serves this worktree and the base
      reproduction is recorded in `reproduce.py` / `probe_click.py`.

## Phase 2 — Tests first (red)

- [x] T003 Add `test_a_created_songbook_opens_in_the_panel` to `tests/e2e/test_editor.py`: create
      from `#panelAdd`, assert the new row's `aria-current`, `data-ch=open` and in-page marker.
- [x] T004 Add `test_a_created_song_opens_on_the_stage`: open a book, create a song, assert URL,
      `#readName`, current row and `data-read=on`.
- [x] T005 Add `test_an_open_from_create_does_not_reload_the_document` and
      `test_a_created_songbook_keeps_the_stage` for FR-003.
- [x] T006 Add `test_an_edited_songbook_keeps_the_selection` and
      `test_a_refused_songbook_create_keeps_the_selection` for FR-004/FR-005.
- [x] T007 Run the focused module; confirm exactly the new create-open tests fail on the base code.

## Phase 3 — Implementation (green)

- [x] T008 In `static/web/reading.js`'s `editor:saved` listener, branch on `created && kind` for
      `songbook` → `navigate('/songs/book/<id>/', {kind: 'lists', forceServer: true})` and
      `song` → `navigate('/songs/<id>/', {kind: 'song', forceServer: true})`, before the generic
      refresh; keep the spec-209 tatib branch first and leave all other saves on the existing path.
- [x] T009 Run the focused module; all new tests pass.
- [x] T010 Run `tests.e2e.test_reading` and the existing spec-209 scenarios; no regression.

## Phase 4 — Fold and release record

- [x] T011 Fold `new: reading/R53` into `docs/spec/reading.md` (four scenarios, header, index).
- [x] T012 Bump `VERSION` 1.36.10 → 1.36.11 and add a `CHANGELOG.md` entry under `[Unreleased]`.
- [x] T013 Update `specs/README.md` index and move the board card/row to In progress. The In review
      and pre-merge Done moves wait for a PR number and the owner's push authorisation.

## Phase 5 — Converge

- [x] T014 Record measurements and results in `converge.md`; close any finding as fixed, carried or
      carded.
