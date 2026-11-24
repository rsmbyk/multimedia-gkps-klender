# Converge: passage search comboboxes

**Spec**: `specs/238-passage-search-pickers/spec.md`
**Plan**: `specs/238-passage-search-pickers/plan.md`

## Convergence results

- **New acceptance module** — `tests.e2e.test_passage_search_pickers`: 11 tests, **11 pass**.
  Covers Book focus/filter/choice, Chapter and From verse filtering and cascade, empty query,
  stored edit values, translation toggle, keyboard and dismissal, and the one-menu-at-a-time rule.
- **Song-picker regression** — `tests.e2e.test_song_entry_pickers`: 10 tests, **9 pass, 1 fail**.
  `test_hidden_and_muted_states` reads 22px where 0px is asserted; the same failure reproduces
  on unmodified base `88b300bf`, so it is not introduced by this slice.
- **Legacy picker module** — `tests.e2e.test_entry_pickers`: migrated from button-trigger
  selectors to the search fields (`#entry-book-search`, `#entry-chapter-search`,
  `#entry-verse_start-search`, `input[type=search]` under each picker, and `get_by_role`
  `searchbox` for the three fields). It remains red from the known `#drawerBackdrop` race
  (`ITEM-174`); the one non-race failure in the layout test (a Book button role lookup) was
  fixed, and the test now matches base exactly: 2 subtest errors at the two narrow widths, 0
  failures at 1200px.
- **Live probes** — `preview/probe.py` and `preview/parity.py` confirmed the measured field and
  menu numbers in the spec's UI/UX table, hidden-select values through the cascade, and Escape
  retaining the chosen label.

## Findings

- **BLOCKER / CRITICAL**: none (0 regression, 0 unknown, 0 high-severity finding).
- Two implementation defects found during live verification and fixed before Gate 2 — stale
  `.is-active` on hidden options, and native Escape clearing a chosen search value (D004/D005).
- One stale test selector (`get_by_role('button', name='Book')`) found in the legacy module and
  fixed; after the fix its results match unmodified base.
- Review of the live preview found a third defect: opening one search combo did not close the
  other pickers' menus (the old button pickers did). `wireSearchCombo.showMenu()` now calls
  `closeMenus(scope)` first; `test_only_one_picker_menu_is_open_at_a_time` pins the rule across
  both search combos and the To verse button picker. Live preview confirmed one open menu at a
  time. The spec gained US4/AC3 and an edge case for this.
- Review of the live preview found a fourth defect: chapter and verse numbers filtered out by
  the query stayed painted but could not be clicked. `.editor__picker-option { display: block }`
  overrode the UA `[hidden]` rule; the missing `.editor__picker-option[hidden] { display: none }`
  author rule was added, matching the book options' existing rule. The two filtering tests now
  assert `:visible` counts, not only the `hidden` attribute.
- **Scope revised after review**: Chapter, From verse and To verse were returned to their
  original button triggers and popout menus, and each menu gained a `type="search"` filter above
  its options (`wireRangeFilter`). Book alone keeps the search combobox. The acceptance module
  was rewritten for the button popovers and gained a To verse filter test: 11 tests, **11 pass**.
  Live preview confirmed `button` triggers, one filter per numeric menu, `12` → 1 chapter and
  hidden chapter `12`. The spec, R59, changelog, data model, contracts and preview notes carry
  the revised scope.
- **Tab commits and advances**: `tabToNextField` was added to `entries.js`, `projector.js` and the OBS dock find handler; the next focus target is read after the choice so a field enabled by that choice (Chapter) is reachable, and option buttons in the closing menu are excluded. Pinned by two new passage tests and one song test: 24 tests run, 23 pass, the single known-red `test_hidden_and_muted_states` unchanged on base.
- **Highlight scroll-follow**: `scrollOptionIntoView` adjusts only `.editor__picker-options`
  `scrollTop` when Arrow keys move `.is-active`, so the row stays visible without moving the
  dialog. Pinned by two new tests; live probe: Book `scrollTop` 0 → 205 after 15 downs and back
  to 181/142 as the highlight moves up, Song `scrollTop` 67 with the active row in view.
- **Numeric popover highlight**: shared `visibleOptions`/`setActiveOption` helpers mark the stored
  (or first) option on open, move it with Arrow keys, scroll it into view and make Tab commit that
  row. Two new pins; live probe: Chapter opened with `1` active, five downs reached `6`, twenty
  downs reached `21` at `scrollTop` 389 with the row in view. 16 passage tests pass, 12 song tests
  with only the known-red base failure.
- The song picker's own code is unchanged, as SC-004 requires.

## Requirements and coverage

| Check | Result |
| --- | --- |
| FR-001…FR-008 | all have a verification driver in `plan.md`; no uncovered requirement |
| US1…US4 | each has an independent test in the new module |
| SC-001…SC-004 | passed: field/menu parity, unchanged payload, no endpoint, song path unchanged |
| Edge cases | disabled options and empty hints inspected in `wireSearchCombo` and covered by tests |
| Plan traceability | 18 test · 12 inspection · 0 manual, all rows resolved |

**Verdict**: converged. Ready for Fold; no follow-up slice required for behaviour found here.
