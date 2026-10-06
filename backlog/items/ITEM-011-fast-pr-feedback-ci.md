---
id: ITEM-011
status: in_review
title: 'Fast PR feedback and repository CI'
type: chore
priority: P1
effort: M
created: 2026-10-06
updated: 2026-10-06
spec: specs/010-fast-pr-feedback-ci/spec.md
branch: feat/010-fast-feedback-ci
pr: 267
archived_at:
archive_reason:
bump: none
release_version:
---

# ITEM-011: Fast PR feedback and repository CI

## Summary

Shorten the local wait before opening or updating a PR without dropping test coverage. Add a fast test lane for draft PR updates and run the full browser E2E suite in parallel when a code-bearing PR is ready for review; rerun it when code changes after that point.

## Notes

- The latest full Django run took about 28 minutes; browser tests account for most of that time.
- At spec time, the suite had six Playwright E2E modules under `tests/e2e/` and the repository had no test workflow.
- GitHub currently rejects branch protection/ruleset configuration for this private repository on its plan. CI can report results, but cannot automatically block merge; the owner must wait for all checks to pass unless repository plan/visibility changes.
- Do not change the local Compose database guard or use production data/credentials in CI.

## Acceptance sketch

- Draft PR code changes run Django checks, migration checks, and all non-E2E tests without launching a browser.
- Marking a code-bearing PR ready starts the browser E2E modules in parallel; later code changes rerun them. Docs/backlog-only changes do not rerun E2E.
- All test files under `tests/e2e/` are covered automatically, and missing browser tooling fails the E2E check rather than silently skipping browser tests.
- The full test coverage is green before merge by review policy; the repository cannot technically enforce that policy on its current GitHub plan.
- CI uses an isolated ephemeral PostgreSQL service and no production credentials.

## Links

- Spec: [`specs/010-fast-pr-feedback-ci/spec.md`](../../specs/010-fast-pr-feedback-ci/spec.md)
- Related: `requirements-dev.txt`, `tests/e2e/`, `docs/ARCHITECTURE.md`
