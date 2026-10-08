---
id: ITEM-036
status: speccing
title: 'Highlight a whole service entry item on hover'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/034-item-hover-highlight/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-036: Highlight a whole service entry item on hover

## Summary

Hovering a service entry in the Tata Ibadah pane currently reveals only the add bar below it; the
item itself gets no feedback. Highlight the **whole item** on hover, so the row the pointer is on is
obvious.

## Notes

- **Today.** `.tatib__item` in `static/styles/design/components.css` carries no hover style; only
  `.tatib__item:hover + .entry__add` reveals the add bar. The sidebars already highlight rows with
  the theme-aware token `--icon-hover-bg` (`.book:hover`, `.songrow:hover`, `#chList li:hover > a`).
- **The highlight.** Give `.tatib__item` (and the legacy `.tatib__eos` row) a hover background using
  `--icon-hover-bg`, long enough to read as a row.
- **Don't shift the layout.** The item is plain text with tight margins (`.tatib__item + .tatib__item
  { margin-top: 2px }`); pad the highlight and pull it back with a matching negative margin, or
  inset it, so adding the background never nudges the text.
- **Share the hover with ITEM-035.** The floating controls (ITEM-035) are revealed on the same item
  hover, so both states should agree, and neither should leave a stale highlight/outline after use
  (spec 025 / ITEM-027).
- **Theme-aware.** Use the token so light and dark both work; honour reduced motion for any fade.

## Open questions

- How far should the highlight bleed — to the text edges, or out to the pane gutter?
- Do legacy `.tatib__eos` rows (and section breaks) get the same highlight?
- Should keyboard focus highlight the item too, or only the pointer?

## Acceptance sketch

- Hovering a service entry highlights the whole item as one row, in both themes.
- Adding the highlight shifts no text (no layout movement).
- The per-item add bar and the floating controls still behave as before.
- No lingering highlight or outline remains after the pointer leaves or a control is used.

## Links

- Spec: [034 — Highlight a whole service entry item on hover](../../specs/034-item-hover-highlight/spec.md)
- Related items: ITEM-035 (floating entry controls), ITEM-009 / ITEM-010 (sidebar tints),
  ITEM-027 / spec 025 (quiet modal focus)
