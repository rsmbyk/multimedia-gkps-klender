---
id: ITEM-229
status: in-review
title: 'The copy confirmation is a dialog of its own, and the copy is named there'
type: feat
priority: P1
effort: M
created: 2026-11-21
updated: 2026-11-21
spec: specs/215-copy-template-dialog/spec.md
branch: feat/215-copy-template-dialog
pr: 567
issue: 566
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-229: The copy confirmation is a dialog of its own, and the copy is named there

## Summary

Spec 212 put the Copy as template confirmation inside the edit dialog's own box, so it reads as a
panel covering the form. It should be a second dialog drawn over the Edit Tata Ibadah dialog — which
stays open, dimmed and legible behind it — and it should let the person name the template before it
exists, defaulting to the source's name plus ` (Copy)`, with a click on the field selecting the whole
value so a new name can be typed straight over it.

## Notes

- The owner accepted the shape at `specs/215-copy-template-dialog/preview/index.html` (2026-11-21):
  the card's content is the "takeover" layout's, the layer is the window's, not the dialog's.
- The endpoint currently writes `name=source.name` and takes no name (`views.py`, `tatib_copy_as_template`).
- Spec 167 FR-021 says a copy keeps the name; this slice changes that requirement, so Fold replaces
  both R37 and R47 rather than adding a third.
- Two markers were open at Specify: an over-long default name, and whether the scrim dismisses.

## Acceptance sketch

- The confirmation's layer covers the window and its card is centred on the window; the edit dialog
  stays open behind it, dimmed but legible, and inert.
- The dialog carries a Name field holding `<source name> (Copy)`; a click selects all of it; typing
  replaces it; a second click places a caret.
- Accepting creates the template under the typed name; an empty name cannot be accepted.
- The edit dialog's height is unchanged by opening or closing the confirmation.

## Links

- Spec: [215](../../specs/215-copy-template-dialog/spec.md)
- Related items: ITEM-181 (a Tata Ibadah is a service or a template), ITEM-226 (the confirmation as a
  layer of the dialog), ITEM-201 (Copy as template in the modal header)
