---
id: ITEM-276
status: in_review
title: 'Use template progress persists for seven days'
type: feat
priority: P2
effort: M
created: 2026-11-28
updated: 2026-11-28
spec: 255-use-template-progress-persist
branch: feat/255-use-template-progress-persist
pr: 658
issue: 657
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-276: Use template progress persists for seven days

## Summary

Spec 253 keeps a template's Use template progress for one browser session. The owner wants it to
survive the browser and last seven days from the last change, and wants the Use template button to
show that a draft is saved.

## Notes

- Owner decisions: seven days counting from the last change (every edit resets the clock); indicator
  variant **A — corner dot**, chosen after seeing all three in the preview.
- Moves the store from `sessionStorage` to `localStorage` with a `savedAt` timestamp and a `v: 2`
  record; expired records are removed on read.
- The mark is a 7px dot inset 3px from the button's top-right; the accessible name states the saved
  draft; the button's width and label are unchanged.
- No server write; R36 still holds.
- Preview and measured numbers: `specs/255-use-template-progress-persist/preview/README.md`.

## Acceptance sketch

- Close the browser, reopen within seven days: progress returns.
- A record older than seven days is ignored and removed.
- An edit on day six restarts the seven-day clock.
- A template with a live record shows the dot before the modal opens; Create clears it.

## Links

- Spec: [255-use-template-progress-persist](../specs/255-use-template-progress-persist/spec.md)
- Related items: ITEM-270 (spec 253, the session-scoped store this extends)