# Analysis — 130-empty-service-tiles

**Coverage**: every `FR-###`, `SC-###` and acceptance scenario in `spec.md` is traced in `plan.md`; none is
unowned. **CRITICAL: 0.**

## Findings

| Severity | Finding | Where |
| --- | --- | --- |
| HIGH | The saved page and the server route can be drawn in differently wide reading columns, so the existing parity test's absolute-coordinate comparison stopped meaning anything once the tiles stood in a row. It now compares label, glyph count and square size, and waits for the saved row before counting. | `tests/e2e/test_saved_render_parity.py` |
| HIGH | The row's arrangement is width-dependent by design (five, then three and two). A test that pins "one row" at every viewport would contradict FR-005; the E2E test asserts one row at 1440×900 only, and the narrow case is an inspection with numbers. | `spec.md` FR-005, `plan.md` traceability |
| MEDIUM | `tests/e2e/test_saved_render_parity.py::test_offline_sidebar_open_has_server_labels_without_reload` fails at its *song page* step (`#readEyebrow` empty) on unmodified `develop` as well — three runs of three on a clean worktree. It is not caused by this slice and it is not fixed by it. | reported, not touched |
| MEDIUM | `multimedia.web.tests.ServiceReorderPaneTests` (6 errors) needs a `collectstatic` or the `StaticFilesStorage` override locally: `Missing staticfiles manifest entry for 'assets/gkps.png'`. Environmental, unchanged by this slice. | reported, not touched |
| LOW | The `Add Break` glyph reads as a sparkle at 22px to a first-time viewer; it is the pre-existing glyph and the tooltip names it. Changing it is a different slice. | `tatib.html` |
| LOW | With the sidebars' `+ Passage` / `+ Song` / … rows still labelled and the empty page's tiles unlabelled, the two surfaces teach different vocabularies. Deliberate: the add rows sit between items the operator is reading, the tiles are the page's only content. | `spec.md` § UI/UX |

## Coverage

| Requirement | Test | Status |
| --- | --- | --- |
| FR-001 | `test_an_empty_service_centres_a_row_of_square_icon_buttons` | green |
| FR-002 | same | green |
| FR-003 | same | green |
| FR-004 | `test_saved_render_parity` `icon_count` 5 | green |
| FR-005 | inspection at 1280×800 / 1024×700 (52px, 3 + 2) | recorded |
| FR-006 | `test_offline_sidebar_open_has_server_labels_without_reload` — blocked by the pre-existing failure above; `test_empty_saved_tatib_shows_add_media_after_sidebar_navigation_offline` covers the saved empty row's glyph and label | green (saved path), blocked (parity test) |
| FR-007 | inspection, service `/tatib/144/` before and after: header 80.7px, margin 30px, body margin 8px, identical | recorded |

## Runs

- `tests.e2e.test_entries`, `multimedia.web.tests`: 265 tests, 6 environmental errors (manifest), 0 failures.
- `tests.e2e.test_saved_render_parity`: 7 of 8 green; the eighth is the pre-existing failure above.
- `tests.e2e.test_offline_library.OfflineLibraryE2ETests.test_empty_saved_tatib_shows_add_media_after_sidebar_navigation_offline`: green.
- `specs/130-empty-service-tiles/preview/probe_empty_stage.py http://127.0.0.1:8802/tatib/145/`: gaps equal at
  all four viewports, tiles square, smallest 52.0px, labels in order.
