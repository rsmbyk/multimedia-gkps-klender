---
id: ITEM-078
status: in_review
title: Repeat a service-entry flash after it finishes
type: fix
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/075-toc-repeat-flash/spec.md
branch: fix/075-toc-repeat-flash
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/329
archived_at:
archive_reason:
bump: patch
release_version: 1.9.1
---

# ITEM-078: Repeat a service-entry flash after it finishes

## Summary

Allow the Tata Ibadah contents quicklink to flash its stage entry again once the prior flash has completed.

## Notes

- The owner accepted the interactive sidebar follow-ups preview on 2026-10-13.
- The Draft in Spec 075 controls implementation after explicit owner acceptance.

## Acceptance sketch

- Clicking a row after the flash ends replays the full stage flash.
- Clicks during an active flash do not restart or queue another flash.
- Stage replacement and reduced motion cannot leave the interaction locked.

## Links

- Spec: [Spec 075](../../specs/075-toc-repeat-flash/spec.md)
