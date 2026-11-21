# Tasks 213: a slot states the kind it resolves to

**Spec**: `spec.md` · **Plan**: `plan.md` · **Bump**: `patch`
**Status**: Awaiting gate 2

> **Ordering note, stated rather than hidden.** T002–T005 landed during **Preview**, not at Implement:
> SDD-06's live tier requires the change to be in the project so a click hits the real code path, and
> the owner reviews on a running server. The red-first proof below is therefore taken against the
> **pre-change tree** (the badge's markup removed, everything else untouched), which is what TDD-01
> asks the test to fail on — not against a tree that never had the feature. Everything from T006 on is
> **not done**; the boxes are unticked because the work is not there.

## Phase 1 — Setup

- [X] T001 [P] Confirm the baseline before touching anything: `tests.e2e.test_tatib_templates` (32
  tests) and `tests.e2e.test_stage_kind_marks` (11) on the slice's base commit (`origin/develop` at
  `ff0cc96c`), so a later failure is this slice's

## Phase 2 — Foundational

- [X] T002 The badge's partial, `multimedia/web/templates/reading/_slot_kind_badge.html`: a
  `.slot__badge` span carrying `data-kind-badge`, one `<svg>` on a 12-unit viewBox per kind, the paint
  declared as attributes (D003, D006) — *landed at Preview*
- [X] T003 `_slot_mark.html`: include the badge after the frame, guarded by `{% if fill_kind %}`
  (D001, FR-007) — *landed at Preview*
- [X] T004 `tatib.html`: pass `fill_kind=item.slot_kind` to the mark's include (D001) — *landed at Preview*
- [X] T005 `static/styles/design/generate.css`: the badge's box and disc, the four fill states'
  `background-image`, the 10px glyph — and `.slot__mark svg` → `.slot__mark > svg` so the frame's rule
  cannot stretch the badge's glyph (D004, D005) — *landed at Preview*

## Phase 3 — US1: a slot's mark names the kind it resolves to (P1)

- [X] T006 [US1] Write `tests/e2e/test_tatib_templates.py::test_a_slot_row_carries_the_kind_it_resolves_to`,
  red first: a template with five slots (song, passage, media, text, and a choice with no options).
  Its first assertion is that each slot row's mark carries a badge — run it against the pre-change
  tree (T002–T005 reverted) and record the failure as **an absent `.slot__badge`**, not a fixture or
  import error
- [X] T007 [US1] Make T006 pass: the five badges carry the five `data-kind-badge` values in page order,
  the four glyphs' path data are pairwise different, the choice with no options is badged while its
  row still reads `No options yet`, and a dated service's page carries none

## Phase 4 — US2: the kind mark's own language, at a slot's scale (P1)

- [X] T008 [US2] Assert in T006 that the mark keeps its own identity: the frame's `stroke-dasharray`
  is `2.8 2.4` and the row's own `+`/`◎` path is unchanged (FR-003, SC-003)
- [X] T009 [US2] Assert in T006 that the badge's `<svg>` computes `fill: none` and a stroke equal to
  the badge's `--head-ink` — the defect D006 records, guarded so it cannot return
- [X] T010 [US2] Assert in T006 that the disc repaints the row's own tint in each fill state: for
  `:hover`, `.is-modal-origin` and keyboard focus, the badge's `background-image` is not `none`
- [X] T011 [US2] `preview/probe_glyphs.py`: print each glyph's 13px pixel map and the pairwise
  normalised difference; the closest pair must clear 0.10 (measured 0.141) — the check that the four
  are told apart, which a path-data comparison alone cannot prove

## Phase 5 — US3: the page's rhythm and text column are untouched (P2)

- [X] T012 [US3] Assert in T006 that nothing moves: every slot row's `y` and `height`, every title's
  `x`, and the page's scroll height are identical with the badge drawn and with it suppressed by an
  injected `display: none` (FR-005, SC-004)
- [X] T013 [US3] Assert in T006 that the badge adds no motion: its computed `transition-property` is
  `none`

## Phase 6 — Polish

- [X] T014 [P] `multimedia/web/tests.py::test_a_slot_with_no_kind_draws_no_badge`: a slot stored with
  `fill_kind=None` renders the mark and no badge — the local data cannot produce such a row (FR-007)
- [X] T015 [P] Assert the accessible name is unchanged: the row's name with the badge and with it
  suppressed are byte-identical (FR-004, SC-005)
- [X] T016 `preview/README.md` and `preview/compare.html`: mark B as adopted, keep A and C visible as
  the alternatives, and record that A was built first and rejected on legibility
- [X] T017 Run the full verification: T006 plus `test_stage_kind_marks`, `test_tatib_preview_parity`,
  `test_entries`, `multimedia.web.tests`, and `probe_adopted.py` + `probe_glyphs.py`; record the
  numbers in `converge.md`
- [ ] T018 Delivery: `VERSION` 1.35.4 → 1.35.5 and one `CHANGELOG.md` line under `## [Unreleased]` →
  `### Added` and `docs/spec/reading.md` R35 folded are **in this slice's first commit**; the card to
  `in-review` with its `pr:` and the board row moved wait for the push to return a PR number, and the
  push waits for the owner's word
