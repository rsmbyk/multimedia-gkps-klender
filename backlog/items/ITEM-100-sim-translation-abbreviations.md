---
id: ITEM-100
status: done
title: 'Use the requested SIM book abbreviations'
type: fix
priority: P2
effort: L
created: 2026-10-16
updated: 2026-10-16
spec: 100
branch: fix/100-sim-translation-abbreviations
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/350
archived_at:
archive_reason:
bump: patch
release_version: 1.13.2
---

# ITEM-100: Use the requested SIM book abbreviations

## Summary

Store the requested SIM abbreviations separately from the full Simalungun book names. Use the
reader's selected Bible edition for mini-sidebar codes and testament headings, match both TB and
SIM codes in all named book searches, and show the displayed edition's full book name above verses.
Switch only the three main rail popups to Bibel, Doding, and Agenda in SIM. Update existing
database rows and fresh Bible seed data.

## Acceptance sketch

- Each SIM book has the requested short code while its full `BookTranslation.translation` name
  and verse relationships remain intact in existing and freshly seeded databases.
- Mini-sidebar codes and Bible testament headings follow the last selected TB/SIM edition in the
  current page visit; passage editor group headings follow that editor's edition.
- Sidebar filtering, projector Go To, and new/edit passage book filtering accept both TB and SIM
  abbreviations in either edition.
- The book name above a Bible chapter follows the edition actually displaying its verses, including
  direct links and saved-copy reading.
- The Alkitab, Kidung, and Tata Ibadah main rail popups become Bibel, Doding, and Agenda while
  SIM is remembered; their accessible link names match, and all other rail popups stay unchanged.

## Links

- Spec: [100](../../specs/100-sim-translation-abbreviations/spec.md)
- Related items: ITEM-043 (TB/SIM book names in the passage picker), ITEM-046 (TB/SIM passage
  translation toggle)
