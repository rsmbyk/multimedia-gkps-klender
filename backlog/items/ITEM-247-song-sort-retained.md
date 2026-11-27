---
id: ITEM-247
status: done
title: 'A new song resets the sidebar song order'
type: fix
priority: P1
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 233-song-sort-retained
branch: fix/233-song-sort-retained
pr: 606
issue: 605
closed_at: 2026-11-23
closed_reason: merged into develop (PR #606)
bump: patch
release_version: 1.37.3
---

# ITEM-247: A new song resets the sidebar song order

## Summary

With the song list sorted alphabetically, creating a song refreshes the list in the server's
last-modified order while the sort button still says `title`. Measured at 1440×900 from a
two-song book (`Zebra` newer, `Alpha` older): toggle gives `Alpha, Zebra`; creating `Beta` gives
`Beta, Zebra, Alpha` on the base commit, against `Alpha, Beta, Zebra` expected. The cause is in the
shared list-reconciliation path, not the create handler, so edits, deletes and row clicks reset the
order too.

## Notes

- The owner chose the root-cause scope: keep the chosen order after every in-place refresh, not
  only after a create.
- The fix re-applies the existing `applySongOrder()` immediately after the list is reconciled; no
  new control, endpoint or persisted state.
- Hymn songbooks have no sort control and keep their number order.
- Probe E2E failed on the base commit and passed with the change; the promoted module fails five
  tests on base and passes all six with it.

## Acceptance sketch

- Alphabetical sort survives a create, an edit, a delete and a row click.
- The default last-modified order and other sections are unchanged.
- The sort button's `data-order` agrees with the painted rows after each refresh.

## Links

- Spec: [233-song-sort-retained](../../specs/233-song-sort-retained/spec.md)
- Related items: ITEM-240 (a created songbook or song opens as its row would)
