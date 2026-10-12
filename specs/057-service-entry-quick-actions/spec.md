# Spec 057: Service entry quick fixes — Save on single-screen text, instant break, no break edit, verse line in the sidebar

- **ID:** 057
- **Status:** Accepted
- **Item:** ITEM-059
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Four operator-reported issues on the Tata Ibadah entry editor and its sidebar:

1. The single-screen text modal's Save button stays disabled after text is typed.
2. Adding a break opens a modal form, though a break has nothing to fill in.
3. A break row offers an Edit control, though a break has nothing to edit.
4. A song's selected verses are not shown in the sidebar.

## Scope

### In scope

- The Save guard on the single-screen text form.
- "+ Break" adds the break at once, with no form.
- No Edit control on break entries (stage and sidebar). Delete stays.
- A verse line on the second line of each song row in the sidebar.
- A shared verse-number formatter, used by that sidebar line and by the stage `Bait` line
  (spec 054).

### Out of scope

- Editing a break's position other than through the existing drag/arrow reorder.
- Changing which song verses an entry keeps, or the song picker.
- Non-song entries (passage, text, single-screen text) in the sidebar: their rows are unchanged.
- Projector screens.

## UI details

Approved preview: the live `/tatib/<id>/` session as the owner used it on 2026-10-11 (the
single-screen modal screenshot, the sidebar list). The owner has not yet OKed the sidebar verse
line's exact styling; it reuses the row's existing second-line style (`songrow__t--lines` /
`songrow__line`).

- **Save button (single-screen text):** enabled exactly when the Text field has non-whitespace
  content; disabled when empty or whitespace-only. Live: it updates on each keystroke, with no
  reload.
- **Break add:** clicking "+ Break" (the add row above the list, the empty-state button) creates
  the break at once and re-renders the body and sidebar in place. No dialog opens, and the
  break appears where its add row sits.
- **Break row:** the thin rule, its grip, and Delete. No Edit button in the stage or the sidebar.
- **Sidebar verse line:** a second line under a song row's label, text `Bait ` + the formatted
  verse numbers (`Bait 1-3, 5`); same size and colour as the existing two-line label; the
  row's width is unchanged.

## Domain rules

- **Save guard covers both text kinds.** The guard applies to the `text` and `single_screen_text`
  forms. It was wired only to `text`, which left single-screen Save disabled.
- **A break needs no input.** Creating a break stores a `section_break` entry with no title or
  text. The position is the add row's position (after the entry above it), or the end of the
  list for the empty-state button.
- **Break edit is not offered.** The Edit control is absent for `section_break` entries
  everywhere it appears. A break's Delete control is kept.
- **Verse formatter.** Input: a set of verse numbers. Sort ascending, remove duplicates. Group
  maximal runs of consecutive numbers. A run of three or more becomes `a-b`; a run of one or two
  stays as separate numbers. Join the groups with `, `.
  - `[1, 2, 3, 5, 6, 8, 9, 10]` → `1-3, 5, 6, 8-10`
  - `[1, 2, 3]` → `1-3`
  - `[5, 6]` → `5, 6`
  - `[4]` → `4`
  - `[]` → `` (empty; no line shown)
- **Sidebar verse line.** Every song entry whose song still exists and is not deleted shows
  `Bait ` + the formatted stored verse numbers on the sidebar row's second line. A deleted target
  shows no verse line. A non-song row is unchanged.
- **Stage line unchanged in rule, changed in format.** Spec 054's rule (show only when the
  stored verses differ from the song's current ones) still governs the stage's `Bait` line; only
  its numbers are formatted by the same formatter.
- **Filter text.** The sidebar's filter text still carries the label and the verse text, so a
  search for a verse number still finds the row.

## Acceptance scenarios

- **Given** the single-screen text form is open and empty, **when** the operator types `feef`,
  **then** Save is enabled without reload; **when** the text is cleared, Save is disabled again.
- **Given** a Tata Ibadah with three entries, **when** the operator clicks the add row after
  entry 2 and chooses "+ Break", **then** a break appears between entries 2 and 3 with no dialog
  shown, and the page is not reloaded.
- **Given** a break row on the stage or in the sidebar, **then** no Edit control is rendered for
  it; its Delete control is present.
- **Given** a song entry that keeps verses 1, 2, 3, 5, 6, 8, 9, 10 of its song, **then** the
  sidebar row's second line reads `Bait 1-3, 5, 6, 8-10`, and the stage's `Bait` line uses the
  same text.
- **Given** a song entry that keeps verses 5 and 6, **then** the second line reads `Bait 5, 6`.

## Traceability

- Formatter (the range rule): `multimedia/web/tests.py::FormatVersesTests` — the spec's six
  examples, including the mixed `1-3, 5, 6, 8-10` case.
- Save guard: `tests/e2e/test_entries.py::EntryModalE2ETests::test_single_screen_save_follows_the_text_content`.
- Instant break: `multimedia/web/tests.py::ServiceEntryViewTests::test_an_instant_break_lands_after_its_add_row_and_the_neighbours_keep_order`,
  `::test_an_instant_break_without_a_position_goes_to_the_end`; E2E
  `tests/e2e/test_tatib_section_break.py::SectionBreakE2ETests::test_plus_break_adds_the_break_at_once_without_a_dialog`.
- No break Edit: `multimedia/web/tests.py::ServiceEntryViewTests::test_a_section_break_renders_the_same_divider_as_a_legacy_row`;
  E2E `tests/e2e/test_tatib_section_break.py::SectionBreakE2ETests::test_the_divider_carries_its_own_controls`.
- Sidebar verse line: `multimedia/web/tests.py::ServiceEntryViewTests::test_the_sidebar_song_row_shows_its_verses_on_a_second_line`,
  `::test_a_deleted_song_target_shows_no_sidebar_verse_line`.
- Stage `Bait` format: `multimedia/web/tests.py::ServiceEntryViewTests::test_a_verse_added_after_preparing_shows_the_line_again`.
