# Implementation Plan: the rail says what each section is, and its marks are the stage's own

**Spec**: `specs/151-rail-icons/spec.md`
**Branch**: `feat/151-rail-icons`
**Bump**: `minor`
**Preview**: `specs/151-rail-icons/preview/preview.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 · Django 4.0 templates (inline SVG) · vanilla JS (`static/web/`) |
| Primary dependencies | none added — no icon font, no sprite, no package |
| Storage | none; the marks are markup |
| Testing | Playwright (Python) E2E via `StaticLiveServerTestCase`; new `tests/e2e/test_rail_marks.py`; `tests/e2e/test_stage_kind_marks.py` must stay green untouched |
| Target platform | every browser the app supports; inline SVG with `currentColor` |
| Project type | server-rendered Django web app, no build step |
| Performance goals | none — the same number of SVG nodes per page (the Bible mark gains one `<path>`, the clipboard gains one `<rect>`) |
| Constraints | every box fixed (44px button, 24px glyph, 20px kind mark at +24, 42px chip with a 23px glyph, 56/80px rows); no CSS change; no template restructured; stroke widths stay per surface |
| Scale / scope | 7 inline SVGs across 3 templates, 2 JS map entries, 1 new E2E file, 1 preview pack, 1 board card |

## Constitution Check

No `CONSTITUTION.md` exists; SDD-01 makes it optional and never auto-created, so the check is not
applicable. The repo's rules apply as the constraints above: markup only, no new token, no new
dependency, no interface.

Re-checked after Phase 1: pass — the design adds three SVG nodes at most and nothing else.

## Phase 0 — Research

See `research.md`. Six decisions, each with its alternatives and provenance; the three shapes with a
real choice were rendered at 1:1 and at 4× before being chosen, and the owner picked the Bible mark and
the song/audio split at gate 1. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity; the four marks, where each is drawn, and the invariants the tests hold.
- `contracts/` — `none` (`contracts/none.md`): no endpoint, payload, template variable, event or stored
  value.
- `quickstart.md` — the run commands, the E2E command, the preview command, the hand checks.

**The four path sets, final.**

```text
BIBLE      <path d="M12 9.6c-1.6-1.3-3.8-1.9-6.9-1.7v10.4c3.1-.2 5.3.4 6.9 1.7 1.6-1.3 3.8-1.9 6.9-1.7V7.9c-3.1-.2-5.3.4-6.9 1.7z"/>
           <path d="M12 9.6v10.4"/>
           <path d="M12 2.6v4.6M10.1 4.5h3.8"/>

CLIPBOARD  <rect x="4.6" y="3.4" width="14.8" height="17.2" rx="2"/>
           <rect x="8.6" y="1.9" width="6.8" height="3.4" rx="1.4"/>
           <path d="M8.2 9.6h7.6M8.2 13h7.6M8.2 16.4h4.8"/>

SONG       <path d="M9 17.4V5.6l10.2-2v11.6"/>
           <circle cx="6.7" cy="17.4" r="2.4"/><circle cx="16.9" cy="15.2" r="2.4"/>

AUDIO      <path d="M3.6 10.2v3.6M7.2 7.2v9.6M10.8 4.4v15.2M14.4 7.2v9.6M18 10.2v3.6"/>
```

**Where each goes.**

| File | Line | Now | Becomes |
| --- | --- | --- | --- |
| `multimedia/web/templates/reading/base.html` | 88-92 | rail Alkitab: open book | **BIBLE** |
| `multimedia/web/templates/reading/base.html` | 78 | rail Search | unchanged |
| `multimedia/web/templates/reading/base.html` | 103-108 | rail Kidung: pair | unchanged (already **SONG**) |
| `multimedia/web/templates/reading/base.html` | 119-123 | rail Tata Ibadah: page + rules | **CLIPBOARD** |
| `multimedia/web/templates/reading/base.html` | 127 | rail Media Library: folder | unchanged |
| `multimedia/web/templates/reading/base.html` | 256-261 | panel empty state, Bible: `M12 6.6S10.1 4.2 …` | **BIBLE** |
| `multimedia/web/templates/reading/base.html` | 251-256 | panel empty state, Tata Ibadah: page | **CLIPBOARD** |
| `multimedia/web/templates/reading/_entry_kind_icon.html` | 4 | `scripture`: square-cover open book | **BIBLE** |
| `multimedia/web/templates/reading/_entry_kind_icon.html` | 4 | `song`: single flagged note | **SONG** |
| `multimedia/web/templates/reading/tatib.html` | 200 | Add Passage tile: open book | **BIBLE** |
| `multimedia/web/templates/reading/tatib.html` | 204 | Add Song tile: pair | unchanged |
| `static/web/entries.js` | 65 | `EMPTY_ADD_ICONS.scripture` | **BIBLE** |
| `static/web/media-stage.js` | 6 | `paths.audio` | **AUDIO** |

The chapter list's own empty states (`base.html:364-392`) draw a *list-shape* metaphor — a 4-square
grid for the Bible, dots-and-bars for Tata Ibadah — not the section's mark, and stay.

**Why the panel empty states are in scope.** They are the largest drawing of each section's mark (48px)
and the place a reader sees it when the section is new. Leaving the rail on the clipboard and the
panel on a page would recreate the report one screen away.

**What is deliberately not done.** No CSS change (every box is already authored); no change to the
Search or Media Library marks; no change to the image, video, PDF, slides or `missing` family paths; no
change to the kind mark's 20px box; no change to `_entry_kind_icon.html`'s comment, its `aria-hidden`
or its empty `<span>` contract; no change to `media-stage.js`'s availability logic; no new icon font,
sprite or package.

**Tests first.** The seven E2E cases below are written against the unmodified templates, run red, and
only then does the markup change — one story at a time, in the order the tasks list them.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 rail Alkitab and the panel's empty state are an open book with a Latin cross | `base.html:88-92`, `base.html:256-261` | `test` → `tests/e2e/test_rail_marks.py::RailMarksE2ETests::test_the_rail_bible_and_a_passage_draw_one_path` | reads the rail button's `d` strings and asserts the cross stem and bar |
| FR-002 a passage row, the Add Passage tile and the rail draw one path | `_entry_kind_icon.html:4`, `tatib.html:200`, `entries.js:65` | `test` → same test | string equality across the three, on the service page and on an empty one |
| FR-003 rail Tata Ibadah and the panel's empty state are a clipboard | `base.html:119-123`, `base.html:251-256` | `test` → `…::test_the_rail_service_is_a_clipboard` | two `rect`s, three rules, and no page/doc path left |
| FR-004 rail Kidung = song kind mark = Add Song tile | `base.html:103-108`, `_entry_kind_icon.html:4`, `entries.js:66` | `test` → `…::test_the_rail_note_and_a_song_draw_one_path` | three-way string equality |
| FR-005 audio is a five-bar waveform everywhere it is drawn | `media-stage.js:6` | `test` → `…::test_an_audio_file_is_a_waveform_in_every_place_it_is_drawn` | `window.gkpsMediaIcon('audio')` and the stage chip's own path |
| FR-006 the other four families and `missing` are unchanged | `media-stage.js:5,7,8,9,10` | `test` → same test | compares against the shipped strings, recorded in the test |
| FR-007 every box is unchanged | `components.css` (untouched) | `test` → `…::test_the_marks_keep_their_boxes` | rail 44/24, kind mark 20 at +24, chip 42/23, rows 56/80 |
| FR-008 inline SVG, `currentColor`, `aria-hidden`, no pointer | all seven edits | `test` → `…::test_the_marks_keep_their_ink_in_both_themes`; `inspection` — the diff adds no `fill`, no `style`, no `tabindex`, no event | |
| FR-009 five destinations; Search and Media Library unchanged | `base.html` | `test` → `…::test_the_five_rail_marks_are_five_shapes_and_none_is_a_media_family` | five buttons in order, five distinct path sets, no overlap with the family map |
| US1 AC2 / AC4 (passage row, dark) | `_entry_kind_icon.html` | `test` → `test_the_rail_bible_and_a_passage_draw_one_path`, `test_the_marks_keep_their_ink_in_both_themes` | |
| US3 AC1 / AC2 (song row, tile) | `_entry_kind_icon.html`, `entries.js` | `test` → `test_the_rail_note_and_a_song_draw_one_path` | |
| US3 AC3 (song vs audio on one stage) | `media-stage.js`, `_entry_kind_icon.html` | `manual` — the preview's stage column at 1:1, then `/tatib/<id>/` | the shapes differ; the test asserts the paths differ |
| Edge: the missing / unavailable audio chip | `media-stage.js:20,26` | `inspection` — `renderRow` still chooses `missing` over the family and the chip keeps `--danger` | the waveform is the family mark, not the state |
| Edge: ≤1272px rail (64px / 40px buttons) | `components.css:116` | `inspection` — resize the live page to 1024px: the glyphs scale with the 24-unit box; no authored size changes | |
| Edge: the phone menu drawer | `base.html` rail markup | `inspection` — 425px window: the same marks beside the names | |
| SC-001 / SC-002 | as FR-009 / FR-002, FR-004 | `test` | |
| SC-003 | as FR-007 | `test` | |
| SC-004 song vs audio silhouette | preview + live page | `manual` | 1:1, both themes |
| SC-005 ink | all | `test` → `test_the_marks_keep_their_ink_in_both_themes` | computed `color` equals the element's own token in both themes |

**Verification split: 7 test · 5 inspection · 2 manual.**
