# dock

**capability**: `dock`
**last folded**: 2026-11-04
**slices**: `185-dock-goto`

The OBS dock — the operator's surface for running a Tata Ibadah from inside OBS. Its earlier
behaviour (spec 119's runner and picker, spec 132's buckets, spec 164's fluid width) is recorded in
`reading.md` and in those slices; this file starts at the go to, which is the first behaviour folded
to a capability of the dock's own.

### R1 — The runner offers a Go To, and the picker does not

The dock's runner SHALL offer a Go To, opened by `G` or by a control in its head, and the picker view
SHALL NOT offer it — a go to needs a service open. Choosing a result SHALL put that song or passage
on air at its first screen or verse; with nothing on air, the browsed service SHALL be adopted at its
first screen underneath it, so Back always has a place to return to. (spec 185)

#### Scenario: the runner is open
- WHEN `G` is pressed, or the head's control is clicked
- THEN the find band opens over the dock with the field empty and holding the focus

#### Scenario: the picker is open
- WHEN the dock is on the picker view
- THEN no Go To control is drawn and `G` does nothing

#### Scenario: nothing is on air
- WHEN a result is chosen with no display state
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
SHALL NOT be drawn, and no row SHALL wear an `On screen` marker. The transport SHALL act on the go
to: an arrow changes its screen or verse, a bait chip its bait, a flip its edition; the service's own
screen and edition SHALL NOT change until Back. `Back` SHALL restore the service's screen and edition
exactly as they stood. (spec 185)

#### Scenario: a go to is on air
- WHEN the dock is looked at
- THEN the block names the go to and draws its screens, and the service's rows are gone

#### Scenario: the arrows are pressed
- WHEN an arrow, a bait chip or `T` is pressed while a go to is on air
- THEN the go to moves or flips, and the service's own place does not change

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
was. While a go to is on air the switch-service control SHALL be disabled rather than hidden — the
head keeps its width and the exit stays visible — and SHALL return the moment the go to ends.
(spec 185)

#### Scenario: the layer is clicked
- WHEN any point of the layer is clicked
- THEN the band closes, nothing goes on air, and the transport is back in place

#### Scenario: a go to is on air
- WHEN the head is looked at
- THEN the switch-service control is drawn disabled, and no press of it changes the view

#### Scenario: the go to ends
- WHEN `Back` or a service screen ends the go to
- THEN the switch-service control is usable again
