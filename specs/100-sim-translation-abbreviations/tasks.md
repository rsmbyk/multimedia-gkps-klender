# Tasks 100: Use the requested SIM book abbreviations

- **Status:** In Progress
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)
- **Preview:** [./preview.html](./preview.html)

<!-- Failing test first → implement → green. Check off in order after acceptance. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Confirm `fix/100-sim-translation-abbreviations` is based on current `develop`
- [x] Red — cover all 66 codes, existing-row migration, preserved full names/verses, and
      repeatable seeding in `tests/test_bible_translation_seed.py`
- [x] Green — add the `BookTranslation` abbreviation field, data migration, SIM abbreviation
      seed mapping, and seeder update
- [x] Red — cover server-rendered mini codes, testament headings, explicit `?ed=sim`, chapter
      title, and passage picker metadata in `multimedia/web/tests.py`
- [x] Green — expose TB/SIM codes and names in the Bible book index, reading views, and templates
- [x] Red — cover mini/open sidebar behavior, remembered edition, chapter fallback, title
      changes, both sidebar search aliases, three rail popup labels, and no-JavaScript direct links in
      `tests/e2e/test_reading.py`
- [x] Green — update `static/web/reading.js` and the server sidebar markup
- [x] Red — cover both abbreviations and edition-specific testament headings in new and edit
      passage pickers in `tests/e2e/test_entry_pickers.py`
- [x] Green — update picker metadata, template, and `static/web/entries.js`
- [x] Red — cover TB/SIM abbreviated references in projector Go To in
      `tests/e2e/test_projector.py`
- [x] Green — expose aliases in the saved Bible library and `static/web/projector-library.js`
- [x] Red — cover saved-copy mini codes, testament labels, sidebar filtering, and chapter
      headings in `tests/e2e/test_offline_library.py`
- [x] Green — update `static/web/offline-render.js` and offline Bible chunk serialization
- [x] Mark the superseded mini-tile clauses in specs 092 and 099 and fill Traceability in
      `./spec.md`
- [x] Set `bump: patch` on ITEM/spec and include `VERSION`, changelog, and
      `release_version` in the implementation PR
- [x] Update ITEM and [`backlog/board.md`](../../backlog/board.md) in the same PR
- [ ] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [x] All nine acceptance scenarios in `spec.md` hold on online and saved-copy paths named
      there
- [x] The focused data, server, and browser checks are green
- [ ] Board, tasks, superseded-spec notes, and version metadata are complete in the same PR
