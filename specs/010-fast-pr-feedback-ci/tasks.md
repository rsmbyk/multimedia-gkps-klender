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
- [x] Verify a docs/spec-only synchronization after a successful full run skips E2E (PR #267, run 37420831514; fast lane and CI result passed)
- [x] Verify browser setup is fail-closed: installation and launch preflight are required, uncaught steps; all six shards launched and passed on run 37420513485
- [x] Update `docs/ARCHITECTURE.md` and `docs/PRODUCT.md` to document CI and remove stale “no CI / CI parked” statements
- [x] Run local fast checks: `manage.py check`, `makemigrations --check --dry-run`, and `manage.py test --exclude-tag=e2e --noinput -v 1`
- [x] Stabilize the song-picker E2E search wait; `tests.e2e.test_entries` passes locally (10 tests) and on PR run 37420513485
- [x] Confirm all CI test lanes are green on the final code revision before merge (PR #267, run 37420513485); the owner must enforce this manually under current GitHub plan limits
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: none` on ITEM-011 and this spec; leave `VERSION` and `CHANGELOG.md` unchanged
- [x] Set ITEM-011 and [`backlog/board.md`](../../backlog/board.md) to Done with `Merged: develop` and PR #267 before merge
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [x] Draft PR changes receive fast non-E2E feedback without waiting for browser tests
- [x] A ready-for-review code PR runs all E2E modules in parallel, and later code changes rerun them
- [x] Docs/spec/backlog-only changes do not rerun E2E after a successful full run
- [x] All test modules are represented in CI and browser setup cannot silently produce a skipped green run
- [x] CI uses only disposable PostgreSQL services; no production data or credentials are accessible
- [x] Fast checks and every E2E shard are green before merge; board and tasks are complete in this PR

## Follow-up: Repair CI regressions (ITEM-013)

- [x] Reproduce the missing E2E import and `SynchronousOnlyOperation` failures without an async-safety override
- [x] Restore Playwright startup after per-test ORM setup and shutdown before database teardown; restore the dynamic parallel E2E matrix
- [x] Add a regression test showing unavailable Git revisions result in unknown scope, which schedules full coverage
- [x] Verify the fast lane, a focused browser test, and every E2E shard on the final PR revision
- [x] Verify a push event with an unavailable before-SHA fails closed to full CI coverage
- [x] Move ITEM-013 to Done and check off completed tasks in this PR before merge
