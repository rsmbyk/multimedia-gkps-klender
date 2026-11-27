# Convergence: A passage cue carries its current and end verse

**Spec**: `specs/229-cue-verse-counter/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-23

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| none | — | FR-001 … FR-007, SC-001 … SC-004, US1/AC1 … AC5, US2/AC1 … AC5 | Each row checked by its declared method below. |

**Outcome**: zero findings, so no `## Phase N: Convergence` tasks were appended.

### Read-back by declared method

- **test (red → green)** — the payload case failed with `KeyError: 'verse_start'` before the
  server change, then `OK` in 0.034s after it. The three new service E2E cases and the new Go To
  case failed on `.cue-verse` not existing (or `1/3 != 2/3`) before the JS change, then `OK` in
  6.686s after it; the four together were red on the untouched cue with three
  `Page.wait_for_selector: Timeout ... waiting for locator(".cue-verse")`.
- **test** — after the change, a targeted lane of the four new cases plus
  `test_corner_cue_parts_share_the_bottom_band_vertical_center`,
  `test_a_verse_step_inside_a_chapter_makes_no_request` and
  `test_goto_passage_translation_flip_brightens_the_label` ran 7 tests: the four new ones and both
  neighbouring regression cases passed.
- **test** — the service case also measures the counter's box at 1440×900: `#corner-cue`,
  `#cue-prefix`, `.cue-verse` and `.cue-translation` all centre at 868px (`viewport − 32px`,
  ±0.5px), so the added span did not move the 24px band or the flip.
- **inspection** — `git diff -- static/styles/design/projector.css` is empty; no token, font,
  selector, state field, endpoint or message changed. `static/web/projector.js` gained one helper
  pair and one call in each cue renderer; the flip's click handler is byte-identical.
- **inspection** — the Go To counter is derived at render time from `detour.editions` and
  `detour.verse`, so a chapter crossing, an edition flip and a Go To started by the dock or the
  reading page use the same path; the new E2E case proves the flip leaves the numbers unchanged.
- **known red, not a regression** — `test_goto_passage_translation_flip_brightens_the_label` and
  `ServiceProjectorTests::test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own`
  fail identically on unmodified `develop` in their own lanes (the first reproduces at
  `4ea9a6ab`, 36s, at the flip locator; the second is the recorded ITEM-217 unit-lane red). Neither
  is caused by this slice; the first's neighbouring cue steps and the rest of `ServiceProjectorTests`
  pass.

## Pass 2

Not needed — Pass 1 converged.

## Accepted gaps

The two pre-existing reds above are left in place; both are outside this slice's behaviour and
already carried on the board as known reds.

## Cap reached

Not reached.
