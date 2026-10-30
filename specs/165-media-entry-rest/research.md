# Research: a media entry ends on a rest like every other entry

**Spec**: `specs/165-media-entry-rest/spec.md` · **Base**: `develop` `59182b12`

## D1 — Where the rest is appended

**Decision.** Build the media screen into a variable, then form the group once:

```python
elif row.kind == tatib_models.ServiceEntryKind.MEDIA:
    payload_key = _MEDIA_SCREEN_KEYS.get(row.media.family) if row.media_id else None
    screen = {'blank': False, 'header': '', 'lines': [], payload_key: row.media_id} if payload_key else None
    group = [screen, _blank_screen()] if screen else [_blank_screen()]
```
with `_MEDIA_SCREEN_KEYS = {'image': 'image_sha256', 'audio': 'audio_sha256', 'video': 'video_sha256',
'pdf': 'pdf_sha256', 'slides': 'slides_sha256'}` beside `_blank_screen()`.

**Rationale.** One place states the rule, so a sixth family cannot be added later without meeting it.
The five-branch chain the branch has today repeats the same screen literal five times; appending
`_blank_screen()` inside each branch would make the rule five statements and hide it from the reader.
The no-file case falls out of the same line: no screen, so one rest, not two.

**Alternatives.** (a) Append in each of the five branches — the rule becomes five statements and the
`else` branch has to remember not to append. (b) Append after the whole `if/elif` for every kind —
wrong for the section break (which *is* one blank) and it would have to test the kind again.
(c) Append in `_projector_data`'s common tail by checking `entry_type == 'media'` — a second reading of
the kind after the branch has already decided it.

**Provenance.** Code reading at `59182b12` (`views.py:1234`–`1252`, `_blank_screen()` at `1192`, the
siblings at `1254`, `1284`, `1298`); the rule is spec 058's, folded as `projector/R11` by this slice.

## D2 — What the rest looks like

**Decision.** The exact dict `_blank_screen()` returns, plus the `entry_index` the common tail stamps on
every screen: `{'blank': True, 'header': '', 'lines': [], 'entry_index': n}`. No `bait`, `bait_rest`,
`split`, `split_total`, `translation` or family payload key.

**Rationale.** The projector's renderer and the dock's row builder both read `screen.blank` first; a rest
that carried a payload key would paint a picture on a blank screen, and one carrying `bait_rest` would be
grouped under a bait it does not belong to. Measured: the existing rests in service 144 (text 0–1,
passage 0–1) carry exactly those four keys.

**Alternatives.** A distinct key (`rest: True`) would be a second spelling of `blank` and every reader
would need to learn it.

**Provenance.** `views.py:1192`, `static/web/obs-dock.js:198` (the `screen.blank` branch),
`static/web/projector.js` (`isRest = Boolean(data.blank)`).

## D3 — No change in the dock or the projector page

**Decision.** `static/web/obs-dock.js` and the projector's template and script are untouched.

**Rationale.** The dock builds one row per screen and already draws `screen.blank` as `Rest`
(`obs-dock.js:203`–`208`, the same row the text entry uses); its step list is every screen of every
non-break entry (`buildStops()`), so the new screen joins it without a rule. The projector renders one
`<section class="screen">` per screen from the island, and `move()` steps one screen at a time; the rest
is the blank it already paints. `unitBoundary(End)` skips a trailing blank, so `End` on a media entry
stops on the media screen — the shape text entries already have.

**Alternatives.** Teaching the dock to synthesise a Rest row from `entry.end + 1` would duplicate the
server's rule in the browser and leave `dock.screens` a different list from the projector's.

**Provenance.** `obs-dock.js:180`–`208` (media rows, `screen.blank`), `buildStops()` (all screens of a
non-break entry), dock probe at `/obs/dock` (service 149: entry 1 shows `Rest`, entries 2–5 do not).

## D4 — A media entry with no file keeps one screen

**Decision.** `row.media_id` missing (or a family outside the five) → `group = [_blank_screen()]`, as
today.

**Rationale.** That screen is already a rest; a second one would be a press that changes nothing. Spec
058 gives a stored section break exactly one for the same reason.

**Provenance.** `views.py:1251` (`else: group = [_blank_screen()]`); spec 058 §Domain rules.

## D5 — Which tests change, and which are added

**Decision.**

- Rewritten (the rule they assert is the one this slice changes): `multimedia/web/test_media.py` —
  `test_powerpoint_entry_has_slide_preview_and_projector_screen` (`screens[-1]` is the slide, `blank`
  false), `test_image_and_pdf_each_have_one_projector_screen`, `test_audio_has_one_projector_screen_in_order`,
  `test_video_has_one_projector_screen_in_service_order` (each asserts `start == end`). The three whose
  names state the old rule are renamed with it — `…_each_have_a_screen_and_a_rest`,
  `…_has_a_screen_and_a_rest_in_order`, `…_has_a_screen_and_a_rest_in_service_order` — and the PowerPoint
  one keeps its name because its claim (a preview and a projector screen) still holds.
- Added (`test_media.py`): one test proving each of the five families ends on exactly one rest; one
  proving a no-file media entry keeps its single rest; one proving the entry's `start` is unchanged and
  its `end` is the rest.
- Added (E2E): `tests/e2e/test_obs_dock.py` — a media entry's inner list reads `Image` then `Rest`, and
  the forward arrow from the media screen lands on the rest; `tests/e2e/test_projector.py` — stepping a
  media screen lands on a blank, and `End` on that entry stays on the media screen.

**Rationale.** TDD-07: a test is rewritten only when the behaviour changes or the test was wrong. Three
of these assert the old rule and are rewritten with the reason recorded in the spec; the rest are new
behaviour that needs a test of its own.

**Provenance.** The four tests read at `59182b12`; the dock's row builder read in `obs-dock.js`; the
projector's `moveEntry`/`unitBoundary` read in `projector.js:731`–`772`.

## D6 — Which capability file takes the requirement

**Decision.** `docs/spec/projector.md` gains **R11** (`new`). No other capability file changes.

**Rationale.** The rule is about the projector's screen list; `projector.md` already holds R1–R10 for
that page and its screens, and last folded 2026-10-29. Spec 058's rule predates the capability tree
(the file starts at spec 136) and is not folded anywhere, so R11 states the extension rather than
duplicating a folded requirement.

**Alternatives.** `reading.md` — the entry model lives there, but the requirement is about what the
projector builds, not about what the stage draws.

**Provenance.** `docs/spec/projector.md` header and R1–R10; `git grep -n "blank" docs/spec/` (no folded
rest rule).
