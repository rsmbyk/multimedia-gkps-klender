# Plan 090: Keep the Bible book sidebar mini when selecting a book

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-093
- **Bump:** patch

## Why

The Bible book panel is meant to remain mini until the operator expands it. Clicking a different book previously routed through `navigate(..., { kind: 'lists' })`; `applyPage()` then took the arriving page's `data-nav="open"`, so the panel jumped open. The existing chapter-click preservation in spec 080 did not cover this path.

## Scope / edges

**In:** Bible book tile selection while the first sidebar is mini or open; the selected book and arriving chapter list; same-book toggling; the explicit expand control.

**Out:** Songbook and Tata Ibadah list navigation, rail switches, search/results, responsive layout changes, and visual styling.

## Approach

Give Bible book tile navigation its own kind. Preserve the live first-sidebar state for that kind while applying the arriving page's second-pane state and content. Keep the same-book in-place toggle and explicit expand action intact.

## TDD

- Domain/app tests: N/A; this is browser navigation state.
- E2E: Add a Playwright case in `tests/e2e/test_reading.py` with two Bible books. Check a different-book click from mini, chapter contents and selection, same-book close/reopen, and explicit expand. Keep the spec 080/088 sidebar cases green.

## Risks

- A newly selected book must still open its chapter pane; preserving `data-nav` must not preserve stale `data-ch` or stale chapter rows.
- The same-book tile follows a separate in-place path; the test must cover it so the fix does not break its toggle.
