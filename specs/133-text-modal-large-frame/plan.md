# Implementation Plan: A text entry is written and edited in the media modal's large frame

**Spec**: `specs/133-text-modal-large-frame/spec.md`
**Branch**: `feat/133-text-modal-large-frame`
**Bump**: `patch`
**Preview**: `specs/133-text-modal-large-frame/preview/` — the running worktree on `:8768`, with
`probe_modal_frame.py` measuring both create dialogs, the edit form, three viewports, both themes, the
switch and the Save guard

*Sequencing note*: the owner reviewed the change on a running branch while the design was settled (the
box, the Chrome parity, the Text box filling the frame, and the scroll-placement fault found while
measuring it), so the working tree already carries the implementation at the moment this plan is written.
Gate 1 accepted the spec afterwards, with the branch updated onto `develop` `ffa5c340` first; the
geometry was re-measured on that base. The tests named in the Traceability table are written after gate
2, against the accepted numbers.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 templates; hand-written CSS, no build step; browser JavaScript untouched |
| Primary dependencies | Django template engine; `static/styles/design/components.css`, `tokens.css`; no new library |
| Storage | none — the frame is presentational; nothing is stored per entry |
| Testing | Django `TestCase` for the rendered form fragment per kind; Playwright (Python) E2E for the measured box, the filling Text box, the narrow-window gutters and the scrolled placement |
| Target platform | the reading shell at any width, light and dark themes; the dialog is a native `<dialog>` in the top layer |
| Project type | server-rendered pages with in-page fragment swaps; the editor body is fetched per kind |
| Performance goals | none affected: one extra attribute per form and one selector change; no new request, no new query |
| Constraints | the media create dialog must keep its exact geometry (it is the reference); every other form must keep its own; the hook must be server-rendered so a 400 re-render keeps it; `:has()` is already the project's mechanism for form-dependent dialog styling |
| Scale / scope | 1 CSS file (6 selectors replaced, 3 added, 1 media query updated, 1 declaration changed), 1 template (2 attributes), 1 unit test module, 1 E2E module, the preview probe + README |

## Constitution Check

`n/a — no CONSTITUTION.md in this repository` (SDD-01: optional, never auto-created).

Re-checked after Phase 1: nothing to check against; the repo's `docs/PROCESS.md` rules were applied
instead (one slice, one branch, no commit before Fold, tests named before the claim). The design-token
guard in `tests/test_design_tokens.py` is untouched: no colour, space or type token was added, and the
frame reuses the tokens the media dialog already uses.

## Phase 0 — Research

See `research.md` — six decisions, **unknowns remaining: 0**.

## Phase 1 — Design

- `data-model.md` — `n/a`, written out: the frame has no entity; the file records what the DOM carries
  instead (the two attributes) and why a model would be a fiction here.
- `contracts/` — `none`: the slice exposes no interface; it changes how one server-rendered fragment is
  drawn. Recorded with its reason.
- `quickstart.md` — how to serve the worktree on `:8768`, click through the states, run the probe and the
  two test modules.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/templates/reading/_entry_form.html` (`data-editor-size`) + `components.css` `.editor:has([data-editor-size="large"])` | `test` → `multimedia/web/tests.py::ServiceEntryViewTests::test_the_large_frame_is_marked_for_both_text_forms`; `tests/e2e/test_entry_modal_frame.py::test_new_text_dialog_matches_new_media` | 840×760 at (300,70) at 1440×900 |
| FR-002 | `components.css` lines 517–529 | `inspection` — the probe's `titleStyle.padding`, `titleStyle.font-size`, `fields[].margin`, `fields[].box.x`, `actionsStyle.margin` must be equal for `+ Text` and `+ Media` | 72.5 band, 788 at x=326, `14px 26px 20px` |
| FR-003 | `components.css` `[data-editor-grow]` rules + `_entry_form.html` text field | `test` → `tests/e2e/test_entry_modal_frame.py::test_text_box_fills_the_frame` | 419 create / 507 edit |
| FR-004 | `_entry_form.html` marker condition | `test` → `multimedia/web/tests.py::ServiceEntryViewTests::test_the_large_frame_is_not_marked_for_the_other_forms` | passage/song/media-edit carry no marker |
| FR-005 | `components.css` line 655 (`@media (max-width: 650px)`) | `test` → `tests/e2e/test_entry_modal_frame.py::test_narrow_window_uses_the_small_gutters` | 352×760, gutters 18, band 64.5 |
| FR-006 | `static/web/entries.js` — unchanged | `test` → the existing `tests/e2e/test_unified_text_screen_mode.py` re-run unchanged | switch, help line, hidden input |
| FR-007 | `components.css` `.editor { position: fixed }` | `test` → `tests/e2e/test_entry_modal_frame.py::test_dialog_is_centred_on_a_scrolled_page`; `inspection` for the date popover | y=70 at scrollY 556; popover 504.3 under a 496.25 trigger |
| US1/AC1 | both dialogs | `test` → `::test_new_text_dialog_matches_new_media` | box equality |
| US1/AC3 | `[data-editor-grow]` | `test` → `::test_text_box_fills_the_frame` | 419 |
| US1/AC4 | `entries.js` `wireTextSave` | `test` → the existing `tests/e2e/test_entries.py::test_text_save_requires_content_and_does_not_resize` | unchanged |
| US1/AC5 | `entries.js` `wireScreenMode` | `test` → the existing `tests/e2e/test_unified_text_screen_mode.py::test_create_edit_switch_custom_confirmation_and_live_projector` | unchanged |
| US2/AC1 | `_entry_form.html` marker for `kind == 'text'` | `test` → `::test_the_large_frame_is_marked_for_both_text_forms` (edit path) + the probe | 840×760, `Edit text` |
| US2/AC2 | `[data-editor-grow]` on the edit form | `test` → `::test_text_box_fills_the_frame` | 507 |
| US2/AC3 | marker condition | `test` → `multimedia/web/tests.py::ServiceEntryViewTests::test_the_large_frame_is_not_marked_for_the_other_forms` | 480 wide, 22px padding |
| US3/AC1 | `.editor { position: fixed }` | `test` → `::test_dialog_is_centred_on_a_scrolled_page` | |
| US3/AC2 | `.editor { position: fixed }` + `.editor__date-picker` | `inspection` — open a service's form on `/tatib/` and click the date field: the calendar opens under the trigger and inside the window | measured 504.3 / 496.25 |
| US3/AC3 | `.editor { position: fixed }` | `inspection` — `+ Passage` on a 400px-scrolled stage is centred (238.6 for a 422.8 form) | |
| SC-001 | both dialogs | `test` → `::test_new_text_dialog_matches_new_media` | six values equal |
| SC-002 | probe | `inspection` — the probe's 1440×900, 1280×800, 1280×600 and 390×844 rows: top ≥ 0, bottom ≤ window, no document scroll | |
| SC-003 | `.editor { position: fixed }` | `test` → `::test_dialog_is_centred_on_a_scrolled_page` | |
| SC-004 | probe | `inspection` — passage 480×422.8 with the page scrolled; media create still 840×760 at (300,70) | |

**Verification split**: 14 test · 5 inspection · 0 manual

## Complexity Tracking

`none — no constitution, no violation to justify.`

## Project Structure

### Documentation

```
specs/133-text-modal-large-frame/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  checklists/checklist.md
  contracts/README.md
  preview/README.md  preview/probe_modal_frame.py
```

### Source

```
multimedia/web/templates/reading/_entry_form.html     + data-editor-size on the text and media-create
                                                      forms; + data-editor-grow on the Text field
static/styles/design/components.css                   the large frame keyed on data-editor-size (was the
                                                      media hook); the grow rules; .editor position: fixed
multimedia/web/tests.py                             + two tests in ServiceEntryViewTests: the marker is
                                                      on both text forms, and not on the others
tests/e2e/test_entry_modal_frame.py                   new — box parity, Text box fill, narrow gutters,
                                                      scrolled placement
backlog/items/ITEM-138-text-modal-large-frame.md      new — the card
backlog/board.md                                      one row
docs/spec/reading.md                                  R10 folded at Fold
VERSION · CHANGELOG.md                                1.20.11 → 1.20.12
```

### Structure Decision

The frame is a property of the dialog, not of a kind's fields, so it belongs in `components.css` beside
the rules it generalises, keyed on an attribute the server writes — the same mechanism the media dialog
already used (`:has([data-media-create])`), renamed to say what it means. The growing field is marked on
the template's own field element rather than matched with `:has(> textarea)`, because the field is what
carries the label as well as the box, and an explicit hook survives the markup changing around it. The
unit test lives beside the app (`multimedia/web/`) like the rest of the app's tests; the E2E test lives in
`tests/e2e/` with the other browser acceptance modules.
