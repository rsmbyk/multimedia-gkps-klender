# Tasks 057: Service entry quick fixes

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from `develop` (`fix/057-service-entry-quick-actions`)
- [x] Red/Green — `format_verses` unit tests (`multimedia/web/tests.py::FormatVersesTests`): the
      spec's examples (`[1,2,3,5,6,8,9,10]` → `1-3, 5, 6, 8-10`; `[1,2,3]` → `1-3`; `[5,6]` →
      `5, 6`; `[4]`; `[]`; a gap keeps a pair separate; unsorted and duplicate input)
- [x] Red/Green — Save guard: the single-screen form's Save follows its Text field (E2E,
      `tests/e2e/test_entries.py::EntryModalE2ETests::test_single_screen_save_follows_the_text_content`)
- [x] Red/Green — instant break: the POST creates a `section_break` at the add row's position or
      the end, the neighbours keep their order
      (`multimedia/web/tests.py::ServiceEntryViewTests::test_an_instant_break_*`; E2E
      `tests/e2e/test_tatib_section_break.py::SectionBreakE2ETests::test_plus_break_adds_the_break_at_once_without_a_dialog`)
- [x] Red/Green — break rows render no Edit control; Delete remains; every other kind keeps Edit
      (`multimedia/web/tests.py::ServiceEntryViewTests::test_a_section_break_renders_the_same_divider_as_a_legacy_row`;
      E2E `tests/e2e/test_tatib_section_break.py::SectionBreakE2ETests::test_the_divider_carries_its_own_controls`)
- [x] Red/Green — the sidebar song row shows its formatted second line; a deleted target shows
      none; the stage `Bait` line uses the same format
      (`multimedia/web/tests.py::ServiceEntryViewTests::test_the_sidebar_song_row_shows_its_verses_on_a_second_line`,
      `::test_a_deleted_song_target_shows_no_sidebar_verse_line`,
      `::test_a_verse_added_after_preparing_shows_the_line_again`)
- [x] Green — implementation (`multimedia/web/reading/formatting.py`,
      `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/tatib.html`,
      `static/web/entries.js`)
- [x] Targeted tests only for the touched classes (`multimedia.web.tests`,
      `tests.e2e.test_tatib_section_break`, `tests.e2e.test_tatib_entry_controls`,
      `tests.e2e.test_reorder`, the two touched `test_entries` cases); the full suite is the
      push/CI step
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header

## Notes

- The two `test_out_of_range_*` cases in `ServiceEntryViewTests` fail under
  `DJANGO_DEVELOPMENT_MODE=1` (sqlite) on a clean `develop` too: the pk-validator lookup raises
  `StopIteration` there. Not this slice's; verified with a stashed tree. The push-time CI run
  (Postgres) is the reference.
