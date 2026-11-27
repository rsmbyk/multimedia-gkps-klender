---
id: ITEM-236
status: done
title: 'Deleting the open song or service falls back to the search page'
type: fix
priority: P2
effort: S
created: 2026-11-22
updated: 2026-11-22
spec: 221-empty-reading-stage
branch: fix/221-empty-reading-stage
pr: 585
issue:
closed_at: 2026-11-22
closed_reason: merged into develop (PR #585)
bump: patch
release_version: 1.37.3
---

# ITEM-236: Deleting the open song or service falls back to the search page

## Summary

Deleting a song or service that is currently on the reading stage moves the shell to its parent list,
which paints the search landing in the stage. The reading surface disappears just because the record
was removed. Keep the reading surface instead, with nothing open in it, so the reader stays in the
reading view and can choose the next song or service from the lists beside it. The stage says
"Nothing open." with a short hint rather than showing the search page.

## Notes

- Reproduced on the served app: opening `/songs/1906/`, confirming its sidebar delete lands on
  `/songs/book/36/` with `data-read="off"`, `data-home="landing"` and the search field visible.
- Applies to the "record was on stage" branch of the confirmed-delete flow (spec 190 / R41); a delete
  of a record that was not on stage keeps today's list-only refresh.
- The parent lists remain visible in both side panels; only the stage changes.

## Acceptance sketch

- Confirming the delete of the open song leaves the reading stage up with "Nothing open." and a hint,
  and the deleted record's songbook still listed beside it; no search field appears in the stage.
- Confirming the delete of the open service leaves that same stage with the service list beside it.
- Reloading the resulting URL keeps the empty reading view; Back does not revisit the deleted record.
- Deleting a row that was not on stage still refreshes its list and keeps whatever was on stage.

## Links

- Spec:
- Related items:
