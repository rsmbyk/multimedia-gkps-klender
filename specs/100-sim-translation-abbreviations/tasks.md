# Tasks 100: Use the requested SIM book abbreviations

- **Status:** In Review; Amendment A Draft pending owner acceptance
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
- [x] Conventional Commit + draft PR linking `./spec.md`

## Done when

- [x] All nine acceptance scenarios in `spec.md` hold on online and saved-copy paths named
      there
- [x] The focused data, server, and browser checks are green
- [x] Board, tasks, superseded-spec notes, and version metadata are complete in the same PR

## Draft Amendment A — projector Go To edition selection

- [x] Record the requested result labels and translation selection as a Draft amendment to Spec 100
- [x] Preview edition-specific Go To results and both states for a shared code
- [ ] Owner accepts Amendment A
- [ ] Red — cover `Pah 1` → `Panguhum 1` → SIM and `1Ta 2` → `1 Tawarikh 2` → TB,
      shared `Rut 1` results for TB and SIM with dimmed suffixes when names collide, and
      edition-specific verse references, in `tests/e2e/test_projector.py`
- [ ] Green — carry a uniquely matched abbreviation's edition from `lookup()` into its
      suggestion label and passage detour, return both edition matches for shared codes, and
      render a muted edition suffix for duplicate full names in
      `static/web/projector-library.js`
- [ ] Preserve Go To cycling and flip control, and prevent cross-edition substitution when a
      matched edition lacks the requested position
