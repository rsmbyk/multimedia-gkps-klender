# Plan 039: Show the short full title for a hymn song in the service sidebar

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-041
- **Bump:** patch

## Why

In the Tata Ibadah sidebar a hymn song reads as its long book name ("Kidung Jemaat 435"), which is
longer than the row needs and hides the song's title. The operator knows the hymnal by its short
name; show `KJ 435 Marolopolop Tondingki` — short reference plus title.

## Scope / edges

**In:**

- The sidebar label for a song entry from a hymn book (`Book.is_hymn_book`) becomes the short full
  title: `Song.book_number` + the song's title.
- The sidebar's filter text carries the same words so filtering still matches.

**Out:**

- Non-hymn songs, which keep their current label.
- The sidebar's other kinds (text, passage, break).

## Approach

- `multimedia/web/reading/views.py` — in `_tatib_stage()`, when the row is a song entry whose book
  is a hymn book, use `f'{song.book_number} {song.title}'` for the sidebar label (and include it in
  the row's `txt`). Leave the title used for the pane as it is unless the owner extends the scope.
- Reuse `Song.book_number` (`multimedia/songs/models.py`); do not re-derive the short reference.
- Decide the title-less case: a hymn song with `is_untitled` or a blank title falls back to
  `book_number` alone.
- **Amends spec 006's** sidebar label for a song entry.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — a hymn song entry labels the sidebar
  `KJ 435 Marolopolop Tondingki`; a non-hymn song keeps its current label; a title-less hymn song
  falls back to the short reference; the filter text contains the words.
- E2E: N/A (covered by the domain tests).

## Risks

- **Scope creep into the pane.** `citation()` is shared; changing it would move the pane heading too.
  Keep the change in the sidebar label unless the owner extends it.
- **Title-less songs.** Guard the blank/untitled title so the label does not end with a stray space.
