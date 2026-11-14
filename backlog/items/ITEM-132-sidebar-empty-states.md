---
id: ITEM-132
status: done
title: 'Centre the sidebars'' empty states, and say which nothing they are'
type: fix
priority: P2
effort: S
created: 2026-10-25
updated: 2026-10-25
spec: specs/129-sidebar-empty-states/spec.md
branch: fix/129-sidebar-empty-states
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/390
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/382
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-132: Centre the sidebars' empty states, and say which nothing they are

## Summary

Both reading sidebars print their empty line as the last flex child of the pane, so `No matching sections.`,
`No matching songs.` and `No matching Tata Ibadah.` sit at the bottom-left — unreadable as a state and easy
to mistake for a footer. The same sentence then covers two different situations: a list that has nothing in
it and a filter that matched nothing, so an operator keeps retyping a filter that was never the problem.

## Notes

- The block is centred on the list's pane, not the whole column, so the filter strip above never biases it.
- Both columns: the first names books / songbooks / Tata Ibadah, the second songs / sections.
- The empty copy is an invitation (`No sections yet.`), the filtered copy is the miss (`No matching
  sections.` / `Try a different search.`) under a crossed-out magnifier.
- A page can arrive empty, so the block is also painted at boot; the saved renderer re-labels it because its
  shell is the cached home page.
- Hidden in the collapsed mini panel and beside the Bible's chapter tiles; never a control.

## Acceptance sketch

- An empty Tata Ibadah, an empty songbook and an empty services column each show a centred glyph + title +
  hint, naming their own list.
- A filter that matches nothing switches the block to the miss copy; clearing it hides the block.
- A page whose list has rows and matches shows no block at all.
- The saved copy of a Kidung or Tata Ibadah page carries the same copy and glyphs as the server route.

## Links

- Spec: [`specs/129-sidebar-empty-states/spec.md`](../../specs/129-sidebar-empty-states/spec.md)
- Related items: ITEM-045 (book picker filter hint), ITEM-126 (saved song sort parity)
