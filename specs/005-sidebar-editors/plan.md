# Plan 005: Sidebar editors for Kidung and Tata Ibadah

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-006
- **Bump:** minor

## Why

The public site is read-only, and the corpus it reads (songbooks, songs, Tata Ibadah) is
maintained elsewhere — today only through the Django admin, which this repo's specs put out of
scope for the public shell. The people who notice a wrong lyric or need Sunday's order are the
people reading the site, so the editing belongs where the material is.

## Scope / edges

**In:** add and edit for songbooks, songs (within their songbook) and Tata Ibadah services,
through modals in the reading design; server-side forms with the models' own constraints;
CSRF; an optional login gate behind one setting.

**Out:** delete/archive, Bible editing, Tata Ibadah *items* (their contents rows stay
quicklinks), bulk import, revision history, a permissions model.

## Approach

- A new `multimedia/web/reading/editors.py` holds `ModelForm`s for the three records plus the
  accept/reject helpers; views live beside the reading views and are POST-only, rendering
  either the form with errors or a "saved" result.
- Modal chrome is hand-written in the reading design language (`<dialog>`-free: a positioned
  panel with a scrim, focus trap, Escape, and focus returned to the control that opened it),
  in `components.css` and a new `static/web/editors.js`.
- The shell keeps owning navigation: `reading.js` dispatches a `shell:applied` event after
  every in-place page swap, `editors.js` binds the add button and the row controls from it.
  On a successful save the modal closes and the shell re-syncs the current page, so the lists,
  panel selection and reading stage all agree without a reload.
- Hymn gating is read from the data (`Book.is_hymn_book`), so the template simply never emits
  an edit control for a hymn songbook or a song whose book is one.
- `SIDEBAR_EDITORS_REQUIRE_LOGIN` (default off, the owner's decision) hides the controls from
  anonymous visitors and rejects their writes when on.

## TDD

- Domain/app tests: `multimedia/web/tests.py` — create/update through the endpoints for each
  record; duplicate short name, duplicate song number and hive number requirements rejected;
  CSRF enforced; the login hook hides the controls and returns 403; a hymn songbook renders no
  edit control while a non-hymn one does.
- E2E: `tests/e2e/test_editor.py` — the three add flows, one edit flow, the hover/focus
  reveal, keyboard operation, the error path, and that the reading stage survives a save.

## Risks

- **Public writes (accepted by the owner).** Anyone who can reach the site can change the
  corpus. Mitigations kept cheap: the login hook, mirrored model constraints, CSRF, and a
  one-line switch documented in the spec. This is the risk to revisit first if the site is
  exposed beyond the team.
- **Shell coupling.** The editors depend on the shell's swap events; if a future change stops
  dispatching `shell:applied`, the controls go inert (they fail closed, not silently half-work).
- **Parity drift.** The new buttons and row controls change the sidebars, so the mockup parity
  harness must exempt them like the earlier named deviations, or the gate turns permanently red.
