# Plan 100: Use the requested SIM book abbreviations

- **Status:** Accepted; Amendment A accepted and implemented
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-100
- **Bump:** patch
- **Visual preview:** [./preview.html](./preview.html)

## Why

The SIM Bible has full Simalungun book names, but no separate short codes. The mini-sidebar
therefore shows the TB book code even after the reader chooses SIM. In the supplied screenshot,
SIM verses are visible while the testament heading and verse-page title still say “Perjanjian
Lama” and “Kejadian 1.” The owner also wants either edition's short code to find the same book
in the sidebar, projector Go To, and passage editor.

## Assumptions for this Draft

- “Last saved translation” means the last deliberate TB/SIM choice in the current page visit,
  as defined by accepted spec 099. A full refresh starts from TB unless the URL explicitly
  requests an edition.
- The mini-sidebar and its testament headings follow that remembered choice. The verse-page
  heading follows the edition whose verses are actually displayed when a chapter has to fall
  back to TB or SIM.
- The existing full SIM book names, such as “1 Musa,” remain the expanded sidebar and
  verse-page names. “1Mu” is the short code, not a replacement for “1 Musa.”

## Scope / edges

**In:**

- Store the owner's 66 SIM abbreviations on the existing SIM book translation rows, and include
  them in fresh Bible seed data without replacing full translation names.
- Use TB or SIM codes in the mini-sidebar according to the remembered Bible edition, including
  server-rendered and saved-copy reading.
- Use “Perjanjian Lama” / “Perjanjian Baru” in TB and “Padan na Basaia” / “Padan na Baru” in SIM
  for Bible sidebar groups and new/edit passage picker groups.
- Match both abbreviations in the Bible sidebar filter, projector Go To references, and the
  new/edit passage book picker while either edition is selected.
- Use the full book name of the visible verse edition in the Bible chapter heading and browser
  page title, including live switches, direct links, history navigation, and saved-copy reading.
- Switch only the three main rail hover/focus popups with the remembered Bible edition:
  Alkitab/Bibel, Kidung/Doding, and Tata Ibadah/Agenda. Keep their accessible names aligned.
- Keep the prior sidebar state, search behavior, book ordering, selected row, and verse links.

**Out:**

- Replacing full SIM names, changing TB codes or canonical `Book.name` keys, and editing verse text.
- Persisting the Bible edition across a full page reload or a separate tab.
- Automatically running the existing Bible seed workflow as part of deployment.

## Approach

1. Add an optional abbreviation to `BookTranslation`. Populate SIM rows by canonical book key
   through a data migration; the TB short code remains the canonical `Book.name`.
2. Add a SIM abbreviation seed mapping alongside the existing full-name seed, and teach the
   Bible seeder to populate or update the abbreviation on its existing row. Keep seeding
   repeatable without creating another `BookTranslation`.
3. Expose both full names and both short codes in the server book index and offline Bible
   chunks. Render online and saved-copy sidebars with the same edition-aware labels.
4. Let all three named search surfaces use both short codes as aliases. Preserve the existing
   sidebar and picker behavior; apply the accepted Go To edition-selection rules in Amendment A.
5. Update the Bible stage title when its visible verse edition changes, and update testament
   headings when the sidebar or passage picker edition changes. Apply that same remembered
   edition to the three main rail popup labels, including during section switches.
6. On implementation, mark the TB-only mini-tile clauses in accepted specs 092 and 099 as
   superseded by this spec.

## TDD and UI checks

- Data and server behavior: migration/seed coverage in `tests/test_bible_translation_seed.py`
  and focused Bible/passage coverage in `multimedia/web/tests.py`.
- Browser behavior: focused cases in `tests/e2e/test_reading.py`,
  `tests/e2e/test_entry_pickers.py`, `tests/e2e/test_projector.py`, and
  `tests/e2e/test_offline_library.py` for every named surface and fallback state.
- Visual review: the [interactive preview](./preview.html) shows the existing dark reading
  layout with the proposed TB/SIM text changes and the open/mini sidebar states.

## Risks

- The current schema has no per-translation book abbreviation, so replacing
  `BookTranslation.translation` would erase full SIM names needed by the expanded sidebar and
  verse heading. The new field and seed must preserve those names.
- A cached library from before this change has no SIM abbreviation. The offline renderer must
  handle it until the next library sync and then show the new code.
- A remembered SIM preference may coexist with TB verse fallback for one chapter. The sidebar
  stays on the remembered preference; the verse heading names the content actually shown.

## Accepted Amendment A: choose Go To edition matches from their abbreviations

**Status: Accepted by the project owner on 2026-10-16; implemented.** This amends only projector
Go To behavior in accepted Spec 100. The accepted implementation currently resolves both codes
to a book and opens the existing default translation. The requested behavior instead carries the
edition identified by the code through the suggestion and into the opened passage, including both
editions when a code is shared.

- A canonical `Book.name` code identifies TB; a per-translation abbreviation identifies its own
  edition. Carry the identified edition through the suggestion into the opened passage.
- Show the full book name from the matching edition in the Go To suggestion, then open that
  edition when the operator selects it. For example, `Pah 1` shows `Panguhum 1` and opens SIM;
  `1Ta 2` shows `1 Tawarikh 2` and opens TB.
- When a code is shared by TB and SIM, return a separate result for each edition and let the
  existing result cycling reach both. Selecting either result opens its edition. If both results
  use the same full book name, append a muted/dimmed `· TB` or `· SIM` suffix; differing names
  already identify the edition.
- Keep the current Go To controls and translation-flip control. If an exact requested position is
  missing from a matched edition, do not substitute a result from the other edition.
- Cover chapter, verse, and shared-code references in the projector E2E test. The preview
  demonstrates the existing suggestion row with edition-specific labels and an explanatory
  opened-edition note; it introduces no new product control or layout change.
