# Plan 089: Name the preview's tabs container so it cannot be mistaken for a tab

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-092
- **Bump:** patch

## Approach

Three string changes, no logic:

1. `_preview_modal.html` — `<div class="preview__tabs-host" data-preview-tabs-host hidden>` becomes
   `<div class="preview__versetabs" data-preview-tabs-host hidden>`.
2. `components.css` — the three selectors naming the container (the shared `[hidden]` rule, the layout
   rule, and the narrow-width rule) take the new name.
3. Nothing else: `preview.js` finds the container through its data attribute, and the tabs and buttons
   keep their names.

## Alternatives considered

- **Tighten the test** to `assertNotIn('class="preview__tab"', html)`. Works, but it edits a
  pre-existing assertion from another slice to accommodate a name chosen in this one, and leaves the
  next reader wondering why the check is so specific.
- **Drop the container and append the tabs straight into the header.** Loses the slot that keeps the
  tabs on their own line under the heading at narrow widths.
- **Give the tabs a different class.** Touches the tab markup, the tablist styling and both E2E selectors
  for the tabs — a larger blast radius than naming the empty slot.

## Verification

- Red: `multimedia/web/tests.py::ServiceEntryViewTests.test_a_song_preview_has_no_tabs_for_a_single_verse`
  fails on `develop` today (`'preview__tab' unexpectedly found`). Its positive twin passes and must stay
  passing.
- Green: the pair plus the whole `tests/e2e/test_entry_preview.py` module. A spike on a throwaway
  worktree at `develop` (discarded) ran both unit tests and that module: 20 tests, OK.
