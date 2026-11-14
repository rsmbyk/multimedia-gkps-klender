---
id: ITEM-113
status: done
title: 'Allow Share online from a fresh Media Library session'
type: fix
priority: P1
effort: S
created: 2026-10-18
updated: 2026-10-18
spec: specs/113-media-library-share-csrf/spec.md
branch: fix/113-media-library-share-csrf
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/361
issue:
closed_at: 2026-10-18
closed_reason: merged into develop (PR #361)
bump: patch
release_version: 1.15.1
---

# ITEM-113: Allow Share online from a fresh Media Library session

## Summary

Sharing from a fresh direct visit to Media Library currently fails because its page does not set the CSRF cookie required by the share-permission POST. Django returns an HTML 403 page where the browser expects JSON, so the operator sees a JSON parse alert and no upload starts.

## Notes

The existing Tata Ibadah page already uses Django's `ensure_csrf_cookie` pattern for browser-initiated POST requests. Keep the Media Library share endpoint protected by CSRF middleware.

## Acceptance sketch

- A fresh direct visit to Media Library supplies the CSRF cookie needed for Share online.
- The matching token is accepted by the share POST; requests without a valid token remain rejected.
- The companion starts the upload after valid permission is returned, with no JSON parse alert.

## Links

- Spec: [113](../../specs/113-media-library-share-csrf/spec.md)
- Related items: [ITEM-112](./ITEM-112-temporary-media-handoff.md)
