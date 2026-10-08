---
id: ITEM-048
status: speccing
title: 'Show the first two text lines in the service sidebar'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/046-sidebar-text-two-lines/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-048: Show the first two text lines in the service sidebar

## Summary

In the Tata Ibadah sidebar (the service's contents list), a text entry should show the **first two
literal lines** of its text — for both the multi-line **Text** kind and the **Single-Screen Text**
kind — so the running order reads as the words themselves. When a row is two lines tall, its reorder
grip stays vertically centered.

## Notes

- **Today.** `_tatib_stage()` in `multimedia/web/reading/views.py` labels an entry with
  `title or row.get_kind_display()`, so an untitled text row reads "Text"; a titled one reads its
  title. (A legacy text row already falls back to `_first_line(row.text)`.)
- **What to change.** For `kind_key in ('text', 'single_screen_text')`, build the sidebar label from
  the first two `\n`-split lines of the entry's text (`resolve()[1]`), and show them as up to two
  lines in the row.
- **The row.** `_toc.html` renders the label in `.songrow__t`; a literal line break needs the markup
  or CSS to preserve it (e.g. `white-space: pre-line`, or two spans).
- **The grip.** `.toc__grip` is `position: absolute; top: 50%; translateY(-50%)` inside a positioned
  `#chList li` (`static/styles/design/components.css`), so it centers on the row — verify it still
  centers when the row is two lines.
- **Different surface from spec 031.** That spec clamps a text in the reading *pane*; this is the
  *sidebar* label.

## Open questions

- A titled text entry: does the sidebar show the title, or the two text lines (replacing it)?
- Blank lines: skipped, or shown as empty lines toward the two?
- Do legacy text rows adopt the same two-line treatment?
- Keep the current 60-character cap on the label?

## Acceptance sketch

- A multi-line Text entry's sidebar row shows the first two lines of its text.
- A Single-Screen Text entry's row does the same.
- A two-line row keeps its grip vertically centered.
- Other kinds (passage, song, break) are unchanged.

## Links

- Spec: [046 — Show the first two text lines in the service sidebar](../../specs/046-sidebar-text-two-lines/spec.md)
- Related items: ITEM-033 / spec 031 (pane clamp), ITEM-041 / spec 039 (hymn sidebar label)
