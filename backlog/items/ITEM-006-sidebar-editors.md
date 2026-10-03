---
id: ITEM-006
status: in-review
title: 'Sidebar editors for Kidung and Tata Ibadah'
type: feat
priority: P1
effort: L
created: 2026-10-03
updated: 2026-10-03
spec: specs/005-sidebar-editors/spec.md
branch: feat/005-sidebar-editors
pr:
archived_at:
archive_reason:
bump: minor
release_version: 0.9.0
---

# ITEM-006: Sidebar editors for Kidung and Tata Ibadah

## Summary

The worship team maintains the corpus while preparing a service, but the public reading site
is read-only: a wrong lyric, a missing song, or a new Tata Ibadah means leaving the site for
the Django admin. This adds an add button and hover-revealed edit controls to the three
sidebars that own that corpus (songbooks, songs, Tata Ibadah), each opening a modal form in
the reading design. Hymn songbooks and their songs stay locked.

## Notes

- Owner decision (2026-10-03): **no login** — anyone may write through these forms. The risk
  is recorded in the spec, along with a one-variable hook
  (`SIDEBAR_EDITORS_REQUIRE_LOGIN`) that can switch to staff-only without redesigning.
- Owner decision: hand-written modal in the reading design, posting a Django form through the
  shell's own JS — not a deep link into the Django admin.
- The repo has no write views, no forms and no permission gate today; this is the project's
  first write surface.
- Bump: minor (target 0.9.0).

## Acceptance sketch

- A full-width accent add button under the filter in the songbook, song, and Tata Ibadah
  sidebars opens a modal that creates the corresponding record.
- Every row in those lists (except hymn songbooks and their songs) reveals an edit control on
  hover/focus that opens the same modal prefilled; saving updates the row in place.
- Validation (duplicate short name, duplicate song number, required hymn number) is shown in
  the modal and writes nothing; CSRF is enforced.

## Links

- Spec: [005-sidebar-editors](../../specs/005-sidebar-editors/spec.md)
- Related items: ITEM-005 (the public site revamp this builds on)
