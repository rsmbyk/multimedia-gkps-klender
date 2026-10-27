# Implementation Plan: a reading page's text wraps at its pane

**Slice**: `specs/137-reading-text-wrap` · **Branch**: `feat/137-reading-text-wrap`
**Date**: 2026-10-27 · **Status**: Draft (gate 1 accepted the spec on 2026-10-27)
**bump**: `patch` — a presentation fix to existing surfaces; no stored value, endpoint or capability
is added or removed. One `CHANGELOG.md` line under `## [Unreleased]`: *"Long text wraps inside its
pane instead of running past it, on every reading page."*

## Technical Context

| | |
| --- | --- |
| Language | Python 3.12, Django 4.0 templates |
| Front end | server-rendered templates, vanilla JS, hand-written CSS; no framework, no build step |
| Files | `static/styles/design/components.css` (the fix); `tests/e2e/test_text_wrap.py` (new) |
| Data | no migration, no payload change — every page already sends the text it draws |
| Tests | Playwright E2E through `StaticLiveServerTestCase` (`tests/e2e/`), the repository's user-visible acceptance layer |
| Constraints | no new tokens, fonts, icons or dependencies; the truncating surfaces keep their own declarations; nothing is added to a template, a view or a model |

## Constitution Check

`CONSTITUTION.md` does not exist and is never auto-created (SDD-01). No principle to check against;
nothing to justify in a Complexity Tracking table.

- Before Phase 0: n/a — no constitution.
- After Phase 1: n/a — no constitution.

## Phase 0 — Research

`research.md` records five decisions, all with provenance, and exits at zero unknowns:

1. `overflow-wrap: break-word` over `anywhere` — the two differ only in whether the soft wrap counts
   toward min-content, and the title is a flex item whose row must keep its present shape (CSS Text
   Level 3; MDN).
2. Three roots, not per-element: `.read`, `.search-results`, `.preview` — the property is inherited,
   and those are the three places a reading surface's text lives.
3. The truncating surfaces keep their own `white-space: nowrap` / `-webkit-line-clamp`; a wrap rule
   cannot reach them.
4. No markup or server change is needed: the text is already in the document.
5. Zero unknowns left.

## Phase 1 — Design artifacts

- `data-model.md` — no entity; the boxes and their computed text properties before and after.
- `contracts/none.md` — this slice exposes no interface; stated rather than absent.
- `quickstart.md` — the commands that run the slice's checks.

## Design

### Stylesheet (`static/styles/design/components.css`, after the `[data-read="on"] .read` block)

```css
.read,
.search-results,
.preview { overflow-wrap: break-word; }
```

That is the whole change. It sits with the other reading-root rules, and every text run inside those
three roots — the title, the eyebrow, section headings, verse and lyric lines, body paragraphs,
search rows, the Preview modal's lines — inherits it.

Why it is enough, measured on the served pages before the rule: `.read__title` 1,082px past its box
on `/tatib/149/`, 444px on `/songs/1817/`; `p.tatib__tx` 215px; `h2.read__sec` 143px at 1280×800;
`.result-row__title` 614px. After it, every one of them is 0 and the document's horizontal overflow
is 0 on every route at 1440, 1280, 820 and 390.

Why `break-word`: `anywhere` also counts its soft wraps in min-content, which would let `.read__row`
keep the TB/SIM toggle beside a title squeezed to a few characters. `break-word` leaves min-content
alone, so the toggle keeps the line it takes today and only a run that cannot fit breaks (CSS Text
Level 3; MDN `overflow-wrap`).

Left alone because they declare their own cut: `.book__n` and the media filenames (`nowrap` +
`text-overflow: ellipsis`), `.songrow__t` (`overflow-wrap: anywhere` + three-line clamp, spec 135).
The projector and the OBS dock already set `break-word` / `anywhere` in their own stylesheets.

### Tests (`tests/e2e/test_text_wrap.py`, new)

One class, `ReadingTextWrapE2ETests`, with fixtures built in `setUp`: a service whose name is a
64-character unbroken run holding a Text entry whose body is a long Drive URL; a song whose title
is a long unbroken run plus a name; a Bible chapter with a long pericope heading and a long verse.
Each test measures the painted text against the box that owns it (range rectangles vs the element's
padding box) and the document's `scrollWidth` against its `clientWidth` — the two numbers the spec's
success criteria name.

## Traceability

| ID | Requirement / scenario | Component | Verified by |
| --- | --- | --- | --- |
| FR-001 | a page title wraps at its box's edge; nothing past the pane, no document overflow | `.read` inheritance on `.read__title` | `test` — `tests/e2e/test_text_wrap.py::test_a_long_title_wraps_inside_the_pane` |
| FR-002 | headings, verse/lyric lines and body paragraphs wrap the same way | `.read` inheritance | `test` — `test_a_bible_heading_and_verse_wrap`, `test_a_body_paragraph_holding_a_link_wraps` |
| FR-003 | a search result's title, meta and excerpt wrap | `.search-results` inheritance | `test` — `test_a_search_result_title_wraps` |
| FR-004 | the Preview modal's lines and references wrap | `.preview` inheritance | `test` — `test_preview_lines_wrap` |
| FR-005 | no reading route scrolls sideways at four widths | the three roots | `test` — `test_no_reading_route_scrolls_sideways` |
| FR-006 | truncating surfaces keep their cut | untouched `nowrap` / clamp declarations | `test` — `test_a_truncating_row_still_truncates` |
| FR-007 | the layout's own measuring is unchanged | `break-word` rather than `anywhere` | `test` — `test_the_title_keeps_its_box_and_the_toggle_its_line` |
| FR-008 | text that already fits renders as today | inheritance is a no-op when a run fits | `test` — `test_a_short_title_is_unchanged` |
| FR-009 | the rule reaches a surface by inheritance from its root | three selectors in `components.css` | `inspection` — the rule block, and `test_a_long_title_wraps_inside_the_pane` asserting the computed value on a nested span |
| SC-001 | no route scrolls sideways at 1440/1280/820/390 | the three roots | `test` — `test_no_reading_route_scrolls_sideways` (eight routes × four widths) |
| SC-002 | a 64-character title is wholly inside the pane | `.read__title` | `test` — `test_a_long_title_wraps_inside_the_pane` |
| SC-003 | titles that fit are unchanged | inheritance no-op | `test` — `test_a_short_title_is_unchanged` |
| SC-004 | truncating surfaces still truncate | untouched declarations | `test` — `test_a_truncating_row_still_truncates` |
| SC-005 | the title's box width is unchanged at every width | `break-word` | `test` — `test_the_title_keeps_its_box_and_the_toggle_its_line` |
| SC-006 | the body paragraph wraps | `.read` inheritance on `.tatib__tx` | `test` — `test_a_body_paragraph_holding_a_link_wraps` |
| SC-007 | the Bible heading and the search row wrap | `.read` / `.search-results` | `test` — `test_a_bible_heading_and_verse_wrap`, `test_a_search_result_title_wraps` |
| US1.1 | the Tata Ibadah title takes 4 lines inside 400px, no overflow | `.read__title` | `test` — `test_a_long_title_wraps_inside_the_pane` |
| US1.2 | the song title wraps at the space and breaks the unbroken part | `.read__title` | `test` — `test_a_long_title_wraps_inside_the_pane` |
| US1.3 | a title that fits is one line, same height | inheritance no-op | `test` — `test_a_short_title_is_unchanged` |
| US1.4 | the same holds at 390×844 | `.read__title` | `test` — `test_a_long_title_wraps_inside_the_pane` (390 viewport) |
| US2.1 | a Bible heading wraps at 1280×800 | `.read__sec` | `test` — `test_a_bible_heading_and_verse_wrap` |
| US2.2 | a pasted URL wraps onto two lines at 1440×900 | `.tatib__tx` | `test` — `test_a_body_paragraph_holding_a_link_wraps` |
| US2.3 | a search result title wraps inside its row | `.result-row__title` | `test` — `test_a_search_result_title_wraps` |
| US2.4 | the Preview modal's lines wrap | `.preview__line` | `test` — `test_preview_lines_wrap` |
| US3.1 | a sidebar service row stays one line ending `…` | `.book__n` | `test` — `test_a_truncating_row_still_truncates` |
| US3.2 | a media filename stays one line ending `…` | `.media-library__filename` | `inspection` — the declaration is untouched; the preview's media-library page shows the same row |
| US3.3 | a contents row keeps its three-line clamp | `.songrow__t` | `test` — `test_a_truncating_row_still_truncates` |
| Edge | a one-character run changes nothing | inheritance | `inspection` — covered by `test_a_short_title_is_unchanged` |
| Edge | the TB/SIM toggle keeps the line it takes today | `break-word` | `test` — `test_the_title_keeps_its_box_and_the_toggle_its_line` |
| Edge | a long title with spaces wraps at the spaces as today | inheritance | `test` — `test_a_short_title_is_unchanged` asserts a spaced title's line count |
| Edge | `nowrap` text keeps not wrapping | the surfaces' own declarations | `test` — `test_a_truncating_row_still_truncates` |
| Edge | a page with no long text is byte-for-byte the same layout | inheritance no-op | `test` — `test_a_short_title_is_unchanged` |
| Edge | the search page's results, where `.read` is hidden, still wrap | `.search-results` root | `test` — `test_a_search_result_title_wraps` |

**Verification split: 30 test · 3 inspection · 0 manual.** Untested is allowed; unverifiable is not.

## Risks

- **The declaration is already in the tree.** The live preview serves it (SDD-06), so Implement's
  first act is the red test rather than the edit; the rule is then confirmed, not re-written. If a
  test disagrees with the rule, the rule moves and the preview is rebuilt.
- **`break-word` is the quieter of the two values** — a future reader may "improve" it to `anywhere`.
  `test_the_title_keeps_its_box_and_the_toggle_its_line` fails if they do, because the toggle's line
  changes.
- **A wrap rule cannot reach `nowrap` text** — that is why the truncating surfaces are unaffected;
  `test_a_truncating_row_still_truncates` pins it, so a later unclip is a red test rather than a
  silent change.
- **The media-library filename path is not exercised by a browser test** (no fixture media file in
  the suite); the declaration is untouched, and the preview shows the same one-line row.
