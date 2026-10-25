---
id: ITEM-137
status: backlog
title: 'The songbook empty-view E2E still expects the old filter copy'
type: fix
priority: P1
effort: S
created: 2026-10-25
updated: 2026-10-25
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-137: The songbook empty-view E2E still expects the old filter copy

## Summary

`tests/e2e/test_reading.py::ReadingE2ETests::test_the_panel_shows_its_empty_view_when_no_songbook_exists`
fails on `develop`: it expects the block to read `No matching songbooks.` for a panel with no rows, while
spec 129 made a list that is both empty and filtered show the *empty* copy (`No songbooks yet.`). The test
was not updated when that rule landed, so the suite has one red browser test.

## Notes

- Found while running the browser suites for spec 132; the failure reproduces on `develop` untouched, and
  it is the only red browser test in that file.
- The behaviour is the acceptable one — the empty copy is what spec 129's `R7` requires for a list that is
  empty before the filter was typed. The test is what is stale, so the fix is the assertion, not the code.
- TDD-09: a red test blocks unless quarantined with a recorded reason and an owner; this card is that
  record.

## Acceptance sketch

- The test asserts the empty copy (`No songbooks yet.` and its hint) for a panel with no rows.
- `tests.e2e.test_reading` is green on `develop`.

## Links

- Spec: none yet (a test-only correction; a docs-only or test-only change may skip the numbered spec)
- Related items: ITEM-132 (the sidebar empty states, spec 129 — the rule this test predates)
