# Tasks: verse reference notice

Phases follow the two user stories. `[P]` means order-independent, not concurrent; the run executes them
in the order written. Every `test` row in `plan.md` is a red task and a green task.

## Setup

- [X] T001 Create `tests/e2e/test_verse_reference_notice.py` with the book/song/verse/service fixtures, a `MEASURE` script and the page helper; no assertions yet.

## Foundational

- [X] T002 [US1] Write failing tests for FR-001, FR-002, FR-003, FR-004, FR-008 and US1/AC1–AC3: note is the row's first child with the right copy, glyph and type, row stays 38px, button is neutral-disabled, `aria-describedby` resolves. Run them red.

## User Story 1 — the reason sits beside the button

- [X] T003 [US1] Emit the note in `multimedia/web/templates/reading/_editor_form.html` inside `.editor__actions` before the buttons, with an id and `aria-describedby` on the disabled button; keep the existing count and disabled flag.
- [X] T004 [US1] Add `.editor__refnote` and the scoped `.editor__delete:disabled` rules in `static/styles/design/components.css`, using only existing tokens.
- [X] T005 [US1] Make the US1 red tests green; leave the shared `.editor__danger:disabled` untouched.
- [X] T006 [US1] Write failing tests for FR-006, FR-007 and US1/AC4–AC5: an unreferenced verse has no note and an enabled button, a non-verse editor is byte-identical, and the delete endpoint still refuses a referenced verse. Run them red.
- [X] T007 [US1] Make those tests pass by scoping the template branch and CSS selector; no endpoint change.

## User Story 2 — the narrow dialog

- [X] T008 [US2] Write failing tests for FR-005 and US2/AC1–AC3 at 420×900, light and dark: note on a full-width line, buttons right-aligned on their own 38px row, no horizontal overflow, token-only colours. Run them red.
- [X] T009 [US2] Add the `max-width: 650px` wrap rule in `static/styles/design/components.css`, scoped to the large editor with a note.
- [X] T010 [US2] Make the narrow tests green; re-measure the 840px row for no regression.

## Polish

- [X] T011 Re-run the targeted E2E module and inspect the diff for files outside the two source paths; report the numbers.
- [X] T012 At delivery only: write `VERSION` bump, changelog line, board/card moves and the capability fold after Converge.
