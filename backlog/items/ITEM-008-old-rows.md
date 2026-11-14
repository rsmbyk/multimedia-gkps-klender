---
id: ITEM-008
title: The old rows — editable, and one running order
status: done
type: feat
priority: P1
effort: L
spec: specs/007-service-order-editor/spec.md
branch: feat/007-service-order-editor
pr: 265
bump: minor
release_version: 0.11.0
created: 2026-10-04
updated: 2026-10-06
---

# ITEM-008: The old rows — editable, and one running order

## Summary

Make the reading pane able to maintain a service whose rows were prepared before spec 006: Edit and
Delete on an old `TataIbadahItem` (danger-coloured Delete, the same modal), and a single running
order per Tata Ibadah so a new entry added under an old row lands right after it instead of at the
end of the service.

## Compatibility

Additive for the old paths: the OBS dock, its sources and `/api/tatib/items/` are untouched. An edit
is an ordinary row update both systems already read; only `order_number` values may be renumbered by
the migration, preserving the order the pane shows today.

## Notes

- Raised by the owner's review of spec 006 (2026-10-04): "cant see edit and delete on old
  tataibadahitems", and a new entry added "at the last position instead of after the entry you click
  the button at".
- Spec 006 deliberately left the old model alone and deferred moving old rows into entries
  (plan 006, slice 6). Spec 007 retains old rows and migrates only their order numbers.
- Draft accepted by the owner on 2026-10-05; the implementation branch includes spec 006.
