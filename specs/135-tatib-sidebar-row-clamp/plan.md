# Implementation Plan: a Tata Ibadah sidebar row is three lines, ellipsized

**Slice**: `specs/135-tatib-sidebar-row-clamp` · **Branch**: `feat/135-tatib-sidebar-row-clamp`
**Date**: 2026-10-26 · **Status**: Draft (gate 1 accepted the spec on 2026-10-26)
**bump**: `patch` — a presentation change to an existing surface; no stored value, endpoint or
capability is added or removed.

## Technical Context

| | |
| --- | --- |
| Language | Python 3.12, Django 4.0 templates |
| Front end | server-rendered template, vanilla JS, hand-written CSS; no framework, no build step |
| Files | `multimedia/web/reading/views.py`, `multimedia/web/templates/reading/_toc.html`, `static/styles/design/components.css`, `static/web/offline-render.js` |
| Data | no migration; `toc_items` payload only |
| Tests | Django `TestCase` for the payload rules (`multimedia/web/tests.py`); Playwright E2E through `LiveServerTestCase` for the rendered geometry (`tests/e2e/`) |
| Constraints | no new tokens, fonts, icons or dependencies; the drag ghost and the in-place rebuild must inherit the change without their own edits |

## Constitution Check

`CONSTITUTION.md` does not exist and is never auto-created (SDD-01). No principle to check against;
nothing to justify in a Complexity Tracking table.

- Before Phase 0: n/a — no constitution.
- After Phase 1: n/a — no constitution.

## Phase 0 — Research

`research.md` records seven decisions, all with provenance, and exits at zero unknowns:

1. one clamped box per label, with `overflow-wrap: anywhere` — the rule every kind inherits;
2. a song's heading and its `Bait …` line are two blocks, no `<br>` between them, the heading clamped
   at two lines so the `Bait …` line is always third;
3. two ellipsis paths (the browser's at the clamp, a literal `…` where the server drops lines);
4. the payload carries `label_lines` rather than a capped string, and `two_line_label` goes;
5. the legacy row follows the Text entry's shape;
6. the four places that draw a row, and why the other two need no edit;
7. no new unknowns.

## Phase 1 — Design artifacts

- `data-model.md` — no entity change; the `toc_items` payload's before/after and the line composition
  per kind.
- `contracts/toc-item.md` — the producer/consumer contract, its six rules, and the compatibility note.
- `quickstart.md` — the commands that run the slice's checks.

## Design

### Stylesheet (`static/styles/design/components.css`, beside `.songrow__t`)

```css
.songrow__t {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  overflow-wrap: anywhere;
  min-width: 0;
}
/* A song with a Bait line spends at most two lines on its heading, so the Bait
   line is always third. */
.songrow__t--song:has(.songrow__verses) .songrow__heading {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}
```

`.songrow__t--lines`'s flex column goes; the lines become `<br>`-separated text in the one box.
`.songrow__line--blank` and `.songrow__t--song .songrow__heading/verses { display: inline }` are
removed with it.

### Template (`_toc.html`)

One branch for every non-song row:

```html
<span class="songrow__t">{% for line in item.label_lines %}{{ line }}{% if not forloop.last %}<br>{% endif %}{% endfor %}</span>
```

and the song branch without its `<br>`, keeping `.songrow__heading` and `.songrow__verses` as the
box's two items.

### Server (`views.py`, `_tatib_stage`)

- Delete `label = label[:60]` and the legacy `label[:60] + '…'`.
- Build `label_lines` for every row: the first three body lines for an untitled text or legacy row
  (`_clamped_paragraphs` already returns three and a `clipped` flag — append `…` to the last line when
  `clipped`), the title alone for a titled row, the citation for a passage, the kind's name for a
  break, `[reference + title]` + `[verse_line]` for a song.
- `label` becomes the plain, space-joined text of those lines; `two_line_label` is dropped.
- `txt` (the filter's haystack) keeps the whole entry, as today.

### Saved renderer (`offline-render.js`, `servicePage`)

Mirror the template: `label_lines` joined with `<br>`; the song row's two blocks without a `<br>`;
drop the `two_line_label` branch.

## Traceability

| ID | Requirement / scenario | Component | Verified by |
| --- | --- | --- | --- |
| FR-001 | a row is capped at three visual lines and ends `…` when text is hidden | `.songrow__t` clamp + payload `…` | `test` — `tests/e2e/test_reading.py::test_a_contents_row_is_three_lines_and_ellipsized` |
| FR-002 | the 60-character cut is gone | `_tatib_stage` | `test` — `multimedia/web/tests.py::test_a_row_label_is_no_longer_cut_at_sixty_characters` |
| FR-003 | an untitled text row carries the body's first three lines | `_tatib_stage` | `test` — `multimedia/web/tests.py::test_an_untitled_text_row_carries_three_body_lines` |
| FR-004 | a titled text row carries its title alone | `_tatib_stage` | `test` — `multimedia/web/tests.py::test_a_titled_text_row_carries_its_title_alone` |
| FR-005 | a song row's heading takes at most two lines and `Bait …` is always third | `_tatib_stage` + heading clamp | `test` — `multimedia/web/tests.py::test_a_song_row_sends_its_heading_and_bait_line_separately`; `tests/e2e/test_reading.py::test_a_song_row_keeps_its_bait_line_under_a_long_heading` |
| FR-006 | passage, media and section-break rows obey the same cap | shared `.songrow__t` | `test` — `tests/e2e/test_reading.py::test_every_row_kind_stays_within_three_lines` |
| FR-007 | a legacy row follows the Text entry's shape | `_tatib_stage` | `test` — `multimedia/web/tests.py::test_a_legacy_row_follows_the_text_entry_shape` |
| FR-008 | any label wraps at the pane's edge, in every kind | `overflow-wrap: anywhere` | `test` — `tests/e2e/test_reading.py::test_no_row_label_overflows_the_panel` |
| FR-009 | the saved copy draws the same rows | `offline-render.js` | `test` — `tests/e2e/test_saved_render_parity.py::test_a_saved_service_row_matches_the_server_row` |
| FR-010 | the filter still matches the whole text | `txt` unchanged | `test` — `multimedia/web/tests.py::test_the_filter_text_keeps_the_whole_entry` |
| SC-001 | no row exceeds three text lines at 1440×900, 1280×800, 390×844 | clamp | `test` — `tests/e2e/test_reading.py::test_every_row_kind_stays_within_three_lines` (three viewports) |
| SC-002 | every row that hides text ends `…` | clamp + literal `…` | `test` — both rows of FR-001/FR-003 assertions |
| SC-003 | no label is cut at 60 characters | `_tatib_stage` | `test` — FR-002's test asserts a 64-character title in full |
| SC-004 | the saved page's rows equal the server's | `offline-render.js` | `test` — FR-009's test compares line counts and trailing `…` |
| SC-005 | no label overflows its pane at the three widths | `overflow-wrap` | `test` — FR-008's test asserts `scrollWidth == clientWidth` |
| US1.1 | a wrapping row is three lines ending `…` | clamp | `test` — FR-001 |
| US1.2 | a row that fits shows no `…` | payload | `test` — `multimedia/web/tests.py::test_a_row_that_fits_carries_no_ellipsis` |
| US1.3 | a 61–64-character title is shown whole when it fits | `_tatib_stage` | `test` — FR-002 |
| US1.4 | a body longer than three lines shows three and ends `…` | `_clamped_paragraphs` | `test` — FR-003 |
| US1.5 | an 81-character unbroken link wraps inside the pane | `overflow-wrap` | `test` — FR-008 |
| US2.1 | a one-line heading then `Bait …` | template/CSS | `test` — FR-005 |
| US2.2 | a two-line heading then `Bait …` | heading clamp | `test` — FR-005 (E2E half) |
| US2.3 | a longer heading is capped at two lines with `…`, `Bait …` third | heading clamp | `test` — FR-005 (E2E half) |
| US2.4 | a song with no verse line uses all three lines | `_tatib_stage` | `test` — `multimedia/web/tests.py::test_a_song_without_a_verse_line_has_three_lines_for_its_heading` |
| US3.1 | the saved row equals the server row | `offline-render.js` | `test` — FR-009 |
| Edge | a blank body line keeps its line | `<br>` lines | `inspection` — `_toc.html`, case 13 of `preview/cases.html`: the blank line draws an empty line box |
| Edge | hover/selected/focus keep the row's height | CSS | `manual` — hover and select a three-line row in `preview/cases.html`; height does not change |
| Edge | the stage's own three-line pane is untouched | `PANE_TEXT_LINES` | `inspection` — `views.py:929` unchanged, `_clamped_paragraphs` still 3 |

**Verification split: 24 test · 2 inspection · 1 manual.** Untested is allowed; unverifiable is not.

## Risks

- **The drag ghost and the in-place rebuild** — both clone or re-render a row, so they inherit the
  change; `test` coverage for the ghost is the existing `tests/e2e/test_reorder.py`, re-run at
  Converge rather than extended.
- **`:has()`** — already used in this stylesheet (`.editor:has([data-editor-size="large"])`), so no
  new baseline; the E2E row tests would fail loudly on a browser without it.
