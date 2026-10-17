---
id: ITEM-109
status: in_review
title: 'Show distinct connection icons in the Media Library status row'
type: fix
priority: P2
effort: S
created: 2026-10-17
updated: 2026-10-17
spec: 109
branch: fix/109-media-connection-status-icons
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/359
archived_at:
archive_reason:
bump: patch
release_version: 1.14.6
---

# ITEM-109: Show distinct connection icons in the Media Library status row

## Summary

Add a small visual cue to the Media Library status popover's Connection row so Connected and Unavailable are easy to distinguish at a glance. Keep Unavailable neutral because the companion may simply be stopped or unreachable; it does not imply an error.

## Notes

The owner accepted the connection-row icon treatment in the [Media Library preview](../../specs/109-media-connection-status-icons/preview.html) on 2026-10-17. The status text stays visible and authoritative; the icon is decorative.

## Acceptance sketch

- Connected shows a muted-size green check-circle beside the existing Connected label.
- Unavailable shows a quiet, theme-muted rounded-square minus beside the existing Unavailable label.
- The status-button dot, local connection detection, and inventory visibility rules remain unchanged.

## Links

- Spec: [109](../../specs/109-media-connection-status-icons/spec.md)
- Related items: [ITEM-103](./ITEM-103-local-media-library.md)
