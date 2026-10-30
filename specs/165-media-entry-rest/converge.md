# Convergence: a media entry ends on a rest like every other entry

**Date**: 2026-10-29 · **Pass**: 1 · **Branch**: `feat/165-media-entry-rest` (base `59182b12`)

## What was checked

Every row of `plan.md`'s traceability table, by the method it declared, against the branch's own server
(`http://127.0.0.1:8864`, worktree code, the compose database) and the named suites.

## Findings

| Row | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001 five families, one rest each | test | `multimedia.web.test_media` (`MediaEntryRestTests::test_each_family_ends_on_one_rest`, five sub-cases) — green | holds |
| FR-002 a no-file entry keeps one rest | test | `…::test_a_media_entry_without_a_file_keeps_its_one_rest` — green | holds |
| FR-003 the rest is the built-in blank | test | `…::test_the_rest_carries_only_the_built_in_blank` (keys exactly `blank, header, lines, entry_index`) — green | holds |
| FR-004 `start` unchanged, `end` = the rest | test | `…::test_the_entry_range_extends_over_the_rest` — green | holds |
| FR-005 the dock lists and steps the rest | test | `tests.e2e.test_obs_dock` (12) green, including the new `test_a_media_entry_lists_and_steps_its_rest`; seen red without the change (`['IMAGE'] != ['IMAGE', 'Rest']`) | holds |
| FR-006 media payloads, fit, lock, overlay unchanged | test | the four rewritten unit cases keep their payload assertions; `tests.e2e.test_projector` green; the five media display modules ran 49 cases with 2 failures that reproduce on the base commit — see below | holds, with a pre-existing red |
| US1 AC1–AC3 four pictures rest between them | test | `…::test_four_images_in_a_row_build_ten_screens`; live `/projector?service=149` — 10 sections, `content, blank` five times | holds |
| US1 AC4 no file, one screen | test | as FR-002 | holds |
| US2 AC2 the forward arrow lands on the rest | test | `tests.e2e.test_projector::…::test_a_media_entry_steps_onto_its_rest` green; seen red without the change (timeout waiting for `is-blank`) | holds |
| US2 AC3 a service ending on media ends on a rest | test | live check: services 149, 146 and 144 each end with `blank: true` | holds |
| US3 AC1–AC3 no other kind moves | test / inspection | the diff touches the media branch only; `multimedia.web.tests` green after `collectstatic` (see below); the projector's 167 → 171 screens on service 144 keep every non-media range's shape | holds |
| SC-001 service 149 builds ten screens, ranges `(0,1)(2,3)(4,5)(6,7)(8,9)` | test | live island read: ranges exactly those, blanks at 1, 3, 5, 7, 9 | holds |
| SC-005 the projector paints the rest as its blank | test | `.screen.is-blank` is the active screen at index 3 on the dock's step; the projector module passes | holds |
| SC-006 the suites stay green | test | see the run list below | holds, with the pre-existing red |

## Runs

| Command | Result |
| --- | --- |
| `manage.py test multimedia.web.test_media multimedia.web.test_obs_dock` | **37 / 37 OK** |
| `manage.py test tests.e2e.test_obs_dock` | **12 / 12 OK** |
| `manage.py test tests.e2e.test_projector` | **OK** |
| `manage.py test multimedia.web.tests` | **OK** (after `collectstatic`; before it, 6 `ServiceReorderPaneTests` error with `Missing staticfiles manifest entry for 'assets/gkps.png'` — the worktree had no `_static/`, and the same errors appear without this change) |
| `manage.py test tests.e2e.test_image_display test_video_display test_pdf_display test_powerpoint_display test_audio_display` | **47 / 49**, the two failures — `test_video_display::test_navigation_and_display_off_stop_and_reset_video` and `test_audio_display::test_untitled_preview_and_projector_idle_display_off` — reproduced with the branch's change stashed on the base commit, both asserting `body[data-showing="false"]` after a `stop` broadcast; that is **ITEM-140** on the board, already carded as identical on `develop` |

## Findings and disposition

- **A pre-existing red, not this slice's.** The two display-off failures are ITEM-140's; no new card. The
  six manifest errors are the local environment (no `_static/`), cured by `collectstatic`.
- **The dock's number is the preview's number.** The live dock at 420px reads the media entry's inner body
  at 69.7px with rows 352×28.8 — the same values the preview and `spec.md §UI/UX` state.
- **Task T011 expected no production change**, and none was needed: the dock's `screenRow`, `buildInner`
  and `buildStops` followed the new screen without an edit.

## Outcome

**Converged** — every row holds by its declared method, with the two pre-existing failures attributed to
ITEM-140 and the environment. No accepted gaps; nothing to fold as `not folded`.
