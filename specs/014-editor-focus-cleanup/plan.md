# Plan 014: Clear stale row-edit visibility after modal close

- **Status:** Accepted (owner, 2026-10-07)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-016
- **Bump:** patch

## Why

After closing a create/edit modal, a song or songbook's row edit button can remain revealed without pointer hover until another click. The shared shell has several modal and sidebar paths, so the fix must cover the underlying focus/hover behavior rather than one row.

## Scope / edges

**In:** pointer- and keyboard-driven close behavior for songbook, song, Tata Ibadah, service-entry, legacy-item, and confirmation modals; row actions in the three sidebars and service pane.

**Out:** changing which records are editable, removing keyboard focus indicators, changing modal content or save semantics.

## Approach

- Trace focus restoration from modal open/close through successful in-place refresh, and compare it with the CSS rules that reveal row actions.
- Keep hover-only visibility tied to actual pointer hover. After pointer-driven close/save, do not leave a row action revealed by stale focus; preserve keyboard focus and the `:focus-visible` affordance for keyboard users.
- Add Playwright regressions covering cancel, Escape, backdrop, and save paths across the shared modal families and idle sidebars.

## TDD

- E2E: `tests/e2e/test_editor.py`, `tests/e2e/test_entries.py`, `tests/e2e/test_old_rows.py`, and `tests/e2e/test_projector.py` as appropriate.
- Focused verification only while drafting/implementing; defer the full browser suite to push verification per owner preference.

## Risks

- An unconditional blur can break keyboard accessibility. Track input modality and assert that keyboard-driven focus remains visible and operable.
- Save refresh replaces sidebar rows; verify focus is not reattached to the replacement button after a pointer save.
