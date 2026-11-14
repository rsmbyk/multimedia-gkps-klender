---
id: ITEM-184
status: backlog
title: 'Three E2E tests are red on develop: two text-wrap assertions and an add-controls opacity'
type: fix
priority: P1
effort: S
created: 2026-10-28
updated: 2026-10-30
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-184: Three E2E tests are red on develop

## Summary

Verifying slice 144's neighbours turned up three red tests that reproduce on unmodified
`origin/develop` (`f85984a8`), in a detached worktree with its own database — so they are not that
slice's doing and predate it:

| test | failure |
| --- | --- |
| `tests.e2e.test_text_wrap.ReadingTextWrapE2ETests.test_a_long_title_wraps_inside_the_pane` | `93 not greater than 93.312` — the title wraps to exactly two lines where the assertion wants more than two |
| `tests.e2e.test_text_wrap.ReadingTextWrapE2ETests.test_a_short_title_is_unchanged` | `47 not greater than 74.6496` — a 57-character spaced title stays on one line at a 1172px width |
| `tests.e2e.test_entries.EntryModalE2ETests.test_the_add_controls_wait_for_a_hover` | `'1' != '0'` — the controls are visible without a hover |

## Notes

- The two `test_text_wrap` failures look like assertions calibrated against an older type scale or
  pane width: the first is off by a third of a pixel (`93` against `93.312`) and its message still
  says "one line again" while the title is on two.
- `test_the_add_controls_wait_for_a_hover` reads the controls' computed `opacity` right after load;
  whether the pointer rests over a row at that moment may decide it, which would make it flaky
  rather than wrong.
- Run for the record:

  ```sh
  DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/gkps144v" \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
    tests.e2e.test_text_wrap.ReadingTextWrapE2ETests.test_a_long_title_wraps_inside_the_pane \
    tests.e2e.test_text_wrap.ReadingTextWrapE2ETests.test_a_short_title_is_unchanged \
    tests.e2e.test_entries.EntryModalE2ETests.test_the_add_controls_wait_for_a_hover
  ```
- Found while converging slice 144; that slice's own module is green and untouched by these.

## Acceptance sketch

- Each of the three tests either passes on `develop` or is rewritten to assert the behaviour the
  page actually has, with the measurement that decided it recorded in the card.

## Links

- Spec: —
- Related items: ITEM-137, ITEM-153, ITEM-156 (the other known-reds on `develop`)
- Found by: [144](../specs/144-passage-song-icons/converge.md)
