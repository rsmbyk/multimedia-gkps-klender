# projector

**capability**: `projector`
**last folded**: 2026-10-29
**slices**: `165-media-entry-rest`, `158-projector-media-fit`, `155-audio-presentation-lock`, `156-audio-play-indicator`, `161-projector-empty-notice`, `157-projector-image-missing-glyph`, `136-remove-offline-library`, `156-audio-play-indicator`, `161-projector-empty-notice`, `157-projector-image-missing-glyph`, `136-remove-offline-library`

The service projector page: what it shows the congregation, and how its operator's Go To finds and
paints a passage or a song, and how a media screen is fitted to the stage. This file starts at spec 136 — the projector's earlier behaviour
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

### R3 — The projector's image placeholder appears only when the image fails

An image screen SHALL paint its picture alone when the bytes arrive, and the unavailable glyph alone when
the load fails; while the fetch has not settled it SHALL paint neither. The glyph SHALL be hidden by its
`hidden` attribute — carried in the markup, as the audio, video, PDF and slides placeholders carry it, and
toggled by the attribute rather than by the `hidden` property, which an SVG element does not have — so the
element leaves the flex row and the picture alone is what the box centres. A screen that stops being
active SHALL drop a failed state with it.

#### Scenario: the bytes arrive
- WHEN an image screen becomes the active one and its fetch resolves
- THEN the picture is painted, the glyph is not, and the picture is centred on the stage's middle

#### Scenario: the load fails
- WHEN the fetch rejects, answers a non-image response or errors in the player
- THEN the glyph alone is painted, 80×80, on the stage's middle

#### Scenario: the fetch has not settled
- WHEN an image screen is active and its bytes have not arrived
- THEN neither the picture nor the glyph is painted

#### Scenario: leaving a screen that failed
- WHEN the operator moves to another screen and returns to the one that failed
- THEN the screen is drawn from its own empty state and its own fetch decides what is painted

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

### R5 — A playing recording owns the projector screen until it pauses

While an audio entry's recording plays, the projector SHALL hold the screen it is on: no page step,
entry or bait jump, page boundary, mouse zone, corner-cue control or Go To SHALL move it, and the
recording SHALL keep playing through any of them. The playing recording SHALL take the viewport the way
a playing video does — the audio screen's own box, not the page — so the corner cue and the mouse zones
are off screen; that is the reading R4's "the page does not enter fullscreen" leaves room for. The pause
that gives the screen back SHALL keep the position playback had reached.

#### Scenario: a key arrives while the recording plays
- WHEN an arrow, page or home/end key arrives — plain, Shift or Ctrl — while a recording plays
- THEN the projector stays on the recording's screen and the recording keeps playing

#### Scenario: the pointer arrives while the recording plays
- WHEN a mouse zone or a corner-cue control is clicked, or the Go To is asked for
- THEN nothing moves, no panel opens, and the recording keeps playing

#### Scenario: the screen is given back
- WHEN the operator pauses — from the control, `Space`, or the browser leaving fullscreen — or the recording ends
- THEN the normal projector screen returns, paused, holding the position playback had reached

#### Scenario: the browser refuses fullscreen
- WHEN the fullscreen request is refused while the recording plays
- THEN the recording plays on the normal projector screen and the screen stays locked until it pauses

#### Scenario: the dock drives the projector
- WHEN the display channel hides, releases or names another screen
- THEN the recording stops and is released, as it did before this requirement

### R6 — An image screen is fitted to the stage, above 1:1 as well as below

A screen whose media is an image SHALL paint it at the scale `min(stage width / image width, stage
height / image height)` — the smaller of the two ratios — whether that scale shrinks the image or
enlarges it, with the whole image visible and centred and its aspect kept. The scale SHALL be
recomputed when the window's size changes. (spec 158)

#### Scenario: an image smaller than the stage
- WHEN a 182×277 image shows on a 1856×1104 stage
- THEN it paints 725×1104, not 182×277

#### Scenario: an image larger than the stage
- WHEN a 600×300 image shows on a 1376×804 stage
- THEN it paints 1376×688 — the same rule below 1

#### Scenario: the window changes size
- WHEN the window narrows to a 960×672 stage
- THEN the same 12×6 image re-fits to 960×480 without a reload

### R7 — A PDF or PowerPoint page is fitted the same way

A screen whose media is a PDF page or a slide SHALL paint it at the same smaller ratio, at the
display's pixel ratio up to the painter's 6-megapixel cap. The reader's Preview dialog keeps its own
rule and never scales a page above 1:1. (spec 158)

#### Scenario: a Letter page on a wide stage
- WHEN a 612×792 pt page shows on a 1856×1104 stage
- THEN its canvas is 853×1104

#### Scenario: the dialog is left alone
- WHEN the same page is opened in the reading page's Preview dialog
- THEN it paints at its own size, never larger

### R8 — `T` switches between fit width and fit height

With a media screen showing, `T` SHALL switch to fit width — the media spans the stage's width and the
excess height is clipped equally above and below — and a second `T` to fit height, the excess width
clipped equally left and right. The default fit is one of the two (the smaller ratio), so the first
press always offers the other. A media screen's fit SHALL return to the default when another entry's
screen shows, and SHALL persist across the pages of one document. Every other screen kind SHALL be
unaffected: `T` still flips a passage's TB/SIM. (spec 158)

#### Scenario: the two states
- WHEN `T` is pressed on a fitted 182×277 image at a 1856×1104 stage
- THEN it paints 1856×2824, cut 860 above and below; a second press returns it to 725×1104

#### Scenario: a page turn keeps it, another entry does not
- WHEN a PDF is at fit width and the operator steps to page 2
- THEN page 2 is still fit width; stepping to the next entry shows that entry at its fit

#### Scenario: a passage still flips
- WHEN `T` is pressed on a passage screen
- THEN the translation flips TB/SIM, as before

### R9 — The shortcut sheet names the key

The projector's shortcut sheet SHALL carry a group naming images and PDFs, whose one row gives `T` for
fit width and fit height, and the sheet SHALL keep the height it had (677 px at 1080p) so it still
fits a 1280×720 window. (spec 158)

#### Scenario: the sheet on a 720p window
- WHEN `K` opens the sheet at 1280×720
- THEN the Image and PDF group is inside the sheet's frame and the sheet is 677 px tall

### R10 — The overflow is panned, by drag and by wheel

While a media screen's painted size exceeds the stage on either axis, a pointer drag on the screen SHALL
pan the media within that overflow, and the mouse wheel SHALL pan it too — `deltaY` vertically, `deltaX`
or `Shift`+`deltaY` horizontally. The pan SHALL be clamped so a media edge never leaves the stage's edge,
SHALL start at the centre whenever the fit or the screen changes, and SHALL never eat the corner's click:
a press that moves no more than 4 px is still a click (enter fullscreen when windowed, then previous,
next or show/hide words). While the media overflows the pointer over the stage SHALL read `grab`, and
`grabbing` while it drags. With nothing overflowing the wheel is inert. (spec 158)

#### Scenario: dragging a zoomed page
- WHEN the fit-width image is dragged upwards on a 1856×1104 stage
- THEN it follows the pointer and stops with its top edge on the stage's top edge

#### Scenario: the wheel
- WHEN the wheel is rolled over a zoomed page
- THEN the page pans on that axis and stops at the same ends

#### Scenario: a press that does not move
- WHEN the operator presses and releases within 4 px on a zoomed page
- THEN the corner's zone still receives its click and no pan is recorded

### R11 — A media entry ends on the built-in rest every other kind ends on

A media entry SHALL contribute its media screen followed by exactly one built-in rest — the blank screen
of spec 058's rule, which is not a section break and never becomes a row in the order — for every family:
image, audio, video, PDF and PowerPoint. A media entry whose file does not resolve SHALL contribute one
screen, that rest, and SHALL NOT gain a second. The rest SHALL carry `blank: true`, an empty `header` and
`lines`, and no family payload key, `bait`, `bait_rest`, `split`, `split_total` or `translation`; the
entry's `start` SHALL be unchanged and its `end` SHALL name the rest. The media screen's own payload and
paint, the fit and pan rules (R6–R10) and the audio and video lock (R5) SHALL be unchanged, and the dock
SHALL list the rest under the media row and step onto it. (spec 165)

#### Scenario: a picture ends on a rest
- WHEN a service holding one image entry builds its screens
- THEN the image is one screen, a blank is the next, and the entry's range covers both

#### Scenario: four pictures in a row
- WHEN four image entries follow one another
- THEN each picture is followed by a rest, and no step goes from one picture to the next

#### Scenario: an entry whose file is gone
- WHEN a media entry has no file attached
- THEN it contributes one blank screen, and no second rest after it

#### Scenario: a service that ends on a picture
- WHEN the last entry of a service is a media entry
- THEN its rest is the service's last screen, so the display can be left blank by stepping
