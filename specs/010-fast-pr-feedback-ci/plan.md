# Plan 010: Fast PR feedback and repository CI

- **Status:** Accepted (owner, 2026-10-06)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-011
- **Bump:** none

## Why

The most recent full Django run took about 28 minutes, with browser-based tests accounting for most of the wait. Running that whole suite locally before every PR update delays feedback and PR creation. The repository had no test CI workflow. Run fast non-browser checks for draft-PR updates, then distribute the browser E2E suite across parallel CI jobs when a code-bearing PR is ready for review.

## Scope / edges

**In:**

- Mark the existing Playwright test classes with a Django `e2e` tag and protect the fast/full test split with a unit test.
- Add a GitHub Actions workflow for Django checks, migration checks, non-E2E tests, and browser E2E tests.
- Run the fast lane on code/test changes to PRs targeting `develop` or `main`; run E2E only once a PR is ready for review, and rerun it after subsequent code/test changes.
- Discover and shard every `tests/e2e/test_*.py` module dynamically so new E2E modules are not omitted.
- Skip E2E for docs/backlog-only changes, cancel stale runs after newer code pushes, and use an isolated ephemeral PostgreSQL service.
- Update architecture/product documentation with the implemented test workflow.

**Out:**

- Changes to worship, OBS/API, or other application behavior.
- Removing, weakening, or silently skipping existing tests.
- Changes to the local Docker Compose database guard or use of production databases/credentials in CI.
- Changes to GitHub plan, repository visibility, or branch-protection settings. The current plan does not permit branch protection/rulesets for this private repository; until that changes, maintainers must manually wait for all required test jobs to pass before merging.

## Approach

- Apply the `e2e` tag to all test classes in `tests/e2e/`; fast tests use Django's `--exclude-tag=e2e`. The current Django test runner supports this option.
- The fast job runs Python 3.12, `manage.py check`, `makemigrations --check --dry-run`, and the complete non-E2E test set. Target a fast-job result within 10 minutes on a normal GitHub-hosted runner.
- A separate E2E matrix discovers each `tests/e2e/test_*.py` module and runs one module per job, with Playwright Chromium installed and a browser-launch preflight. Matrix jobs run in parallel with the fast job. A browser setup failure must fail the job, not become an all-skipped green result.
- Draft PR updates run the fast lane but not browser E2E. On `ready_for_review`, run all E2E shards; if code/test changes arrive after that, rerun them. Changes limited to docs, specs, backlog, `VERSION`, or `CHANGELOG.md` do not rerun E2E.
- Trigger CI on relevant PR changes to `develop`/`main` and relevant pushes to those integration/production branches. Cancel older in-progress runs for the same PR/ref.
- Use a disposable PostgreSQL service per CI job; do not pass production data or credentials to GitHub Actions.
- To merge, verify the fast job and every E2E shard are green. This is a human-enforced merge rule unless repository settings become available to enforce required checks.

## TDD

- Domain/app tests: add `tests/test_ci_test_selection.py` to assert that discovered test classes under `tests/e2e/` carry the `e2e` tag; first demonstrate it failing, then tag the classes.
- E2E (tool named after stack exists): no new product-facing acceptance. Run the existing `tests/e2e/test_*.py` modules in the CI matrix and verify all browser checks execute.
- Workflow verification: validate both the fast-only draft path and ready-for-review full-coverage path on a test PR; verify docs-only tracking changes skip E2E.

## Risks

- GitHub Actions runners have variable startup and dependency-install times; the 10-minute fast-lane target is a measurement to verify, not a guaranteed SLA.
- E2E modules have uneven runtimes; record shard wall time on the first workflow run and rebalance only if the slowest shard remains a bottleneck.
- GitHub does not permit branch protection/rulesets on this private repository under the current plan, so a green result cannot be made an automatic merge prerequisite without changing plan/visibility.
