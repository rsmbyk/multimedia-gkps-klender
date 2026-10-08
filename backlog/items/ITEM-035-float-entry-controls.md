---
id: ITEM-035
status: in_review
title: 'Float the entry controls over each item, top-right'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/033-float-entry-controls/spec.md
branch: chore/033-float-entry-controls
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.3.1
---

# ITEM-035: Float the entry controls over each item, top-right

## Summary

The entry-specific controls — preview, Edit, Delete — currently sit inside the per-item add bar below
the item, pushed to its far end. Move them into the item itself, at its **top-right**, drawn over the
text, with a brief background behind the buttons so they stay legible. They appear only while the
item is hovered.

## Notes

- **Today.** In `multimedia/web/templates/reading/tatib.html`, the per-item add bar
  (`.entry__add`, `data-entry-after=…`) carries the four add buttons plus a `.entry__acts` span with
  Edit/Delete; `static/styles/design/components.css` gives `.entry__acts { margin-left: auto }` and
  reveals `.entry__add` on `:hover` / `:focus-within` with a small delay.
- **The move.** Take `.entry__acts` (preview + Edit + Delete) out of `.entry__add` and place it in
  the item element — `section.tatib__item`, and the legacy `.tatib__eos` row — positioned
  `absolute; top/right`, over the content. The item needs `position: relative`.
- **The backing.** A brief panel behind the button group (rounded, using the existing surface tokens)
  so the controls read over the words, without covering more than they must.
- **The preview button** is the one from ITEM-034 / spec 032; this item governs where the three
  controls live together. The add bar keeps its four `+` buttons (adding after the item).
- **Reveal on hover — and on keyboard focus.** Hover-only would strand keyboard users; mirror the
  add bar's `:focus-within` reveal. Dismissal/reveal must not leave a stale outline (spec 025 /
  ITEM-027, ITEM-016).

## Open questions

- On touch / coarse pointers (no hover), do the controls always show, or reveal on tap?
- Does the backing cover the button group only, or the whole top-right strip?
- Do legacy `.tatib__eos` rows get the same top-right treatment?

## Acceptance sketch

- Preview, Edit, and Delete render at the item's top-right, over its text, only while the item is
  hovered (and while a control has keyboard focus).
- A brief background sits behind the buttons so they are readable over the words.
- The per-item add bar still offers the four add actions and no longer carries the controls.
- No control leaves a lingering outline/hover state after use.

## Links

- Spec: [033 — Float the entry controls over each item, top-right](../../specs/033-float-entry-controls/spec.md)
- Related items: ITEM-034 (entry preview modal), ITEM-027 / spec 025 (quiet modal focus),
  ITEM-016 (stale row-edit visibility)
