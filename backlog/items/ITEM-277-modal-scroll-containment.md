---
id: ITEM-277
status: in-review
title: 'An open modal keeps the scroll to itself'
type: fix
priority: P1
effort: S
created: 2026-11-28
updated: 2026-11-28
spec: specs/257-modal-scroll-containment/spec.md
branch: fix/257-modal-scroll-containment
pr: 654
issue: 653
bump: patch
release_version:
---

# ITEM-277: An open modal keeps the scroll to itself

## Summary

Scrolling a modal past the end of its own view — or scrolling a view with nothing to scroll — hands
the wheel to the page behind it, and a nested picker hands it to the editor content under it. Hold
the document while a native dialog is open and contain each modal scrollport so the scroll stays in
the layer the operator is looking at.

## Notes

- The leak was measured in the browser: editor content 600 → 1700, short editor 600 → 2360, and
  picker options moving the editor 0 → 341 while the page went 600 → 1480.
- A top-layer dialog does not chain to sibling reading panes; the document and the enclosing modal
  scrollport are the two real paths. Thirteen scrollports were surveyed in
  `specs/257-modal-scroll-containment/research.md`.
- Rules in `static/styles/design/components.css`: `:root:has(dialog[open]) { overflow: hidden }` and
  `overscroll-behavior: contain` on the named modal scrollports. No JS state is added.
- Gate 1 accepted 2026-11-28; card was promoted to `Ready`, then to `In review` on the push that
  opened PR #654. Tracker anchor #653 was verified absent and created with `board:item`; the PR says
  `Refs #653`, never `Closes`.

## Acceptance sketch

- A wheel at the end of the editor, Preview, picker or media list leaves the document at its opening offset.
- A modal with no scroll range passes no scroll to the page or to its parent scrollport.
- The focused scrollport still reaches its own end; close restores page scrolling without a layout shift.
- Every named modal scrollport computes `contain` while a dialog is open.

## Links

- Spec: [257](../../specs/257-modal-scroll-containment/spec.md)
- Related items: [ITEM-259](ITEM-259-picker-scrollbar-edge.md) (picker edge), [ITEM-236](ITEM-236-song-modal-scrollbar.md) (editor edge).
