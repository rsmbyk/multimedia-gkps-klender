---
id: ITEM-091
status: done
title: Keep the contents pane following the page on a stage-only swap
type: fix
priority: P1
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/088-sidebar-state-guard-beyond-nav/spec.md
branch: fix/088-sidebar-state-guard-beyond-nav
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/342
archived_at:
archive_reason:
bump: patch
release_version: 1.10.9
---

# ITEM-091: Keep the contents pane following the page on a stage-only swap

## Summary

Spec 080 (PR #334) made a stage-only swap preserve the sidebar state, but it preserved both levels:
the first-level panel — which is what the operator reported — and the second-level contents pane.
Opening a Tata Ibadah service from the first-level panel therefore leaves its contents pane closed and
its rows invisible.

## Notes

- Found by the post-merge full suite on `develop`: 585 tests, 2 failures, 3 errors. Two of the errors and
  one failure are pre-existing on the merge base (`4a61b58`) under `DJANGO_DEVELOPMENT_MODE=1`; this one is
  not.
- `tests/e2e/test_reading.py::ReadingE2ETests.test_service_text_sidebar_shows_two_lines_and_centers_grip`
  fails on `develop` and passes at `4a61b58`.
- Specs 080's own cases must keep passing; they are the guard against over-correcting.

## Acceptance sketch

- A service opened from the first-level panel arrives with its contents pane open and its rows visible.
- The first-level state (open / mini / closed) is still preserved on every stage-only swap.

## Links

- Spec: [../../specs/088-sidebar-state-guard-beyond-nav/spec.md](../../specs/088-sidebar-state-guard-beyond-nav/spec.md)
- Related items: ITEM-083 (spec 080)
