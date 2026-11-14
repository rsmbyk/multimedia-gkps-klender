---
id: ITEM-059
status: done
title: 'Fix single-screen Save, add breaks at once, drop break Edit, show song verses in the sidebar'
type: fix
priority: P2
effort: S
created: 2026-10-11
updated: 2026-10-11
spec: specs/057-service-entry-quick-actions/spec.md
branch: fix/057-service-entry-quick-actions
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/310
archived_at:
archive_reason:
bump: patch
release_version: 1.3.23
---

# ITEM-059: Fix single-screen Save, add breaks at once, drop break Edit, show song verses in the sidebar

## Summary

Four operator-reported issues on the Tata Ibadah entry editor: the single-screen text Save stays
disabled after typing; "+ Break" opens a form with no fields; a break row offers an Edit button;
and song rows in the sidebar do not show their selected verses. The verse list uses one
formatter that collapses runs of three or more into ranges (`1-3, 5, 6, 8-10`), shared with the
stage's `Bait` line.

## Notes

- Save root cause: the text Save guard in `static/web/entries.js` matches only the `text` form,
  not `single_screen_text`.
- Verse format decided by the owner on 2026-10-11: ranges when consecutive, comma-separated
  otherwise, mixed lists supported, and the same format on the Tata Ibadah page.

## Acceptance sketch

- Single-screen Save enables on typing and disables when cleared.
- "+ Break" adds a break in place with no dialog.
- No Edit control on break rows; Delete remains.
- Song rows show `Bait 1-3, 5, 6, 8-10` on the second line; the stage uses the same format.

## Links

- Spec: [057 — Service entry quick fixes](../../specs/057-service-entry-quick-actions/spec.md)
- Related items: ITEM-056 / spec 054 (the `Bait` line and its rule)
