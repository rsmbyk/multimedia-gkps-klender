---
id: ITEM-194
status: done
title: 'Delete songs, songbooks and Tata Ibadah records from their sidebars'
type: feat
priority: P2
effort: S
created: 2026-11-14
updated: 2026-11-14
spec: specs/190-sidebar-delete/spec.md
branch: feat/190-sidebar-delete
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/501
issue:
closed_at: 2026-11-14
closed_reason: merged into develop (PR #501)
bump: minor
release_version: 1.29.0
---

# ITEM-194: Delete songs, songbooks and Tata Ibadah records from their sidebars

## Summary

The reading sidebars could add and edit records but never remove them, so retired songbooks, stray
songs and dead services stayed in the lists forever. The request (2026-11-13, chat): add delete
buttons on the sidebar items for songs (non-hymn), songbooks (non-hymn), and the services sidebar.

## Notes

- Hymn songbooks and their songs stay read-only (spec 005's standing rule).
- Delete is confirmed in the shared editor modal before any request; the endpoints are POST-only with
  CSRF, and a template only ever deletes through the template kind.
- Songs and songbooks soft-delete; a Tata Ibadah leaves the lists by its own active flag.
- The card was created at Fold (2026-11-14) — the demand arrived as a chat prompt and was specced as
  spec 190 directly; Gate 1 accepted the same day.

## Acceptance sketch

- Hovering an eligible row reveals trash beside pencil; a dated Tata Ibadah row hides its date while
  the actions are revealed.
- Confirm names the record and its kind's noun (`Delete template`, not "Tata Ibadah", for templates).
- A confirmed delete removes the row; deleting the record on stage returns to the parent list with the
  history entry replaced.

## Links

- Spec: [190](../specs/190-sidebar-delete/spec.md)
- Related items: ITEM-193 (spec 189, the song-page verse editors the delete control sits beside)
