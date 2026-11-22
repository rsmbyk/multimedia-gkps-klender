# Convergence: the song entry's pickers

**Date**: 2026-11-21
**Spec**: `specs/210-song-verse-picker/spec.md` · **Plan**: `plan.md`

## Phase 1: Convergence

Every one of the plan's 44 traceability rows was checked by the method it declared.

| Kind | Rows | Evidence |
| --- | --- | --- |
| `test` | 40 | `tests/e2e/test_song_entry_pickers.py` 6/6 green; `tests/e2e/test_entries.py` song tests green after updating them to the shipped markup; form modules 363/366 with the three develop-level failures reproduced on unmodified `develop`. |
| `inspection` | 4 | `entry_song_options` and `SongEntryForm` are unchanged by diff; the verse menu selector and trigger rule are gone from the rendered fragment. |
| `manual` | 0 | None declared. |

### Findings

| ID | Type | Finding | Outcome |
| --- | --- | --- | --- |
| C1 | `missing` | None | — |
| C2 | `partial` | None | — |
| C3 | `contradicts` | None | — |
| C4 | `unrequested` | None | — |

### Applied mechanically

- The plan's 19 abbreviated `…::` test paths were expanded to
  `tests/e2e/test_song_entry_pickers.py::…`; no requirement changed.
- Two E2E assertions were corrected to the accepted contract: the summary collapses consecutive
  numbers (`Verses 1–2`), and saved verses are IDs, not display numbers.
- The throwaway database runner derives its password from the compose container at run time and
  writes no credential value to the worktree.

### Accepted outside this slice

- `tests.e2e.test_entries` has three failures reproduced on unmodified `develop` (hover
  opacity, empty-service tiles and empty-service invite); they are not attributed here.
- `multimedia.web.tests` / `multimedia.tatib.tests` have three failures reproduced on
  unmodified `develop` (shortcuts sheet, legacy route payload, image projection).

**Outcome**: Converged in one pass — the code matches the accepted pack.
