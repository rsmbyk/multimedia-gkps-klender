# Plan 043: Fix the passage modal book picker's search filter

- **Status:** Draft
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-045
- **Bump:** patch

## Why

The book picker's search box does nothing: `filterBooks()` sets `option.hidden`, but
`.editor__songoption { display: block }` overrides the `hidden` attribute, so the option never
disappears. Fix the visibility, and widen the match to both names the picker shows after spec 041.

## Scope / edges

**In:**

- Typing in the book picker's search hides non-matching books and shows the matches; clearing it
  restores the list.
- The match covers the TB name and the SIM name (the option's secondary, per spec 041).

**Out:**

- The song picker's search (it fetches, and already filters).
- The chapter / verse selects.

## Approach

- `static/styles/design/components.css` — make the option honour `hidden` like the menu and the
  group already do: add `.editor__songoption[hidden] { display: none; }` (or switch the option to a
  hidden class).
- `static/web/entries.js` — `filterBooks()` currently matches `option.dataset.bookName`; extend it to
  also match the SIM/secondary name (a `data-*` from spec 041, or the option's text). Keep it
  case-insensitive and keep the group-hiding and the "No matching books" hint in step.

## TDD

- Domain/app tests: N/A — client-side filtering; the fragment markup is unchanged.
- E2E: `tests/e2e/test_entry_pickers.py` — type a TB name and a SIM name; only matching books remain;
  clear; the full list returns.

## Risks

- **The `[hidden]` trap.** The whole bug is author `display` beating `[hidden]`; the fix must win on
  specificity (or use a class), not merely set the attribute.
- **Two names.** The match key must include the SIM name, or a SIM-only query finds nothing once
  spec 041 lands.
