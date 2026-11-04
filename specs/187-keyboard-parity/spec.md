# Feature Specification: one keyboard grammar for the dock and the projector

**Slice**: `specs/187-keyboard-parity`
**Branch**: `feat/187-keyboard-parity`
**Created**: 2026-11-04
**Status**: Accepted — gate 1 2026-11-05
**Input**: the owner's list, as written: *"on the dock, run view -> back to the picer requires the same
hold of esc key as to leave fullscreen"* · *"on the dock, g also available on the picker"* · *"on the
dock, match the goto's shift+arrow, ctrl+arrow, ctrl/shift Home/End to match to be the same as in
project[or]"* · *"add k to the dock"* · *"on the picker list, only up and down arrow keys are available
to navigate the service"* · *"also add the same guard while a go to fetch is in flight"* · *"make
metakey also work in projector"* · *"make the dock's Home/End to match the projector's"* · *"merge the
Display, Find, and Fullscreen in projector into one group: Display. and rename the While Finding to
Find. also do the same for the dock's"* · *"merge the Audio and Video on the projector's and move it
and \"Image and PDF\" to the left column"* · *"when the dock page regain focus while goto panel is open, it
should focus on the goto search field automatically"*. The one question it left open — what sits under a
go to started from the picker — was answered: *"choosing a result puts the go to on air alone, with no
service underneath"*.

## What the two surfaces do today

The dock (`static/web/obs-dock.js`) and the projector (`static/web/projector.js`) already share the
arrow grammar: plain arrows step screens, `Shift` steps baits, `Ctrl` steps entries. They part company
at `Home`/`End` — the projector takes the ends of the unit on show, the bait in a song and the entry
otherwise; the dock takes the ends of the whole service — and everywhere else.

- **`Home`/`End` disagree on scope** (`obs-dock.js:1258-1283` against `projector.js:763-782`): the
  projector's plain chord lands on the ends of the unit on show — the live bait in a song, the live
  entry otherwise — while the dock's lands on the first or last screen of the entire service; and
  `Shift+Home`/`End` on an entry with no baits falls through to the service's ends in the dock, where
  the projector moves nothing.
- **The dock parks the keyboard on the panel** (`obs-dock.js:1341-1351`): every pointerdown inside it,
  and any focus that lands outside it, is pulled back to `#dockPanel`. The find band's field lives
  inside that panel, so a window that regains focus lands on the panel and a keystroke goes nowhere;
  the field only holds the keyboard from the moment the band opens until something pulls it away.
- **The dock has no `K`.** Its key table exists only as a comment at the top of `obs-dock.js:14-25`;
  nothing in the panel lists it. The projector's `K` opens a sheet (`projector_controls.html:52-134`).
- **`Esc` in the dock's runner returns to the picker on the tap** (`obs-dock.js:1295-1298`). The
  projector's fullscreen needs a hold (`projector.js:1717-1724`), so the same key means two
  different gestures on two surfaces.
- **The dock's `G` is refused on the picker** (`obs-dock.js:1319-1321`) and its state module refuses a
  go to with no service (`display.js:182-188`), because spec 185 pinned a go to as something over a
  service (`docs/spec/display-state.md` R2, `docs/spec/dock.md` R1).
- **The dock's go to steps by verse or screen only** (`obs-dock.js:985-1002`): `Shift` picks a bait,
  but a chapter or a book is unreachable from the dock, while the projector crosses both
  (`projector.js:1450-1499`, `projector-library.js:322-360`).
- **The picker moves on six keys** — `←`/`→` and `PgUp`/`PgDn` move its cursor as `↑`/`↓` do
  (`obs-dock.js:1302-1311`).
- **The dock has no fetch guard**: a go to's chapter or song is fetched with every key and click still
  live (`obs-dock.js:960-1002`), where the projector swallows every input while its fetch runs
  (`projector.js:1207-1215`).
- **The projector reads `Ctrl` only** — `metaKey` makes its handler return (`projector.js:1629`), so
  `⌘` does nothing there while the dock treats `⌘` as `Ctrl` (`obs-dock.js:1289`).
- **The overlay paints a go to only while a service is on air** (`obs-overlay.js:350-351`), so a go to
  with no service underneath would paint nowhere.

## The keyboard, after this slice

One table, two surfaces:

| Chord | Dock (runner) | Projector |
| --- | --- | --- |
| `→` `↓` `PgDn` / `←` `↑` `PgUp` | next / previous screen | next / previous screen |
| `Shift` + those | next / previous bait | next / previous bait |
| `Ctrl` **or `⌘`** + those | next / previous entry | next / previous entry |
| `Home` / `End` | first / last screen of the **unit on show** — the live bait in a song, the live entry otherwise; `⇧` the live entry's first / last bait; `Ctrl`/`⌘` the service's first / last entry | same |
| In a go to, `Home` / `End` | the go to's own unit: first / last verse (passage) or the live bait's first / last screen (song) | same |
| In a go to, `Shift` + arrows | next / previous chapter (passage) or bait (song) | same |
| In a go to, `Ctrl`/`⌘` + arrows | next / previous book (passage) | same |
| In a go to, `Shift` + `Home`/`End` | first / last chapter or bait | same |
| In a go to, `Ctrl`/`⌘` + `Home`/`End` | first / last book | same |
| `Space` | display / hide the words | play/pause a recording, else the words |
| `T` | flip TB / SIM | flip TB / SIM, or fit width / height on media |
| `G` | Go To — on the runner **and the picker** | Go To |
| `K` | the dock's shortcut sheet | the projector's shortcut sheet |
| `Esc` | a **900 ms hold** returns to the picker; a tap does nothing | close a layer, leave a Go To; a held `Esc` leaves fullscreen |
| While finding | `↑` `↓` cycle · `Enter` opens · `Esc` / `Backspace` (empty) closes | same |
| Picker | `↑` `↓` move · `Enter` opens · `G` a go to | n/a — no picker |

## User Scenarios & Testing

### US1 — A held `Esc` returns to the picker, and a tap does not (P1)

**Why this priority**: the runner is the surface that runs a service; a stray tap of `Esc` must not
cost the operator the service he is in the middle of.

**Independent Test**: open a service in the dock's runner, tap `Esc` (under 900 ms) — nothing happens;
hold it for 900 ms — the picker shows and the service stays where it was on air.

**Acceptance scenarios**

1. **Given** the dock's runner **When** `Esc` is pressed and released before 900 ms **Then** the
   runner stays, nothing moves, and no state is written.
2. **Given** the dock's runner **When** `Esc` is held for 900 ms **Then** the picker shows in the
   runner's place, and the service that was on air is still on air at its screen.
3. **Given** the dock's picker **When** `Esc` is held or tapped **Then** nothing happens.
4. **Given** the find band open over either view **When** `Esc` is pressed **Then** the band closes on
   the tap, and holding it does nothing more.
5. **Given** the shortcut sheet open **When** `Esc` is pressed **Then** the sheet closes on the tap.

### US2 — `G` works on the picker, and a go to can stand alone (P1)

**Why this priority**: the dock usually sits on the picker; an unplanned song must not require opening
a service first, and the owner chose that it stand alone rather than adopt one.

**Independent Test**: with the dock on the picker and nothing on air, press `G`, type `NKB 43`, press
`Enter` — the song is on air on the projector and the overlay, the stored state names no service, the
dock shows the go to's own block, and `Back` leaves every surface idle and returns the dock to the
picker.

**Acceptance scenarios**

1. **Given** the dock's picker **When** `G` is pressed **Then** the find band opens over the picker,
   the field holds the focus, and the index is read once.
2. **Given** the band open over the picker **When** a result is chosen **Then** it goes on air at its
   first screen or verse with **no service underneath**: the stored state has `service: null` and the
   go to, the projector and the overlay paint the go to, and the dock shows its runner holding the go
   to block alone.
3. **Given** a go to on air with no service **When** `Back` is pressed **Then** the go to ends, every
   surface is idle, and the dock returns to the picker.
4. **Given** a service already on air **When** a go to is chosen from either view **Then** it goes over
   that service exactly as today, and `Back` returns to the service's screen and edition.
5. **Given** the picker with no service chosen **When** `Enter` is pressed on a go to result **Then**
   the dock never adopts the marked service: no `show` is written for it.

### US3 — The dock's go to steps like the projector's (P1)

**Why this priority**: the operator's hands should not have to learn a second grammar mid-service.

**Independent Test**: put `Matius 5:3` on air from the dock's runner, step with `Shift+→` to chapter 6,
`Ctrl+→` to the next book, `Shift+End` to the last chapter, `Ctrl+Home` to the first book — each lands
where the projector's own keys land, and each crossing fetches its chapter once.

**Acceptance scenarios**

1. **Given** a passage go to **When** `Shift+→` / `Shift+←` is pressed **Then** the go to moves to the
   next / previous chapter and its first verse, fetching that chapter once.
2. **Given** a passage go to **When** `Ctrl+→` / `⌘+→` / `Ctrl+←` is pressed **Then** the go to moves
   to the next / previous book's first chapter, fetching it once.
3. **Given** a passage go to **When** `Shift+Home` / `Shift+End` is pressed **Then** the go to is on
   the first / last chapter of its book.
4. **Given** a passage go to **When** `Ctrl+Home` / `Ctrl+End` is pressed **Then** the go to is on the
   first / last book's first chapter.
5. **Given** a song go to **When** `Shift+Home` / `Shift+End` is pressed **Then** the go to is on its
   first / last bait.
6. **Given** a go to **When** a plain `Home` / `End` is pressed **Then** it is on the first / last verse
   of the loaded chapter, or the first / last screen of the song.
7. **Given** the projector and the dock on the same go to **When** the same chord is pressed on either
   **Then** both surfaces land on the same place.

### US4 — The picker moves on `↑` and `↓` only (P2)

**Why this priority**: four extra keys on a vertical list were a second way to do one thing; the owner
wants one.

**Independent Test**: on the picker, `←`, `→`, `PgUp`, `PgDn` move nothing; `↑` and `↓` move the mark
one row and clamp at the ends.

**Acceptance scenarios**

1. **Given** the picker **When** `←` / `→` / `PgUp` / `PgDn` is pressed **Then** the mark does not move,
   nothing opens and no state is written.
2. **Given** the picker **When** `↑` / `↓` is pressed **Then** the mark moves one row and stops at the
   first and last row.

### US5 — `K` shows the dock's own shortcuts (P2)

**Why this priority**: the dock's table is invisible today; the projector's has a sheet, and the dock
should match.

**Independent Test**: press `K` on the runner and on the picker — a sheet listing the dock's keys opens
over the dock; `K` again, `Esc`, its close control, or a click on the frame round the panel closes it.

**Acceptance scenarios**

1. **Given** either view **When** `K` is pressed **Then** the shortcut sheet opens over the dock as a
   layer, and the controls behind it do not act.
2. **Given** the sheet open **When** `K` is pressed again, or `Esc`, or its close control, or the
   8 px frame round the panel is clicked **Then** it closes, the transport returns, and the dock is
   where it was.
3. **Given** the sheet open **When** any other key is pressed **Then** the dock does not act on it.
4. **Given** the sheet **Then** it lists the dock's own keys in five groups — the service's screens, a
   song, a passage and a go to, the display, and the find — with `Esc`'s hold named; **while the picker
   is showing** it adds a sixth group above them, the picker's own two keys (`↑` / `↓`, `Enter`), and on
   the runner those two are not listed.

### US6 — No input changes what is on air while a go to is fetching (P2)

**Why this priority**: a chapter crossing takes a round trip; the keys pressed during it act on the
chapter that is leaving, which is how a go to lands somewhere the operator did not ask for.

**Independent Test**: choose a verse in another chapter and, while its fetch is in flight, press ten
arrows and click the transport three times — the go to's position when it paints is the one the chord
asked for, and nothing else moved.

**Acceptance scenarios**

1. **Given** a go to fetch in flight **When** any key is pressed **Then** nothing on air changes, and
   the block's header reads `Loading…`.
2. **Given** a go to fetch in flight **When** the transport, a row, the display control or `Back` is
   clicked **Then** nothing on air changes.
3. **Given** the fetch settles or fails **When** the next key is pressed **Then** the keys act again;
   a failure leaves what was on air in place and says so.
4. **Given** the band is closed and the fetch is still running **Then** the guard holds until it ends.

### US7 — `⌘` is a modifier on the projector too (P2)

**Why this priority**: a Mac's keyboard says `⌘`, the projector's sheet draws `⌘`, and the projector
ignores it.

**Independent Test**: on the projector, `⌘+→` lands where `Ctrl+→` lands, and `⌘+T` flips nothing.

**Acceptance scenarios**

1. **Given** the projector on any screen **When** `⌘+→` / `⌘+←` is pressed **Then** it moves an entry,
   exactly as `Ctrl+→` / `Ctrl+←` does.
2. **Given** the projector **When** `⌘+Home` / `⌘+End` is pressed **Then** it takes the first / last
   entry.
3. **Given** the projector **When** `⌘+T`, `⌘+C` or `⌘+Space` is pressed **Then** no projector action
   fires and the browser keeps its own shortcut.

### US8 — Home and End act on the unit on show, as the projector's do (P2)

**Why this priority**: the same chord must mean the same thing on both surfaces; today `Home` in the
dock throws the operator to the first screen of the whole service, where the projector takes him to
the start of the entry — or the bait — he is in.

**Independent Test**: in a text entry of the service, press `End` with the dock's runner focused — the
live row is that entry's last screen, not the service's; step into a song's second bait and press
`Home` — the live row is that bait's first screen.

**Acceptance scenarios**

1. **Given** the runner with a text entry on air **When** `Home` / `End` is pressed **Then** the live
   row is that entry's first / last screen, and the service's first and last screens are untouched
   chords.
2. **Given** the runner with a song's bait on air **When** `Home` / `End` is pressed **Then** the live
   row is that bait's first / last screen.
3. **Given** the runner with a text entry on air **When** `Shift+Home` / `Shift+End` is pressed
   **Then** nothing moves — there is no bait to take — and in a song the same chord takes the entry's
   first / last bait.
4. **Given** any entry **When** `Ctrl`/`⌘+Home` / `End` is pressed **Then** the live row is the
   service's first / last entry.
5. **Given** a go to on air **When** any of these chords is pressed **Then** the go to's own levels
   apply (US3), not the service's.

### US9 — One Display group and one Find group on both sheets (P2)

**Why this priority**: the projector's last column splits four ways — Display, Find, While Finding,
Fullscreen — for acts that all belong to what is on screen, and the dock inherited a single merged
"Display and find" from it. One grouping for both sheets.

**Independent Test**: open the projector's sheet with `K` — one `Display` group carrying the words,
corner, shortcuts, the two find openers and the fullscreen pair, and one `Find` group; open the dock's
with `K` — the same two headings, holding the dock's rows.

**Acceptance scenarios**

1. **Given** the projector's sheet **Then** it carries exactly one `Display` group and one `Find`
   group, and no group named *While Finding* or *Fullscreen*.
2. **Given** the projector's `Display` group **Then** its rows read Show or Hide Words, Show or Hide
   Corner, Keyboard Shortcuts, Find in Service, Passage or Song, Enter or Leave, Hold to Leave — the
   present order, the rows only re-parented.
3. **Given** the dock's sheet on the runner **Then** `Display` carries Show or Hide Words, Keyboard
   Shortcuts, Passage or Song, Back to Services (hold), and `Find` carries Previous Match, Next Match,
   Open Match, Close When Empty, Close Find.
4. **Given** either sheet **Then** no label or chord changed, and no row was added or dropped by the
   merge.

### US10 — The media groups sit with the service, and Audio and Video is one group (P2)

**Why this priority**: the middle column carries five groups while the left carries three, and the
media keys act on the service's own screens; one row (`Play/Pause` on `Space`) cannot need two
headings.

**Independent Test**: open the projector's sheet — the left column ends with `Image and PDF` and
`Audio and Video`; the middle carries `Library passage` and `Library Detour` only.

**Acceptance scenarios**

1. **Given** the projector's sheet **Then** its left column reads Service, Song, Passage, Image and
   PDF, Audio and Video.
2. **Given** the middle column **Then** it carries Library passage and Library Detour, and no media
   group.
3. **Given** the `Audio and Video` group **Then** it holds one `Play/Pause` row on `Space`, not two.
4. **Given** a 1080p window **Then** the sheet measures its tallest column (835.5 px against today's
   677) with no row clipped; at 720p it scrolls internally and no row is lost.
5. **Given** either sheet **Then** no label or chord changed, and the merge removed one heading and
   one row.

### US11 — The find band keeps the keyboard (P2)

**Why this priority**: the field lives inside the panel that parks the keyboard, so switching windows
and coming back leaves the band open with the caret nowhere — the operator's next keystrokes are lost.

**Independent Test**: open `G`, let the window lose focus, bring it back — the field holds the caret and
typing appends; close the band — the panel holds it again.

**Acceptance scenarios**

1. **Given** the find band open with the index ready **When** the window regains focus **Then** the field
   holds the caret and the next keystroke appends to the query.
2. **Given** the find band open while the index is still loading **When** the index arrives **Then** the
   field takes the focus and the caret, without a click.
3. **Given** the find band open **When** the dock takes a pointerdown, or focus lands outside the panel
   **Then** the focus lands in the field, not on the panel.
4. **Given** the band open with a query typed and a match chosen **When** the window regains focus
   **Then** the query, the chosen match and the list's scroll are unchanged — only the caret returns.
5. **Given** the band closing — `Esc`, the scrim, `Backspace` on an empty field **Then** the panel holds
   the focus and the dock's keys act again.

### Edge Cases

- **When** `Esc` is held in the runner while the find band is open **Then** the band closes on the
  keydown and the hold does nothing further.
- **When** `Esc` is held in the runner while the shortcut sheet or the service list is open **Then**
  the layer closes on the tap and the runner stays.
- **When** `Esc` is held while a go to is on air **Then** the view still returns to the picker; the go
  to stays on air.
- **When** the go to is service-less and `Space` is pressed **Then** the words blank and the go to
  keeps its place; a second `Space` brings them back.
- **When** the go to is service-less and a service screen goes on air from any writer **Then** the go
  to ends and the service paints.
- **When** the go to is service-less and the browser session ends **Then** every surface is idle and
  the dock returns to the picker.
- **When** a chapter or book step is asked for and the chapter fetch fails **Then** the go to keeps
  the place it had and says the content could not be loaded.
- **When** a chapter step is asked for at the first or last book **Then** the go to clamps to that book
  and stays, as the projector's own step does.
- **When** the go to is a song and `Ctrl+→` is pressed **Then** nothing happens (there is no book in a
  song), as on the projector.
- **When** `K` is pressed while the find band is open **Then** nothing happens: the band owns the keys.
- **When** the sheet is open and the pointer clicks a control behind it **Then** the click lands on the
  sheet's frame, the sheet closes and the control does not act.
- **When** the picker is empty **Then** `↑`, `↓`, `Enter` and `G` do nothing.
- **When** `⌘` is held with a plain key on the projector **Then** no plain action fires, even where
  `Ctrl` would have made the key inert instead.
- **When** `Home` / `End` is pressed with the live screen between two entries **Then** nothing moves,
  as on the projector, where no entry is found at that screen.
- **When** an entry ends on a blank rest **Then** `End` lands on its last screen with words, not on
  the rest.
- **When** the window regains focus while the shortcut sheet is open **Then** the panel holds the
  focus, as it does today: the sheet has no field to give it to.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | On the dock's runner, `Esc` SHALL return to the picker only when held for 900 ms; a press released before it SHALL do nothing, and a hold SHALL be cancelled by the key's release, the window losing focus, or a layer opening. `Esc` SHALL keep closing the find band, the shortcut sheet and the service list on the tap. | `dock/R5` (new) |
| FR-002 | The dock's `G` SHALL open the Go To band on the picker as well as on the runner, with the same layer, field, lookup and keys; the find control in the runner's head SHALL keep its present behaviour. | `dock/R1` (modified) |
| FR-003 | A go to SHALL be put on air with no service underneath: `goTo` SHALL accept it, `stepGoto`, `hide`, `resume` and `flip` SHALL act on it, `back` SHALL end it leaving the display idle (`service: null, on: false`), and `show` SHALL end it as it ends any go to. The state SHALL keep carrying no verse text, title or lyric, and SHALL be stamped with the browser session. | `display-state/R2` (modified) |
| FR-004 | Choosing a result from a band opened on the picker SHALL NOT adopt a service: the go to is written over `service: null`, the dock SHALL show its runner holding the go to block alone, and `Back` SHALL end the go to and return the dock to the picker. Choosing from a band opened on the runner SHALL keep adopting the browsed service underneath, as today. | `dock/R3` (modified) |
| FR-005 | In a go to, the dock's keys SHALL be the projector's: plain arrows step the verse or screen, `Shift` steps a chapter (passage) or a bait (song), `Ctrl`/`⌘` steps a book, `Home`/`End` take the first or last verse (passage) or the live bait's first or last screen (song), `Shift+Home`/`End` the first or last chapter or bait, and `Ctrl`/`⌘+Home`/`End` the first or last book. A chapter or book step SHALL fetch exactly the chapter it enters and paint it; a verse step inside the loaded chapter SHALL make no request. | `dock/R3` (modified) |
| FR-006 | On the picker, only `↑` and `↓` SHALL move the mark; `Enter` SHALL open the marked service and `G` SHALL open the Go To band. `←`, `→`, `PgUp` and `PgDn` SHALL do nothing there. | `dock/R6` (new) |
| FR-007 | `K` SHALL open a shortcut sheet over the dock on either view; `K` again, `Esc`, its close control, or a click on the 8 px frame around the panel SHALL close it; the sheet SHALL be a layer — no control behind it acts, and no other key acts — and the band and the sheet SHALL never be open together. | `dock/R7` (new) |
| FR-008 | The dock's shortcut sheet SHALL list the dock's own keys in **five groups** — the service's screens, a song, a passage and a go to, the display, and the find — and SHALL name `Esc`'s hold rather than a tap. It SHALL add the **picker's own keys** — `↑` / `↓` and `Enter` — as a sixth group only while the picker is the view on show, and SHALL not list them on the runner. Every row SHALL wear the **projector's own wording, verbatim**, and stand in the **projector's own order** within its group, wherever the projector has the same shortcut (`Next`, `Previous`, `First`, `Last`, `Next Entry`, `Next Bait`, `First Chapter`, `Show or Hide Words`, `Keyboard Shortcuts`, …); only the rows the projector does not have (`Move the Pick`, `Open the Service`, `Back to Services (hold)`) SHALL be worded for the dock. | `dock/R7` (new) |
| FR-009 | While a go to's content is being fetched or a chapter or book step is in flight, the dock SHALL refuse every key and every pointer action that would change what is on air, and the block's header SHALL read `Loading…` until the fetch settles; the guard SHALL end when it paints or fails. | `dock/R8` (new) |
| FR-010 | On the projector, `Ctrl` and `⌘` SHALL be the same modifier for the arrow and `Home`/`End` chords; `⌘` with any other key SHALL leave the projector inert so the browser keeps its own shortcut. | `projector/R13` (new) |
| FR-011 | The projector and the overlay SHALL paint a go to that names no service, exactly as they paint one that does, and a `back` from it SHALL leave both idle. | `projector/R1` (modified), `overlay/R1` (modified) |
| FR-012 | On the dock's runner with no go to up, `Home` / `End` SHALL act on the **unit on show**, as the projector's plain chord does: the first or last screen of the live **bait** when the live entry is a song, otherwise of the live **entry** — never the first or last screen of the service. `Shift+Home`/`End` SHALL take the live entry's first or last bait and move nothing on an entry with none, and `Ctrl`/`⌘+Home`/`End` SHALL take the service's first or last entry. With the live screen between entries, `Home` and `End` SHALL move nothing. The arithmetic SHALL be the projector's own `unitBoundary`, so the two surfaces land on the same screen for the same chord. | `dock/R9` (new) |
| FR-013 | The projector's shortcut sheet SHALL carry **one `Display` group**, merging today's Display, Find and Fullscreen groups — `Show or Hide Words`, `Show or Hide Corner`, `Keyboard Shortcuts`, `Find in Service`, `Passage or Song`, `Enter or Leave`, `Hold to Leave` — and **one `Find` group**, today's *While Finding* — ordered `Previous Match`, `Next Match`, `Open Match`, `Close When Empty`, `Close Find`. The Display rows SHALL keep their present order. The regrouping SHALL remove two headings and no row, SHALL NOT change any label or chord, and SHALL NOT clip a row at 720p. The dock's sheet SHALL carry the same two groups, holding the rows the dock has. | `projector/R12` (modified), `dock/R7` (modified) |
| FR-014 | The projector's sheet SHALL carry **one `Audio and Video` group** in place of today's `Audio` and `Video` groups, holding `Play/Pause` on `Space` once; that group and `Image and PDF` SHALL sit at the end of the sheet's **left** column, after `Passage`, and the middle column SHALL carry `Library passage` and `Library Detour` only. No label or chord SHALL change, and the merge SHALL remove one heading and one row. The sheet's frame SHALL keep following its tallest column, which makes it **835.5 px at 1080p** where it is 677 today; at 720p the sheet SHALL scroll internally rather than clip a row. | `projector/R9` (modified), `projector/R12` (modified) |
| FR-015 | While the find band is open, the dock SHALL keep the keyboard in its field: the field SHALL take the focus as soon as it is usable — at open when the index is ready, and the moment the index arrives when it is not; a window that regains focus, a pointerdown in the dock, and any focus landing outside the panel SHALL each leave the focus in the field rather than on the panel; and closing the band SHALL return the focus to the panel. A refocus SHALL NOT change the query, the chosen match or the list's scroll. | `dock/R10` (new) |

### Key Entities

- **Go to** — what is on air instead of a service: a song with its screen index or a passage with its
  book, chapter, verse and shown edition. It may now stand alone, with `service: null` beside it, and
  then its own end is the display's idle state.
- **Dock's shortcut sheet** — the panel layer that lists the dock's keys by group, opened by `K`.
- **Hold** — a key gesture that acts only after 900 ms held, cancelled by release or blur.
- **Unit** — what a plain `Home` / `End` acts on: the live **bait** when the live entry is a song, the
  live **entry** otherwise. It is never the whole service; `Ctrl`/`⌘` is the chord that reaches that.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A 300 ms `Esc` tap in the runner moves nothing; a 1000 ms hold shows the picker. | E2E: dispatch keydown, wait, keyup; read the view. |
| SC-002 | A go to chosen from the picker writes `service: null` and its goto: no `show` is written, and the stored state's `service` is null. | E2E: read `localStorage['gkps-display']`. |
| SC-003 | From `Matius 5:3`, `Shift+→` makes exactly 1 request, `Ctrl+→` exactly 1, a plain step in the loaded chapter 0. | E2E counting `/projector/goto/chapter/` requests. |
| SC-004 | The dock and the projector land on the same go to place for the same chord: 6 chords compared on both surfaces. | E2E walk comparing both readouts. |
| SC-005 | On the picker, `←`, `→`, `PgUp`, `PgDn` produce 0 row moves; `↑`/`↓` move 1 and clamp. | E2E reading the marked row's index. |
| SC-006 | `K` opens a sheet with the dock's rows on both views; `Esc` closes it; a click aimed at a control behind the sheet lands on its frame and never acts on the control. | E2E: count rows, click through, read the view. |
| SC-007 | During a chapter fetch, 10 key presses and 3 transport clicks change nothing: after the fetch the go to is where the chord asked. | E2E with a delayed route. |
| SC-008 | On the projector, `⌘+→` lands where `Ctrl+→` lands, and `⌘+T` flips nothing. | E2E on the projector page. |
| SC-009 | With `service: null` and a goto, the overlay's stage carries the plate and the projector paints the detour; after `Back` both paint nothing. | E2E reading both surfaces. |
| SC-010 | `Home` / `End` in a text entry and in a song's bait land on that unit's first / last screen — the service's ends are never reached by the plain chord; `Shift+Home` on a text entry moves 0 rows. | E2E reading the live row's index against the service's own ends. |
| SC-011 | The projector's sheet carries one `Audio and Video` group with a single `Play/Pause` row, sits it and `Image and PDF` at the end of the left column, leaves the middle with Library passage and Library Detour, and measures 835.5 px at 1080p. | E2E: read the three columns' headings in order and the sheet's box. |
| SC-012 | With the band open, a window blur and refocus leaves `document.activeElement` on `#findInput`, and typing `NKB 4` appends to the query; after `Esc` it is on `#dockPanel`. | E2E: blur/refocus the window, read `activeElement`, type, close. |

## UI/UX

`static preview at specs/187-keyboard-parity/preview/index.html` — the dock's own panel, drawn from
the product's template, stylesheet and captured data, at 320 / 400 / 520, dark and light. The probe
(`preview/probe.py`) prints exactly these numbers at 400 × 800, dark.

- **The go-to-only runner**: the head keeps its 65.1 px and its three 38 px controls; its title line
  reads `Go To` and the date line is `display: none`, so the head names the mode and the block below
  names the go to. The block starts at y 65.1 exactly as it does over a service — same 400 × 43
  header, same full-bleed rows — and the switch-service control is **not** disabled (there is no
  service to lose; it returns to the picker). The list holds the block alone.
- **The sheet**: a rail panel **384 × 784 at (8, 8)** — the dock inset 8 px — with a 1 px `--divider`
  border, a 12 px radius and `rgba(0, 0, 0, .34) 0 18px 40px` beneath it. Its head is 49 px tall: the
  title `KEYBOARD` at 10.5 px/650, letter-spacing .08em, `--head-ink`, and a 30 × 30 close control
  (8 px radius) whose right edge is flush with the keycap column at x 377.
- **Its rows**: a scrolling body 382 × 733 at (9, 58), carrying **32 rows in five groups** on the
  runner — service, song, passage and go to, display, find — and **34 in six** on the picker, whose
  own two keys lead it: *Move the Pick* `↑` / `↓` and *Open the Service* `Enter`, drawn only while the
  picker is the view, so the runner's sheet never offers a key it does not have. **One row per
  direction**, as the projector's own sheet draws it: `next` and `previous`, `first` and `last` never
  share a row, and what sits beside a label is the set of keys that do the same thing (`→` or `↓` or
  `PgDn`). **Each shared row wears the projector's own label, verbatim, in the projector's own order
  within its group** — `Next`, `Previous`, `First`, `Last`, `Next Entry`, `Next Bait`, `First Chapter`,
  `Show or Hide Words`, `Keyboard Shortcuts` — so the two sheets read alike; only the three rows the
  projector has no counterpart for (*Move the Pick*, *Open the Service*, *Back to Services (hold)*) are
  the dock's own, and the last of them closes the sheet as the projector's `Hold to Leave` closes its
  own. A group's heading is 10 px/650 at letter-spacing .7 px in `--head-ink`, its first one at y 68
  and **16 px above the next**; a row is **354 × 30 px** with 10 px between its label and its chords
  and **4 px of air above and below the cap**; the label is 12.5 px/400 in the ink on one ellipsized
  line. The first row starts at y 80. The table is **1117 px** on the runner and **1206 px** on the
  picker. In an 800 px dock the body is 733 px, so the runner's sheet scrolls by 384 px and the
  picker's by 473; at 1000 px by 184 and 273; at **1200 px tall** the body is 1133 px, the runner's
  table fits and the picker's still scrolls 73. The scrollbar is the app's own (spec 087): a 5 px
  capsule in `--scroll-thumb`, `border-radius: 999px` on a transparent track, and the standard
  `scrollbar-width`/`scrollbar-color` gated behind `@supports not selector(::-webkit-scrollbar)` so
  Blink never paints the platform's thin bar (`800h` / `1000h` / `1200h` on the preview's bar).
  A **1 px hairline** in the ink at 12 % separates consecutive rows — the projector's own
  `.row + .row` rule — drawn as an inset shadow so it costs the table no height. At 320 px the
  narrowest rows wrap their chords under the label. No row overflows its box horizontally at 320, 400
  or 520.
- **A keycap**: the projector's own cap at the dock's scale — **22 px square**, word keys **44 px**
  (two units), the space bar **66 px** (three), a 4 px radius (its 5 scaled), a 1 px edge and the
  inset top highlight. The space bar carries the projector's own **`␣` open-box mark** (14 px,
  stretched **1.3×** wide) rather than the word `Space`, and the mark's box centres in the cap with
  4 px of air above and below. Letter caps are 11 px/400, word caps 10.5 px, glyphs 13 px with an
  11 px mark. The dark theme wears the projector's exact colours (`#2A2722` fill, `#4A463F` edge, its
  two shadows); the light theme derives the same relationship from the dock's tokens (`#D4D2CB` fill,
  an edge of the ink at 30 %).
- **What a chord means**: the keys inside one chord are pressed together; the word **`or`** (11 px/650
  in `--head-ink`, 4 px of space each side) separates keys that do the same thing and nothing else —
  `→ or ↓ or PgDn` are three ways to take the next screen — the projector's own separator. Because each
  row carries one direction, `or` never joins a direction to its opposite.
- **States reachable by hand**: the picker · the service at rest · the find band (match, no match,
  loading) · a song on air · a passage on air · words hidden · **a go to alone** · **a fetch in
  flight** · the sheet over the runner · the sheet over the picker · light · 320 · 400 · 520 · 800
  tall · 1000 tall · 1200 tall.
- **Motion**: the sheet rises 180 ms — `translateY(6px) scale(.99)` to none on `--ease-timing` —
  while its 8 px frame fades over 160 ms; reduced motion gets a cut on both. Opening it never moves
  the dock: it is a layer over the panel, not a view swap.
- **Not shown**: every fetch — the page answers the lookup from a captured index and paints captured
  payloads, so `NKB 43` and `Matius 5` carry content and any other result shows the product's own
  "could not load" row. The picker is the live dock's own section, captured whole, but its keys are
  not wired here; only the sheet's picker group reacts to the view. The projector's own sheet is not
  drawn: its regrouping (FR-013, US9) and its media columns (FR-014, US10) land in
  `projector_controls.html` with the implementation; this page draws the dock's half of the same
  grouping, and `projector-sheet/before.png` / `after.png` hold the living sheet's before and after.
  The band's refocus when the window regains focus is not drawn either: a page inside a frame cannot be
  trusted to report window focus, and SC-012 asserts it in the E2E instead.

## Assumptions

- The hold is 900 ms — the projector's own fullscreen hold (`projector.js:1717-1724`) — and a release
  before it cancels the gesture, which the projector's implementation does not do; the dock's rule is
  the gesture the owner asked for, not the projector's timer.
- A go to chosen from the picker takes the dock to its runner holding the go to block alone, because
  the block is where a go to is stepped and `Back` lives; the dock does not stay on the picker with a
  live go to and no control over it.
- In that state the runner's head reads `Go To` in its title line and hides the date line; the block
  below names the go to, so the head does not repeat it.
- The shortcut sheet is one scrolling column in the dock's own vocabulary, not the projector's
  three-column sheet: the dock is 320–520 px wide.
- `K` works on both views and lists both; the sheet is the dock's, not a copy of the projector's.
- The picker's `G` needs no service adopted, so a go to can now be the only thing on air.
- A chapter or book step loads `projector-library.js` on first use, as the find band already does.
- The projector's shortcut sheet keeps its look and rows; `⌘` is already the glyph it draws.
- The overlay paints a service-less go to because it is the room-facing surface and the owner's intent
  is that the words are on air; nothing else about the overlay changes.

## Clarifications

### Session 2026-11-04

- Q: Dock · `G` from the picker: when nothing is on air, what should sit underneath the chosen go to?
  → A: **nothing** — the band opens over the picker and choosing a result puts the go to on air alone,
  with no service underneath. (FR-003, FR-004)
