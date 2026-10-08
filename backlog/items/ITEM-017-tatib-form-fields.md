---
id: ITEM-017
status: in_review
title: 'Remove first-section and active controls from Tata Ibadah forms'
type: fix
priority: P1
effort: S
created: 2026-10-07
updated: 2026-10-07
spec: specs/015-tatib-form-fields/spec.md
branch: feat/026-live-projection-editing
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/275
archived_at:
archive_reason:
bump: patch
release_version: 1.0.0
---

# ITEM-017: Remove first-section and active controls from Tata Ibadah forms

## Summary

Remove the initial legacy-section fields from Tata Ibadah creation and remove the `is_active` control from both create/edit forms, while retaining the model's create default and each existing service's active state.

## Notes

- Owner decision: new services keep the model's active default; edits preserve their current activation state.
- Extra posted values for omitted form fields must be ignored.
- Empty active services remain listed and can be filled through the existing service-entry controls.

## Acceptance sketch

- Forms expose no first-section title/text or active field.
- Create makes an empty active service; edit does not change `is_active`.

## Links

- Spec: [015 — Remove first-section and active controls from Tata Ibadah forms](../../specs/015-tatib-form-fields/spec.md)
- Related items: ITEM-006 (sidebar editors), ITEM-007 (service entries)
