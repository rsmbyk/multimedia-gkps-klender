# Implementation Plan: Audio and video name their play/pause key

**Spec**: `specs/160-shortcuts-audio-video-groups/spec.md`
**Branch**: `feat/160-shortcuts-audio-video-groups`
**Bump**: `patch` — 1.22.10 → 1.22.11
**Preview**: `static preview at specs/160-shortcuts-audio-video-groups/preview/preview.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | HTML inside a Django template; Python (Django `TestCase`) for the test |
| Primary dependencies | none added |
| Storage | none — the sheet is static markup |
| Testing | `multimedia/web/tests.py::ServiceProjectorTests` (one new case), `multimedia/web/test_media.py` (one assertion updated), and the existing E2E cases that guard Space |
| Target platform | every browser the app supports; the sheet has no script |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none — one row and one heading fewer, two headings more, in a static response |
| Constraints | markup only: no JS, CSS, token, route, payload or template variable; the sheet's box must not grow; Space's behaviour untouched |
| Scale / scope | −1 `<p class="row">`, +2 `<section class="group">` in one template; 1 new test, 1 assertion updated; preview + pack + card |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
constraint row above stands in its place.

Re-checked after Phase 1: pass — the design adds no file to the product, no script and no state.

## Phase 0 — Research

See `research.md`. Six decisions, each measured or read: markup-only (D001), two one-row groups
(D002), the middle column (D003), the label and the chord (D004), a template test rather than a new
browser case (D005), and `projector/R3` as the Fold target (D006). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the sheet's five parts (sheet, column, group, row, chord) with their measured
  boxes and the typed delta Fold will write.
- `contracts/` — `none` (`contracts/none.md`): no interface changes.
- `quickstart.md` — the DB-isolated run, the new case, the module, the measurement script, and the
  post-merge check.

### The design

`multimedia/web/templates/reading/projector_controls.html` — two edits.

1. The `Display` group loses its second row, and keeps its other three verbatim:

```html
      <section class="group">
        <h3>Display</h3>
        <p class="row"><span class="fn">Show or Hide Words</span>…</p>
        <p class="row"><span class="fn">Show or Hide Corner</span>…</p>
        <p class="row"><span class="fn">Keyboard Shortcuts</span>…</p>
      </section>
```

2. The second `.stack` gains, after the `Library Detour` group, two groups whose row is the Space
   chord the removed row carried:

```html
      <section class="group">
        <h3>Audio</h3>
        <p class="row"><span class="fn">Play/Pause</span><span class="combo"><span class="chord"><span class="k sp glyph" title="Space" aria-label="Space"><span class="space-mark">␣</span></span></span></span></p>
      </section>
      <section class="group">
        <h3>Video</h3>
        … the same row …
      </section>
```

`multimedia/web/tests.py` — one case in `ServiceProjectorTests`, reading the rendered sheet:

```python
def test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own(self):
    sheet = self.html().split('<div class="sheet" id="key-list">', 1)[1].split('\n  </div>', 1)[0]
    groups = [(heading, rows) for heading, body in re.findall(r'<h3>([^<]+)</h3>(.*?)</section>', sheet, re.S)
              for rows in [[re.sub(r'<[^>]+>', '', fn) for fn in re.findall(r'class="fn">(.*?)</span>', body, re.S)]]]
    …
```

The assertions: the headings in document order; `Audio` and `Video` each hold `['Play/Pause']` and
carry `class="k sp glyph"` with `aria-label="Space"`; `Display` holds its three rows; the string
`Audio/Video Play/Pause` is absent; the two groups sit in the second column (between `Library Detour`
and `Display`).

`multimedia/web/test_media.py:278` — the video contract's incidental assertion moves from
`'Audio/Video Play/Pause'` to the two headings it now reads.

**What is deliberately not done.** No E2E case (D005), no CSS or token, no change to
`static/web/projector.js` (D001), no re-ordering of the sheet's existing nine groups, and no
qualifier on the label (D004).

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 `Audio` group with its `Play/Pause` row | `projector_controls.html` (sheet, column 2) | `test` → `multimedia/web/tests.py::ServiceProjectorTests::test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own` | heading, label, Space cap |
| FR-002 `Video` group with the same row | same | `test` → the same case | |
| FR-003 `Display` holds three rows; the combined row is gone | same | `test` → the same case | `Audio/Video Play/Pause` absent from the sheet |
| FR-004 both groups in the middle column, after `Library Detour` | same | `test` → the same case | the case reads the sheet's document order |
| FR-005 the sheet's box and every other metric unchanged | the diff; `preview/measure.py` | `inspection` — the diff is one removed row and two added groups; `manual` — run the script, read 676.1px before and after at both window sizes | SC-002, SC-003 |
| FR-006 Space still toggles audio, video and words, and the open sheet still swallows it | `static/web/projector.js:1254-1260` (untouched) | `test` → `tests/e2e/test_audio_display.py::…::test_projector_space_navigation_and_reset`, `tests/e2e/test_video_display.py::…::test_projector_fullscreen_play_pause_and_navigation_guard`, `tests/e2e/test_projector.py::…::test_the_keyboard_moves_and_turns_the_display_on_and_off` — **deferred to the push step**; `inspection` — the handler is not in the diff | |
| US1 AC1 the two headings and their rows | the template | `test` → the new case | |
| US1 AC2 `Display`'s three rows, no combined row | the template | `test` → the new case | |
| US1 AC3 a 1280×720 window still fits | the sheet's CSS + markup | `manual` → `preview/measure.py`: 676.1px against a 688px limit, `scrollHeight` 675 | |
| US1 AC4 a 1920×1080 window: 676.1 × 1094.4px, 34px pitch | the sheet's CSS + markup | `manual` → `preview/measure.py` | |
| US2 AC1 audio toggles, words do not | `projector.js` (untouched) | `test` → `test_audio_display.py::…::test_projector_space_navigation_and_reset` (push step) | |
| US2 AC2 video toggles, words do not | `projector.js` (untouched) | `test` → `test_video_display.py::…::test_projector_fullscreen_play_pause_and_navigation_guard` (push step) | |
| US2 AC3 words toggle when no media shows | `projector.js` (untouched) | `test` → `test_projector.py::…::test_the_keyboard_moves_and_turns_the_display_on_and_off` (push step) | |
| US2 AC4 the open sheet swallows Space; K/Escape close it | `projector.js` (untouched) | `test` → `test_projector.py::…::test_f_and_k_toggle_fullscreen_and_shortcut_sheet` (push step) | |
| Edge: a window shorter than the sheet scrolls it | `projector.css:461-466` | `inspection` — `max-height: calc(100vh - 32px); overflow: auto` is untouched | |
| Edge: the middle column keeps its width | `projector.css` `.stack` | `manual` → `preview/measure.py`: the column stays 379px wide and the sheet 1094.4px | |
| Edge: no hover state is added | the diff | `inspection` — no CSS in the diff; `.row` has no hover rule today | |
| Edge: reduced motion unchanged | `projector.css:501-505` | `inspection` — the media query is untouched | |
| Edge: eleven headings | the template | `test` → the new case counts them | |
| SC-001 the groups, the rows and the absent combined row | the rendered sheet | `test` → the new case | |
| SC-002 no taller than today | `preview/measure.py` | `manual` — 676.1px before and after at 1920×1080 and 1280×720; the running page reads 676.5px in both states | |
| SC-003 nothing else moves | `preview/measure.py` | `manual` — pitch 34px, heading 21.5px, group gap 24px, column gap 32px, padding 20px 24px; column 2 380 → 539.3px | |
| SC-004 the keys unchanged | `projector.js` (untouched) + the E2E cases | `inspection` — the handler is not in the diff; `test` → the four E2E cases, push step | |

**Verification split: 14 test · 6 inspection · 6 manual** across 23 rows — three rows carry a second
method, because both read the same sheet (`FR-005`, `FR-006`, `SC-004`).

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-006 each carry a row; every SC and every story scenario is mapped |
| Entity coverage | sheet, column, group, row, chord and the typed delta are in `data-model.md` |
| Interface coverage | `contracts/none.md` states `none` and why |
| Decision provenance | D001–D006 in `research.md`, each with its code read or measurement |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 14 `test` · 6 `inspection` · 6 `manual` across 23 rows; no row is un-tested *and* unverifiable |
| `quickstart.md` runnable | yes — the module, the new case and `preview/measure.py` all run on this worktree; the two live checks are the `manual` rows |

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/160-shortcuts-audio-video-groups/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md  fold.md
  contracts/none.md  checklists/requirements.md
  preview/preview.html  preview/build_preview.py  preview/measure.py
```

### Source

```
multimedia/web/templates/reading/projector_controls.html   one row removed, two groups added
multimedia/web/tests.py                                    one new case in ServiceProjectorTests
multimedia/web/test_media.py                               one assertion updated (:278)
docs/spec/projector.md                                     R3 at Fold
backlog/items/ITEM-166-shortcuts-audio-video-groups.md     card
backlog/board.md                                           the card's row
specs/README.md                                            the spec's index row, at Accept
VERSION, CHANGELOG.md                                      patch bump and one line, at delivery
```

### Structure Decision

No new module, file or class in the product: the sheet is one template's markup, and the test joins
the class that already owns the projector page's contracts.
