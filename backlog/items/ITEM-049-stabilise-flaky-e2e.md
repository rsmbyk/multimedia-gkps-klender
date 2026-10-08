---
id: ITEM-049
status: done
title: 'Stabilise the flaky E2E tests'
type: test
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/047-stabilise-flaky-e2e/spec.md
branch: test/047-stabilise-flaky-e2e
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/284
archived_at:
archive_reason:
bump: none
release_version:
---

# ITEM-049: Stabilise the flaky E2E tests

## Summary

Two Playwright tests read the page mid-animation and so fail intermittently (they have made
`develop` push runs red): the date-picker geometry test reads the calendar before its reposition
lands, and the search-state test reads `window.scrollY` before the restore animation settles. Wait
for the state instead of racing a fixed pause.

## Notes

- **Date picker.** `tests/e2e/test_editor.py::test_date_picker_dropdown_overlaps_the_scrollable_modal_content`
  scrolls the modal content to 0 and immediately reads the calendar's box; `date-picker.js`
  repositions on the content's scroll event (`scroll` listener → `positionCalendar`), which lands
  after the read. Fix: `wait_for_function` until the calendar is 8px below the trigger (or above it).
- **Search state.** `tests/e2e/test_reading.py::test_search_state_survives_sidebar_browsing` restores
  the remembered offset with an animation, then reads `window.scrollY` after a fixed 250ms. Fix:
  wait until the scroll is stable (and has moved) before reading.
- Pre-existing, unrelated to the specs 028–032 work; observed on `#278`'s and `#283`'s develop push
  runs.

## Acceptance sketch

- Both tests pass repeatedly (locally and in CI) with no fixed-pause race.
- No application code changes.

## Links

- Spec: [047 — Stabilise the flaky E2E tests](../../specs/047-stabilise-flaky-e2e/spec.md)
- Related items: ITEM-024 / spec 022 (date picker over the modal), ITEM-021 / spec 019 (search reset)
