---
id: ITEM-033
status: speccing
title: 'Show only the first lines of a text in the Tata Ibadah pane'
type: chore
priority: P2
effort: S
created: 2026-10-08
updated: 2026-10-08
spec: specs/031-clamp-pane-text/spec.md
branch:
pr:
archived_at:
archive_reason:
bump: patch
release_version:
---

# ITEM-033: Show only the first lines of a text in the Tata Ibadah pane

## Summary

In the Tata Ibadah reading pane, a text entry (and a legacy text row) prints every line it holds, so
a long text pushes the running order down the page. Show only the first few lines and hide the rest —
clipped or ellipsized — so the pane stays a readable running order.

## Notes

- **Where the words come from.** `_paragraphs()` in `multimedia/web/reading/views.py` splits the
  body into one `<p class="tatib__tx">` per line, rendered in
  `multimedia/web/templates/reading/tatib.html`. Legacy text rows use the same shape.
- **Per-line blocks defeat a naive clamp.** Because every line is its own `<p>`, a
  `-webkit-line-clamp` on `.tatib__tx` would clamp each line, not the whole entry. Clamping the
  entry needs a wrapper the clamp applies to (lines inline inside it) or a server-side cap on the
  lines rendered by `_paragraphs()` / the pane context.
- **Existing pattern.** `.result-row__excerpt` in `static/styles/design/components.css` already uses
  `display:-webkit-box; -webkit-box-orient:vertical; -webkit-line-clamp:2; overflow:hidden` — a
  precedent to follow.
- **Scope.** Only text entries and legacy text rows carry words in the pane; scripture and song rows
  show their reference alone. Leave those, and the other reading panes, untouched.

## Open questions

- How many lines to show?
- Clip (hard hide / fade) or ellipsize with a visible "…"?
- Should the full text stay reachable from the pane (an expand or "show more"), or is the pane only a
  running order and the words belong on the display?
- Do blank lines count toward the limit (an empty `<p>` still occupies a row)?

## Acceptance sketch

- A long text entry shows only its first few lines in the Tata Ibadah pane; the rest is clipped or
  ellipsized.
- A short text entry renders unchanged.
- Scripture and song rows, and the other reading panes, are unaffected.

## Links

- Spec: [031 — Clamp a text entry in the Tata Ibadah pane](../../specs/031-clamp-pane-text/spec.md)
- Related items: ITEM-031 (one-screen fitted text), ITEM-032 (add an entry at the beginning)
