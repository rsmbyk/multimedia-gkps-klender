---
id: ITEM-258
status: done
title: 'A slow rail or sidebar fetch gives no sign of work'
type: fix
priority: P1
effort: M
created: 2026-11-25
updated: 2026-11-26
spec: 243-navigation-loading-feedback
branch: fix/243-navigation-loading-feedback
pr: 624
issue: 623
closed_at: 2026-11-26
closed_reason: merged into develop (PR #624)
bump: patch
release_version:
---

# ITEM-258: A slow rail or sidebar fetch gives no sign of work

## Summary

On a slightly slow network, clicking a rail section or a sidebar row leaves the page and the
sidebar looking frozen: nothing marks the clicked item as pending. Operators can read the shell as
dead and click again. The fix shows the work at the point of the click and at the surface that will
change, without locking unrelated controls.

## Notes

- One choke point: `navigate()` in `static/web/reading.js`. Every rail, sidebar, search and history
  fetch that replaces content goes through it, so the pending state is set and cleared in one place.
- The clicked item locks immediately. A rail icon stays in place at reduced opacity; a sidebar row
  dims and its edit/delete/add controls disable with it. No spinner, label, edge fill or ring.
- A 3px bar runs at the top edge of each section that will be refreshed. A list-only fetch (rail,
  chapter-number list, songbook) leaves the reading page untouched. A stage write (song, passage,
  service) disables the stage, sets `aria-busy` and shows a seeded placeholder in that page's real
  layout, including the songbook name for a song with no number.
- A later click cancels the in-flight fetch, except that a stage write continues when the new click
  is list-only. Cancelled items unlock at once.

## Acceptance sketch

- With a delayed rail fetch and both lists open, the rail icon dims and both list tops show a bar;
  the reading page keeps its current content.
- With a delayed song write, the stage is disabled and its placeholder matches the song header and
  numbered verses, seeded from the sidebar.
- Edit/delete controls on the clicked row are disabled while its fetch is pending and return when
  it settles; another item can still be clicked.

## Links

- Spec: `specs/243-navigation-loading-feedback/spec.md`
- Capability: `docs/spec/reading.md` — `reading/R61`
- Anchor issue: #623
