## What changed

The Media Library page now declares `data-section="media-library"` instead of inheriting the
shell's default Alkitab section. The first Alkitab rail click from the library is therefore a
section change and fetches `/bible/`; it no longer toggles an empty sidebar with "No books yet.".
No endpoint, schema, template, CSS or JavaScript behaviour changes.

## Why

The shell compares a rail tile's `data-panel` with the document's `data-section` to decide between
toggling the current section and fetching another. The library page carried `alkitab` but no
sidebar rows, so the first Alkitab click took the toggle branch.

## Evidence

- Spec: `specs/246-media-library-bible-rail/spec.md`; capability block `reading/R63`.
- Preview: live rail path at gate 1; `preview/probe.py` base vs fixed.
- Tests: `tests.e2e.test_media_library_bible_rail` (red before, green after) plus
  `tests.e2e.test_navigation_pending` — 26 tests green.

Refs #635 (ITEM-263)
