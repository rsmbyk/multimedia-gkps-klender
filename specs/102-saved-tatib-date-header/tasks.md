# Tasks 102: Show the Tata Ibadah date header in the saved-copy reading path

- **Status:** Accepted (owner, 2026-10-17)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`fix/102-saved-tatib-date-header`)
- [x] Red — E2E: `tests/e2e/test_offline_library.py` — add
      `test_saved_dated_tatib_reading_keeps_its_date_header` with a dated service created in the
      test (`date(2026, 8, 23)`, name `Ibadah Minggu III`), the library made ready
      (`wait_for_offline_ready`), and four assertions: the saved-copy render's `#readEyebrow`
      (`GKPSOfflineRender.render('/tatib/<id>/')`), the sidebar click path
      (`expect(...).to_have_text('23 Agustus 2026')`), the undated service still reading
      `Tata Ibadah`, and the dated service under `?mode=template` still reading the date
- [x] Green — implementation: `static/web/offline-render.js` — `servicePage()` writes the eyebrow from
      `service.date` via `dateParts()`/`MONTHS_LONG` after its `common(...)` call, falling back to
      `Tata Ibadah`
- [x] Run the `OfflineLibraryE2ETests` class (browser E2E is the CI step; locally, only this class)
      — 17 tests, OK (40s, local)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on the ITEM and spec header
- [x] If bump is not `none`: `VERSION` (1.13.4), changelog `## [1.13.4]`, and `release_version` in **this PR**
- [x] Create ITEM-102 and update [`backlog/board.md`](../../backlog/board.md) in **this PR**
      (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] All acceptance scenarios in spec.md hold
- [ ] Tests named above are green
- [ ] Board, tasks, and version (if any) are complete in this PR
