# Tasks: an open modal keeps the scroll to itself

**Spec**: `specs/257-modal-scroll-containment/spec.md` (Accepted, gate 1)
**Plan**: `specs/257-modal-scroll-containment/plan.md`
**Verification split**: 7 test · 6 inspection · 1 manual
**Order used**: one thread, in the order listed; `[P]` marks order independence, not concurrency.

Chronology note: the CSS edit was already uncommitted in the worktree as the gate-1 live preview.
Implement re-assesses it against these tasks; it does not re-type it or commit before Fold.

## Phase 1 — Setup

- [X] T001 [Setup] Verify the slice branch is cut from `1cd9f081`, is zero commits ahead, and `_static/` and `__pycache__` stay ignored.

## Phase 2 — Foundational

- [X] T002 [Foundational] Confirm [contracts/none.md](contracts/none.md) and [data-model.md](data-model.md) stand: no endpoint, schema or JS state work in this slice.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a wheel spent at the end of a modal's own view stays in that view.
**Independent test**: document `scrollY` 600 → 600 while the editor body reaches 617 on 8765, against 600 → 1700 on 63404.

- [X] T003 [US1] `test` — write a failing test for FR-001's end-of-range case: `tests.e2e.test_modal_scroll_containment.ModalScrollContainmentE2ETests.test_wheel_at_the_end_of_editor_content_leaves_the_document_still`; confirm it fails on the leaked document offset, not an import error.
- [X] T004 [US1] `test` — write a failing test for US1/AC2: `…test_wheel_at_the_end_of_preview_body_leaves_the_document_still`; confirm the preview body reaches 512 while the document moves on base.
- [X] T005 [US1] `test` — write a failing test for FR-002: `…test_picker_options_at_their_end_do_not_scroll_the_editor`; confirm the editor moves 0 → 341 on base.
- [X] T006 [US1] `test` — make FR-001, US1/AC2 and FR-002 pass with the two CSS rules already present in `components.css`; inner maxima stay 617/512/870.
- [X] T007 [US1] `inspection` — compare `preview/probe.py` tall and nested cases on both servers: document 600 → 1700/1480 before, 600 → 600 after; editor leak 341 before, 0 after.

## Phase 4 — US2 (P2)

**Goal**: a modal with no scrollable range gives the wheel to nothing behind it.

- [X] T008 [US2] `test` — write a failing test for FR-003: `…test_short_editor_does_not_scroll_the_document`; confirm 600 → 2360 on base.
- [X] T009 [US2] `test` — write a failing test for US2/AC2: `…test_wheel_over_the_editor_header_leaves_the_document_still`.
- [X] T010 [US2] `test` — make FR-003 and US2/AC2 pass by the root hold; no wheel listener or body class is added.
- [X] T011 [US2] `test` — write and pass a test for FR-005/US2/AC3: `…test_closing_the_dialog_restores_document_scrolling_at_the_same_offset`; `clientWidth` and dialog box stay unchanged.
- [X] T012 [US2] `inspection` — run `preview/geometry.py` on both servers and confirm 1200/1200/1200 and 480×100 at (360, 300).

## Phase 5 — US3 (P2)

**Goal**: the rule covers every modal scrollport and every open dialog.

- [X] T013 [US3] `test` — write a failing test that reads `getComputedStyle` for each of the ten scrollports named in `research.md` with dialogs open: `…test_every_named_modal_scrollport_contains_scroll`.
- [X] T014 [US3] `test` — make T013 pass with the selector list in `components.css`; the already-contained reading/dock/toast rules stay as they were.
- [X] T015 [US3] `inspection` — open two native dialogs, close one, and read root `overflow-y` = `hidden` until the last `dialog[open]` is gone.

## Phase 6 — Polish

- [X] T016 [Polish] `test` — SC-001 red evidence: copy the new test module into the detached base worktree, run it with its own throwaway database, record the failures by name, restore the base file.
- [X] T017 [Polish] `test` — SC-001 green evidence: run the same module on the slice with `gkps257`; all cases pass.
- [X] T018 [Polish] `inspection` — FR-004: `git diff --name-only 1cd9f081` and confirm `components.css` is the only behaviour file changed.
- [X] T019 [Polish] `inspection` — re-run both probes after the final selector edit and confirm the frozen `UI/UX` numbers still match.
- [ ] T020 [Polish] `manual` — after deployment, open an editor on a scrollable page and wheel past its end; the page behind stays put.
- [X] T021 [Polish] Fold — only at Converged: first commit carrying spec pack, code, card row and the `reading/R66` capability delta.
- [ ] T022 [Polish] Delivery — after a separate owner word: tracker anchor, PR, version/changelog line, card moves and report.
