# Plan 048: Make the passage book search hide non-matching books

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-050
- **Bump:** patch

## Why

The passage book picker accepts a search query but leaves non-matching books visible. The filter in
`static/web/entries.js` sets `option.hidden`, but `.editor__songoption--book` in
`static/styles/design/components.css` sets `display: flex`, which overrides the browser's default
hidden display rule. The reading page loads the design styles without the legacy Fomantic stylesheet;
before this fix, the design stylesheet had no explicit hidden rule for these book options.

## Scope / edges

**In:**

- Hide every non-matching book option while a query is entered.
- Keep matching against both TB and SIM book names, regardless of the selected edition.
- Hide empty testament groups, show the no-match hint only when no books match, and restore the
  full list when the query is cleared.

**Out:**

- The song picker, chapter / verse pickers, and any visual redesign of the dropdown.

## Approach

- `static/styles/design/components.css` — add an explicit `[hidden]` display rule for book options
  so the existing `filterBooks()` state controls what is actually rendered.
- `tests/e2e/test_entry_pickers.py` — cover a matching book and a non-matching book together; check
  TB-name and SIM-name searches, no matches, and clearing the query.
- Leave the existing filter logic in `static/web/entries.js` unchanged unless the regression test
  shows it also needs correction.

## TDD

- Domain/app tests: N/A — client-side visibility behavior.
- E2E: `tests/e2e/test_entry_pickers.py` — only matching books are visible; both names match; no
  matches show the hint; clearing restores every book.

## Risks

- The fix must beat the option's author `display:flex` rule; merely setting the `hidden` attribute
  reproduces the reported behavior.
- The regression test failed with the hidden option still visible when the explicit `[hidden]` rule
  was removed, then passed with the rule restored. The focused E2E test ran in the local web
  container after installing Playwright's missing Debian browser libraries; the full E2E suite was
  not run.
