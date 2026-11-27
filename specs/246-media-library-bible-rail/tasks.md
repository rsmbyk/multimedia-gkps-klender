# Tasks — spec 246

**Order used**: Setup → Foundational → US1 → US2 → Polish → Fold (one agent, one thread).
`[P]` means order-independent, not concurrent. Items marked `[X]` landed during the gate-1
approved preview; gate 2 reviews that work against the plan before the continuous run to Fold.

## Setup

- [X] T001 [P] verify worktree and branch — `git worktree list`, branch `fix/246-media-library-bible-rail` cut from `origin/develop`
- [X] T002 [P] claim the next free numbers — spec 246, card ITEM-263, patch 1.37.4 (checked across all local and remote refs)

## Foundational

- [X] T003 [P] reproduce the reported behaviour on the live app — `preview/probe.py` base column
- [X] T004 [P] write the red E2E seam — `tests/e2e/test_media_library_bible_rail.py` (two assertions, red before the fix)

## US1 — Bible rail fetches its books on the first click

- [X] T005 add the library's own section identity — `multimedia/web/reading/views.py` (`media_library` context)
- [X] T006 [US1] make the new E2E module green — `tests/e2e/test_media_library_bible_rail.py`
- [X] T007 [US1] compare base with preview through the rail — `specs/246-media-library-bible-rail/preview/probe.py`

## US2 — Other rail navigation is unchanged

- [X] T008 [US2] verify own-tile toggle, cross-section switch and direct load — `preview/manual_probes.py`
- [X] T009 [US2] run the targeted navigation lane at Converge — `tests/e2e/test_navigation_pending.py` (named in plan SC-004)

## Polish

- [X] T010 [P] write research, data model, contracts, quickstart and plan — `specs/246-media-library-bible-rail/`
- [X] T011 [P] write tasks and analysis with artifact SHAs — `specs/246-media-library-bible-rail/`
- [X] T012 [P] Fold the added `reading/R63` block and bump `last folded` — `docs/spec/reading.md`
- [X] T013 [P] write the delivery commit — `VERSION`, `CHANGELOG.md`, `backlog/board.md`, `backlog/items/ITEM-263-media-library-bible-rail.md`, `docs/spec/reading.md`
- [X] T014 [P] prepare PR title and body; push still waits on the owner's word — `specs/246-media-library-bible-rail/`

## Delivery steps declared by this repo

- Git Flow branch and squash PR (GIT-02/03/04), no push without the owner's word (GIT-07).
- SemVer patch declared at Plan and applied at Fold (VER-03/04); one changelog line (VER-07).
- Kanban card closes in the delivery PR (BRD-06/07); GitHub issue anchor when the card passes `Speccing` (BRD-10).
- Tracker mirror uses `Refs`, never `Closes`.
