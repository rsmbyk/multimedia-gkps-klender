---
id: ITEM-048
status: done
title: 'Show the first two text lines for untitled service entries'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-09
spec: specs/046-sidebar-text-two-lines/spec.md
branch: chore/046-sidebar-text-two-lines
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/298
archived_at:
archive_reason:
bump: patch
release_version: 1.3.13
---

# ITEM-048: Show the first two text lines for untitled service entries

## Summary

In the Tata Ibadah sidebar, untitled Text and Single-Screen Text entries should show their first two
literal body lines instead of the generic kind label. Preserve an operator-provided title when one
exists, and keep the reorder grip centered on two-line rows.

## Notes

- **Today.** In `_tatib_stage()` (`multimedia/web/reading/views.py`), a new service entry uses its
  `title or kind display` for the TOC label; a legacy text row has a separate path that uses its title
  or first body line.
- **Untitled entries.** For new service-entry kinds `text` and `single_screen_text` with an empty
  title, use the first two literal lines from `resolve()[1]`, split on `\n`.
- **Titles.** If either kind has a non-empty title, keep the title as the sidebar label; do not replace
  it with body text.
- **Blank lines and length.** Blank lines count among the first two lines. Cap the final label
  (retained title or body preview) at 60 characters overall, matching the current service-entry cap.
- **Legacy and other rows.** Legacy `TataIbadahItem` rows and passage, song, and break entries remain
  unchanged.
- **The row.** `_toc.html` renders the selected body lines separately and represents an empty line
  explicitly so a trailing blank second line remains visible.
- **The grip.** `.toc__grip` is centered with `top: 50%` and `translateY(-50%)`; verify this remains
  centered when a row is two lines tall.

## Decisions

- Titled Text and Single-Screen Text entries keep their title.
- Blank lines count literally; do not skip them to fill two visible text lines.
- Scope is limited to new service-entry Text and Single-Screen Text kinds; legacy rows stay as-is.
- The final label (title or body preview) has a 60-character overall cap.

## Acceptance sketch

- An untitled Text entry shows its first two literal body lines; a blank line counts as a line.
- An untitled Single-Screen Text entry shows its first two literal body lines.
- Titled entries keep their title; the final label is capped at 60 characters overall.
- A two-line row keeps its reorder grip vertically centered.
- Legacy text rows and passage/song/break rows are unchanged.

## Links

- Spec: [046 — Show the first two text lines for untitled service entries](../../specs/046-sidebar-text-two-lines/spec.md)
- Related items: ITEM-033 / spec 031 (pane clamp), ITEM-041 / spec 039 (hymn sidebar label)
