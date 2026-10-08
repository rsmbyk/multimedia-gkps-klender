# Tasks 013: Remove songbook language and merge duplicate songbooks

- **Status:** In progress (owner accepted, 2026-10-07)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner
- [x] Branch from the current base (`feat/013-songbook-language-removal`)
- [x] Red — migration regression tests in `multimedia/songs/test_migrations.py`: merge duplicate books, preserve IDs/verses/references, resolve number collisions deterministically, choose keeper, enforce unique names
- [x] Green — data/schema migration and model updates in `multimedia/songs/`
- [x] Red — exact book API payload regression in `multimedia/api/songs/tests.py`; editor behavior in `multimedia/web/tests.py`
- [x] Green — serializers, forms, admin, search/order consumers and fixtures
- [ ] Red/green — E2E in `tests/e2e/test_editor.py` (or mark N/A in the accepted spec)
- [x] Run `manage.py check`, `makemigrations --check --dry-run`, focused tests and migration verification on a disposable local database
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: major` on ITEM-015 and this spec; update `VERSION`, changelog, and `release_version` to 1.0.0 in PR #275
- [x] Update ITEM + [`backlog/board.md`](../../backlog/board.md) in PR #275
- [x] Conventional Commit + draft PR #275 linking `./spec.md`

## Done when

- [ ] Every acceptance scenario in spec.md holds
- [ ] Migration tests prove no songs, verses, or Song IDs are lost and all tests named above are green
- [ ] Board, tasks, and version are complete in the implementation PR
