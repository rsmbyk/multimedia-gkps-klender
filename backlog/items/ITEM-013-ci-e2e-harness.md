---
id: ITEM-013
status: in_review
title: 'Restore reliable CI and E2E execution'
type: fix
priority: P1
effort: M
created: 2026-10-06
updated: 2026-10-06
spec: specs/010-fast-pr-feedback-ci/spec.md
branch: fix/013-ci-e2e-harness
pr: 271
archived_at:
archive_reason:
bump: none
release_version:
---

# ITEM-013: Restore reliable CI and E2E execution

## Summary

Repair regressions in the accepted CI workflow: E2E module import/discovery, Django ORM access while Playwright's sync event loop is active, and push-scope detection when the previous commit is unavailable.

## Notes

- These are implementation defects against accepted Spec 010, not a new CI capability.
- `DJANGO_ALLOW_ASYNC_UNSAFE` is not an acceptable fix; keep Django's async-safety guard enabled.
- Restore the previously green per-test Playwright lifecycle and parallel E2E matrix, while making unknown Git comparisons fail closed to full test coverage.

## Acceptance sketch

- The fast lane imports every E2E module and the tag-discovery regression test passes.
- Each E2E test completes Django ORM setup before starting Playwright and stops Playwright before Django database teardown.
- Every discovered `tests/e2e/test_*.py` module remains scheduled in the parallel browser matrix; missing browser tooling still fails closed.
- If a push's previous SHA is unavailable, change detection requests the full test lanes instead of failing or suppressing coverage.
- No async-safety override is required; the fast lane and every E2E shard pass on the final PR revision, and a push to `develop` completes CI successfully.

## Links

- Spec: [Spec 010 — Fast PR feedback and repository CI](../../specs/010-fast-pr-feedback-ci/spec.md)
- Related: [ITEM-011 — original CI implementation](./ITEM-011-fast-pr-feedback-ci.md)
- Pull request: [#271](https://github.com/rsmbyk/multimedia-gkps-klender/pull/271)
