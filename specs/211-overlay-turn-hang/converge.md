# Convergence: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`
**Plan**: `specs/211-overlay-turn-hang/plan.md`
**Tasks**: `specs/211-overlay-turn-hang/tasks.md`

## Phase 1: Convergence

**Checked**: every row of the plan's traceability table against the present code and artifacts;
the two production files read back line by line; the focused E2E module run in full.

**Evidence**: `DJANGO_DEVELOPMENT_MODE=true … manage.py test tests.e2e.test_obs_overlay --noinput`
— 15 tests OK (5 new continuation cases, 10 existing). Red-first evidence is in the gate-2 pack:
before the fix the short case was 29.8 px out and the class was absent.

| Requirement | Method | Result |
| --- | --- | --- |
| FR-001 | test → `test_a_continuation_hangs_at_the_marked_words` | OK — first glyph 0.2 px from the marked words x |
| FR-002 | test → same | OK — indent is column + gap, no mark span on the row |
| FR-003 | test → `test_a_no_mark_screen_keeps_its_continuations_flush` | OK — no class, no column, lines at the content edge |
| FR-004 | test → `test_a_cue_and_an_ordinary_body_stay_flush` | OK — cue and speakerless body unchanged |
| FR-005 | test → `test_a_continuation_hangs_at_the_marked_words` | OK — `is-leader` and its colour preserved |
| FR-006 | test → `test_a_wrapped_continuation_keeps_every_row_at_the_words_column` | OK — every glyph row at the column, ink inside the plate |
| SC-001 | test → short case | OK — within the 1 px budget |
| SC-002 | test → wrap case | OK — row rects and plate content box measured |
| SC-003 | test → no-mark case | OK — glyph x equals the plate's content edge |
| SC-004 | test → the two existing liturgy cases | OK — mark grid, colours and wrap unchanged |
| US1/AC1 | test → short case | OK — the owner's screenshot case |
| US1/AC2 | test → short case | OK — voice class and colour |
| US1/AC3 | test → widest-column case | OK — `L.`, continuation and `J.` share one x |
| US2/AC1 | test → no-mark case | OK — mid-turn screen stays flush |
| US2/AC2 | test → cue case | OK — cue and neighbour stay flush |
| US2/AC3 | test → speakerless body | OK — second screen of the cue fixture stays flush |
| UI/UX | inspection — `preview/index.html` readout and production CSS | checked by inspection — preview still reads −28.8 px / 0.0 px; the production rule uses the same column + gap |
| overlay/R5 | inspection — `docs/spec/overlay.md` R5 | checked by inspection — R5 is the mark-column block; its typed delta is the Fold step that follows this pass |

**Findings**: none. No `missing`, `partial`, `contradicts` or `unrequested` gap; no extra control,
no payload change, no second measurement.

**Outcome**: Converged in one pass. Fold may run.

## Fold confirmation

- 2026-11-21 — T016 folded the `modified` delta into `overlay/R5`; the inspection row above was
  re-read against the resulting block and `fold.md`.
