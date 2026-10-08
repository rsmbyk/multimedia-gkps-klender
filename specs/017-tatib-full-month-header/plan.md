# Plan 017: Show a full month name in the Tata Ibadah date header

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-019
- **Bump:** patch

## Why

The date above a Tata Ibadah title should be readable at a glance and should not abbreviate the month.

## Scope / edges

**In:** Full Indonesian month name in the service page eyebrow/header above the title.

**Out:** Sidebar grouping/date labels, search excerpts, form picker display, undated-service label.

## Approach

Use the existing Indonesian long-month vocabulary in the server-rendered service context, extending the date formatter only if needed. Pin one exact date/header result in a focused app or browser test.

## TDD

- App/E2E: `tests/e2e/test_reading.py` (`ReadingE2ETests`) and/or a focused format test in `multimedia/web/tests.py`.

## Risks

The header is updated in-place by the shell; assert the click-through reading path as well as the directly rendered page if the relevant response fragment is swapped.
