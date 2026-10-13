---
id: ITEM-092
status: done
title: Name the preview tabs container so it cannot be mistaken for a tab
type: fix
priority: P2
effort: S
created: 2026-10-13
updated: 2026-10-13
spec: ../../specs/089-preview-tabs-container-name/spec.md
branch: fix/089-preview-tabs-container-name
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/343
archived_at:
archive_reason:
bump: patch
release_version: 1.10.10
---

# ITEM-092: Name the preview tabs container so it cannot be mistaken for a tab

## Summary

Spec 085 (PR #339) added the preview header's tabs container as `preview__tabs-host`. Its name contains
`preview__tab`, which is the substring two unit tests probe for to decide whether a song preview renders
verse tabs — so the "one verse → no tabs" test now fails even though no tab is rendered.

## Notes

- Found by the post-merge full suite on `develop`; passed at the merge base `4a61b58`.
- Behaviour is correct; the name collides with the assertion. The fix renames the container and leaves
  both pre-existing tests untouched.
- The container is reached by `data-preview-tabs-host` in `preview.js`, so no JavaScript changes.

## Acceptance sketch

- The served markup of a single-verse song contains no `preview__tab` string.
- The two-verse case still renders its tabs in the header and swaps verses.

## Links

- Spec: [../../specs/089-preview-tabs-container-name/spec.md](../../specs/089-preview-tabs-container-name/spec.md)
- Related items: ITEM-088 (spec 085)
