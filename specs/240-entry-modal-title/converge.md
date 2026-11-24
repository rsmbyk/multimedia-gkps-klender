# Convergence: entry modal title band

**Spec**: `specs/240-entry-modal-title/spec.md`
**Plan**: `specs/240-entry-modal-title/plan.md`
**Date**: 2026-11-24
**State**: Converged on pass 1; 0 gaps

## Pass 1: Convergence

Every row is checked by the method its traceability entry declared.

| Requirement | Declared method | Evidence | Result |
| --- | --- | --- | --- |
| US1/AC1 | `test` → `test_large_entry_titles_have_the_band` | 3 cases (New text, New media, Edit text): text 26/21px, band 72.5px, border 1px, frame 840×760 | met |
| US1/AC2 | `inspection` — frame, field y, action row, probe | frame 840×760; New text first field y 133.5 → 174.5px; field width 788px and action row unchanged in existing module | met |
| US2/AC1 | `test` → `test_new_verse_header_has_one_rule` | head `20px 26px 14px`, title padding/border `0px`, zero ruled descendants | met (green baseline on base and fix) |
| US2/AC2 | `inspection` — compact frames | passage, song, media Edit and old-item dialogs keep the 480px compact frame and divided title; no selector matches them | met |
| US3/AC1 | `test` → `test_narrow_title_keeps_small_gutters` | 390×844: text 18/17px, band 64.5px, padding `16px 18px`, border 1px | met |
| US3/AC2 | `inspection` — probe readouts | `probe.py` prints before/after at 1440 and 390px in dark theme, frame 352×760, no page scrollbar | met |
| FR-001 | `test` → `test_large_entry_titles_have_the_band` | all three large forms restored | met |
| FR-002 | `test` → `test_narrow_title_keeps_small_gutters` | narrow `16px 18px` with divider | met |
| FR-003 | `test` → two verse header cases | spec 226 reset intact | met |
| FR-004 | `inspection` — one CSS diff; existing frame module | no template, script, loading-state or sr-only change; `test_entry_modal_frame` green | met |
| SC-001 | `test` → title band module | 26/21px, 72.5px, 1px | met |
| SC-002 | `test` → verse header module + compact inspection | zero ruled descendants; compact dialogs unchanged | met |
| SC-003 | `test` → title band module | 18/17px, 64.5px | met |
| SC-004 | `test` → three modules + `inspection` probe | 11/11 targeted tests green; full suite deferred to push | met |

## Evidence summary

- Red on the gate-1 CSS edit temporarily removed: 4 assertion failures, no timeouts —
  text x `0` vs `26` in the three large dialogs, narrow border `0px` vs `1px`.
- Green with the edit restored: `tests.e2e.test_entry_modal_title` 2/2.
- Guards: `tests.e2e.test_entry_modal_frame` (5), `tests.e2e.test_verse_modal_header`
  (4) and the new module (2) — 11 tests, all green in one run.
- Live probe on the slice server reproduces the gate-1 readouts; the served worktree
  carries the fix and only the probe's local override reads the broken state.

## Gaps

None. `missing`: 0 · `partial`: 0 · `contradicts`: 0 · `unrequested`: 0.

T013's ID recheck and the delivery records (VERSION, changelog, card and board) are
bookkeeping steps at Fold, not code gaps; they are recorded in `fold.md`.
