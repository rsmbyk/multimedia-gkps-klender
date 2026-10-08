---
id: ITEM-031
status: in_review
title: 'One-screen text entry that auto-fits its font'
type: feat
priority: P2
effort: M
created: 2026-10-08
updated: 2026-10-08
spec: specs/029-single-screen-text/spec.md
branch: feat/029-single-screen-text
pr:
archived_at:
archive_reason:
bump: minor
release_version: 1.1.0
---

# ITEM-031: One-screen text entry that auto-fits its font

## Summary

Add a new service entry kind — a text variant. Where the existing **text** entry splits its body
into screens of two lines before fitting, this kind shows its **entire** text on a **single screen**
and shrinks the font (down to a smallest permitted size) until the whole text fits that one screen.
If the text still does not fit at the smallest size, it is ellipsized rather than allowed to
overflow.

## Notes

- **Kind.** Add a value to `ServiceEntryKind` in `multimedia/tatib/models.py` (0–3 are taken; the
  next is 4). It shares the **text** rules: `clean()` requires non-empty `text`, and `resolve()`
  returns `(title, text)`.
- **Editor wiring.** `multimedia/web/reading/entries.py` — register the kind in `KINDS`, `FORMS`
  (reuse `TextEntryForm`), and `TITLES`; `kind_name()` derives the URL name from the enum name, so
  the enum label sets the URL slug. Add the matching add-button to
  `multimedia/web/templates/reading/tatib.html` (beside Passage / Song / Text / Break).
- **Screens.** `multimedia/web/reading/views.py` `_projector_screens()` currently routes every text
  body through `_line_pairs()` (two lines a screen, blank line ends a screen). The new kind must
  bypass that and emit one screen carrying the whole body (the existing header/title stays).
- **Fitting.** `static/web/projector.js` `resizeTextFont()` shrinks from 100px by 1 down to >1px,
  then lets the final line hang over the bottom edge — there is no floor and no ellipsis today. This
  kind needs a defined smallest size and, at that floor, an ellipsized (clamped) render instead of
  overflow.
- **Reading pane.** Decide whether the pane shows this like a normal text entry (full text) or
  otherwise; the pane currently shows text-entry paragraphs via `_paragraphs()`.

## Open questions

- Name and label for the kind (e.g. `TEXT_FIT` / "Text (one screen)")? The enum name becomes the
  URL slug.
- What is the smallest permitted font size that triggers ellipsizing?
- Ellipsize how — CSS line-clamp over the fitted box, or hard truncation with a trailing ellipsis?
- Do blank lines still act as block/pause separators inside the single screen, or is the body
  rendered as-is?

## Acceptance sketch

- The entry editor offers the new kind with a title and text field, like a text entry.
- The projector shows this entry's whole text on one screen (no two-line splitting).
- The font shrinks until the text fits; if it cannot fit even at the smallest size, the text is
  ellipsized and never overflows the screen.

## Links

- Spec: [029 — Single-screen text entry](../../specs/029-single-screen-text/spec.md)
- Related items: ITEM-028 (live projection editing)
