# Converge: a newly created songbook or song opens as its row would

**Spec**: `specs/225-open-created-songbook-song/spec.md`
**Date**: 2026-11-23 · **Slice**: `225-open-created-songbook-song`

This file is filled in at the end of the slice. Gate 1 evidence (base-commit measurements) is in
`spec.md`; gate 2 evidence is the accepted spec/plan/tasks set.

## Findings

| # | Area | Finding | Disposition | Evidence |
| --- | --- | --- | --- | --- |
| F1 | create navigation | The save only refreshed the lists; no row current, child pane closed, stage empty. | Fixed — `editor:saved` now opens the new songbook with `lists` and the new song with `song`, both `forceServer`. | Base probe: `currentBook=null`, `ch=closed`, `currentSong=null`, `read=off`. After fix: `currentBook=39`, `ch=open`, `/songs/1909/`, `readName="Probe Song 397984"`, `read=on`; marker `alive` throughout. |
| F2 | focus | An early implementation bypassed the quiet focus restore that spec 025 requires after a save. | Fixed — `restoreRequestedFocus` runs in the navigation promise's `.then`, as spec 209 does for a service. | `test_sidebar_save_restores_focus_to_the_matching_kind_row` failed before the fix, OK after. |
| F3 | existing test | `test_the_shell_survives_a_save` asserted the old stage stayed on the previous song; it only passed by timing before the fetch completed. | Fixed by restating the test against the new contract (new song on stage, URL changed in place, no reload). | Test OK after the change. |
| C1 | editor suite | Five errors in `tests.e2e.test_editor` (date-picker cells across month boundary ×2, pointer-closed control, two date-picker load/clear/keyboard tests). | Carried — identical on unmodified develop `e83e7154`; carded on the board (ITEM-174, ITEM-220 etc.). | `base_errors.txt`: 4 tests run, 5 errors on base. |
| C2 | related suites | `test_tatib_sidebar_save_refreshes_row_and_active_stage` error and `test_the_panel_shows_its_empty_view_when_no_songbook_exists` failure. | Carried — both reproduce on unmodified develop. | `base_related.txt`. |
| C3 | related suites | `test_bible_language_highlight_slides_without_reflow` failed once in a 102-test combined run. | Carried as flaky/order-dependent: passes alone on the branch and on base. | `highlight.txt` OK; `related.txt` combined run. |

## Verification

| Check | Result |
| --- | --- |
| Six focused create/edit/refusal tests (`tests.e2e.test_editor`) | 6 run, OK; red on base before the code change (see `red.txt`, `green.txt`). |
| Focus and shell-survival tests | 3 run, OK after the focus fix and test restatement. |
| `tests.e2e.test_editor` module | 42 run; after F2/F3 fixes, only the five base-carried errors remain. |
| `tests.e2e.test_reading` + `tests.e2e.test_sidebar_save_freshness` | 102 run; only the carried/flaky C2/C3 results. |
| Live worktree server (`127.0.0.1:8768`) | `reproduce.py` shows both records opened after save with no reload. |

## Gate

- Gate 1 — measured defect and click-through target, recorded in `spec.md` with base-commit values.
- Gate 2 — accepted spec, plan, research and tasks, 2026-11-23.
