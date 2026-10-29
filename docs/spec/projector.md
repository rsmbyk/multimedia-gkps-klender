# projector

**capability**: `projector`
**last folded**: 2026-10-29
**slices**: `155-audio-presentation-lock`, `136-remove-offline-library`

The service projector page: what it shows the congregation, and how its operator's Go To finds and
paints a passage or a song. This file starts at spec 136 — the projector's earlier behaviour
(specs 006, 091, 119) is recorded in those slices and is folded as a slice touches it.

### R1 — The Go To searches a page-memory index and fetches the content it paints

The projector page SHALL fetch a Go To index when it loads and hold it in page memory: every Bible
book with its editions' chapter and verse counts, the songbooks and the song titles — and no verse
text, no lyric. A query SHALL be answered from that index without a request. Choosing a result SHALL
fetch the whole chapter in both editions, or the whole song, and paint it; a step that leaves the
loaded chapter SHALL fetch the chapter it enters. `Update` SHALL re-fetch the index, so a song added
while the page is open is findable after it.

While any of those fetches is in flight the panel SHALL hold its loading state: the chosen row shows
a loading indicator in place of its count, a second indicator shows left of the shortcuts button in
the corner cue, the search field is disabled, Escape and the dismiss overlay do nothing, and no
shortcut or click changes the screen. The state SHALL end when the content paints, or when the fetch
fails — a failure leaves the panel open with its rows and says the content could not be loaded.

#### Scenario: the page loads
- WHEN the projector opens
- THEN one index request is made, and typing in Go To makes none

#### Scenario: choosing a passage
- WHEN a passage result is chosen
- THEN the chapter is fetched, every input is refused until it paints, and the passage appears

#### Scenario: stepping inside a chapter
- WHEN an arrow steps a verse in the loaded chapter
- THEN the verse paints with no request

#### Scenario: leaving a chapter
- WHEN a step crosses to another chapter or book
- THEN the fetch runs under the same lock, and the corner indicator shows beside the shortcuts button

#### Scenario: a fetch fails
- WHEN a chapter or song request fails
- THEN the lock ends, the panel stays open, the field is usable and the row says the content could not be loaded

### R2 — The projector page renders from its own response alone

The projector SHALL paint the screens the server sent with the page. It SHALL NOT read a saved
service, wait for a library update, or promise a saved copy in its empty state; a service with no
items SHALL show the empty state.

#### Scenario: a service with items
- WHEN the projector opens for a service
- THEN its screens are the response's, and no other store is read

#### Scenario: a service with no items
- WHEN the projector opens for a service holding nothing
- THEN it shows its empty state, naming no saved copy

### R3 — A playing recording owns the projector screen until it pauses

While an audio entry's recording plays, the projector SHALL hold the screen it is on: no page step,
entry or bait jump, page boundary, mouse zone, corner-cue control or Go To SHALL move it, and the
recording SHALL keep playing through any of them. The playing recording SHALL take the viewport, as a
playing video does, so the corner cue and the mouse zones are off screen; the pause that gives the
screen back SHALL keep the position playback had reached.

#### Scenario: a key arrives while the recording plays
- WHEN an arrow, page or home/end key arrives — plain, Shift or Ctrl — while a recording plays
- THEN the projector stays on the recording's screen and the recording keeps playing

#### Scenario: the pointer arrives while the recording plays
- WHEN a mouse zone or a corner-cue control is clicked, or the Go To is asked for
- THEN nothing moves, no panel opens, and the recording keeps playing

#### Scenario: the screen is given back
- WHEN the operator pauses, or the browser leaves fullscreen, or the recording ends
- THEN the normal projector screen returns, paused, holding the position playback had reached

#### Scenario: the browser refuses fullscreen
- WHEN the fullscreen request is refused while the recording plays
- THEN the recording plays on the normal projector screen and the screen stays locked until it pauses

#### Scenario: the dock drives the projector
- WHEN the display channel hides, releases or names another screen
- THEN the recording stops and is released, as it did before this requirement
