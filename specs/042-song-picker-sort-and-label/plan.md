# Plan 042: Sort and label the add-song picker like the hymn books

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-044
- **Bump:** patch

## Why

The song picker orders every songbook alphabetically by book name and shows `number — title` for all
songs, which suits neither the hymnals (read by number) nor the non-hymn songbooks (read by title).

## Scope / edges

**In:**

- Within a hymn book: songs ordered by number (sub-number as tiebreak).
- Within a non-hymn book: songs ordered alphabetically by title.
- Group order: hymn songbooks first, by songbook id; then non-hymn songbooks by name.
- Option label: hymn → `<short_name> <number><sub_number> <title>` (e.g. `HAL 123 Some Title`);
  non-hymn → the title alone.

**Out:**

- The book (passage) picker, the sidebar, the projector.
- The picker's filter semantics (still title/number).

## Approach

- `multimedia/web/reading/views.py` `entry_song_options()` — stop relying on a single
  `order_by('book__name', 'number', 'title')`. Order by the book first (hymn before non-hymn;
  hymn by `book_id`, non-hymn by `book__name`) and within a book by number for hymn books and by
  title for non-hymn books — a conditional ordering, or sort in Python over the active songs.
- `multimedia/web/templates/reading/_entry_song_options.html` — label a hymn option with the short
  full title (reuse `Song.book_number` + title) and a non-hymn option with the title; keep
  `data-song` / `data-song-title` (and decide the closed label).
- `static/web/entries.js` — only if the closed control's label should also carry the short full
  title.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — a hymn book's options are in number order; a non-hymn
  book's options are in title order; hymn groups precede non-hymn groups (hymn by id, non-hymn by
  name); a hymn option's text is `HAL 123 …`; a non-hymn option's text is the title.
- E2E: `tests/e2e/test_entry_pickers.py` — the rendered option text and the group order.

## Risks

- **Mixed ordering.** One `order_by` cannot express "hymn by number, non-hymn by title"; sort
  deliberately (a `Case`/`When`, or in Python) so the two never interleave wrongly.
- **The closed label.** The control's label comes from `data-song-title`; leaving it as the plain
  title while the option shows the short full title is an intentional open question.
- **Songbook ids.** Hymn order depends on the stored `Book` ids; keep it stable.
