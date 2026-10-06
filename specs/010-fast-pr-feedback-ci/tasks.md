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
- [x] Add `.github/workflows/ci.yml`: fast job, dynamic E2E module matrix, change-scope detection, ephemeral PostgreSQL, Playwright/Chromium preflight, stale-run cancellation, and full-coverage summary
- [ ] Verify a draft PR code change runs fast checks only; verify ready-for-review starts all E2E shards; verify a docs/backlog-only change does not start E2E
- [ ] Verify Playwright/Chromium setup failures make E2E jobs fail rather than silently skip browser tests
- [x] Update `docs/ARCHITECTURE.md` and `docs/PRODUCT.md` to document CI and remove stale “no CI / CI parked” statements
- [x] Run local fast checks: `manage.py check`, `makemigrations --check --dry-run`, and `manage.py test --exclude-tag=e2e --noinput -v 1`
- [ ] Confirm all CI test lanes are green on the final code revision before merge; the owner must enforce this manually under current GitHub plan limits
- [x] Fill Traceability in `./spec.md`
- [x] Set `bump: none` on ITEM-011 and this spec; leave `VERSION` and `CHANGELOG.md` unchanged
- [x] Set ITEM-011 and [`backlog/board.md`](../../backlog/board.md) to In review with PR #267 (move to Done before merge)
- [x] Conventional Commit + draft PR linking `./spec.md` (same PR; extra commits fine)

## Done when

- [ ] Draft PR changes receive fast non-E2E feedback without waiting for browser tests
- [ ] A ready-for-review code PR runs all E2E modules in parallel, and later code changes rerun them
- [ ] Docs/backlog-only changes do not rerun E2E
- [ ] All test modules are represented in CI and browser setup cannot silently produce a skipped green run
- [ ] CI uses only disposable PostgreSQL services; no production data or credentials are accessible
- [ ] Fast checks and every E2E shard are green before merge; board and tasks are complete in the same PR
