---
id: ITEM-141
status: backlog
title: 'The bible edition-preference E2E cannot find the SIM verse text'
type: fix
priority: P1
effort: S
created: 2026-10-25
updated: 2026-10-25
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-141: The bible edition-preference E2E cannot find the SIM verse text

## Summary

`test_bible_edition_preference_returns_after_unavailable_chapter` fails waiting for `Garam ni dunia.` —
the Simalungun text it expects to come back after a chapter the edition cannot serve. The element is not in
the page at all (not hidden: not found). Either the preference no longer resolves to SIM on the way back, or
the fixture text differs from what the Simalungun seed now holds.

## Notes

- Reproduced on `develop` `ffa5c340`: same failure, same missing text, so it is not a slice's regression.
- Failing test: `tests/e2e/test_reading.py::ReadingE2ETests::test_bible_edition_preference_returns_after_unavailable_chapter`.
- The distinguishing question for the slice: read the page after the preference flips, and print which
  edition the read actually rendered before choosing between "the preference is not restored" and "the
  fixture text moved".

## Acceptance sketch

- The scenario passes with the preference restored, and the assertion names the edition it expects rather
  than only a verse string, so a seed change fails the fixture check instead of the behaviour check.

## Links

- Spec: —
- Related items: ITEM-124 (bible edition block identity)
