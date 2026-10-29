# projector

**capability**: `projector`
**last folded**: 2026-10-29
**slices**: `156-audio-play-indicator`, `136-remove-offline-library`

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

### R4 — The audio screen carries its playback control

An audio entry's screen SHALL paint its play/pause control above the seek bar: a 48 × 48 circle whose
mark follows the audio — a play triangle while paused or ended, two bars while playing — at full opacity
whenever the screen's chrome is up. When the chrome settles into its idle state the control SHALL hide the
way the bar dims, leaving its 48px of height reserved so the bar does not move; any pointer move or key
press SHALL bring it back with the bar and the times. The seek bar and the times keep their own dimming
(`.52` and `.4`) and their boxes.

The control SHALL be reachable by the pointer: no pointer zone may cover it, and the page's windowed
fullscreen reservation SHALL NOT consume its click. Clicking it SHALL toggle playback exactly as `Space`
does, and its `aria-label` SHALL read `Play audio` while paused and `Pause audio` while playing.

#### Scenario: an audio screen at rest
- WHEN an audio entry is showing and nothing has played
- THEN a 48 × 48 play triangle sits 30px above the seek bar, and the times read `0:00 / <total>`

#### Scenario: playback starts and stops
- WHEN the audio plays
- THEN the mark becomes two bars
- WHEN it pauses or reaches its end
- THEN the triangle returns

#### Scenario: the chrome settles while playing
- WHEN the audio plays and the chrome has been idle for 3.5 s
- THEN the control is hidden and takes no pointer, the bar is `.52` and the times are `.4`, and the bar has not moved
- WHEN the pointer moves or a key is pressed
- THEN the control returns at full strength with the mark for the state the audio is in

#### Scenario: the control is pressed
- WHEN the control is clicked on a windowed projector
- THEN the audio toggles and the page does not enter fullscreen
- WHEN anything else on the projected page is clicked
- THEN it enters fullscreen as before

#### Scenario: the local copy is missing
- WHEN the companion has no copy of the file, or the bytes are not audio
- THEN the player stays hidden, the missing-file mark shows, and no control is painted
