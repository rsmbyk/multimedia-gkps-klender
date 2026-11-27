# Research: entry modal title band

**Spec**: `specs/240-entry-modal-title/spec.md`

## Decision / Rationale / Alternatives / Provenance

**D001 — Scope the fix to headerless large forms.**
- Decision: add one selector requiring both `[data-editor-size="large"]` and
  `:not(:has(.editor__head))`, restoring `padding: 20px 26px` and the 1px divider on
  `.editor__title`; add the matching narrow override.
- Rationale: spec 226 moved the inset to `.editor__head` to kill a double rule in the
  verse editor. `_entry_form.html` has no head; the other large forms do. A scoped
  selector leaves spec 226 untouched and keeps R10's existing numbers.
- Alternatives: (a) wrap the entry title in `.editor__head` — rejected because the head
  puts padding on the head and zeroes the title, so the existing spec-133 test that
  reads the title's padding/divider would have to be rewritten; (b) revert spec 226 —
  rejected because it reintroduces the verse double rule.
- Provenance: `git show 04c6a817 -- static/styles/design/components.css`; live readback
  of all four dialogs on the slice server; red E2E on unmodified `origin/develop`.

**D002 — Keep the existing spec-133 E2E as the primary red.**
- Decision: use `tests/e2e/test_entry_modal_frame.py::test_new_text_dialog_matches_new_media`
  as the regression guard, and add a small module for text-level offsets and the narrow band.
- Rationale: the existing test already failed on the base with the exact mismatch
  (`'0px' != '20px 26px'`), so it proves the regression without new machinery. Text
  offsets need the Range measurement used by spec 226's module.
- Alternatives: rely only on screenshots — rejected; they are not a preview and cannot
  pin the 26/21px offsets.
- Provenance: red run recorded in the spec's gate-1 evidence; `test_verse_modal_header.py:29-54`.

**D003 — Live preview, not static.**
- Decision: serve the change from the slice worktree on port 8790 and inject a
  browser-local override for the "before" readout.
- Rationale: the dialog is fetched and rendered by the server; a static copy cannot
  show the real form and its media-library response.
- Alternatives: static HTML snapshot — rejected because it would not exercise the
  fetched fragment or the real CSS manifest.
- Provenance: SDD-06; `preview/README.md`; gate-1 probe output.

**Unknowns remaining: 0.**
