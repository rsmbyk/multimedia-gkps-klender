# Convergence: Keep Add song when the songbooks sidebar is closed

**Spec**: `specs/222-add-song-parent-closed/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-22

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| none | — | FR-001–FR-004, SC-001–SC-005, US1 AC1–AC5 | E2E `test_add_song_stays_when_the_songbooks_sidebar_is_closed` failed red on `('none', 0) != ('flex', 38)` before the CSS change and passed green after it; it covers the real collapse control, the mini state, the editor dialog, both sidebars' add controls and 1440/1000/390px widths. |
| none | — | FR-005, US1 AC6 | `git diff --stat` shows only `static/styles/design/components.css` and `tests/e2e/test_editor.py`; no editor, template or hymn-book path changed. |
| none | — | preview parity | Static preview measured `#songAdd flex 38px` / `#panelAdd none` with the proposed rule and `#songAdd none 0px` with the shipped selector; the product E2E measures the same 38px box after the fix. |

**Outcome**: Converged — nothing remains; no tasks appended.

## Verification note

`manage.py test tests.e2e.test_editor` ran 37 tests: 32 pass and 5 errors. Four date-picker errors match
the month-boundary card already on the board (ITEM-144); the fifth (`.editor__cancel` strict-mode
violation) was reproduced on unmodified `develop` with a separate throwaway database. None touches
this slice's paths.

## Accepted gaps

None.

## Cap reached

Not reached.
