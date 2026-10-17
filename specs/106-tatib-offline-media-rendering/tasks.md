# Tasks 106: Keep media entries visible in saved Tata Ibadah pages

- **Status:** Implemented; draft PR [#358](https://github.com/rsmbyk/multimedia-gkps-klender/pull/358) open
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Test first → implement → green. -->

## Checklist

- [x] Spec Accepted by the project owner on 2026-10-17
- [x] Branch `fix/106-tatib-offline-media-rendering` from the current feature stack
- [x] Red — offline chunk test failed because the public item omitted `kind`
- [x] Green — serialize the required media metadata in `multimedia/web/reading/offline.py`
- [x] Test-first — saved-renderer E2E for media rows and add actions in `tests/e2e/test_offline_library.py`
- [x] Green — render media entries and `+ Media` / `Add Media` in `static/web/offline-render.js`
- [x] Verify saved-page media icon and add actions after in-place navigation
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: patch` on the ITEM and spec header
- [x] Add `VERSION`, changelog `## [1.14.3]`, and `release_version: 1.14.3`
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR** (In review while open; Done before merge)
- [x] Conventional Commit `6676a6e` + draft PR [#358](https://github.com/rsmbyk/multimedia-gkps-klender/pull/358)
      linking `./spec.md`

## Done when

- [x] All covered acceptance scenarios in `spec.md` hold
- [x] Named targeted tests are green
- [x] Board, tasks, and version metadata are complete in the implementation PR

The offline chunk test showed the expected failure first. The E2E tests were written before the
renderer change; their first run could not start Chromium because the slim test image lacked
browser libraries. They passed after running in a disposable container with the host Playwright
browser cache and its required libraries.
