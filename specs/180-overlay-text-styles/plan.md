# Implementation Plan: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md`
**Branch**: `feat/180-overlay-text-styles`
**Bump**: `minor`
**Preview**: `specs/180-overlay-text-styles/preview/` — static preview (`overlay-preview.html`, `overlay-motion.html`,
`overlay-sequence.html`, `overlay-walkthrough.mp4`) and the live surface at `http://127.0.0.1:8816/obs/source/overlay`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 · Django 4.0 · vanilla ES2017 in the browser (no build step) |
| Primary dependencies | none added — the overlay is plain DOM + CSS; Source Sans 3 is already bundled under `static/assets/fonts/` |
| Storage | none — the overlay keeps no record; it reads the projector page's data islands once per service and the `gkps-display` state |
| Testing | Django `LiveServerTestCase` + Playwright (Python) E2E; one Django unit test on the screen payload |
| Target platform | OBS browser source (CEF) and any browser; transparent page, any output resolution from 720p to 2160p |
| Project type | server-rendered Django templates + static CSS/JS |
| Performance goals | one repaint per screen change; motion 180 ms in / 120 ms out on the compositor; no reflow while a panel morphs |
| Constraints | listen-only surface — no control, no focusable element; every size in container units of the stage; the page must stay transparent for OBS |
| Scale / scope | three kinds · 15 review states · a 170-screen service; text up to the longest verse in the database (501 characters) |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| — | `n/a` | this repository carries no `CONSTITUTION.md`; SDD-01 makes it optional and forbids creating it automatically |

Re-checked after Phase 1: `n/a` — still no constitution, and nothing in the design would violate the repo's standing
conventions (listen-only overlay, container-unit sizing, no new dependency, no server route).

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the four objects the overlay reads or paints (Screen, Entry, Display state, Plate); no table.
- `contracts/` — `none`: this slice exposes no external interface. It *consumes* two internal ones (the projector
  page's data islands and the `gkps-display` state), both owned elsewhere and unchanged.
- `quickstart.md` — runserver + dock + overlay, the E2E commands, and the three preview pages.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/obs-overlay.js` (`modelOf` · `paint`) | `test` → `tests/e2e/test_obs_overlay.py::test_a_passage_wears_a_plate_naming_its_reference_and_title`, `::test_a_song_screen_keeps_the_bare_caption_style` | kind read from `projectorEntryData` |
| FR-002 | `static/styles/design/obs-overlay.css` (`.obs-overlay__caption`) | `test` → `test_obs_overlay.py::test_a_song_screen_keeps_the_bare_caption_style` | 800 weight, outline, transparent fill, no plate |
| FR-003 | `static/web/obs-overlay.js` (`plate` heading) | `test` → `test_obs_overlay.py::test_a_passage_wears_a_plate_naming_its_reference_and_title`, `::test_a_song_screen_does_not_repeat_the_entry_title` | kicker = first header line, title = the rest |
| FR-004 | `obs-overlay.js` (`plate` body, voice classes) | `test` → `test_obs_overlay.py::test_a_liturgy_text_wears_a_plate_with_its_title_and_quieter_leader_lines` | `is-leader` · `is-assembly` · `is-join` |
| FR-004a | `obs-overlay.css` (`[data-kind="liturgy"]` block) | `test` → same liturgy test (`borderLeftWidth`, radius in `em`) | left-aligned panel, leading bar, near-square corner |
| FR-005 | `obs-overlay.css` (`.obs-overlay__plate`) | `inspection` — live page: fill `rgba(10,12,16,.88)`, 1 px `rgba(255,255,255,.12)` border, no outline on the words | |
| FR-006 | `obs-overlay.css` (insets, `min/max-width`, `cqw` scale) | `inspection` — live page at 1920×1080: panels at `left/right/bottom: 5%`, width between 34 % and 90 % | measured in `## UI/UX` |
| FR-007 | `obs-overlay.js` (`paint` under `translation`) | `test` → `test_obs_overlay.py::test_the_translation_flip_repaints_the_plate_heading` | |
| FR-008 | `obs-overlay.js` (`paint` guard for blank/media/hidden) | `test` → `test_obs_overlay.py::test_hide_empties_the_overlay_and_nothing_is_focusable` | |
| FR-009 | `multimedia/web/templates/reading/obs_overlay.html` + `obs-overlay.js` | `test` → `test_hide_empties_the_overlay_and_nothing_is_focusable` | zero focusable elements |
| FR-010 | `multimedia/web/reading/views.py` (`_screen_lines`) · `obs-overlay.js` (`applySpeakerColumn`) | `test` → `multimedia/web/tests.py::test_a_voiced_line_carries_its_mark_and_words_apart`, `tests/e2e/test_obs_overlay.py::test_a_wrapped_speaker_line_hangs_under_its_words` | mark + words in the payload; one column per screen |
| FR-011 | `obs-overlay.css` (`overlay-plate-in/out`) · `obs-overlay.js` (`animateIn`/`animateOut`) | `test` → `test_obs_overlay.py::test_a_panel_enters_and_leaves_with_a_short_motion` | 180 / 120 ms, names asserted |
| FR-012 | `obs-overlay.css` (`overlay-caption-in/out`) | `test` → `test_obs_overlay.py::test_a_caption_enters_and_leaves_with_the_same_clock` | same clock, shorter travel |
| FR-013 | `obs-overlay.js` (`resizePlate`) · `obs-overlay.css` (`.is-resizing`) | `test` → `test_obs_overlay.py::test_a_second_screen_morphs_the_panel_box` | width/height morph, words resolve at 110 ms |
| SC-001 | `obs-overlay.css` (`.obs-overlay__caption`) | `inspection` — live page at 1920×1080: 1728×202 at (96, 824), 72 px, weight 800, no fill | |
| SC-002 | `obs-overlay.css` (`[data-kind="passage"]`) | `inspection` — live page: 1728×238 at (96, 788), body 36 px / 50.40 px, radius 11.52 px | |
| SC-002a | `obs-overlay.css` (`[data-kind="liturgy"]`) | `inspection` — live page: 1544×201 at (188, 825), bar 3 px, radius 2.88 px | |
| SC-003 | `obs-overlay.js` (`plate` heading) | `test` → `test_a_passage_wears_a_plate_naming_its_reference_and_title` | kicker and title equal the header's lines |
| SC-004 | `obs-overlay.css` (ink alphas `.381` / `.8` / full) | `test` → `test_a_liturgy_text_wears_a_plate_with_its_title_and_quieter_leader_lines` | leader ink darker than assembly |
| SC-005 | `obs-overlay.html` / `obs-overlay.js` | `test` → `test_hide_empties_the_overlay_and_nothing_is_focusable` | no focusable, hide empties, media paints nothing |
| SC-006 | `obs-overlay.js` (`paint`) | `test` → `test_the_translation_flip_repaints_the_plate_heading` | |
| SC-007 | `obs-overlay.css` + `obs-overlay.js` motion | `test` → `test_a_panel_enters_and_leaves_with_a_short_motion`, `::test_a_caption_enters_and_leaves_with_the_same_clock` | animation names and durations |
| US1/AC3 | `obs-overlay.js` (`plate` heading, empty case) | `inspection` — preview state 3 (reference only): no empty title element, no extra rule | |
| US2/AC4 | `obs-overlay.css` (`min-width: 34%`) | `inspection` — preview state 7 (one short answer) keeps the panel's width | |
| US2/AC5 | `obs-overlay.css` (leader ink) | `test` → liturgy test | |
| US3/AC3 | `obs-overlay.js` (`paint`, same-kind branch) | `test` → `test_a_second_screen_morphs_the_panel_box` | no re-entry on a step |
| US3/AC4 | `obs-overlay.css` (`prefers-reduced-motion`) | `inspection` — emulated reduced motion in devtools: the panel paints with no animation | |
| US3/AC5 | `obs-overlay.css` (caption keyframes) | `test` → `test_a_caption_enters_and_leaves_with_the_same_clock` | |
| US1/AC2, US2/AC2 | `obs-overlay.css` (per-kind blocks) | `test` → passage and liturgy tests | the two kinds diverge structurally |

**Verification split**: 20 test · 6 inspection · 0 manual

## Complexity Tracking

No constitution to violate and no structural exception taken.

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/180-overlay-text-styles/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md  fold.md
  contracts/  checklists/  preview/
```

### Source

```
static/styles/design/obs-overlay.css     the caption, the plate, per-kind structure, motion, resize morph
static/web/obs-overlay.js                kind dispatch, heading, speaker column, enter/leave/resize
multimedia/web/reading/views.py          _screen_lines carries mark + words beside the full line
multimedia/web/templates/reading/obs_overlay.html   unchanged stage
tests/e2e/test_obs_overlay.py            10 browser tests
tests/e2e/test_obs_dock.py               one wait adapted to the exit animation
multimedia/web/tests.py                  one payload unit test
```

### Structure Decision

No new module: the overlay is one page with one script and one stylesheet, and the change is entirely inside them. The
only server-side touch is the screen payload in `reading/views.py`, because the speaker column cannot be inferred from
a rendered string without guessing at 133 distinct marks.

## Process note

The preview stage ran against a working tree: the owner iterated on the live surface (type scale, weights, spacing,
ink and motion) before gate 1, so the implementation exists ahead of this plan. The spec, plan and tasks were written
against what was built, and Converge re-assesses every row from the code rather than from a checkbox (SDD-22).
