---
id: ITEM-263
status: done
title: 'Bible rail shows No books yet from Media Library'
type: fix
priority: P1
effort: S
created: 2026-11-27
updated: 2026-11-27
spec: '246-media-library-bible-rail'
branch: fix/246-media-library-bible-rail
pr: 636
issue: 635
closed_at: 2026-11-27
closed_reason: merged into develop (PR #636)
bump: patch
release_version:
---

# ITEM-263: Bible rail shows No books yet from Media Library

## Summary

Opening Alkitab from the rail while the Media Library page is on stage opens an empty sidebar with
"No books yet."; opening any other section first and then Alkitab shows the books normally.

## Notes

The Media Library page inherits the shell's default `data-section="alkitab"` but supplies no
sidebar rows, so the rail handler treats Alkitab as already selected and toggles instead of fetching.
The fix gives the library its own section identity.

## Acceptance sketch

- From Media Library, the first Alkitab click fetches `/bible/` and shows real book rows.
- Clicking another section first, then Alkitab, still works.
- A section's own tile keeps its existing toggle behaviour.

## Links

- Issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/635
- Spec: [246](../specs/246-media-library-bible-rail/spec.md)
- Related items: ITEM-260
