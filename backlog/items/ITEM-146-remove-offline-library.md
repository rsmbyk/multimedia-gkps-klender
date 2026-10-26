---
id: ITEM-146
status: in-progress
title: 'Remove the offline library; the projector Go To fetches on selection'
type: feat
priority: P1
effort: L
created: 2026-10-26
updated: 2026-10-26
spec: specs/136-remove-offline-library/spec.md
branch: feat/136-remove-offline-library
pr:
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/401
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-146: Remove the offline library; the projector Go To fetches on selection

## Summary

The app stops keeping a local copy of the public library: no IndexedDB store, no service worker, no
offline status control. The projector's Go To holds a page-memory lookup index (126 KB raw, 29 KB
gzipped) so search stays instant, and choosing a result fetches the whole chapter or song behind a
blocking loading mode — a chapter change inside a passage detour uses the same mode.

## Notes

- Removes the behaviour shipped by specs 092 and 106: the revisioned browser library, its page
  shells, the rail's status control and the saved-copy paint.
- The Go To's own lookup rules are frozen by `multimedia/web/reading/search.py`'s docstring ("do not
  touch anything on goto"): the result set and order are the ones the browser lookup produces today;
  only the index's source changes, from IndexedDB to a fetched payload held in page memory.
- The projector page's live paths (reflow, adopt) and the service screens themselves are untouched.
- `ITEM-139` (offline projector E2E errors) is retired by this slice rather than fixed.

## Acceptance sketch

- After a normal browsing session the browser holds no library database, no cache entry and no
  service-worker registration.
- `G` on the projector lists the same results it lists today, and choosing one fetches it while
  every key, click and dismissal is refused and both loading indicators show.

## Links

- Spec: `specs/136-remove-offline-library/spec.md`
- Related items: ITEM-095, ITEM-106, ITEM-139
