---
id: ITEM-147
status: in-progress
title: 'A long title runs past the reading pane instead of wrapping'
type: fix
priority: P1
effort: S
created: 2026-10-27
updated: 2026-10-27
spec: specs/137-reading-text-wrap/spec.md
branch: feat/137-reading-text-wrap
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-147: A long title runs past the reading pane instead of wrapping

## Summary

A reading page's title is painted straight out of the pane when it holds no break opportunity. On
`/tatib/149/` a 64-character title — the column's own limit — pushes the document 1,033px past the viewport at 1440×900, so
the page scrolls sideways and the title cannot be read past the pane's edge; the song page does the
same (380px). The same defect reaches the Bible pericope headings, verse lines, Tata Ibadah body
paragraphs (a pasted Drive link runs 215px past its box) and search-result rows.

## Notes

- Owner report with two screenshots: Tata Ibadah and songs, plus "make sure it is fixed in other
  kind of pages".
- One property, inherited: `overflow-wrap: break-word` on the reading pane, the search results and
  the Preview modal. `break-word`, not `anywhere`, so the title's flex row keeps measuring a word
  the way it does today and the TB/SIM toggle keeps its line.
- Already correct today and untouched: the contents rows (`anywhere` + three-line clamp, spec 135),
  the OBS dock (`anywhere`), the projector (`break-word`).
- Deliberate truncations stay: sidebar service/songbook rows and media filenames are one line
  ending `…`.

## Acceptance sketch

- A 64-character title draws inside its pane at any width and the document no longer scrolls
  sideways.
- A pasted link in a text entry wraps inside the pane instead of running past it.
- Bible headings, verse lines and search rows wrap the same way.
- Rows that truncate on purpose still truncate.

## Links

- Spec: [137](../specs/137-reading-text-wrap/spec.md)
- Related items: ITEM-145 (the contents rows' three-line clamp, spec 135)
