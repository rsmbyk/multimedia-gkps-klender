# Convergence: A song opened from the sidebar can edit its verses

**Date**: 2026-11-23
**Pass**: 1
**Spec**: `specs/230-song-verse-script-boot/spec.md`

## What was checked

Every row of Plan's traceability table was checked by the method it declared, against the present
tree. The 16 `test` rows resolve to four new E2E cases plus the neighbouring modules; the 5
`inspection` rows were read from the diff and the probe output.

| Requirement | Typed finding | Evidence |
| --- | --- | --- |
| US1/AC1 · FR-003 · SC-001 | covered | `tests.e2e.test_song_verse_script_boot::test_add_verse_opens_from_sidebar` green; probe `add_dialog_open=True`. Red on unmodified templates. |
| US1/AC2 · FR-004 · SC-002 | covered | `test_edit_verse_opens_from_sidebar` green; probe title `Edit verse 1`. Red on unmodified templates. |
| US1/AC3 · FR-005 · SC-004 | covered | `test_direct_load_still_opens_both_dialogs` green; probe direct load opens. |
| US1/AC4 · FR-001 · SC-003 | covered | `test_script_boots_at_shell_load` green: `(1, 1, 1)`; probe home 1 tag, resource fetched before the swap. |
| US1/AC5 · FR-006 · SC-005 | covered by inspection | `git diff` changes only the two template lines; button box 111.765625×38 at x=900, y=681.34375 in both trees. |
| US2/AC1 · US2/AC2 · FR-002 | covered | one script node, `inFragment: false` on direct load; zero script tags in `song.html`. |
| US2/AC3 | covered | one `/editor/verse/new/?song=` request and one dialog per click. |
| FR-007 | covered by inspection | `reading/R55` appended to `docs/spec/reading.md` by Fold. |
| SC-006 | covered | `page_errors=[]` in both probe trees and in the E2E cases. |

## Findings

None. Zero `missing`, `partial`, `contradicts` or `unrequested` rows.

## Verification evidence

- Red run (unmodified templates): 4 failures — dialogs closed, script in fragment, counts `(0, 0, 1)`.
- Green run (slice templates): 4 passed.
- Targeted suite: 12 tests (`test_song_verse_script_boot`, `test_verse_modal_header`,
  `test_verse_add_gate`) — all passed, with a throwaway `test_gkps230` database.
- Live probe: behaviour and geometry as recorded in the spec's `## UI/UX`.

## Outcome

**Converged** on pass 1. Fold may run.
