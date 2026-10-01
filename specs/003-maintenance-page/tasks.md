# Tasks 003: Maintenance page at the site root

- **Status:** Accepted
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner (including the plan's three decisions)
- [x] Branch from `develop` (`feat/003-maintenance-page`)
- [x] Red — `multimedia/web/tests.py`: `MaintenanceModeTests` for `/` on/off,
      temporary home, and unaffected surfaces
- [x] Green — `multimedia/settings.py`: `MAINTENANCE_MODE`
- [x] Green — `multimedia/web/views.py`: `IndexView` (maintenance **or** home)
- [x] Green — `multimedia/web/urls.py`: home at `home/` (`web-home`), root at
      `''` (`web-index`)
- [x] Green — `multimedia/web/templates/reading/maintenance.html`
- [x] Green — unit tests pass
- [x] Red — E2E: move `tests/e2e/test_reading.py` flows to the temporary home
      and add the maintenance-page test
- [x] Green — E2E (skips cleanly without a browser; verified by hand instead)
- [x] `docs/ARCHITECTURE.md`: record the new URL roots and `MAINTENANCE_MODE`
- [x] `docs/GLOSSARY.md`: **Maintenance page** and **Temporary home** terms
- [x] `specs/001-public-songs-reading/spec.md`: additive note that the home
      scenario is conditionally superseded by spec 003 (preserve the body)
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump` on the ITEM and spec header (`minor`)
- [x] `bump` is `minor`: `VERSION` `0.6.0` → `0.7.0`, changelog `## [0.7.0]`,
      and `release_version` on ITEM-004 — in **this PR**
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in **this PR**
      (In review while open; Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra
      commits fine)

## Done when

- [x] All acceptance scenarios in spec.md hold
- [x] `python manage.py test` green (E2E skipped without a browser)
- [x] `/` verified by hand in both maintenance states
- [x] Board, tasks, and version are complete in this PR
