# Plan 066: Always show a song entry's verses on the Tata Ibadah stage

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-069
- **Bump:** patch

## Why

Spec 054 shows the stage's `Bait …` line only when an entry keeps a strict subset of its
song's current verses. Spec 057 later gave the sidebar a verse line that always shows. In
practice most entries keep every verse, so the stage looks like it lost the line, and the
operator sees the verses in the sidebar but not beside the heading they read from.

## Scope / edges

**In:** the condition that decides whether `_tatib_stage` fills a song entry's `subtitle`.

**Out:** the line's markup and CSS, the sidebar, headings, preview modal, projector, legacy rows.

## Approach

1. In `_tatib_stage`, compute the song entry's verse string once —
   `'Bait ' + format_verses(row.verses)` when the entry is a song, has a song, its target is
   not deleted, and `row.verses` is not empty.
2. Use that one string for both the stage `subtitle` and the sidebar `verse_line`, so the two
   cannot drift. Drop the `current` verse-set query and the `chosen != current` comparison —
   one fewer query per song entry.
3. Template and CSS stay as they are (`.read__sub` already renders `item.subtitle`).

## TDD

- Red first in `multimedia/web/tests.py` (the spec 054 stage verse-line block):
  - `test_a_full_verse_selection_shows_no_verse_line` → becomes
    `test_a_full_verse_selection_shows_its_numbers`, expecting `Bait 1-3`.
  - `test_a_verse_added_after_preparing_shows_the_line_again` → becomes a test that the line
    shows `Bait 1-3` both before and after verse 4 is added.
  - New: the stage line and the sidebar `verse_line` match for `[1, 2, 3, 5, 6, 8, 9, 10]`.
  - Keep: partial selection, non-hymn partial selection, deleted-verse suppression.
- Targeted local command:
  `python manage.py test multimedia.web.tests --noinput -v 1` (scoped further with `-k` to the
  Tata Ibadah stage test class if it is slow).
- Targeted E2E: `python manage.py test tests.e2e.test_entry_preview --noinput -v 1`.
- Full suite and full browser E2E run only in push/CI.

## Risks

- Taller song entries: each song entry gains one ~19px line. Low risk; the entry box already
  grows with content and the floating controls sit in the reserved top band (spec 053).
- E2E or snapshot tests that assumed no `.read__sub` on full selections — search shows only the
  unit tests above; `test_entry_preview.py` asserts a partial line and stays valid.
