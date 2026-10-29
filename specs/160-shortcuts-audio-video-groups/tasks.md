# Tasks: Audio and video name their play/pause key

**Spec**: `specs/160-shortcuts-audio-video-groups/spec.md` · **Plan**: `plan.md`

Ordered by user story. `[P]` means order-independent, not concurrent — one agent ran these in the
order written.

## Phase 1 — Setup

- [X] T001 [US1] Set the worktree's run up and see the module green before touching it: `DATABASE_URL` for a database no other worktree uses, then `$PY manage.py test multimedia.web.tests.ServiceProjectorTests --keepdb --noinput` — `quickstart.md`

## Phase 2 — Foundational

- [X] T002 [US1] Add `test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own` to `ServiceProjectorTests` and run it **red for the right reason**: the sheet's headings read `… Library Detour, Display, …`, `Display` still holds `Audio/Video Play/Pause`, and no `Audio` heading exists — `multimedia/web/tests.py`

## Phase 3 — US1 (P1): the sheet names audio and video

- [X] T003 [US1] Remove the `Audio/Video Play/Pause` row from the `Display` group, leaving its other three rows verbatim — `multimedia/web/templates/reading/projector_controls.html`
- [X] T004 [US1] Append the `Audio` and `Video` groups, each with its `Play/Pause` row on the Space chord, to the second `.stack` after `Library Detour` — `multimedia/web/templates/reading/projector_controls.html`
- [X] T005 [US1] Update the video contract's incidental assertion from `Audio/Video Play/Pause` to the two headings it now reads, and run `multimedia.web.test_media` green — `multimedia/web/test_media.py:278`
- [X] T006 [US1] Run T002's case green, then regenerate the preview (`$PY specs/160-shortcuts-audio-video-groups/preview/build_preview.py`) and record `preview/measure.py`'s numbers for `today` and `after` — `specs/160-shortcuts-audio-video-groups/preview/`

## Phase 4 — US2 (P1): the keys are unchanged

- [X] T007 [US2] Confirm the diff touches no script, stylesheet or token: `git diff --stat` names one template and one test module, and `static/web/projector.js:1254-1260` is absent from it — the key handler is the one that ran before this slice

## Phase 5 — Polish

- [X] T008 Fold `projector/R3` into `docs/spec/projector.md`, with the sheet's groups and the absence of the combined row — `docs/spec/projector.md`
- [X] T009 Write `converge.md` and `fold.md`, and confirm the spread of `analysis.md` is unchanged after the edits — `specs/160-shortcuts-audio-video-groups/`
- [ ] T010 *(delivery — completed at the push step)* Delivery bookkeeping: the card set `done` with its `spec:`, `branch:`, `bump: patch` and `closed_reason:`, the board row moved to `Done`, one `CHANGELOG.md` line under `Changed`, `VERSION` 1.22.10 → 1.22.11 — `backlog/`, `CHANGELOG.md`, `VERSION`
