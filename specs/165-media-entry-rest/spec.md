# Feature Specification: a media entry ends on a rest like every other entry

**Slice**: `specs/165-media-entry-rest`
**Branch**: `feat/165-media-entry-rest`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1 and gate 2, 2026-10-29)
**Input**: "add rest after media entries"

## What the page does today

`_projector_data` builds a service's projector screens one entry at a time
(`multimedia/web/reading/views.py:1209`). Every entry kind ends its group on a built-in rest — a blank
screen that is not a service row and cannot be moved or edited (spec 058, `_blank_screen()` at
`views.py:1192`):

| entry kind | how its group ends | line |
| --- | --- | --- |
| legacy text row | one line screen, then `group.append(_blank_screen())` | `1298` |
| section break | the break *is* one blank | `1222`, `1232` |
| scripture | `_scripture_screens(row) + [_blank_screen()]` | `1254` |
| song | one blank after **each** verse | `1284` |
| **media** | **the media screen and nothing else** — for all five families | `1234`–`1252` |

The media branch is the one kind written without a trailing rest:

```python
elif row.kind == tatib_models.ServiceEntryKind.MEDIA:
    if row.media_id and row.media.family == 'image':
        group = [{'blank': False, 'header': '', 'lines': [], 'image_sha256': row.media_id}]
    ...                                        # audio, video, pdf, slides the same shape
    else:
        group = [_blank_screen()]
```

Media screens arrived in specs 117 and 118, after spec 058 wrote the "one blank after content" rule for
the kinds that existed then; the rule was never extended, so the branch that builds a picture, a
recording, a PDF page or a slide deck is the only one that runs straight into the next entry.

Measured on the running product (`http://127.0.0.1:63404`, `develop` `59182b12`), through
`_projector_data` and the dock at `/obs/dock`:

| service | entry | its screens today |
| --- | --- | --- |
| 149 (25 Oct, 5 entries: 1 legacy text, 4 images) | 1 legacy text | `0–1` — the line, then a rest |
| | 2 image `random.jpg` | `2–2` — **the picture alone** |
| | 3 image `images (1).jpeg` | `3–3` — **the picture alone** |
| | 4 image `side-view-silhouette…webp` | `4–4` — **the picture alone** |
| | 5 image `random.jpg` | `5–5` — **the picture alone** |
| 144 (20 Oct, 16 entries) | 1 passage | `0–1` — the verse, then a rest |
| | 2 video | `2–2` — **the video alone** |
| | 3 image | `3–3` — **the image alone** |
| | 4 song | lyrics, rest, lyrics, rest … one rest per bait |
| | 5 PDF | `5–5` — **the page alone** |
| | 6 text | its screens, then a rest |
| | 7 audio | `7–7` — **the recording alone** |

Service 149 produces **6 screens**, and the sixth is its fourth picture: pressing next at the end of the
service does nothing, so a service that finishes on a picture has no rest to leave the display on.
Between two media entries the same gap means a picture goes straight to the next picture — the rest
every other entry gives the operator before moving on is missing exactly where the content is loudest.

In the dock (`/obs/dock`, 420×900, service 149, screen 2 live) the same fact is visible in the entry's
inner list: entry 1 shows its line and `Rest` (a 69.7px body); entries 2–5 each show a single `IMAGE` row
(a 37.8px body, the row itself 352×28.8). Service 144 shows `VIDEO`, `IMAGE`, `PDF`, `AUDIO` — one row
each — beside song rows carrying `Rest` after every bait.

Four unit tests pin today's shape: `test_media.py`
`test_powerpoint_entry_has_slide_preview_and_projector_screen` (`screens[-1]` is the slide and
`assertFalse(blank)`), `test_image_and_pdf_each_have_one_projector_screen`
(`image_entry['start'] == image_entry['end']`), `test_audio_has_one_projector_screen_in_order` and
`test_video_has_one_projector_screen_in_service_order` (the same equality for audio and video). They are
rewritten red first, and the three that name the old rule in their names are renamed with it
(`…_each_have_a_screen_and_a_rest`, `…_has_a_screen_and_a_rest_in_order`,
`…_has_a_screen_and_a_rest_in_service_order`).

## User Scenarios & Testing

### US1 — A media entry rests after its screen, whatever the media is (P1)

**Why this priority**: this is the request, and the gap is the whole of it. Every kind of entry but this
one already leaves the display blank before the next thing; an operator running a service of images has
to reach for the display toggle instead of stepping.

**Independent Test**: open `/projector?service=149` and step through it: the text line, a rest, an image,
a rest, an image, a rest, an image, a rest, an image, a rest.

**Acceptance scenarios**

1. **Given** a service holding one image entry, **When** the projector builds its screens, **Then** the
   image is screen 1 and a rest is screen 2, and the entry's own range covers both.
2. **Given** a service holding an audio, a video, a PDF and a slides entry, **When** it builds,
   **Then** each media screen is followed by one rest.
3. **Given** a service of four images in a row (service 149), **When** it builds, **Then** it produces
   ten screens and stepping never goes from one picture to the next without a rest between them.
4. **Given** a media entry with no file attached, **When** it builds, **Then** it still produces exactly
   one screen — its rest — and not two.

### US2 — The dock steps and lists the same rest (P1)

**Why this priority**: the dock is how the service is run. A rest the transport cannot land on, or that
the entry's inner list does not show, would be a screen on the projector page only.

**Independent Test**: at `/obs/dock` open service 149 and point at entry 2 — its inner list reads
`IMAGE` then `Rest` — then press the forward arrow from screen 2 and the display lands on 3, the rest.

**Acceptance scenarios**

1. **Given** the dock's runner for service 149, **When** the first image's entry is the live entry,
   **Then** its inner list shows the media row and, under it, one `Rest` row, styled as the rests the
   text and song rows already draw.
2. **Given** the display is on a media screen, **When** the operator presses the forward arrow, **Then**
   the display steps to that entry's rest, and a second press enters the next entry.
3. **Given** a service that ends on a media entry, **When** the operator reaches its rest, **Then** the
   display is blank and the forward arrow is at the end of the service.

### US3 — Nothing else about the screens moves (P2)

**Why this priority**: the media screens carry payloads and fitting rules of their own (R3, R4, R6–R10).
Adding a rest must not touch a picture, a page's fit, a recording's lock, or any other entry's shape.

**Independent Test**: compare `_projector_data` for service 144 before and after: every media screen's
payload is unchanged, every passage, text and song screen is at a new index but with the same content,
and only media entries have a longer range.

**Acceptance scenarios**

1. **Given** any media screen, **When** it is built, **Then** it keeps its own payload key
   (`image_sha256`, `audio_sha256`, `video_sha256`, `pdf_sha256`, `slides_sha256`), its empty `header`
   and `lines`, and paints exactly as it does today.
2. **Given** a passage, text, song or section break, **When** it is built, **Then** its screens are the
   same screens in the same order, and its rest is the same one rest as before.
3. **Given** the projector's fitting, panning, audio lock and the overlay, **When** a rest follows a
   media screen, **Then** none of them changes behaviour: the rest is a blank screen like any other.

### Edge Cases

- **A media entry with no file** already contributes one rest as its only screen; it gains no second one.
  Two rests in a row would cost a press that changes nothing.
- **A media entry followed by a section break** shows the new rest and then the break's own blank; two
  adjacent rests stay two, as they do after a text entry (spec 058).
- **A service that ends on a media entry** now ends on a rest, so the display can be left blank without
  leaving the service.
- **A playing recording** keeps the lock it has (R5): the rest is reached by stepping once playback is
  paused or finished; no rest is inserted before it.
- **A multi-page PDF or slide deck** still steps inside its own pages before the screen changes; the
  rest comes after the last page, as the next screen.
- **A browser left projecting** keeps its screen index in local storage: screens after the first media
  entry shift by one, so that index can name a different screen until the operator steps. The display
  state is a live pointer, not stored content, and no migration is invented for it.
- **The overlay and the dock's "next" band** read the entry's range, so they follow the new `end`
  without a change of their own.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A media entry whose file resolves SHALL contribute its media screen followed by exactly one built-in rest, for all five families — image, audio, video, PDF and PowerPoint. | `new: projector` → R11 |
| FR-002 | A media entry whose file does not resolve SHALL contribute one screen, that rest, and SHALL NOT gain a second. | `new: projector` → R11 |
| FR-003 | The rest SHALL be the built-in rest the other kinds use: `blank: True`, empty `header` and `lines`, no `bait`, `bait_rest`, `split`, `translation` or media payload key, not stored, and not a row in the service order. | `new: projector` → R11 |
| FR-004 | The media entry's `end` SHALL include its rest and its `start` SHALL be unchanged; every entry's `type`, `label` and order SHALL be unchanged. | `new: projector` → R11 |
| FR-005 | The dock's inner list SHALL show the media row and, under it, the rest row in the same `.screenerow--rest` treatment the text and song rests carry, and the display's step list SHALL include it. | `new: projector` → R11 |
| FR-006 | Nothing else SHALL change: the media screens' payloads and paint, the fit and pan rules (R6–R10), the audio and video lock (R5), the overlay, the stage, the editors and the Media Library keep their present behaviour. | `projector/R3` |

### Key Entities

- **Built-in rest** — `_blank_screen()` (`views.py:1192`): a blank projector screen that belongs to an
  entry without being a service row. Spec 058's rule; this slice extends it to the media kind.
- **Media entry** — a `ServiceEntry` of kind `MEDIA` (kind 4) with a `MediaIdentity` and one of five
  families. Its screen carries only the identity's hash under the family's key.
- **Entry range** — `{'start': …, 'end': …}` on each entry of `_projector_data`, the dock's step list and
  the "next" band read it. The rest moves `end` by one and no `start`.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Service 149 builds 10 screens: text, rest, image, rest, image, rest, image, rest, image, rest. | `_projector_data(service 149)`: entry ranges `[(0,1),(2,3),(4,5),(6,7),(8,9)]`, blank at 1, 3, 5, 7, 9 |
| SC-002 | Service 144 gains exactly one rest per media entry and nothing else. | the same call: video, image, PDF and audio each `start+1 == end`, the rest blank; passage, text and song ranges hold their own screens and rests |
| SC-003 | A media entry with no file still yields one screen. | the same call on an entry with `media=None`: one screen, `blank` true |
| SC-004 | The dock lists and steps the rest. | `/obs/dock` service 149: the live media entry's inner body holds `IMAGE` then `Rest`, the body 37.8 → 69.7px; forward from screen 2 lands on 3 |
| SC-005 | The projector paints the rest as the blank screen it already has. | `/projector?service=149`: `.screen.is-blank` at indices 1, 3, 5, 7, 9; the media sections unchanged |
| SC-006 | The suites stay green, the four media-shape tests rewritten to the new rule. | `multimedia.web.test_media` 12, `multimedia.web.test_obs_dock`, `multimedia.web.tests` (projector class), `tests.e2e.test_obs_dock`, `test_projector`, `test_image_display`, `test_video_display`, `test_pdf_display`, `test_powerpoint_display`, `test_audio_display` |

## UI/UX

**Static preview at `specs/165-media-entry-rest/preview/preview.html`** — two 420px panels, the real runner
markup of `/obs/dock` for service 149 at screen 2, with the dock's own `tokens.css` and `obs-dock.css`
frozen at `59182b12`; the right panel adds the slice's one row to each media entry. The page carries a
theme switch, so both states are seen in the dock's dark default and in light.

- **Layout / position**: the rest row takes the media row's own column — 352px wide inside the
  420px dock, its 10px side padding aligned with the media row's — and sits 3px under it
  (`.screenerow + .screenerow`). Nothing moves horizontally; no other entry's row moves.
- **Size / spacing**: the rest row is 28.8px tall (5px padding top and bottom around 13px/1.45 text),
  the same box every rest row already takes. The media entry's inner body grows **31.9px** —
  37.8 → 69.7px — and the entry row above keeps its 38px.
- **Colour / typography**: `.screenerow--rest` — italic, `color-mix(--head-ink 66%)` — the treatment the
  text entry's rest already draws one row above it in the same list. No new token, no new mark.
- **States**: the rest row at rest, under hover (`--icon-hover-bg`), as the current screen
  (`--sidebar-selected-bg` at 55%), in dark and in light; the media row above it keeps
  `screenerow--media`'s 10px/650 uppercase label. The entry's inner list keeps its 200ms
  grid-track open/close motion — the extra row is part of the same list, so nothing new animates.
- **The projector's rest** is the blank screen the other kinds already paint (`section.screen.is-blank`),
  so no new screen style is introduced and no screenshot of it is the preview: it is the shipped
  component, reached by stepping.
- **Responsive**: at 420px the dock's row is 352px; at the 560px maximum the row is 492px and the rest
  row matches it. Nothing about the row depends on the viewport.
- **Motion**: none added. Stepping onto the rest is the projector's ordinary screen change.

## Assumptions

- **"Media entries" are the service entries of the media kind** — a picture, a recording, a video, a PDF
  page or a slide deck in a Tata Ibadah — not the Media Library's file rows and not a media screen's own
  preview. The request names the entry, and the entry is where the gap is.
- **The rest goes after the media screen, inside the entry.** Putting it before the media would blank the
  display before a picture the operator asked for, and a rest between entries would be a service row —
  which spec 058 refuses.
- **A media entry with no file keeps its one screen.** Its only screen is already a rest; a second would
  be a press that changes nothing, and the same reasoning gives a stored section break exactly one.
- **All five families are treated alike.** There is no reason a video should rest and a PDF should not;
  the families differ in what they paint, not in where the entry ends.
- **The display state is not migrated.** `gkps-display` holds a screen index in the operator's browser;
  screens after the first media entry shift by one, so an already-open browser can be one screen off
  until it is stepped. This is a live pointer, not content, and every previous change to the screen list
  (specs 058, 091, 144) has the same effect.
- **Bump: patch** — `VERSION` 1.23.2 → **1.23.3**, one `### Changed` line in `[Unreleased]`; the card is
  `ITEM-178`, the capability requirement `projector/R11`.
- **The four unit tests that pin today's shape are rewritten, not deleted.** They assert the old rule
  (`start == end`, the last screen is the media); the requirement changes, so the assertions change with
  it and the reason is recorded in the slice.

## Clarifications

### Session 2026-10-29

- **What "rest" names** — the built-in blank projector screen the product already calls rest in the
  dock's row and in spec 058, and "media entries" the entries of the media kind. Read from the request
  ("add rest after media entries") against the code and the running surface; no other kind of entry is
  missing its rest, and the dock's own list shows exactly that gap. Zero open markers remain.
