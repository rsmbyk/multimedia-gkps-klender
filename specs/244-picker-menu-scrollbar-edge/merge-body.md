The entry modal's Book search and Chapter/verse popouts painted the 5px scrollbar inside the
menu's 8px padding, so the bar floated inside the panel instead of belonging to its edge. The
options scrollport now reaches the menu's inner right and bottom borders (only the 1px border
remains), the lane is clipped to the 10px radius, and compensating padding keeps every option,
heading and filter exactly where it was. A one-option menu still draws no bar.

**Spec**: 244 (`specs/244-picker-menu-scrollbar-edge/spec.md`), accepted at both gates.
**Capability**: `reading/R59` modified — search, filtering, Tab commit and scroll-follow unchanged.
**Verification split**: 14 test · 5 inspection · 0 manual.
- Focused `tests/e2e/test_picker_menu_scrollbar_edge.py`: 4/4 green on the merged tree; on unmodified
  base three edge tests fail `9 != 1` for the reported reason and the content-guard test passes.
- `tests.e2e.test_passage_search_pickers`: 19/19 green. `tests.e2e.test_song_entry_pickers`: 11/12
  green; `test_hidden_and_muted_states` fails identically on unmodified base (pre-existing).
- Live geometry: Book/Chapter scrollport right/bottom 929/883 → 937/891 against menu 938/892;
  verse 706/883 → 714/891 against 715/892. First option and chapter filter boxes unchanged.
  Dark and flipped menus measured at 1px/1px.

**Board**: ITEM-259 — `Done` (`status: done`, `closed_at`, `closed_reason: merged into develop (PR #625)`, board row `develop via [#625]`), merged with this PR.
**Bump**: patch (declared at Plan; applied immediately before merge).

Refs ITEM-259
