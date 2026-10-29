# Implementation Plan: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`
**Branch**: `fix/162-song-verse-empty-state`
**Bump**: `patch`
**Preview**: `specs/162-song-verse-empty-state/preview/preview.html` (static, built from the app's own
rendered fragment by `preview/build_preview.py`; opened directly)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 / Django 4.0 — one model sentence, one form property, one template expression; JavaScript (ES5 style, no build step) in `static/web/entries.js` |
| Primary dependencies | none added — jQuery-free vanilla JS, Django templates, the existing `editor__*` classes and tokens |
| Storage | none: no migration, no new field, no change to `ServiceEntry.verses` |
| Testing | Django's runner. Unit: `multimedia/tatib/tests.py` (model), `multimedia/web/tests.py` (server-rendered fragment). Browser: Playwright (Python) E2E through `StaticLiveServerTestCase` in `tests/e2e/test_entries.py` |
| Target platform | every viewport the modal draws at (436px dialog at 1440, 338px field at a 420 viewport), both themes — the change is text and a disabled attribute |
| Project type | server-rendered Django web app, no build step; WhiteNoise serves a collected `static/` |
| Performance goals | no request added; the verses endpoint is called exactly as often as today |
| Constraints | the model rule that a song entry keeps at least one verse stays; the endpoint's payload stays; the other four summary lines and their enabled/disabled rules stay byte-identical |
| Scale / scope | 1 model line, 1 form property, 1 template expression, 1 script argument, 3 tests |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check is not applicable.
The repo's standing constraints are honoured: one home per fact (the verse list, not a flag; the
model, not the form, for the refusal), no new dependency, no inline style, no literal colour, and no
change to a route or a payload.

Re-checked after Phase 1: pass. The slice adds no table, stores nothing, and touches no surface other
than the song entry's Verses field and the model's refusal text.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Decisions D001–D006 cover the signal (the picked song,
not the box count), the first paint (server-rendered), the refusal's home (the model), the test split
(one per layer), the endpoint (unchanged) and the fixtures (a real song with no `Verse` rows; an edit
entry created through the ORM).

## Phase 1 — Design

- `data-model.md` — the Song, the ServiceEntry and the Verses field's lines and states; the
  invariants the change has to keep.
- `contracts/` — `none`: no endpoint, no payload and no data attribute changes; the two internal
  identifiers (`SongEntryForm.song_has_no_verses`, the split refusal texts) are named in
  `contracts/none.md` so a later reader does not mistake them for contracts.
- `quickstart.md` — the dev server, the preview build, and the three targeted test runs.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/entries.js` — `verseSummary(picker, box, songPicked)` and its three call sites | `test` → `tests/e2e/test_entries.py::EntryModalE2ETests::test_a_song_with_no_verses_is_named_and_cannot_be_saved` | after picking, the trigger's text is `This song has no verses` |
| FR-002 | `multimedia/web/reading/entries.py` — `SongEntryForm.song_has_no_verses`; `multimedia/web/templates/reading/_entry_form.html` (the summary span) | `test` → `multimedia/web/tests.py::ServiceEntryViewTests::test_an_edit_form_for_a_verse_less_song_states_it_in_the_markup` | the server's own fragment, with no script run: contains `This song has no verses`, not `Pick a song first` |
| FR-003 | `static/web/entries.js` — `trigger.disabled` in the no-boxes branch | `test` → the same E2E test | `to_be_disabled()` on the trigger, and a click leaves the menu closed |
| FR-004 | `multimedia/tatib/models.py` — `ServiceEntry.clean`, the song branch | `test` → `multimedia/tatib/tests.py::ServiceEntryTests::test_a_song_entry_with_no_verses_names_the_song` and `test_a_song_entry_keeps_at_least_one_verse` | two sentences, one cause each; the second test exists today and must stay green |
| FR-005 | `static/web/entries.js` and `_entry_form.html` — every other branch | `test` → `tests/e2e/test_entries.py::EntryModalE2ETests::test_the_song_pick_searches_and_the_verses_start_all_checked` and `test_single_verse_song_keeps_checked_verse_and_disables_picker` | both exist today and must pass unchanged |
| SC-001 | as FR-001 | `test` → the E2E test | the line differs from `Pick a song first` and names verses |
| SC-002 | as FR-005 | `test` → the same E2E test, before a song is picked | `to_have_text('Pick a song first')` |
| SC-003 | `static/styles/design/components.css` (unchanged) + the rendered boxes | `test` → the E2E test, `bounding_box()` on the trigger in the verse-less state | height 38px, and the summary's box 18.89px tall — one line |
| SC-003 (window) | 436px at 1440 and 338px at a 420 viewport | `inspection` — the preview at both widths | the trigger's width follows the field; the line stays one line |
| SC-004 | as FR-004 | `test` → the E2E test pressing Save | the field's error names the song and the entry is not written |
| US1/AC1 | as FR-001 and FR-003 | `test` → the E2E test | one assertion block: text, disabled, no menu |
| US1/AC2 | as SC-002 | `test` → the E2E test | the line before any pick |
| US1/AC3 | as FR-005 | `test` → the two existing song E2Es | unchanged lines and states |
| US1/AC4 | as FR-002 | `test` → the web test | the server's fragment, not the script's aftermath |
| US2/AC1 | as FR-004 | `test` → the model test and the E2E's Save | the sentence, and the dialog staying open |
| US2/AC2 | `multimedia/tatib/models.py` — the `elif not self.verses` branch | `test` → `test_a_song_entry_keeps_at_least_one_verse` | the existing sentence is kept for a song that has verses |
| Edge — failed fetch | `static/web/entries.js` — `loadVerses`'s `.catch` | `inspection` — read the catch: it shows the failure toast and calls no summary update | the line keeps its previous value; nothing states a count it never received |
| Edge — stored verses, song emptied | `multimedia/web/reading/entries.py` — choices = live ∪ stored | `test` → `ServiceEntryViewTests::test_an_edit_form_keeps_the_verses_an_entry_stored` | choices carry the stored numbers, so the no-verses line does not appear and the entry stays saveable |
| Edge — one-verse song | as FR-005 | `test` → `test_single_verse_song_keeps_checked_verse_and_disables_picker` | `All verses`, disabled |
| Edge — narrow dialog | `components.css` (unchanged) | `inspection` — the preview at 420 | one line, 356px field |

**Verification split**: 17 test · 3 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

- `specs/162-song-verse-empty-state/spec.md` — the requirements
- `specs/162-song-verse-empty-state/plan.md`, `research.md`, `data-model.md`, `quickstart.md`,
  `tasks.md`, `analysis.md`
- `specs/162-song-verse-empty-state/contracts/none.md` — the explicit “no interface”
- `specs/162-song-verse-empty-state/checklists/requirements.md` — reviewer-owned
- `specs/162-song-verse-empty-state/preview/` — `preview.html`, `build_preview.py`, `README.md`, `shots/`

### Source

```
multimedia/tatib/models.py                      the refusal split in two by cause
multimedia/web/reading/entries.py               SongEntryForm.song_has_no_verses
multimedia/web/templates/reading/_entry_form.html   the summary span's first paint
static/web/entries.js                           verseSummary's third argument and its call sites
multimedia/tatib/tests.py                       one model test (one existing test stays)
multimedia/web/tests.py                         one fragment test, one stored-verses test
tests/e2e/test_entries.py                       one E2E test and one fixture song
```

### Structure Decision

All four source files already own the sentence they change: the model owns the refusal, the form owns
what the field's choices are, the template owns the first paint, and `entries.js` owns every later
line. No new module: a helper file for one boolean would put a two-line rule one indirection away
from the template that reads it. The tests sit where their subjects are tested today — the model's in
`multimedia/tatib/tests.py`, the fragment's in `multimedia/web/tests.py`, the modal's beside the two
song tests it shares fixtures with.
