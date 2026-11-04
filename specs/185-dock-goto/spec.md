# Feature Specification: the dock's Go To — a passage or a song on air without leaving the service

**Slice**: `specs/185-dock-goto`
**Branch**: `feat/185-dock-goto`
**Created**: 2026-11-03
**Status**: Accepted — gate 1 2026-11-04 · gate 2 2026-11-04 (checklist 20/20 ticked)
**Input**: *"i wanna add something like the goto function into the obs dock. how would you do that?"* —
answered with the shared-state design; the owner's ruling: *"all goto states are synced between
pages and reset on browser restart (just like the tataibadah project)"*.

## What the surfaces do today

One object in `localStorage['gkps-display']` decides what is on air in a browser:
`{service, screen, on, translation, at, session}` (`static/web/display.js`). The dock and the
projector write it; the caption overlay, the projector and every reading page read it; the
`gkps-service-display` channel carries each change. Spec 184 stamped it with the browser session, so
a restart finds no state on air.

That pointer can only name a **service screen**. Both readers rebuild the screen from the service's
own page — the projector from the data islands it was served (`static/web/projector.js`), the
overlay by fetching `/projector?service=<id>` and reading the same islands
(`static/web/obs-overlay.js`). A song that is not in the Tata Ibadah has no index in that pointer,
and a passage outside the service has no row.

The projector's Go To therefore lives **inside that one page**: `detour`, `returnScreen` and the
corner cue's "back to …" are page-local memory (`static/web/projector.js`). The dock cannot reach
them, the overlay never learns of them, and while a detour is up the dock's transport moves the
service invisibly underneath it.

The content for a Go To already exists as three payloads (spec 136):

| Endpoint | What it carries |
| --- | --- |
| `/projector/goto/index/` | the lookup's data — book names, editions, chapter/verse counts, songbooks, song titles; no verse text, no lyric |
| `/projector/goto/chapter/<book>/<chapter>/` | one chapter in both editions, so a verse step inside it is local and the TB/SIM flip needs no request |
| `/projector/goto/song/<id>/` | one song's screens and bait ranges, shaped exactly as the projector paints them |

and the lookup itself is a pure function over that index in `static/web/projector-library.js`.

## The Go To, after this slice

- The display state gains one field, `goto`, and stays a **pointer**: what is on air while the
  service is not is named, never copied. No verse text and no lyric ever enters the state.
- A goto names what is on air — a song with its screen index, or a passage with its book, chapter,
  verse and shown edition — and the service's own place to come back to: its screen and its edition.
- `show` ends a goto: "the service is on air" is one statement, whichever act produces it. `hide`
  and `release` keep their meanings (`hide` blanks whatever is on air and keeps its place; `release`
  lets everything go).
- `flip` flips **what is on air**: the goto's edition while a goto is up, the service's otherwise.
  The service keeps its own edition throughout and gets it back on return.
- Writers: the dock and the projector (its own `G`). Readers: the dock, the projector and the
  overlay. A surface opened or reloaded mid-goto catches up to it, as it does to a screen.
- The session stamp (spec 184) covers it: a browser restart finds no state, so no goto either.
- No new endpoint and no server state. Every surface fetches the payload it paints from the existing
  `/projector/goto/*` endpoints with `cache: 'no-store'`.
- This extends the shape spec 119 pinned in its domain rules (`{service, screen, on, translation,
  at}`) and inherits spec 184's stamp. The delta is one field and one rule: `goto`, and `show` ends
  it.

## User Scenarios & Testing

### US1 — The operator puts a passage or a song on air from the dock (P1)

**Why this priority**: this is the request. The dock is the surface the operator runs a service from
inside OBS; an unplanned song, or a verse the congregation asks for, must not require leaving it.

**Independent Test**: open the dock's runner for a service, press `G`, type a reference, press
Enter — the projector paints it and the overlay paints it, while the service's own position is
untouched.

**Acceptance scenarios**

1. **Given** a service open in the dock's runner **When** `G` is pressed **Then** the find band opens
   over the dock — a layer covering the head and the list — with the field empty and the prompt to
   type, and the index is read once.
2. **Given** the find band open **When** a songbook reference (`NKB 2`), a passage reference
   (`Matius 2:3`), a book name or a bare number is typed **Then** the suggestion and the `n / n` count
   change, and no request is made.
3. **Given** a suggestion **When** Enter (or the result row) is pressed **Then** that song or passage
   goes on air at its first screen or verse on the projector and the overlay, the dock's runner shows
   it as the list's live block, and its switch-service control is disabled.
4. **Given** the find band open **When** Escape is pressed, or the layer is clicked, or Backspace is
   pressed with the field empty **Then** the band closes, nothing goes on air, and the transport
   returns in place.
5. **Given** a query with no match **When** the field settles **Then** the row says there is no
   matching passage or song, and Enter does nothing.

### US2 — The Go To is one state, and every surface agrees (P1)

**Why this priority**: two independent gotos would let the dock show the service while the projector
paints a song — the disagreement this slice exists to end.

**Independent Test**: start a goto from the projector's own `G`; the dock's runner shows it as on
air and its transport steps it; the overlay paints the same words. Start one from the dock; the
projector's cue names it and its `Back` returns to the service.

**Acceptance scenarios**

1. **Given** a service on air **When** a goto is started from any surface **Then** the other two
   follow within one channel message, and each names the same thing.
2. **Given** a goto on air **When** the dock's transport steps it **Then** all three follow, the
   block's marked row moves with them, and the service's screen is unchanged.
3. **Given** a goto on air **When** a surface opens or reloads **Then** it catches up to the goto,
   not to the service beneath it.
4. **Given** a goto started from the projector **When** the dock's Back is pressed **Then** the
   projector returns to the service, at the place it stood before the goto began.

### US3 — Back restores the service exactly (P1)

**Why this priority**: a detour that costs the service its place would make operators avoid the
feature mid-service.

**Independent Test**: step the service to a known screen, flip a passage's edition, note both, start
a goto, step it, flip the goto's edition, then press Back: the projector is on the same screen with
the same edition, and the dock's chip agrees.

**Acceptance scenarios**

1. **Given** the service on screen 12 with the SIM edition shown **When** a goto is started and
   returned from **Then** the projector is on screen 12 with SIM still shown.
2. **Given** a goto on air **When** Back is pressed **Then** every surface shows the service's
   screen, the dock's block is gone, and the projector's cue names the service entry again.
3. **Given** a goto on air **When** the dock is looked at **Then** the service's own rows are not
   drawn at all; Back brings them back, with the service still on the screen it stood on.

### US4 — The Go To lives exactly as long as the display state (P2)

**Why this priority**: it is the owner's ruling, and it keeps one lifecycle for everything on air.

**Independent Test**: put a goto on air, close every surface, reopen them in the same session (the
goto is still there); then start a browser session without the marker holding that state — every
surface is idle and paints no goto.

**Acceptance scenarios**

1. **Given** a goto on air **When** the browser session ends and starts again **Then** the overlay
   paints nothing, the projector paints no screen, the dock marks no service on screen and offers no
   go-to strip.
2. **Given** a goto on air **When** the operator releases **Then** the goto goes with the service and
   every surface is idle.
3. **Given** a goto on air **When** the operator hides the words **Then** the goto stays on air at
   its place, blank, exactly as a service screen does.

### Edge Cases

- **When** a playing audio or video recording holds the projector screen (projector/R5) **Then** a
  goto arriving from another surface stops the recording and paints, as another screen from the
  channel does; the projector's own `G` stays refused while the recording plays.
- **When** the chosen song has no lyric **Then** nothing goes on air and the find band says the
  content could not be loaded, keeping the query.
- **When** a chapter or song request fails **Then** what is on air does not change, and the find band
  says it could not be loaded.
- **When** the service is edited during a goto so its return screen no longer exists **Then** the
  return lands on its last screen instead of failing.
- **When** a goto is started while nothing is on air **Then** the browsed service is adopted at its
  first screen underneath it, so Back always has a place to return to.
- **When** the operator presses `T` during a passage goto **Then** only the goto's edition flips, and
  the service's edition is what a return restores.
- **When** the operator hides the words during a goto and then returns **Then** the service comes
  back with its words still hidden — `on` is one flag for whatever is on air.
- **When** two surfaces start a goto at the same moment **Then** the last write wins and all three
  surfaces settle on it; no surface keeps a private detour.
- **When** the reading page's Stop projecting is pressed during a goto **Then** the goto ends with the
  service and every surface is idle.
- **When** the dock is on the picker view **Then** there is no Go To: a goto needs a service open.
- **When** the layer is clicked **Then** the band closes and nothing goes on air, whatever the query
  had found.
- **When** the state is corrupt or carries a goto it cannot parse **Then** readers treat it as no
  goto and paint the service screen named beside it.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The display state SHALL carry the goto on air: its kind, its reference and position (a song's screen index, or a passage's book, chapter, verse and shown edition) and the service's own return place (screen and edition). It SHALL remain a pointer — no verse text, title or lyric in the state. | `display-state/R2` (new) |
| FR-002 | `show` SHALL end a goto on every surface; `hide`, `release`, `flip` and `update` SHALL keep their meanings, with `flip` naming the edition of whatever is on air. | `display-state/R2` (new) |
| FR-003 | A goto SHALL be stamped with the browser session like the rest of the state, and a state from an earlier session SHALL read as no state, goto included. | `display-state/R1` (kept) |
| FR-004 | The dock's runner SHALL offer a Go To, opened by `G` or by a control in its head; the picker SHALL NOT offer it. | `new: dock` |
| FR-005 | The dock's Go To SHALL answer a query from a page-memory index fetched through `/projector/goto/index/`, with the projector's grammar and labels, and SHALL make no request while typing. | `new: dock` |
| FR-006 | Choosing a result SHALL fetch that chapter or song once and put it on air at its first screen or verse; a step inside the loaded chapter SHALL make no request, and a step into another chapter SHALL fetch it. | `new: dock` |
| FR-007 | The dock's runner SHALL display what is on air as the list's live block: a pinned header naming the go to with its `On screen` marker and `Back`, and beneath it the go to's own screens — a song's baits and lyric rows, a passage's verses — with the current one marked and every row a jump. While a go to is up the service's own rows SHALL NOT be drawn. | `new: dock` |
| FR-008 | Back SHALL restore the service's screen and edition exactly as they stood when the goto began, whatever was done during it. | `new: dock` |
| FR-009 | A go to SHALL end by `Back` or by a `show` that puts a service screen on air; a row of its own block SHALL move the go to to that screen or verse instead of ending it. | `new: dock` |
| FR-010 | The projector's `G` SHALL write the same goto to the state instead of keeping a private detour; its panel, cue, loading lock and `Back` SHALL keep their present look and behaviour, and `Back` SHALL write the service's return place. | `projector/R1` (modified) |
| FR-011 | The overlay SHALL paint a goto from the state: a song as the lyric caption, a passage as the quotation card, by the rules those screens already carry, and SHALL paint nothing when the goto is blank, hidden or gone. | `overlay/R1` (modified) |
| FR-012 | A goto arriving over the display channel while a recording holds the projector SHALL stop that recording and paint, as another screen does; the projector's own `G` SHALL stay refused while a recording plays. | `projector/R5` (modified) |
| FR-013 | The slice SHALL add no endpoint, no server-side state and no new storage key; the index, chapter and song payloads are the existing ones, fetched `no-store`. | `display-state/R2` (new) |
| FR-014 | A surface opened or reloaded mid-goto SHALL catch up to the goto in its current position, never to the service beneath it. | `new: dock`, `projector/R1`, `overlay/R1` |
| FR-015 | While a goto is on air the dock's transport SHALL act on the goto: an arrow changes its screen or verse, a bait chip its bait, a flip its edition. The service's own screen and edition SHALL NOT change until Back. | `new: dock` |
| FR-016 | A goto SHALL be startable while nothing is on air; the browsed service is then adopted at its first screen underneath it, so Back always has a place to return to. | `new: dock` |
| FR-017 | While a goto is on air no picker row SHALL wear the "On screen" pill, and the go to's own header SHALL NOT carry it either: the list shows nothing but the go to, which is its own marker. | `new: dock` |
| FR-018 | While the find band is open the rest of the dock SHALL be covered by a layer in the product's own backdrop (`--backdrop`): every pointer over it SHALL close the band and do nothing else, and no covered control SHALL be operable. `Escape`, a click on the layer, and `Backspace` with an empty field SHALL each close it — the last two being the projector Go To panel's own gestures. Closing SHALL put the transport back and leave the dock where it was, and choosing a result SHALL take the layer with it. While the band is open the dock's transport keys (arrows, `Home`/`End`, `Space`, `T`) SHALL NOT act. | `new: dock` |
| FR-019 | While a go to is on air the runner's switch-service control SHALL be disabled rather than hidden — the head keeps its width and the exit stays visible — and SHALL be usable again the moment the go to ends. | `new: dock` |

### Key Entities

- **Goto** — what is on air while the service is not: its kind, its reference and position, the
  passage's shown edition, and the service's return place. Lives in `gkps-display` only as a
  pointer; the words are fetched by each surface.
- **Find band** — the dock runner's search, in the transport's place: a field and one result row
  with an `n / n` count, answering from the page-memory index.
- **Go To block** — the list's live block while a goto is on air: its pinned header (the `On screen`
  marker, the label and Back) and, beneath it, the go to's own screens.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Typing in the dock's Go To makes 0 requests; choosing a song makes 1; a verse step inside the loaded chapter makes 0 and a chapter crossing makes 1. | E2E counting requests on the dock's page. |
| SC-002 | Back lands on the exact screen and edition: the projector's active screen and the dock's chip equal their values from before the goto. | E2E: note both, goto, step and flip, Back, compare. |
| SC-003 | The three surfaces agree at every step of a goto: the dock's block header, the projector's cue label and the overlay's painted words name the same thing. | E2E walk comparing the three readouts. |
| SC-004 | After a browser session ends, no surface paints a goto: 0 children on the overlay stage, no block in the dock, no detour on the projector. | E2E with the stored state and no session marker. |
| SC-005 | The stored state carries no passage: none of the chapter's verse words appear in `gkps-display`. | Read of the stored JSON. |
| SC-006 | The dock's Go To is the projector's own lookup, not a second one: the same module answers both, and its labels and order match on a fixed set of queries. | Unit/E2E: the same query through both surfaces. |

## UI/UX

`static preview at specs/185-dock-goto/preview/index.html` — the dock's own runner, drawn by the
product's builders from a captured service, with the two proposed parts added. The probe
(`preview/probe.py`) prints exactly these numbers at 400 × 800, dark.

- **Where the Go To is**: one more 38 px icon-only control in the runner's head, left of the
  service-switch control, carrying `G` as its key. It exists in the runner only.
- **The layer**: with the band open, `--backdrop` (`rgba(20, 20, 18, .52)` light, `rgba(0, 0, 0, .68)`
  dark) covers the whole dock — 400 × 800 at the dock's size, from the head's top down — fading in and
  out over 160 ms (`--ease-timing`; none under reduced motion). The foot band is drawn above it with
  its own `--rail-bg` back, so the field and its suggestion stay at full strength while everything
  behind reads inactive. A click anywhere on the layer closes the band.
- **The find band**: it takes the transport's place in the foot band — the band becomes two 34 px
  boxes, a field and the suggestion, 8 px apart (372 × 76 at the dock's 400 px width, 14 px side
  padding). The list gives up those 38 px; the transport returns where it was when the band closes.
- **The field**: 372 × 34, 13.5 px/400, 1 px `--divider` border, 9 px radius, the dock's ink; on
  focus the border takes `--focus`. Placeholder `Passage or song`.
- **The field's keys**: `Escape` closes the band, `Backspace` on an empty field closes it (the
  projector's own rule), `Enter` takes the suggestion, `↑`/`↓` cycle results; the field holds the
  focus throughout, and closing puts the focus back on the dock's panel.
- **The suggestion**: the same 372 × 34 box, 13.5 px/400, so the pair reads as one control; the
  count sits inside it at the right, 11 px/650 `--head-ink` (`1 / 1`). A row **holding a match**
  wears the selected tint (`--sidebar-selected-bg`, measured `rgb(57, 63, 79)` dark, with its border)
  so a match and an empty query never look alike; no match, no query, loading and failure keep the
  plain box and turn the text italic `--head-ink` (`Start typing to find a match`, `No matching
  passage or song`, `Loading search…`, `Could not load — try again`).
- **The Go To block**: the go to is drawn as the list's live block, not a banner — a 43 px header
  spanning the dock (400 × 43) whose emphasis is **colour, not type** (the owner's preference): the
  bar is filled with the app's own selected tint, `--sidebar-selected-bg` (measured `rgb(57, 63, 79)`
  dark, `#B9D7C9` light), the colour its live row already wears, while the label stays 13 px/400 in
  the ink — text width 167.6 px for `NKB 43 Sinar Matahari Pagi`. The block's current row keeps the
  lighter `color-mix(… 55%, transparent)` tint, so the header reads stronger than the row it is on.
  The pinned header's 4 px shadow takes the same tint, so nothing rail-coloured shows above it. A
  longer title is truncated with an ellipsis (the label's box is 311.7 px at 400, 231.7 at 320,
  431.7 at 520 — the current title fits all three). Beside it, a bordered `Back` control 50.3 × 28,
  11 px/650 that **keeps its own fill** — `--rail-bg` (`rgb(35, 32, 25)` dark, `rgb(237, 234, 227)`
  light) with a `--divider` border — rather than taking the header's tint, so it still reads as a
  control on the bar; its hover stays opaque (92 % rail + ink). It carries no `On screen` pill. The header is sticky at the
  list's top (`top: -4px`, `--rail-bg` behind it) and pins there while the block's own rows scroll
  under it (measured 65.1 px from the frame's top while scrolled).
- **Its rows**: the dock's own row vocabulary, **full-bleed** — the row's box starts at the list's
  8 px padding and its text at 18 px, which is the column a service entry's number occupies, where a
  service entry's own label sits at 61.6 and its inner rows at 62. That left alignment is the
  distinction the header does not carry. The rows are `Bait N` heads and the lyric screens for a song
  (8 rows for `NKB 43`, each 28.8 px, the built-in rest an italic `Rest`), one numbered row per verse
  for a passage (48 for `Matius 5`, the number riding inside the line as a service verse does). The
  row that is on air carries the same `aria-current` tint a live screen row carries; a row is a
  button and jumps the go to there. The block is 384 × 502.8 for the song and fills the list: while a
  go to is up the service's own rows are not drawn, so the list holds one thing. Back restores them,
  still on the service's own screen.
- **The head while a go to is up**: the find and display controls stay usable; the switch-service
  control is disabled — `opacity: .45`, default cursor, no hover fill — so the head keeps its 65.1 px
  height and the exit is still visible. It returns with Back.
- **While a go to is up**: no entry row carries `aria-current`; the service's own entry stays
  expanded (the place Back will land on) but unhighlighted; the transport shows the go to's baits
  (34 px chips) or its edition chip (39.3 × 34), with the arrows 40 × 40 disabled at its ends; the
  display control reads `Hide words` / `Show words` rather than naming the service. **The bar itself
  is the service's own**: one 40 px flex line with its chips and arrows vertically centred (measured
  a shared 820 px centre line) and nothing clipped — the go to changes what the controls act on,
  never the bar's layout.
- **States reachable by hand**: service at rest · find with a suggestion (layer up) · no match · index loading ·
  content failed · song on air (baits) · passage on air (edition chip) · words hidden · light · 320 ·
  400 · 520.
- **Motion**: opening and closing is **one 200 ms height morph** on `--ease-timing` — the transport
  row (40 px) collapses while the find band (76 px) grows in the same place, so the list gives up or
  takes back the 36 px difference on that single curve and nothing jumps (measured mid-flight at
  55 ms: transport 16.1 px, band 45.5 px; settled 0 / 76). The layer fades over 160 ms alongside it.
  Reduced motion gets a cut on both. The block itself appears with the list's own step, and the
  header pins as the rows scroll.
- **A second page** — `sync.html` — shows the three surfaces together: the dock, a projector stage
  and the caption overlay, each the product's own markup and stylesheet, following **one** display
  state through nine steps (service on air → `G` → song → step → passage → `T` → `Space` → `Back` →
  `Space`), with the state object printed beside them and each surface's own report of what it
  painted. It is a review surface, not a product screen.
- **Not shown**: the projector's and the overlay's *look* does not change — only what they paint (a
  passage card, a lyric caption, by their own rules); and every fetch, which a static page cannot
  run.

## Assumptions

- The find band replaces the transport row in place rather than opening a third view or a sheet;
  the dock's own vocabulary is a band and a list, and a view change is what the owner asked the dock
  to avoid. It grows the band by the suggestion's 38 px, so the list gives up that height while the
  band is open.
- The overlay follows a Go To, because the stream shows the room the same words.
- `on` stays one flag: hiding during a goto blanks the goto, and a return keeps the words hidden.
- A goto from an idle dock adopts the browsed service at its first screen underneath it.
- The service's edition survives a goto untouched, and a return restores it.
- The goto's stepping units are the projector's: screens for a song, verses for a passage, Shift for
  baits, Ctrl for books and chapters.
- The dock loads `static/web/projector-library.js` for the lookup rather than growing a second one.
- A goto is not a service: the picker gains no entry and the board of services does not list it.

## Clarifications

### Session 2026-11-03

- Q: While a Go To is on air, what should the dock's arrows and transport do — step the go to, the
  service underneath it, or both on different modifiers? → A: **step the Go To**; arrows, bait chips
  and Back act on what is on air, and the service waits behind it until Back. (FR-015)
- Q: Is a Go To allowed before anything is on air? → SKIPPED, assumed: **yes** — the browsed service
  is adopted at its first screen underneath it, so Back always has a place; the alternative was
  refusing the act until the service is displaying, which would make an unplanned opening song
  impossible. (FR-016)
