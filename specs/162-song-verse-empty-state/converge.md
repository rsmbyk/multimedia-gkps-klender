# Convergence: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`
**Passes**: 2 of 3

## Pass 1 — 2026-10-29

Every row of `plan.md`'s traceability table was checked by the method it declared.

| Row | Method | Result |
| --- | --- | --- |
| FR-001, SC-001, US1/AC1 | `test` → `EntryModalE2ETests.test_a_song_with_no_verses_is_named_and_cannot_be_saved` | pass — the trigger reads `This song has no verses` after the pick |
| FR-002, US1/AC4 | `test` → `ServiceEntryViewTests.test_an_edit_form_for_a_verse_less_song_states_it_in_the_markup` | pass — the server's fragment carries the line and no `Pick a song first` |
| FR-003 | `test` → the same E2E | **`partial`** — `to_be_disabled()` was asserted, but nothing tried to open the menu, which `plan.md`'s own note promised ("a click leaves the menu closed") |
| FR-004, US2/AC1 | `test` → `ServiceEntryTests.test_a_song_entry_with_no_verses_names_the_song` and the E2E's Save | pass — the field's error is `This song has no verses: pick another song.` |
| FR-005, US2/AC2, US1/AC3, edge one-verse | `test` → `test_a_song_entry_keeps_at_least_one_verse`, `test_the_song_pick_searches_and_the_verses_start_all_checked`, `test_single_verse_song_keeps_checked_verse_and_disables_picker` | pass — unchanged behaviour, unchanged tests |
| SC-002, US1/AC2 | `test` → the E2E, before any pick | pass — `Pick a song first` |
| SC-003 | `test` → the E2E's `bounding_box()` in the verse-less state | pass — trigger 38px, summary 18.89px |
| SC-003 (window), edge narrow dialog | `inspection` — the live page and the preview, 1440 and 420 wide | checked by inspection — live: dialog 480 / trigger 436×38 / summary 158.52×18.89 at 1440; dialog 382 / trigger 338×38 at 420. Preview: 480 and 356 wide, one line both |
| SC-004 | `test` → the E2E pressing Save | pass — the dialog stays open and no entry is written |
| Edge — failed fetch | `inspection` — `static/web/entries.js` `loadVerses`'s `.catch` | checked by inspection — it calls `feedback.showFailure` and returns; no summary write, so the field keeps its previous line |
| Edge — stored verses | `test` → `ServiceEntryViewTests.test_an_edit_form_keeps_the_verses_an_entry_stored` | pass — stored numbers remain choices; the no-verses line does not appear |

**Outcome**: 1 finding, appended below as T014 and fixed in this pass.

## Pass 2 — 2026-10-29

| Row | Method | Result |
| --- | --- | --- |
| FR-003 (re-check) | `test` → the E2E, now also a JS click on the disabled trigger | pass — `#entry-verses-menu` stays hidden |
| every other row | as in pass 1 | unchanged |

**Outcome**: Converged — nothing remains.

**Correction applied, no requirement changed**: `spec.md` §UI/UX said the trigger sat "inside a
436px-wide field (desktop, dialog 436)"; the live dialog is 480px wide and the trigger 436 (measured
again after the change: dialog 480 / trigger 436×38 at 1440, dialog 382 / trigger 338×38 at 420). The
sentence was corrected to say field and dialog. No `FR-`, `SC-` or scenario wording moved.

**Outside the table — the picker harness**: `tests.e2e.test_entry_pickers` was run as extra evidence
(the song field shares that harness) and answered 21 errors in 20 tests, all of the same kind —
`<div id="drawerBackdrop" class="drawer-backdrop">` intercepting the pointer on a hover. The same
single test errors identically on unmodified `develop` (`~/Projects/multimedia-gkps-klender`,
`24a6d6d2`, its own database `test_gkpsdevelop`), so the module is red before this slice, not because
of it. Reported, not fixed here: it is not a row of this slice's table.

## Accepted gaps

None.
