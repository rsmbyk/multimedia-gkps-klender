# Implementation Plan: the overlay's text wraps inside the box that owns it

**Slice**: `specs/183-overlay-text-wrap` · **Branch**: `fix/183-overlay-text-wrap`
**Date**: 2026-11-02 · **Status**: Draft (gate 1 accepted 2026-11-02; scope widened at gate 2 the same
day, so the spec and this plan were revised before delivery)
**bump**: `patch` — a presentation fix on an existing surface; no stored value, endpoint or capability
is added or removed. One `CHANGELOG.md` line under `## [Unreleased]`: *"A long run in the OBS overlay's
text — a lyric, a reference, an entry title or a liturgy turn — wraps inside its panel instead of
running across the frame."*

## Technical Context

| | |
| --- | --- |
| Language | Python 3.12, Django 4.0 templates |
| Front end | server-rendered shell plus a vanilla-JS controller; hand-written CSS, no framework, no build step |
| Files | `static/styles/design/obs-overlay.css` (the fix); `tests/e2e/test_obs_overlay_wrap.py` (new) |
| Data | no migration, no payload change — the words are already in the display state |
| Tests | Playwright E2E through `StaticLiveServerTestCase` (`tests/e2e/`), the repository's user-visible acceptance layer |
| Constraints | no new tokens, fonts, icons or dependencies; the speaker mark keeps its own `nowrap`; nothing is added to a template, a view or a model |

## Constitution Check

`CONSTITUTION.md` does not exist and is never auto-created (SDD-01). No principle to check against, and
nothing to justify in a Complexity Tracking table.

- Before Phase 0: n/a — no constitution.
- After Phase 1: n/a — no constitution.

## Phase 0 — Research

[`research.md`](./research.md) records six decisions with provenance and exits at zero unknowns:
`break-word` over `anywhere` (measured identical here; only `anywhere` can move a box), one declaration
on the stage (widened by the owner at gate 2 — D002 carries the revision), no height limit (the
surface's answer to too much text is the operator's screen breaks), ink against the content edge as the
measurement, "unchanged" measured by taking the rule away on the live page, and the fixture's shapes.

## Phase 1 — Design artifacts

- [`data-model.md`](./data-model.md) — no entity; the elements, their computed property before and
  after, and the three panel boxes the change moves.
- [`contracts/none.md`](./contracts/none.md) — this slice exposes no interface; stated rather than
  absent.
- [`quickstart.md`](./quickstart.md) — the database, the fixture, the tests, the review page and the
  probe, each as a command that runs.

## Design

### Stylesheet (`static/styles/design/obs-overlay.css`, on the `.obs-overlay__stage` block)

```css
.obs-overlay__stage {
  /* … */
  overflow-wrap: break-word;
}
```

The property inherits, so every text the surface paints is covered without a second declaration: the
plate's body rows, its `.obs-overlay__words` column when a speaker mark owns the first, its `.kicker`
and `.title`, and the song's `.caption`. A speaker's mark is the one exception — it is a label and keeps
its own `white-space: nowrap`. No box, margin, padding or type is touched; each panel's height follows
the rows that result, and its width, anchor and `fit-content` measure are untouched (FR-003).

### Test (`tests/e2e/test_obs_overlay_wrap.py`, new)

Nine cases, driving the dock and reading the overlay the way an operator produces it: the report's body
at 1080p, a marked row's pasted link, the same body at 1280×720 and 960×540, the song caption and its
own look, the passage's long verse title, the 64-character kicker, a control body with the rule removed
and re-measured, the property's inheritance from the stage, and the mark's `nowrap` column.

## Traceability

`Verified by` = `test` · `inspection` · `manual`. Every `test` row names its file and function.

### Requirements

| ID | Behaviour | Component | Verified by |
| --- | --- | --- | --- |
| FR-001 | any text breaks at the edge of the box that owns it — body, words column, kicker, title, caption | `obs-overlay.css` `.obs-overlay__stage` | `test` — `tests/e2e/test_obs_overlay_wrap.py::test_a_long_run_wraps_inside_the_plate`, `::test_a_pasted_link_wraps_in_the_words_column_after_a_mark`, `::test_a_song_caption_wraps_its_long_run`, `::test_a_passage_heading_wraps_its_long_run`, `::test_the_wrap_holds_at_three_frame_sizes` |
| FR-002 | one declaration on the stage reaches every text | same | `test` — `::test_the_rule_is_inherited_from_the_stage` |
| FR-003 | the panels' measuring and a fitting text are unchanged | same | `test` — `::test_a_body_that_fits_draws_the_same_box_with_the_rule_removed`, `::test_a_long_kicker_stays_inside_the_plate` |
| FR-004 | a speaker's mark keeps `nowrap` and its column | `obs-overlay.css` `.obs-overlay__speaker`, `.obs-overlay__line.has-mark` | `test` — `::test_the_mark_keeps_its_own_column` |
| FR-005 | the surface paints nothing when nothing is on air | `static/web/obs-overlay.js` `modelOf`, `paint` | `inspection` — `modelOf` returns `null` for a blank screen, `media` and `break`; the sheet adds no paint. The hide case is covered by `tests/e2e/test_obs_overlay.py::test_hide_empties_the_overlay_and_nothing_is_focusable` |
| FR-006 | the caption keeps its type, centring and balance | `obs-overlay.css` `.obs-overlay__caption` | `test` — `::test_a_song_caption_wraps_its_long_run` (weight 800, `text-align: center`, `text-wrap: balance`, outline present) |
| FR-007 | the same wrap at 1920×1080, 1280×720 and 960×540 | same | `test` — `::test_the_wrap_holds_at_three_frame_sizes` |

### Success criteria

| ID | Criterion | Verified by |
| --- | --- | --- |
| SC-001 | no text ink past its panel on seven states at three frames | `test` — `::test_a_long_run_wraps_inside_the_plate`, `::test_a_pasted_link_wraps_in_the_words_column_after_a_mark`, `::test_a_song_caption_wraps_its_long_run`, `::test_a_passage_heading_wraps_its_long_run`, `::test_a_long_kicker_stays_inside_the_plate`, `::test_the_wrap_holds_at_three_frame_sizes` |
| SC-002 | text that fits is identical to 1.26.0 | `test` — `::test_a_body_that_fits_draws_the_same_box_with_the_rule_removed`, `::test_a_long_kicker_stays_inside_the_plate` |
| SC-003 | the rule is inherited, not repeated | `test` — `::test_the_rule_is_inherited_from_the_stage` |
| SC-004 | nothing painted on blank, hidden, released, media and rest | `inspection` — `modelOf`/`paint` in `obs-overlay.js`; the hide path by the existing 119 test named in FR-005 |
| SC-005 | the marks still hold their column | `test` — `::test_the_mark_keeps_its_own_column` |
| SC-006 | the caption keeps its own look | `test` — `::test_a_song_caption_wraps_its_long_run` |

### Story scenarios

| Scenario | Verified by |
| --- | --- |
| US1.1 — the report's body at 1080p | `test` — `::test_a_long_run_wraps_inside_the_plate` |
| US1.2 — a pasted link after a mark | `test` — `::test_a_pasted_link_wraps_in_the_words_column_after_a_mark` |
| US1.3 — the song caption's 66-character run | `test` — `::test_a_song_caption_wraps_its_long_run` |
| US1.4 — the passage's long verse title | `test` — `::test_a_passage_heading_wraps_its_long_run` |
| US1.5 — the same at 1280 and 960 | `test` — `::test_the_wrap_holds_at_three_frame_sizes` |
| US1.6 — a 64-character kicker | `test` — `::test_a_long_kicker_stays_inside_the_plate` |
| US2.1–2.3 — fitting text, unchanged, at three frames | `test` — `::test_a_body_that_fits_draws_the_same_box_with_the_rule_removed`; the three-frame boxes are the review page's |
| US3.1 — nothing on air paints nothing | `inspection` — `paint(null)` on a state with `on: false` |
| US3.2 — media and rests paint nothing | `inspection` — `modelOf` returns `null` for `media` and `break` |
| US3.3 — the panels' arrivals and exits still animate | `test` — `tests/e2e/test_obs_overlay.py::test_a_panel_enters_and_leaves_with_a_short_motion`, `::test_a_caption_enters_and_leaves_with_the_same_clock` |

**Split: 16 test · 2 inspection · 0 manual.**

## Exit gate

Requirement coverage 7/7 · entity coverage n/a (no entity) · interface coverage stated `none` ·
decision provenance six decisions in `research.md` · constitution conformance n/a · zero unknowns ·
verification declared above · `quickstart.md` runs as written.
