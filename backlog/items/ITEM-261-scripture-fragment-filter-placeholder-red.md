---
id: ITEM-261
status: backlog
title: 'Scripture fragment test still expects the old book filter placeholder'
type: fix
priority: P1
effort: S
created: 2026-11-26
updated: 2026-11-26
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-261: Scripture fragment test still expects the old book filter placeholder

## Summary

`multimedia.web.tests.ServiceEntryViewTests.test_the_scripture_fragment_groups_searchable_books_by_testament`
asserts `placeholder="Filter books..."` in the response; the rendered fragment no longer carries it.
The failure reproduces identically on unmodified `origin/develop` `fa452197` under
`manage.py test multimedia --keepdb --noinput`.

## Notes

- Base assertion: `False is not true : Couldn't find 'placeholder="Filter books..."' in response`.
- One of the nine unit-lane failures; the other eight are ITEM-217.

## Acceptance sketch

- The assertion follows the current filter control's markup or the control is restored.

## Links

- Spec: —
- Related items: ITEM-217 (the other eight unit-lane reds)
