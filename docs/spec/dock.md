# dock

**capability**: `dock`
**last folded**: 2026-11-14
**slices**: `193-reading-project-button`, `187-keyboard-parity`, `185-dock-goto`

The OBS dock — the operator's surface for running a Tata Ibadah from inside OBS. Its earlier
behaviour (spec 119's runner and picker, spec 132's buckets, spec 164's fluid width) is recorded in
`reading.md` and in those slices; this file starts at the go to, which is the first behaviour folded
to a capability of the dock's own.

### R1 — A Go To starts from either view, and from the picker it stands alone

The dock SHALL offer a Go To on the runner — by `G` or by the control in its head — and on the
picker by `G`, with the same layer, field, lookup and keys. Choosing a result from the runner SHALL
put that song or passage on air at its first screen or verse, adopting the browsed service
underneath it when nothing is on air, so Back always has a place to return to. Choosing from the
picker SHALL NOT adopt a service: the go to SHALL be written with no service beside it, the dock
SHALL show its runner holding the go to's block alone, and `Back` SHALL end the go to, leave every
surface idle and return the dock to the picker. (specs 187, 185)

#### Scenario: the runner is open
- WHEN `G` is pressed, or the head's control is clicked
- THEN the find band opens over the dock with the field empty and holding the focus

#### Scenario: the picker is open
- WHEN `G` is pressed on the picker
- THEN the band opens over the picker, the field holds the focus and the index is read once

#### Scenario: a result is chosen on the picker
- WHEN a result is chosen with no service chosen
- THEN the go to goes on air with `service: null`, the runner shows the block alone, and the
  marked service is never adopted

#### Scenario: a go to that stands alone ends
- WHEN `Back` is pressed
- THEN the display is idle — no service, nothing on air — and the dock is on the picker

#### Scenario: nothing is on air on the runner
- WHEN a result is chosen from the runner's band with no display state
- THEN the browsed service is adopted at screen 0 and the go to is written over it

### R2 — The find band answers from the projector's own index, read once

The dock SHALL answer a query from the projector's lookup over `/projector/goto/index/`, held in page
memory: the same module, the same grammar and the same labels the projector uses. The index SHALL be
read once, at the first opening of the band — not with the dock page — and typing SHALL make no
request. A row holding a match SHALL wear the selected tint and show its `n / n` count; no query, no
match, loading and failure SHALL each say so plainly. Choosing a result SHALL fetch that chapter or
song once, and a step inside the loaded chapter SHALL make no request. (spec 185)

#### Scenario: the band opens
- WHEN the band is opened for the first time on a page
- THEN the index is fetched once, and the row says the search is loading until it arrives

#### Scenario: the operator types
- WHEN a reference, a book name, a bare number or a songbook reference is typed
- THEN the suggestion and the count change and no request is made

#### Scenario: nothing matches
- WHEN the query matches nothing
- THEN the row says there is no matching passage or song, and Enter does nothing

#### Scenario: the content cannot be loaded
- WHEN the chosen chapter or song request fails
- THEN what is on air does not change and the row says the content could not be loaded

### R3 — What is on air is the list's live block, and the transport acts on it

While a go to is on air the runner's list SHALL hold the go to and nothing else: a pinned header
naming it with `Back`, and beneath it the go to's own screens — a song's bait heads and lyric rows, a
passage's numbered verses — with the one on air marked and every row a jump. The service's own rows
SHALL NOT be drawn, and no row SHALL wear an `On screen` marker. A go to that names no service SHALL
be shown the same way, its head reading `Go To` with no date line, and the switch-service control
SHALL stay usable — there is no service to lose, and it returns to the picker.

The transport SHALL act on the go to, and so SHALL the keys, in the projector's own grammar: plain
arrows step the go to's screen or verse, `Shift` a bait or a chapter, `Ctrl`/`⌘` a book; a chapter or
book step SHALL fetch exactly the chapter it enters and a verse step inside the loaded chapter SHALL
make no request; a bait chip takes a bait, a flip the go to's edition. The service's own screen and
edition SHALL NOT change until Back, and `Back` SHALL restore them exactly as they stood. (specs 187,
185)

#### Scenario: a go to is on air
- WHEN the dock is looked at
- THEN the block names the go to and draws its screens, and the service's rows are gone

#### Scenario: the arrows are pressed
- WHEN an arrow, a bait chip or `T` is pressed while a go to is on air
- THEN the go to moves or flips, and the service's own place does not change

#### Scenario: a chapter is entered
- WHEN `Shift+→` crosses the last verse of the loaded chapter
- THEN exactly that chapter is fetched, nothing on air changes until it lands, and the go to lands on
  its first verse

#### Scenario: a go to stands alone
- WHEN the block is looked at with no service on air
- THEN the head reads `Go To`, the date line is not drawn, and the switch-service control is usable

#### Scenario: Back is pressed
- WHEN `Back` is pressed
- THEN the service's rows return, its screen and edition are what they were, and the block is gone

#### Scenario: a row is clicked
- WHEN a row of the block is clicked
- THEN the go to moves to that screen or verse and stays on air

### R4 — The find band is a layer, and the exit stays visible

While the find band is open the rest of the dock SHALL be covered by a layer in the product's
backdrop: every pointer over it SHALL close the band and do nothing else, no covered control SHALL
act, and the transport keys SHALL be inert. `Escape`, a click on the layer and `Backspace` on an
empty field SHALL each close it; closing SHALL put the transport back and leave the dock where it
was. The band SHALL cover whichever view is showing: opened from the picker, the footer that carries
it rides that view and folds away with the band.

While a go to is on air the switch-service control SHALL be disabled rather than hidden — the head
keeps its width and the exit stays visible — and SHALL return the moment the go to ends. (specs 187,
185)

#### Scenario: the layer is clicked
- WHEN any point of the layer is clicked
- THEN the band closes, nothing goes on air, and the transport is back in place

#### Scenario: the band opens on the picker
- WHEN `G` is pressed on the picker
- THEN the band covers the picker, the picker's list keeps its place behind it, and closing returns
  the list untouched

#### Scenario: a go to is on air
- WHEN the head is looked at
- THEN the switch-service control is drawn disabled, and no press of it changes the view

#### Scenario: the go to ends
- WHEN `Back` or a service screen ends the go to
- THEN the switch-service control is usable again

### R5 — `Esc` returns to the picker on a hold, not a tap

On the runner `Esc` SHALL return to the picker only when held for 900 ms. A press released earlier
SHALL do nothing, and a hold SHALL be cancelled by the key's release, by the window losing focus, by
the tab hiding, or by a layer opening. `Esc` SHALL keep closing the find band, the shortcut sheet and
the service list on the tap. (spec 187)

#### Scenario: the key is tapped
- WHEN `Esc` is pressed and released inside 900 ms
- THEN nothing moves; the runner stays the view and what is on air does not change

#### Scenario: the key is held
- WHEN `Esc` is held past 900 ms
- THEN the picker becomes the view and what is on air is untouched

#### Scenario: a layer is open
- WHEN `Esc` is pressed while the band or the sheet is up
- THEN that layer closes on the tap and the view does not change

### R6 — The picker moves on `↑` and `↓` only

On the picker `↑` and `↓` SHALL move the mark and clamp at either end; `Enter` SHALL open the marked
service and `G` SHALL open the Go To band. `←`, `→`, `PgUp` and `PgDn` SHALL do nothing there.
(spec 187)

#### Scenario: the pad is pressed
- WHEN the picker holds the keyboard and any of `←`, `→`, `PgUp`, `PgDn`, `Home`, `End` is pressed
- THEN the mark does not move

#### Scenario: the arrows are pressed
- WHEN `↓` is pressed past the last row, or `↑` past the first
- THEN the mark stops at the last, or the first, row

### R7 — `K` lists the dock's own keys

`K` SHALL open a shortcut sheet over the dock on either view, and `K` again, `Esc`, its close control
or a click on the 8 px frame around the panel SHALL close it. The sheet SHALL be a layer: no control
behind it acts, no other key acts, and it SHALL never be open beside the band.

The sheet SHALL list the dock's own keys in five groups — the service's screens, a song, the passage,
the display, and the find — one row per direction, with the projector's own wording verbatim and in
the projector's own order wherever the projector has the same shortcut. Only the rows the projector
does not have — `Move the Pick`, `Open the Service`, `Back to Services (hold)` — SHALL be worded for
the dock, and the last of them SHALL name `Esc`'s hold. The picker's own two keys SHALL lead the
sheet only while the picker is the view. (spec 187)

#### Scenario: the runner's sheet
- WHEN `K` is pressed on the runner
- THEN the sheet lists five groups and does not offer the picker's keys

#### Scenario: the picker's sheet
- WHEN `K` is pressed on the picker
- THEN the picker's own two rows lead the sheet, above the service's

#### Scenario: the frame is clicked
- WHEN the 8 px frame around the panel is clicked
- THEN the sheet closes and no control behind it acts

### R8 — A fetch in flight takes no input

While a go to's content is being fetched, or a chapter or book step is in flight, the dock SHALL
refuse every key and every pointer action that would change what is on air, and the block's header
SHALL read `Loading…` until the fetch settles. The guard SHALL end when the go to paints or the fetch
fails. (spec 187)

#### Scenario: a crossing is in flight
- WHEN keys and transport presses arrive while a chapter fetch is pending
- THEN nothing on air changes, and the chord that asked for the crossing lands where it asked once
  the fetch settles

### R9 — Home and End act on the unit on show

On the runner, with no go to up, `Home` and `End` SHALL act on the unit on show, by the projector's
own arithmetic: the first or last screen of the live bait when the live entry is a song, of the live
entry otherwise — never the first or last screen of the service. `Shift` with them SHALL take the
live entry's first or last bait when it is a song, and the entry's own first or last screen when it
has none, a blank trailing rest skipped. `Ctrl`/`⌘` with them SHALL take the service's first or last
entry, and with the live screen between entries nothing SHALL move. (spec 187)

#### Scenario: a text entry is live
- WHEN `End` is pressed
- THEN the live row is that entry's last screen, and the service's end is only reachable with `Ctrl`

#### Scenario: a song's bait is live
- WHEN `End` is pressed
- THEN the live row is that bait's last lyric, and `Shift+End` takes the last bait

#### Scenario: a text entry is live with `Shift`
- WHEN `Shift+Home` / `Shift+End` is pressed
- THEN the live row is that entry's first / last screen, as the projector's fall-through does

### R10 — The band keeps the keyboard

While the find band is open the dock SHALL keep the keyboard in its field: the field SHALL take the
focus as soon as it is usable — at open when the index is ready, and the moment the index arrives
when it is not; a window that regains focus, a pointerdown in the dock, and any focus landing outside
the panel SHALL each leave the focus in the field rather than on the panel; and closing the band
SHALL return the focus to the panel. A refocus SHALL NOT change the query, the chosen match or the
list's scroll. (spec 187)

#### Scenario: the window comes back
- WHEN the dock window loses focus and regains it with the band open
- THEN `document.activeElement` is the band's field and typing appends to the query

#### Scenario: the band closes
- WHEN `Esc` closes the band
- THEN the focus is back on the panel

### R11 — A refresh lands where the operator is

On load the dock SHALL open what is on air rather than the picker: the service the state names, in
its runner with that service's live screen marked; or, when a go to stands with no service, the
runner holding the go to's block, its head reading `Go To`. It SHALL stay on the picker when nothing
is on air, and when the state names a service this picker does not list. (spec 187)

#### Scenario: a service is on air
- WHEN the dock is reloaded
- THEN its runner opens that service with the live row marked, and nothing on air changes

#### Scenario: nothing is on air
- WHEN the dock is reloaded
- THEN the picker is the view

#### Scenario: a go to stands alone
- WHEN the dock is reloaded while a go to with no service is up
- THEN the runner is the view and the go to's block is drawn

### R12 — A reading page starts a Go To

The song page and the Bible chapter page SHALL start a Go To through their Project control
(`reading/R42`): the display state gains the same pointer the dock's find band writes —
`{kind: 'song', song_id, index: 0}` for the open song, `{kind: 'passage', book_id, chapter, verse,
translation}` for the open chapter, `verse: 1` and the page's own shown edition — and `{type:
'goto'}` is broadcast on the display channel. The control SHALL NOT adopt or release a service, and
an adopted service keeps its screen and edition underneath the detour. The dock's own re-pick stays
an explicit restart: the never-reset rule is the reading control's, not the shared verb's. (spec 193)

#### Scenario: the pointer
- WHEN a reading page's control is clicked with this detour not already open
- THEN the state carries the same pointer shape a dock find writes, with the service untouched

#### Scenario: the control never resets
- WHEN the stored state already opens that song or chapter
- THEN the pointer is left untouched (hidden words resume where they kept), and the dock keeps
  re-picking from its own first screen or verse
