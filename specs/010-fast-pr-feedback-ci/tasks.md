# Tasks 010: Fast PR feedback and repository CI

- **Status:** Accepted (owner, 2026-10-06)
- **Plan:** [./plan.md](./plan.md)
- **Spec:** [./spec.md](./spec.md)

<!-- Failing test first → implement → green. Check off in order. -->

## Checklist

- [x] Spec Accepted by the project owner (2026-10-06)
- [x] Continue on `feat/010-fast-feedback-ci`, based on current `origin/develop`
- [x] Red — add `tests/test_ci_test_selection.py` asserting every discovered test class under `tests/e2e/` has the `e2e` tag; verified it failed listing all six untagged classes
- [x] Green — tag E2E classes in `tests/e2e/test_editor.py`, `test_entries.py`, `test_old_rows.py`, `test_projector.py`, `test_reading.py`, and `test_reorder.py`; the regression and fast suite pass (208 tests, no skips)
- [x] Add `.github/workflows/ci.yml`: fast job, dynamic E2E module matrix, change-scope detection, ephemeral PostgreSQL, `collectstatic`, Playwright/Chromium preflight, stale-run cancellation, and full-coverage summary
- [x] Verify draft PR code changes run fast checks only (PR #267, run 37419789515; browser E2E skipped)
- [x] Verify `ready_for_review` runs all six E2E shards and requires them with the fast lane (PR #267, run 37420513485)
- [ ] Verify docs/backlog-only changes after a successful full run do not start E2E
- [x] Verify browser setup is fail-closed: installation and launch preflight are required, uncaught steps; all six shards launched and passed on run 37420513485
- [x] Update `docs/ARCHITECTURE.md` and `docs/PRODUCT.md` to document CI and remove stale “no CI / CI parked” statements
- [x] Run local fast checks: `manage.py check`, `makemigrations --check --dry-run`, and `manage.py test --exclude-tag=e2e --noinput -v 1`
- [x] Stabilize the song-picker E2E search wait; `tests.e2e.test_entries` passes locally (10 tests) and on PR run 37420513485
- [x] Confirm all CI test lanes are green on the final code revision before merge (PR #267, run 37420513485); the owner must enforce this manually under current GitHub plan limits
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: none` on ITEM-011 and this spec; leave `VERSION` and `CHANGELOG.md` unchanged
- [x] Set ITEM-011 and [`backlog/board.md`](../../backlog/board.md) to In review with PR #267 (move to Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Draft PR changes receive fast non-E2E feedback without waiting for browser tests
- [x] A ready-for-review code PR runs all E2E modules in parallel, and later code changes rerun them
- [ ] Docs/backlog-only changes do not rerun E2E
- [x] All test modules are represented in CI and browser setup cannot silently produce a skipped green run
- [x] CI uses only disposable PostgreSQL services; no production data or credentials are accessible
- [x] Fast checks and every E2E shard are green before merge; board and tasks will be moved to Done before merge
