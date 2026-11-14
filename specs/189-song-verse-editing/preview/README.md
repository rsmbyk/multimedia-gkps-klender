# Verse editing — preview (spec 189)

One page: **`index.html`**, the song page of the local library (`/songs/1825/`, *BN. HKBP 730:
Berdayakan Diriku*, songbook **Lagu**) with this slice's verse controls drawn over it.

It is assembled from the product's own materials, not drawn to look like them:

| Part | Where it comes from |
| --- | --- |
| the shell — rail, songbook panel, song list, header | `shell.html`, a snapshot of the running page (2026-11-05, compose stack serving `develop`) |
| the verse text | the same snapshot — the four stanzas of song 1825, unchanged |
| the styles | `static/styles/design/tokens.css`, `components.css`, `generate.css` |
| the editor dialog | the page's own `<dialog class="editor" id="editorModal">`, the `.editor__*` rules, and the large frame `data-editor-size="large"` (spec 133) |
| the verse controls | `preview.css` — the only new CSS this slice proposes |

**The page is one self-contained file.** The desktop chat's `::preview{file=…}` frame loads a page
through `srcdoc` in a sandboxed iframe with an opaque origin, so a relative `<link>` or `<script src>`
never resolves there; every stylesheet and script is inlined, and `fonts.css` is left out on purpose —
its two faces (CMG Sans, Source Sans 3) are not used by one pixel of the reading shell, and embedding
1.2 MB of TTF would make the page 2 MB for nothing.

```sh
python3 specs/189-song-verse-editing/preview/build.py            # writes index.html
~/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/189-song-verse-editing/preview/probe.py               # measures, writes shots/
```

`build.py` reads `shell.html` + `preview.css` + `preview.js`; `index.html`, `shots/` and
`report.json` are generated (shots and the report are gitignored).

## The reorder: B, by decision

Reordering long stanzas by dragging full-height rows was the complaint, so two designs were built on one
engine and the owner chose **B · Grab collapse** (2026-11-06).

| | B · Grab collapse — **ships** | A · Reorder mode — rejected |
| --- | --- | --- |
| how it starts | nothing — grab any verse's handle | a **`Reorder verses`** button in the song header |
| what happens | the list collapses to one-line rows **for the gesture only** | it collapses and stays that way |
| how it ends | letting go | **`Done`** in the same place |
| what it costs | the reading view changes under the pointer | the reader leaves the page to change it |
| the page carries | no new control at all | a button and a hint line |

Two things follow from B being the design:

- **The page carries no reorder control at rest** — no button, no mode. A's `Reorder verses` button now
  exists only while A is being compared in the state bar.
- **The row in hand reads `from→now`** in its own number column (`2→2` at the grab, `2→8` five slots
  later), because the collapse takes the order as it stood off the screen: the row in hand is the only
  place that still knows where this verse started.

A is kept in the state bar, labelled rejected, so the decision can be re-compared rather than taken on
trust.

**Try it**: press `Long song`, then `B · Grab collapse` and drag a handle. Both are live to the hand: the row follows the pointer, the rows it passes slide, the list
auto-scrolls near the page's edges, and **the numbers renumber as the row crosses**, not on release
(spec 081's rule for the Tata Ibadah order). `Long song` stays on while switching between A and B, so
the comparison is the same song.

The row in hand is a surface and a shadow — a fill on `--rail-bg` and a shadow under it, never a 1px
ring. A ring around a full-column row reads as a frame drawn round the list rather than as the thing
being carried.

The engine is one rAF loop, one measurement per crossing (FLIP) and edge auto-scroll. Its FLIP snapshot
is keyed **by the row element**, never by a `data-verse` attribute: with a shared key the snapshot
collapses to one entry and every row is thrown the list's whole height and slides back — a shake on
every crossing, which is what a clone-built fixture produced before this.

**The `Drag trace` state is that check, live** (14 independent checks per run). It holds the pointer
still for 150ms after the grab, then walks the first verse down the compact list, recording what every
other row does and where the verse in hand sits. Verdict in `report.json`:

- **the grab itself changed nothing — `grabHeld: true`**: the verse keeps its own slot until the
  pointer has travelled one slot's height;
- **its slot follows its travel — `indexFollowsTravel: true`**: one slot per 44px (44 → slot 2, 88 → 3,
  132 → 4, 176 → 5, 220 → 6, 264 → 7). The rule is *the grabbed slot plus one per slot of travel*;
  adding that travel to the slot it currently holds instead of the one it was grabbed from counts it
  again every frame and runs the verse to an end of the list within two slots. The check was verified
  to fail on that version;
- **reversals: 0**, and each row the carried verse passed moved **exactly one 44px slot, once**
  (−43.5 / −44), while the row it never reached moved 0.

Measured during a scripted drag (the probe's synthetic pointer, not a hand — a loose reading): A 34
frames, p95 gap 33.3ms, worst 50.2ms; B 42 frames, p95 gap 27.6ms, worst 43.4ms; CDP counters over a
40-step drag: LayoutCount 3, RecalcStyleCount 38, ScriptDuration 11ms — the cost is not layout.

## What to click

The bar at the bottom left switches state; the last button toggles the theme (the page opens in dark,
the mode the app is reviewed in).

| State | What it shows |
| --- | --- |
| **Rest** | the page as every reader gets it: verses, numbers, one `Add verse` row. No control is painted |
| **Hover** | verse 2 hovered: the number yields the gutter to the grip and the pencil, centred on the row; the lyric column does not move by a pixel |
| **Short** | verse 4 reduced to `Amin.` with its tools up — the one-line row, where a 42px stack meets a 36.8px row (see *Numbers*) |
| **New** | `New verse` in the **large** editor frame: 840 × 760, the title its own band, the field holding the textarea |
| **Edit** | `Edit verse 2`: the same frame, pre-filled, caret at the end |
| **Used** | `Edit verse 2` for a verse two Tata Ibadah name: `Delete verse` is disabled and a help line says why |
| **Confirm** | `Delete verse 2?` — the frame's body replaced by the confirmation (the app's own delete pattern, `entries.js` `confirmDelete`), so the dialog returns to its small size for the question |
| **A · Reorder mode** | *(rejected)* the header button, the hint line, one-line rows |
| **Drag trace** | a scripted gesture, not a state to judge: it drags the first verse down the compact list and records each row's travel — the regression check for the crossing shake |
| **B · Grab collapse** | **the design**: frozen mid-gesture — no mode button at all, one-line rows, the verse in hand on a fill and a shadow (no ring) |
| **Long song** | a toggle, not a state: the page's four stanzas are swapped for a fixture of **eight real stanzas, one from each of eight ordinary songs** (`long_song.json`). The library's longest single ordinary song holds four verses, so no song of its own outgrows the stage; every line in the fixture is the library's text, only the composition is the preview's. 8 × 271.9px = 2200.3px of reading column against a 900px viewport |
| **Empty** | a song with no verses: the app's own `.entry__empty` invitation and one `Add verse` |
| **Hymn** / **Restricted** | the same page with no verse control **in the DOM at all** — a hymn song's page, or a reader when editing is restricted. Hovering moves nothing: the number stays |
| **Light** | the theme toggle, for the light tokens |

In **Rest** the page is live to the hand: hovering a verse reveals its tools, the pencil opens
`Edit verse N`, `Add verse` opens `New verse`, and a handle can be dragged. **Nothing is saved** — the
drag and the saves are local to the page, which is what a static preview is.

## Numbers (1440×900, dark; measure with the probe)

| Part | Measured |
| --- | --- |
| stage / reading column | 648px stage at x = 792; the read article 520px at x = 856 (64px of stage padding each side) |
| a four-line verse | 520 × 137.6; number column 41.6 wide; lyric column starts at x = 900, 476 wide |
| verse type | 18.88px / 33.6px `ui-serif, Georgia, …` — unchanged |
| number | 11px/590 right-aligned, 0.9rem inset, `--head-ink` (`rgb(156,154,145)` dark / `rgb(100,99,87)` light) |
| the tools | two 20 × 20 buttons, 2px apart, stacked and centred in the gutter: the stack is 42px tall, at x = 866.8 |
| hover | opacity 0 → 1 over 120ms with a 90ms delay; the lyric column stays at x = 900 / 476 in both states |
| `Add verse` | 111.8 × 38 at x = 900 (the lyric column, not the gutter); 1px dashed `color-mix(--focus 42%, --divider)`; 13px/600 `--head-ink`, turning `--ink` on hover |
| the editor dialog | **840 × 760 at (300, 70)**; the title band 840 × 72.5; the field 788 wide, the textarea 788 × 580.3; the actions 788 × 38 at y = 772; `Save` 66.6 × 38, `Cancel` 81.6 × 38; focus lands in the textarea |
| the confirmation | the dialog back at its small size: a 436-wide block, 203.1 tall, `Cancel` / `Delete` 38px, right-aligned |
| `Delete verse` (disabled) | 1px `--divider` border and `--head-ink` label — neutral, not a faded red; the reason is a 12px/18px help line under the field |
| a collapsed row | 44px, one line: the number in its 2.6rem gutter (line-height raised to fill the row), the lyric ellipsized at 14px serif, a 1px `--divider` hairline between rows, the grip at the row's right and the pencil hidden |
| the seams | the hairlines are the list's, not the card's: the row in hand draws none, and the slot it will land in is bounded **above and below**. The seam above the slot is marked by the engine on the row before it (`is-seam-above`), not by a `:has(+ .is-dragging)` sibling rule — that rule reads well until a verse is dropped at the **end** of the list, where the row above is no longer the card's previous sibling and the line disappears |
| the readout | the row in hand's own 41.6px number column, `2→2` → `2→8`; the readout ends 2.4px short of the lyric column, so the text never moves (measured at 1440 and at 420) |
| mode B (ships) | no control added; those 44px rows are held for the gesture only, and the full stanzas return 170ms after the drop |
| mode A (rejected) | the header button 119.3 × 34 (`Reorder verses`) becoming 60.1 × 34 (`Done`), present only while A is compared — at rest the page has no reorder control |
| the row in hand | fill `--rail-bg` + `0 14px 30px -16px var(--backdrop)`; **no ring** — a `0 0 0 1px` ring around a 520px-wide row reads as a frame round the list |
| numbering during a drag | live, on every crossing: mid-gesture the rows read `1…8` with the row in hand holding its prospective number |
| a crossing, traced | each row the carried verse passes travels exactly one slot (−43.5 / −44), once, with **0 reversals** — measured by the `Drag trace` state, not by eye |
| long song | 8 stanzas of 271.9 each: the reading column 2200.3 tall against a 900px viewport (~3.3 rows in view); mode A collapses the same eight to a 392px list, all in view |
| the empty song | the invitation block 365.5 × 128, centred in the stage; title 20px/600, hint `--head-ink`, one `Add verse` |
| a one-line verse | the row is 36.8 tall; the 42px tool stack overhangs it by 2.6px top and bottom — into the neighbouring gutter's blank, with no visible collision (`short` state) |
| 420×900 | the read column 384 wide, gutter 27.2, lyric column 354.4 at x = 47.6; `Add verse` at x = 47.6; the dialog 382 × 760 with a 346-wide field (Chrome caps the dialog at `calc(100vw - 6px - 2em)`) |

## What this page does NOT prove

- The endpoints: adding, editing, deleting and reordering against the database, and the migration that
  moves a service entry's verse references from numbers to IDs. The slice's tests own those.
- A hymn song's real page: `Hymn` here takes the controls out of this ordinary song's markup.
- That the drag feels right under a hand: the frame gaps come from the probe's synthetic pointer.
- The number a control shows after a reorder is the page's own renumbering, not a server read.
| cursor | the carried verse follows the pointer Y-position, so it stays under the hand during the gesture. The reorder target is still computed from pointer travel (origin + round(travel/44)), and the verse lands in the correct slot on drop.|

