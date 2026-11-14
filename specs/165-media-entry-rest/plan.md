# Implementation Plan: a media entry ends on a rest like every other entry

**Spec**: `specs/165-media-entry-rest/spec.md`
**Branch**: `feat/165-media-entry-rest`
**Bump**: `patch` — 1.23.2 → 1.23.3 (one screen per media entry in the projector's screen list; nothing
existing changes shape)
**Preview**: `specs/165-media-entry-rest/preview/preview.html` — static, opened directly

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 / Django 4.0 — one function, `_projector_data` in `multimedia/web/reading/views.py`; no JavaScript, CSS, template or model change |
| Primary dependencies | none added |
| Storage | none — the screens are built per request; no field, no migration |
| Testing | `multimedia/web/test_media.py` (unit, Django `TestCase`) and `tests/e2e/test_obs_dock.py`, `tests/e2e/test_projector.py` (Playwright, `StaticLiveServerTestCase`) |
| Target platform | unchanged — the server-rendered projector page and the dock's browser |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | none; the function already builds one dict per screen and this adds one dict per media entry |
| Constraints | the media screens' payloads, the entry `type`/`label`, the fit and pan rules, the audio/video lock and the dock's script are untouched; a media entry with no file keeps one screen |
| Scale / scope | ~12 lines of production code in one branch of one function; 4 unit tests rewritten, 3 added, 2 E2E cases |

## Constitution Check

No `CONSTITUTION.md` exists (SDD-01: optional, never auto-created), so the check does not apply. The
Constraints row above stands in its place.

Re-checked after Phase 1: **pass** — the design adds no file, no request, no dependency, no stored state
and no new screen key; the only seam it crosses is the JSON island the dock already parses
(`contracts/none.md`), whose shape it extends by exactly the invariant the dock already assumes.

## Phase 0 — Research

See `research.md`. Six decisions: one construction point in the media branch with a family→key map (D1);
the rest is `_blank_screen()`'s own four keys (D2); no change in `obs-dock.js` or the projector page
(D3); a no-file media entry keeps its single rest (D4); which four tests are rewritten and which three
cases are added (D5); the requirement lands in `projector` as R11 (D6). **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the screen dict, the family→payload-key table, the entry range, and the before/after
  ranges of services 149, 146 and 144 (167 → 171 screens).
- `contracts/` — `none` (`contracts/none.md`): no external interface changes; the embedded screen island
  the dock parses is recorded there because two of the project's scripts share it.
- `quickstart.md` — the isolated test database, the modules, and the two routes to look at by hand.

### The design

`multimedia/web/reading/views.py`, the media branch of `_projector_data` (today `1234`–`1252`):

```python
# The family decides the screen's one payload key; the rest is the built-in blank every other
# entry kind ends on (spec 058), so a picture, a recording, a page or a deck never runs
# straight into the next entry.
elif row.kind == tatib_models.ServiceEntryKind.MEDIA:
    key = _MEDIA_SCREEN_KEYS.get(row.media.family) if row.media_id else None
    screen = {'blank': False, 'header': '', 'lines': [], key: row.media_id} if key else None
    group = [screen, _blank_screen()] if screen else [_blank_screen()]
    entry_type, label, untitled = 'media', row.citation(), not bool(row.title)
```

with, beside `_blank_screen()`:

```python
_MEDIA_SCREEN_KEYS = {'image': 'image_sha256', 'audio': 'audio_sha256', 'video': 'video_sha256',
                      'pdf': 'pdf_sha256', 'slides': 'slides_sha256'}
```

Nothing else moves: the common tail stamps `entry_index` on both screens and computes the entry's range
from `len(group)`, so `start` is unchanged and `end` grows by one. The dock's row builder reads
`screen.blank` and its step list reads every screen of a non-break entry, so both follow without a
change; the projector's `move()` steps onto the blank it already paints, and `unitBoundary(End)` still
stops on the media screen because it skips a trailing blank.

## Traceability

| Requirement / scenario | Component / file | Verified by |
| --- | --- | --- |
| FR-001 each of the five families gets its screen then one rest | `views.py` `_projector_data` media branch, `_MEDIA_SCREEN_KEYS` | `test` → `multimedia/web/test_media.py::MediaEntryRestTests::test_each_family_ends_on_one_rest` |
| FR-002 a media entry with no file keeps one rest | the same branch (`key` None → one blank) | `test` → `…::test_a_media_entry_without_a_file_keeps_its_one_rest` |
| FR-003 the rest is the built-in blank, with no payload or bait keys | `_blank_screen()`; the common tail | `test` → `…::test_the_rest_carries_only_the_built_in_blank` |
| FR-004 `start` unchanged, `end` = the rest, order and labels unchanged | the common tail's `entries.append` | `test` → `…::test_the_entry_range_extends_over_the_rest` |
| FR-005 the dock lists and steps the rest | `static/web/obs-dock.js` `screenRow`/`buildInner`/`buildStops` — unchanged | `test` → `tests/e2e/test_obs_dock.py::ObsDockE2ETests::test_a_media_entry_lists_and_steps_its_rest` |
| FR-006 every media screen keeps its payload and paint | the same branch's payload key | `test` → the four rewritten cases in `test_media.py` assert each payload key and the media screen's paint; `tests.e2e.test_image_display` / `test_video_display` / `test_pdf_display` / `test_powerpoint_display` / `test_audio_display` stay green |
| US1 AC1–AC3 a service of media entries rests between every picture | the branch | `test` → `…::test_four_images_in_a_row_build_ten_screens` |
| US1 AC4 no file, one screen | the branch | `test` → `…::test_a_media_entry_without_a_file_keeps_its_one_rest` |
| US2 AC2 the forward arrow lands on the rest | `projector.js` `move()` — unchanged | `test` → `tests/e2e/test_projector.py::ProjectorTests::test_a_media_entry_steps_onto_its_rest` |
| US2 AC3 a service ending on media ends on a rest | the branch | `test` → `…::test_four_images_in_a_row_build_ten_screens` (last screen blank) |
| US3 AC1–AC3 no other kind's screens move | the four untouched branches | `test` → `test_media.py` passage/song cases in `multimedia/web/tests.py`; `inspection` — the diff touches the media branch only |
| SC-001 service 149 builds ten screens with ranges `(0,1)(2,3)(4,5)(6,7)(8,9)` | the branch | `test` → `…::test_four_images_in_a_row_build_ten_screens` |
| SC-005 the projector paints the rest as its blank screen | `projector.js` `isRest` — unchanged | `test` → `tests/e2e/test_projector.py::…::test_a_media_entry_steps_onto_its_rest` asserts `.screen.is-blank` is active |
| SC-006 the suites stay green | the five modules named in `quickstart.md` | `test` → the runs recorded in `converge.md` |

**Split**: 13 test · 1 inspection · 0 manual.

The four rewritten cases — `test_powerpoint_entry_has_slide_preview_and_projector_screen`, and the three
renamed with the rule they now assert, `test_image_and_pdf_each_have_a_screen_and_a_rest`,
`test_audio_has_a_screen_and_a_rest_in_order`, `test_video_has_a_screen_and_a_rest_in_service_order` —
change because they asserted the rule this slice replaces (`start == end`, the last screen is the media).
They were rewritten red-first (seen failing before the branch changed) with the reason in `research.md`
D5, never deleted; each keeps its payload assertion.

## Risks

- **Screen indices shift.** Every screen after a media entry moves by one, and the operator's browser
  holds a screen index. Named in the spec's edge cases and assumptions; no migration is invented.
- **A service of many media entries gains many presses.** Ten pictures become twenty screens. That is the
  point of the change — the rest is the only way to leave the display blank without the toggle — but it
  is a cost the operator will feel, and it is recorded rather than smoothed over.
- **The four rewritten tests could hide a regression.** Each keeps its payload assertion (the media
  screen's key and value) and only its range assertion changes, so a broken payload still fails.
