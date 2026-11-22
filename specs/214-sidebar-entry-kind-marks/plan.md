# Implementation Plan: a contents row marks its entry's kind

**Spec**: `specs/214-sidebar-entry-kind-marks/spec.md`
**Branch**: `feat/214-sidebar-entry-kind-marks`
**Bump**: `patch` — one new visual affordance on an existing surface, matching specs 144/206/213
**Preview**: `specs/214-sidebar-entry-kind-marks/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 (Django 4.0), HTML templates, CSS, vanilla JS |
| Primary dependencies | Django, DRF, PostgreSQL, WhiteNoise; no new package |
| Storage | none — no field, migration or fixture changes |
| Testing | Django `TestCase` for rendered markup; Playwright (Python) E2E through `StaticLiveServerTestCase` |
| Target platform | desktop and drawer/phone reading shell, light and dark themes |
| Project type | existing Django app; server-rendered templates with in-place DOM reconciliation |
| Performance goals | no extra query; no script injected; mark adds no row height or scroll height |
| Constraints | spec 063 number centring, spec 135 three-line clamp, spec 137 wrapping, spec 144 stage classes, spec 213 slot badge |
| Scale / scope | one partial, one view function's `toc` payload, one CSS block, one Django test module, one E2E module |

## Constitution Check

`CONSTITUTION.md` does not exist and is never auto-created (SDD-01). No principles to check.

Re-checked after Phase 1: **n/a — no constitution exists**.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** The owner's two questions (layout B, slot modifier) and
the skipped break-row question are closed; no research question needed an owner decision.

## Phase 1 — Design

- `data-model.md` — n/a — no stored state; documents the two new `toc` payload keys.
- `contracts/toc-markup.md` — the markup seam and the untouched contracts.
- `quickstart.md` — links both, with runnable commands.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_passage_and_song_rows_carry_their_marks` | distinct `data-mark` |
| US1/AC2 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_text_and_media_rows_carry_their_marks` | legacy row included |
| US1/AC3 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_slot_rows_keep_the_kind_modifier` | disc glyph pair |
| US1/AC4 | `multimedia/web/tests.py` | `test` → `ServiceEntryViewTests::test_mark_set_is_pairwise_distinct` | all kinds in one service |
| US2/AC1 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_row_accessible_name_is_unchanged` | byte-identical name |
| US2/AC2 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_mark_takes_no_pointer` | hover fill unchanged |
| US2/AC3 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_focus_never_lands_on_the_mark` | link and grip only |
| US3/AC1 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_number_centre_and_row_heights_hold` | 24px box, 10px left edge |
| US3/AC2 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_three_line_clamp_and_pane_wrap_hold` | 404px and 280px |
| US3/AC3 | `multimedia/web/tests.py` | `test` → `ServiceEntryViewTests::test_deleted_target_keeps_its_mark` | kind, not availability |
| US3/AC4 | `static/styles/design/components.css` | `inspection` — no animation, keyframes or transition on `.songrow__mark` or `.slot__badge` | reduced motion |
| FR-001 | `reading/_toc.html`, `reading/_toc_mark.html` | `test` → `ServiceEntryViewTests::test_every_numbered_row_has_one_mark` | second child of the link |
| FR-002 | `reading/_toc_mark.html` | `test` → `ServiceEntryViewTests::test_mark_set_covers_every_kind` | slot badge included |
| FR-003 | `reading/views.py::_tatib_stage` | `test` → `ServiceEntryViewTests::test_marks_survive_in_place_rebuild` | no new field/migration |
| FR-004 | `reading/_toc_mark.html` | `test` → `test_row_accessible_name_is_unchanged` | `aria-hidden`, no control |
| FR-005 | `static/styles/design/components.css` | `test` → `test_number_centre_and_row_heights_hold` | 24px box grows past 999 |
| FR-006 | `reading/views.py::_tatib_stage` | `test` → `test_deleted_target_keeps_its_mark` | legacy rows too |
| FR-007 | `static/styles/design/components.css` | `test` → `test_contrast_in_both_themes` | 5.57 / 6.59 |
| FR-008 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_dock_and_projector_keep_their_own_rows` | existing stage suite stays green |
| SC-001 | `multimedia/web/tests.py` | `test` → `test_every_numbered_row_has_one_mark` | one mark per row |
| SC-002 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_column_sits_between_number_and_label` | geometric order |
| SC-003 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_number_centre_and_row_heights_hold` | baseline comparison |
| SC-004 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_three_line_clamp_and_pane_wrap_hold` | no horizontal scroll |
| SC-005 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_row_accessible_name_is_unchanged` | reachability |
| SC-006 | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_contrast_in_both_themes` | token figures |
| Edge — break row | `multimedia/web/tests.py` | `test` → `ServiceEntryViewTests::test_divider_row_has_no_mark` | both break shapes |
| Edge — legacy EOS | `multimedia/web/tests.py` | `test` → `test_divider_row_has_no_mark` | no `.songrow__c` either |
| Edge — unreadable slot kind | `multimedia/web/tests.py` | `test` → `ServiceEntryViewTests::test_slot_with_no_kind_draws_no_badge` | frame without disc |
| Edge — drawer / phone | `tests/e2e/test_sidebar_kind_marks.py` | `test` → `test_mark_column_at_drawer_and_phone_widths` | fixed 16px column |
| Edge — in-place rebuild | `multimedia/web/tests.py` | `test` → `test_marks_survive_in_place_rebuild` | server-rendered |

**Verification split**: 29 test · 1 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/214-sidebar-entry-kind-marks/
  spec.md  plan.md  research.md  data-model.md  quickstart.md
  contracts/toc-markup.md  checklists/requirements.md  preview/
```

### Source

```
multimedia/web/templates/reading/_toc.html          # include the new partial after the number
multimedia/web/templates/reading/_toc_mark.html     # new: the mark and slot modifier
multimedia/web/reading/views.py                     # two new keys on toc rows
static/styles/design/components.css                 # .songrow__mark and B's number/gap rules
multimedia/web/tests.py                             # rendered-markup tests
tests/e2e/test_sidebar_kind_marks.py                # new: geometry, states, surfaces
```

### Structure Decision

The mark belongs beside `_toc.html`'s number, so its partial sits in the same `reading/templates`
folder as `_toc.html` and the two existing mark partials. All new CSS is scoped to `#chList` and
`.songrow__mark`, leaving the stage's mark rules (`components.css:2081+`) and spec 213's slot badge
rules untouched; the sidebar reuses the badge partial but resizes it with a scoped rule.
