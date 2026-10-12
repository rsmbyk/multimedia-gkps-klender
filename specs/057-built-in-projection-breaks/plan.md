# Plan 057: Built-in blank after each entry and each song verse

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-059
- **Bump:** minor

## Why

On the service projector, a blank screen exists only when the operator inserts a
**Section break**. That break is a real service entry: it can be reordered and
deleted. The owner wants a blank that belongs to the content itself — one after
every service entry, and one after every verse of a song entry — that is not a
row in the order and cannot be moved or deleted.

## Scope / edges

**In:**

- Projector screen list (`_projector_screens`): after the content screens of each
  text, single-screen text, scripture, and legacy text row, append one blank
  screen.
- Song entries: split lyrics by stored verse, project each verse with the existing
  two-line screens, then one blank. The blank after the last verse is that
  entry's trailing blank (not a second one).
- A stored **Section break** (and a legacy end-of-section row) stays one blank
  screen of its own, with no extra built-in blank after it.
- Tests for the screen list. The editor list, reorder, and delete stay unchanged
  because the blank is not an entry.

**Out:**

- A new entry kind, or writing blanks into `ServiceEntry` rows.
- Blanks between the two-line screens inside one text body or one verse.
- A blank between scripture verses (one blank follows the whole passage).
- The OBS dock and its item list.
- Collapsing a built-in blank when the next row is already a section break. Two
  blank screens in a row are allowed.

## Approach

Build the extra screens in `_projector_screens` only. Song lyrics are already
joined with a blank line between verses in `ServiceEntry.resolve()`; the
projector should walk `entry.verses` (the same order resolve uses) so each verse
is a group, then append `{'blank': True, ...}` after the group. Other content
rows append that same blank once after their screens.

## TDD

- Domain/app tests: `multimedia/web/tests.py` (projector screen sequence).
- E2E: extend `tests/e2e/test_projector.py` if it already steps screens; otherwise
  the app tests are enough and E2E is N/A beyond a single step-through.

## Risks

- A content entry followed by a stored section break shows two blanks. Called out
  so it can be rejected at Accept.
- A song whose verses are missing from the book still needs a defined screen list
  (no crash, no extra phantom verse).
