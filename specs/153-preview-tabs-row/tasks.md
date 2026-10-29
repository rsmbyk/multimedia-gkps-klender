# Tasks: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md` · **Plan**: `specs/153-preview-tabs-row/plan.md`

Order used: the order below, one thread. `[P]` marks a task that is order-independent, not one run
concurrently.

## Phase 1 — Setup

- [X] T001 [P] Confirm the worktree `../multimedia-gkps-klender-153` is on `fix/153-preview-tabs-row` and that a throwaway database (`gkps153`) carries the suite, so no other worktree's test run collides — `specs/153-preview-tabs-row/quickstart.md`

## Phase 2 — US1: the title gets the header's whole width

- [X] T002 [US1] Write the two failing cases: a long-titled song preview whose title box equals the header's content width (704 − 44 = 660px, ellipsized from 730), and a song preview whose tab host is not a child of `.preview__head` and starts 52px from the dialog's top — `tests/e2e/test_entry_preview.py`
- [X] T003 [US1] Make T002 pass: move `<div class="preview__versetabs" data-preview-tabs-host hidden>` out of `.preview__head` in the dialog's skeleton — `multimedia/web/templates/reading/_preview_modal.html`
- [X] T004 [US1] Make T002 pass: the tab band's own rules — `display: flex; margin: 0; width: 100%; padding: 0 22px 14px`, the mobile padding, and `flex-wrap` dropped from the head — `static/styles/design/components.css`

## Phase 3 — US2: one rule, under the tabs

- [X] T005 [US2] Write the failing cases: a song preview draws exactly one rule and it is the tab band's (head `0px`), and a passage preview keeps its 704×52 header, its own rule, and a body at 52px — `tests/e2e/test_entry_preview.py`
- [X] T006 [US2] Make T005 pass: the band carries `border-bottom: 1px solid var(--divider)` and the head drops its own only when a visible band follows it (`:has(+ .preview__versetabs:not([hidden]))`) — `static/styles/design/components.css`

## Phase 4 — US3: the dialog opens on the reading body

- [X] T007 [US3] Write the failing cases: a pointer open leaves `document.activeElement` on `#previewContent` with no tab carrying `:focus-visible`; a keyboard open does the same and the body carries the ring; `Tab` on the body reaches the selected verse tab and `Shift+Tab` returns — `tests/e2e/test_entry_preview.py`
- [X] T008 [US3] Make T007 pass: `liftIdentity()` sets the head's and the band's `hidden` independently; the open handler focuses `#previewContent` with `preventScroll`; the dialog's keydown handler carries the two-step loop, guarded by a visible band and `footer.hidden` — `static/web/preview.js`

## Phase 5 — Polish

- [X] T009 Move the two existing song cases' locators from `.preview__head .preview__tab` to `.preview__versetabs .preview__tab`, assertions unchanged, and run the whole module — `tests/e2e/test_entry_preview.py`
- [X] T010 Re-run the preview probe and check every number in `spec.md`'s `## UI/UX` against it — `specs/153-preview-tabs-row/preview/probe.py`
- [X] T011 Converge against the traceability table, then Fold `reading/R27` into the capability file — `docs/spec/reading.md`, `specs/153-preview-tabs-row/converge.md`, `specs/153-preview-tabs-row/fold.md`
- [ ] T012 Delivery: the spec's index row, `VERSION` 1.22.10 → 1.22.11 and the `## [Unreleased]` line, the card's `branch`/`pr`, its `In review` move once the PR exists, and the `Done` move in the closing pass — `specs/README.md`, `VERSION`, `CHANGELOG.md`, `backlog/items/ITEM-162-preview-tabs-row.md`, `backlog/board.md`

## Phase 6: Convergence

Pass 1 (2026-10-29): one `partial` — C001, the passage case opened a passage but never asserted the focus —
was fixed inside the pass (`test_a_passage_preview_keeps_its_header_box_and_rule` now asserts
`document.activeElement.id === 'previewContent'`) and re-run green. No `missing`, no `contradicts`, no
`unrequested`. See `converge.md`; `reading/R27` folded in `fold.md`.
