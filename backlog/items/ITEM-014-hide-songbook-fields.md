---
id: ITEM-014
status: in-review
title: 'Hide short name and hymn-book fields in songbook forms'
type: chore
priority: P2
effort: S
created: 2026-10-06
updated: 2026-10-06
spec: specs/012-hide-songbook-fields/spec.md
branch: feat/012-hide-songbook-fields
pr: 272
archived_at:
archive_reason:
bump: patch
release_version: 0.11.4
---

# ITEM-014: Hide short name and hymn-book fields in songbook forms

## Summary

Remove the short-name and hymn-book controls from songbook create/edit forms. Preserve existing stored values on edits; new songbooks use the model defaults (blank short name and not a hymn book).

## Notes

- The model fields remain available to other workflows and continue to be used by the rest of the product.
- Owner accepted that new songbooks use the model defaults: no abbreviation and non-hymn.

## Acceptance sketch

- Songbook create and edit forms render neither `short_name` nor `is_hymn_book`, including as hidden inputs.
- Editing preserves both stored values, and extra submitted values for omitted fields are ignored.
- Creating a songbook uses the model defaults for those fields.
- Hymn songbooks remain read-only.

## Links

- Spec: [012 — Hide songbook form fields](../../specs/012-hide-songbook-fields/spec.md)
- Related items: ITEM-006 (sidebar editors)
