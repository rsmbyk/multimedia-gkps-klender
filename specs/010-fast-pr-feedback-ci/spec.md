# Spec: Fast PR feedback and repository CI

- **ID:** 010
- **Status:** Accepted (owner, 2026-10-06)
- **Item:** ITEM-011
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none

## Intent

Keep local PR iteration fast without reducing test coverage: run the non-browser checks for draft PR updates, and run the complete browser E2E suite in parallel when the PR is ready for review. A full browser run is not required before every intermediate push to a draft PR.

## Scope

### In scope

- Tag all current Playwright test classes under `tests/e2e/` with Django's `e2e` test tag.
- Add a regression test that guards the tagged E2E / non-E2E test split.
- Add a repository GitHub Actions workflow for PRs targeting `develop` or `main`, and pushes to those branches.
- Run Django system checks, migration checks, and all non-E2E tests in a fast job for relevant code/test changes.
- On a code-bearing PR's transition to ready-for-review, run every browser E2E module as an independently reported parallel job; rerun on later code/test changes while the PR is ready.
- Skip browser E2E for docs/spec/backlog/version/changelog-only changes, and cancel stale in-progress test jobs when newer relevant changes arrive.
- Run tests against disposable CI PostgreSQL services only; do not access production data or credentials.
- Update architecture/product documentation to describe the CI lanes and the review merge rule.

### Out of scope

- Changes to application, worship, OBS, or API behavior.
- Removing, weakening, or silently skipping an existing test.
- Changes to the local Compose database guard, production data, or production credentials.
- Enabling automatic branch protection/ruleset enforcement. GitHub currently rejects those settings for this private repository under its plan; until the repository plan/visibility changes, maintainers must manually wait for every test job to pass before merge.

## Domain rules

- The fast lane excludes only tests tagged `e2e`; every other discovered Django test remains included.
- Every test class under `tests/e2e/` carries the `e2e` tag, and every `tests/e2e/test_*.py` module is included in the dynamically generated E2E matrix.
- A draft PR's relevant code/test update runs the fast lane but does not start the full browser suite.
- A code-bearing PR marked ready for review runs all E2E shards on the same head revision as the fast lane. Later relevant code/test updates rerun the test lanes; docs/spec/backlog/version/changelog-only updates do not rerun E2E.
- A successful full-coverage result consists of the fast lane plus every E2E shard passing. Missing Playwright/Chromium must fail the E2E check rather than report a green run with browser tests skipped.
- CI uses an isolated, short-lived PostgreSQL service and contains no production database access or credentials.
- Because branch protection is unavailable, green checks are a manual pre-merge requirement, not an automatically enforced repository rule.

## Acceptance scenarios

### Scenario: Draft PR updates get fast feedback without full browser E2E

- **Given** a draft PR targets `develop` or `main` and changes application/test/CI code
- **When** the PR is opened or receives a relevant commit
- **Then** CI runs `manage.py check`, `makemigrations --check --dry-run`, and all non-E2E Django tests
- **And** the E2E matrix does not run while the PR remains draft
- **And** the fast job targets completion within 10 minutes on a normal GitHub-hosted runner

### Scenario: Ready-for-review PR receives complete browser coverage

- **Given** a relevant code-bearing PR has passed through the draft iteration phase
- **When** it is marked ready for review
- **Then** CI runs every discovered `tests/e2e/test_*.py` module in separate parallel jobs on the same revision
- **And** the full-coverage result is green only when the fast lane and all browser jobs pass

### Scenario: Later changes invalidate prior E2E results

- **Given** a ready-for-review PR has green test jobs
- **When** application or test code changes
- **Then** the fast lane and every E2E shard run again for the new head revision
- **But when** only docs, specs, backlog, `VERSION`, or `CHANGELOG.md` change
- **Then** browser E2E does not run again

### Scenario: Browser setup failure is visible

- **Given** a browser E2E job starts
- **When** Playwright or Chromium cannot be imported/launched
- **Then** the job fails before its test run rather than succeeding with skipped browser tests

### Scenario: CI cannot reach production data

- **Given** any test job runs
- **When** it creates its Django test database
- **Then** the database is an isolated ephemeral PostgreSQL service and no production data or credentials are configured

### Scenario: Merge awaits complete test results

- **Given** a PR has completed fast and E2E jobs
- **When** a maintainer considers merging
- **Then** all fast checks and E2E shards must be green
- **And** this requirement is followed manually because current GitHub plan settings cannot enforce it

## Traceability

- Domain/app tests: `tests/test_ci_test_selection.py` (new; every discovered E2E test class is tagged `e2e`).
- E2E modules: `tests/e2e/test_editor.py`, `tests/e2e/test_entries.py`, `tests/e2e/test_old_rows.py`, `tests/e2e/test_projector.py`, `tests/e2e/test_reading.py`, `tests/e2e/test_reorder.py` (discovered dynamically).
- Implementation: `.github/workflows/ci.yml`; E2E test class decorators; `docs/ARCHITECTURE.md`; `docs/PRODUCT.md`.
