# projector

**capability**: `projector`
**last folded**: 2026-10-29
**slices**: `136-remove-offline-library`, `161-projector-empty-notice`

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
items SHALL show the empty state. The empty state SHALL be painted only while the stage holds
nothing: while a Go To detour is on the stage the empty notice SHALL NOT be painted and SHALL take no
room in the stage's layout, so the detour is laid out in the full stage; closing the detour SHALL
bring the notice back when the service still holds nothing. A re-read that ends with screens SHALL
hide the notice in that same render, and one that ends with none SHALL leave it visible.

#### Scenario: a service with items
- WHEN the projector opens for a service
- THEN its screens are the response's, and no other store is read

#### Scenario: a service with no items
- WHEN the projector opens for a service holding nothing
- THEN it shows its empty state, naming no saved copy

#### Scenario: a Go To passage or song over an empty service
- WHEN a Go To detour paints over a service with no items
- THEN the empty notice is not painted, takes no room, and the detour is fitted to the full stage
- AND closing the detour brings the notice back

#### Scenario: a re-read that brings the first screens
- WHEN the page re-reads its service and the response carries screens
- THEN the empty notice is hidden in the same render
- AND a re-read that carries no screens leaves it visible
