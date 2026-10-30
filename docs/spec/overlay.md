# overlay

**capability**: `overlay`
**last folded**: 2026-10-30
**slices**: `180-overlay-text-styles`

The OBS browser source: what the stream shows the congregation while a service runs. It is a listen-only page — the
dock drives it and the projector shows the room the same screens — so everything here is what the page *paints* from a
state it does not own. This file starts at spec 180; the caption it inherits was written by spec 119 and is recorded
as folded behaviour from here on.

### R1 — The overlay paints from the display state alone, and carries no control

The overlay SHALL render from the browser-local display state — `{service, screen, on, translation}` — pushed by the
dock over its channel, and SHALL carry no control, no focusable element and no chrome of its own. A page opened with
no state SHALL paint nothing. (spec 180)

#### Scenario: nothing is on air
- WHEN the overlay loads with no display state
- THEN the stage is empty and nothing in the page can take focus

#### Scenario: the dock hides the words
- WHEN the display state goes `on: false`
- THEN the words leave the stage once their exit ends, and the page keeps its place in the layout

### R2 — A song screen paints the caption

A screen belonging to a `song` entry SHALL paint the accepted lyric caption: one block of white text at weight 800,
an eight-way black outline that scales with the type, no fill, no border, no heading, centred at the caption's 5 %
inset. (spec 180, carrying spec 119)

#### Scenario: a two-line lyric at 1080p
- WHEN a song screen with two lines is on air at 1920×1080
- THEN the caption paints 1728×202 at (96, 824), 72 px, weight 800, transparent fill

#### Scenario: the entry's title is not painted
- WHEN the song entry carries a citation such as `KJ 152 Bait 1`
- THEN the caption paints the lyric only — never the citation

### R3 — A passage screen paints a quotation card

A screen belonging to a `passage` entry SHALL paint a centred card at the caption's inset: the screen header's first
line as a kicker, its remaining lines as an italic title, a hairline, then the verse. With no header the card paints
the words alone — no empty kicker, no orphan hairline. The card hugs its content between 34 % and 90 % of the frame
width, keeps a rounded `.32em` corner and a near-opaque dark fill, and its words carry no outline. (spec 180)

#### Scenario: a passage with a reference and a verse title
- WHEN the screen header is `Matius 5:3` over `Kesembuhan pada hari Sabat`
- THEN the kicker reads `Matius 5:3`, the title reads `Kesembuhan pada hari Sabat`, and the verse sits under a hairline

#### Scenario: a passage with the reference only
- WHEN the screen header is a single line
- THEN the kicker paints alone and no title element or extra hairline is emitted

#### Scenario: a long verse
- WHEN a 467-character verse is on air at 1920×1080
- THEN the card takes the frame's 90 % measure before it grows taller

### R4 — A liturgy screen paints a script panel

A screen belonging to a `text` entry SHALL paint a left-aligned panel at the same inset, carrying the entry's title
as its kicker when the screen has one, and the screen's lines as turns: the leader's quieter than the congregation's,
a joined line between the two. The panel is its own object — no centring, an almost square `.08em` corner, a bar on
its leading edge, and enough left padding to clear that bar. (spec 180)

#### Scenario: a titled liturgy turn
- WHEN a text screen titled `VOTUM, INTROITUS, DOA` carries a leader line and an `J. Amin.` answer
- THEN the panel paints 1555×201 at (182, 825) with the title above the turns, left-aligned, bar on the left

#### Scenario: the stored case, with no title
- WHEN a text screen carries no header
- THEN the panel paints 1553×145 with no kicker, no title and no hairline

#### Scenario: a single short answer
- WHEN the screen holds one three-word answer
- THEN the panel keeps its 34 % floor rather than collapsing to a chip

### R5 — A speaker mark sits in a column of its own

A liturgy line that carries a speaker mark SHALL paint the mark in its own column and the words beside it, and the
marked lines of one screen SHALL share one column sized by the widest of them, so every wrapped row and every line
begins at the same x — whatever the mark's width, `L.` or `Pelayan :`. The screen data SHALL carry the mark and the
words beside the full line the projector paints. (spec 180)

#### Scenario: a long turn wraps
- WHEN a leader line longer than the panel wraps to three rows
- THEN every row starts under the words, not under the mark

#### Scenario: two marks of different widths
- WHEN one screen carries `P:` and `P + K:`
- THEN both lines' words begin at the same x, the column sized by `P + K:`

### R6 — Blank, media, break and released screens paint nothing

A screen that is the built-in rest, a section break, or a media payload SHALL paint nothing, and `hide` or `release`
SHALL empty the stage. No object survives a rest. (spec 180)

#### Scenario: the rest after a verse
- WHEN the entry's trailing blank is on air
- THEN the stage is empty once the exit ends

#### Scenario: an image is projected
- WHEN a media screen is on air
- THEN the overlay paints nothing; the projector shows the image

### R7 — Text arrives and leaves, and a step morphs the panel

A caption or a panel SHALL arrive over 180 ms — fading in while rising, on `cubic-bezier(.4, 0, .2, 1)` — and leave
over 120 ms as it fades and sinks, after which the stage is empty. When consecutive screens of one entry are both
panels, the panel SHALL keep its place and morph its own box from the old measure to the new one over 180 ms with the
words resolving inside it, rather than re-entering; a caption simply swaps its words. A machine asking for reduced
motion SHALL get a cut. (spec 180)

#### Scenario: a passage goes on air
- WHEN a passage screen replaces nothing
- THEN the panel fades in over 180 ms while rising 18 px and growing from 97.5 %

#### Scenario: the next verse
- WHEN the next screen is the same entry's next verse
- THEN the panel keeps its place and its box moves to the new measure; nothing fades out and back

#### Scenario: the display blanks
- WHEN the screen becomes the entry's rest
- THEN the panel leaves over 120 ms and the stage is empty afterwards

#### Scenario: reduced motion
- WHEN the machine asks for reduced motion
- THEN the same changes paint and clear with no animation

### R8 — A flip repaints the heading and the words together

When the operator flips the edition, the plate SHALL paint the shown edition's header as its heading and its line as
the body, both changing together. (spec 180)

#### Scenario: flipping to the Simalungun edition
- WHEN `T` is pressed on a passage that carries a second edition
- THEN the kicker names the other edition and the body is that edition's verse

#### Scenario: flipping with no second edition
- WHEN `T` is pressed on a screen with no other edition
- THEN the plate repaints unchanged
