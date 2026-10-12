---
id: ITEM-060
status: in-progress
title: 'Clear stale service entry highlight after modal dismissal'
type: fix
priority: P2
effort: S
created: 2026-10-12
updated: 2026-10-12
spec: 058
branch: fix/058-entry-modal-highlight
pr:
archived_at:
archive_reason:
bump: patch
release_version: 1.4.1
---

# ITEM-060: Clear stale service entry highlight after modal dismissal

## Summary

After Preview, Edit, or Delete closes, restored focus keeps an unhovered service
entry highlighted. Make quiet pointer restoration visually idle while preserving
hover, deliberate keyboard navigation, and touch controls.

## Notes

- Owner approved the state preview on 2026-10-12; spec 058 accepted on 2026-10-12.
- Existing focus restoration supplies a quiet marker, but entry background and
  control-visibility selectors do not account for it.

## Acceptance sketch

- Pointer-opened modals leave no highlight or floating controls after dismissal
  when the pointer is elsewhere; keyboard and real hover remain usable.
- Cover all three controls, supported dismissal paths, refresh, both themes,
  and the existing coarse-touch control visibility rule.

## Links

- Spec: [058](../../specs/058-entry-modal-highlight/spec.md)
- Preview: [state preview](../../specs/058-entry-modal-highlight/preview.html)
- Related items: ITEM-027, ITEM-035, ITEM-036
