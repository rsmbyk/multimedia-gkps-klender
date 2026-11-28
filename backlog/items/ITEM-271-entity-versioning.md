---
id: ITEM-271
status: ready
title: 'Entity versions and safe concurrent edits'
type: feat
priority: P0
effort: L
created: 2026-11-28
updated: 2026-11-28
spec: specs/254-entity-versioning/spec.md
branch: feat/254-entity-versioning
pr:
issue: 652
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-271: Entity versions and safe concurrent edits

## Summary

Services, service entries, legacy items, songs, songbooks and verses need an incrementing version so a write made from a stale page is rejected instead of overwriting another operator's edit. The same slice closes the related deletion hole: a referenced verse, song or songbook cannot be deleted, and the refusal names the distinct Tata Ibadah records affected.

## Notes

- No-op saves do not move a version; the comparison is against stored values.
- A service's version also moves when a referenced song or verse changes, including templates.
- The notice wording and glyph are reused from the verse edit modal; only the count changes from entries to distinct services.
- The four live-surface behaviours are separate cards: ITEM-272 through ITEM-275.
- Renumbered from ITEM-269 when `origin/develop` claimed that ID while this slice was being written; anchor issue #652 was created on gate 1 Accept.

## Acceptance sketch

- Two editors open one row at version 5; the second write is refused with 409 and leaves the row untouched.
- An identical-value save leaves the version unchanged.
- A referenced song's delete confirmation shows `Used in <count> Tata Ibadah — delete unavailable` with Delete disabled.
- A service with two qualifying entries counts once; a template counts too.

## Links

- Spec: [254](../specs/254-entity-versioning/spec.md)
- Related items: ITEM-272, ITEM-273, ITEM-274, ITEM-275
