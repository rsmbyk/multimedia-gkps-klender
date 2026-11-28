---
id: ITEM-272
status: done
title: 'Invalidate a stale service or song page and offer reload'
type: feat
priority: P1
effort: L
created: 2026-11-28
updated: 2026-11-28
spec: specs/258-live-reading-freshness/spec.md
branch: feat/258-live-reading-freshness
pr: 661
issue:
closed_at: 2026-11-28
closed_reason: merged into develop (PR #661)
bump: patch
release_version:
---

# ITEM-272: Invalidate a stale service or song page and offer reload

## Summary

An open service or song page SHALL poll its object's version every 10 s; when the server is ahead it closes the page's dialogs, disables add/edit/delete, reorder and project in place, and shows a top-centre badge saying the page was edited elsewhere with a Reload button that re-fetches only the current page.

## Notes

- Depends on the version field and 409 guard from ITEM-271.
- The poll is presentation only; the server guard prevents the lost write.
- Reload uses the existing in-place navigation refresh, not a browser reload.

## Acceptance sketch

- A change made on another computer invalidates the open page within 10 s.
- All page dialogs, including the copy-confirm layer, are closed on invalidation.
- Reload restores the page without a full browser reload.

## Links

- Spec:
- Related items: ITEM-271
