# Fold: A song with no verses is named, not mistaken for no song

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-29

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R30` | A song entry names a song that has no verses: the Verses field reads `This song has no verses` instead of `Pick a song first`, the line is in the server's fragment, the trigger stays disabled, and a save refusal caused by the song reads `This song has no verses: pick another song.` while a cleared checklist keeps `Keep at least one verse in the service.` |

**Before / after counts**: 29 requirements before, 30 after — 0 modified, 0 removed, 0 renamed.

## Drift guard

- **Files changed in this capability**: `multimedia/tatib/models.py`,
  `multimedia/web/reading/entries.py`, `multimedia/web/templates/reading/_entry_form.html`,
  `static/web/entries.js`, `multimedia/tatib/tests.py`, `multimedia/web/tests.py`,
  `tests/e2e/test_entries.py`
- **Declared no behaviour change**: no — the delta above is the behaviour change; the other four
  summary lines are unchanged by FR-005 and stay described where they already were.
