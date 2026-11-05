# Go To in the dock — previews (spec 185)

Two pages:

| Page | What it is |
| --- | --- |
| `index.html` | the dock's runner with the Go To — states, keys, measurements |
| `sync.html` | the dock, the projector and the caption overlay side by side, following **one** display state through nine steps |

**Both pages are self-contained single files** — every stylesheet and script inlined,
the two fonts as base64 data URIs — because the desktop chat's `::preview{file=…}` frame
does not load a page by URL: it reads the file's text and sets it as an iframe's `srcdoc`
with `sandbox="allow-scripts"` and no `allow-same-origin`. In that opaque origin a
relative `<link>` or `<script src>` never resolves, so a page that works when opened
directly renders as bare markup in the chat. `build.py` produces the bundles from the
source `.css` / `.js` beside this file (and from `static/`), which stay the authors.

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python specs/185-dock-goto/preview/probe.py
~/Projects/multimedia-gkps-klender/.venv/bin/python specs/185-dock-goto/preview/probe_sync.py
~/Projects/multimedia-gkps-klender/.venv/bin/python specs/185-dock-goto/preview/probe_frame.py
```

The first walks every dock state, asserts the behaviours below, writes `shots/`
(gitignored) and prints the numbers `## UI/UX` quotes. The second drives the nine sync
steps and asserts each surface's own DOM, not the page's report lines. The third loads
both pages the way the chat does — `srcdoc`, sandboxed, opaque origin — and checks that
the styles, the scripts and the fonts actually arrive there.

## What to click

The bar above the dock switches the state, the width (320 / 400 / 520) and the theme.

| State | What it shows |
| --- | --- |
| **Service** | the runner at rest: the service's own place is the live row, its block open, the transport with the edition chip and arrows |
| **Go To** | the find band open as a layer: the dock behind it dimmed by `--backdrop`, `NKB 4` typed, one tinted suggestion, `1 / 1`, the field holding the focus |
| **No match** | `zzzz`: the row says `No matching passage or song` and Enter does nothing |
| **Loading** | the index still in flight: the field is disabled, the row says `Loading search…`, the count is `0 / 0` |
| **Song on air** | a Go To song as the list's live block, and nothing else: the pinned header naming the song with `Back`, then its own `Bait 1–4` rows; the service's rows are not drawn; the bait chips and arrows at the foot act on the song |
| **Passage on air** | a Go To passage at `Matius 5:3`: the same block with its 48 verse rows, the edition chip at the foot and no bait chips |
| **Words hidden** | the same song with the words blanked: the eye reads `Show words` |
| **Content failed** | type `Yoh 3` and press Enter: the result row says `Could not load — try again`, because this page carries only `Matius 5` |
| Light / 320 / 520 | the same states in the other theme and at the dock's other widths (the strip's label ellipsizes at 320; the Back control keeps its box) |

In the page itself: `G` opens the find band over a dimmed dock, typing answers from the
product's own lookup, `Enter` puts the suggestion on air, `↑`/`↓` cycle results; `Esc`,
a click on the dimmed area, or `Backspace` on an empty field each close it. The arrows
step what is on air, `T` flips a passage's edition, `Space` blanks it, and `Back`
returns the service to the screen and edition it stood on.

## Numbers (400 × 800, dark; measure with the probe)

| Part | Measured |
| --- | --- |
| head | 65.1 px tall, three 38 px controls (find · switch · display) |
| find band | 372 × 76 at (14, 710): two 34 px boxes, 8 px apart |
| field | 372 × 34, 13.5 px/400, 1 px divider border, 9 px radius |
| suggestion | 372 × 34 (same width as the field), count 11 px/650 at its right |
| go to block | 384 × 502.8 (song) and the whole list while it is up; header 400 × 43 filled with `--sidebar-selected-bg` (`rgb(57, 63, 79)` dark / `#B9D7C9` light), label 13 px/400 in the ink at the dock's 14 px padding, its `Back` on its own `--rail-bg` fill rather than the header's tint, at 65.1 px from the frame's top at rest and pinned — the same place, so pinning moves nothing; `Back` 50.3 × 28; no on-screen pill |
| its rows | **full-bleed**: box at 8 px, text at 18 px — the column a service entry's number occupies, against 61.6 for a service label and 62 for its inner rows |
| its rows | the dock's own screen rows, one step in: 28.8 px each, `Bait N` heads for a song, a numbered line per verse for a passage, the live row tinted |
| transport | edition chip 39.3 × 34, baits 34 px tall, arrows 40 × 40 |
| rows (unchanged) | one-line entry row 38 px, one-line screen row 28.8 px |
| light | strip background `#EDEAE3` (rail), label ink `#1F1F1D` |

## The sync page

`sync.html` is **one document** holding the three surfaces: the dock (the product's runner,
driven by `preview.js`), a projector stage (`projector.css`, painted by `sync.js` with
`web/projector.js`'s `overflows`/`fit`), and the caption overlay (`obs-overlay.css`, painted
by `sync.js` with `web/obs-overlay.js`'s `modelOf`/`caption`/`plate`). One state object is
handed to all three — the stand-in for `BroadcastChannel('gkps-service-display')` — and each
surface reports what it painted, which is what the page prints under the panels.

It is one document because the desktop chat's preview frame runs no nested documents: the
first version put each surface in an iframe and all three stayed empty there. The board is
a fixed 1084 px wide (dock 400 + gap 16 + display 640); when the column is narrower — the
chat's frame is 640 — `sync.js` zooms the whole stage as one piece rather than stacking it
out of view, so the three surfaces stay side by side.

Two **adapters** in `sync.css` repeat the declarations `projector.css` and
`obs-overlay.css` hang on `body.projector` / `body.obs-overlay` (the canvas colour, the
display font, the `--display-*` colours, the `data-showing="false"` fade, and the overlay
stage's `position: fixed`). `probe_sync.py` checks the result against the real pages'
computed values.

| Step | Dock | Projector | Overlay |
| --- | --- | --- | --- |
| 1 the service is on air | the service's list, its live row | the service's own screen | the liturgy plate |
| 2 `G` | the find band over a dimmed dock | unchanged | unchanged |
| 3 NKB 43 chosen | the go to block, its Bait rows | the song's first lyric | the lyric caption |
| 4 it steps | the block's live row moves | the next lyric | the next lyric |
| 5 Matius 5:3 chosen | the block, 48 verse rows, `TB` chip | the verse, fitted | the passage plate |
| 6 `T` | the `SIM` chip (the label keeps the TB reference) | `Mateus 5:3` and the Simalungun verse | the same plate, Simalungun |
| 7 `Space` | the block stays, the eye offers the words back | no words | empty stage |
| 8 `Back` | the service's list, still blank | the service's screen, blank | empty stage |
| 9 `Space` | the eye reads `Hide words` | the service's screen | the liturgy plate |

## What these pages cannot show

- **Fetches.** A static page cannot read `/projector/goto/index/`, `/chapter/…` or
  `/song/…`. The lookup is the product's own module (`static/web/projector-library.js`,
  loaded unchanged) answered from a captured index; choosing a result paints from a
  captured payload. Only `NKB 1`, `NKB 2`, `NKB 43`, `KJ 152` and `Matius 5` carry
  content here — any other result shows the product's own `Could not load — try again`
  row, because that is what a fetch that is not served produces.
- **The projector and the overlay.** Their look does not change: a Go To passage
  paints as the quotation card and a song as the lyric caption, by the rules they
  already carry (specs 136, 180). The visible delta of this slice is the dock's; the
  other two surfaces change *what* they paint, which a static page cannot show.
- **The service under a goto.** While a go to is up the service's rows are not drawn at all; Back
  restores them at the place they stood on.

## The data and how to refresh it

`build.py` writes `index.html` from the captured payloads:

| File | Captured from |
| --- | --- |
| `service.json` | `/projector?service=142` — 27 entries, 51 screens, real liturgy |
| `index.json` | `/projector/goto/index/`, sliced to four songs and `Matius` |
| `songs.json` | `/projector/goto/song/{1390,1391,1434,667}/` |
| `chapter.json` | `/projector/goto/chapter/40/5/` — `Matius 5`, both editions |

`build.py` writes `panels.js` (one copy of that data) and the three pages that use it:
`index.html`, `panel-projector.html`, `panel-overlay.html`. Re-capture, then run it.

## Decisions this page records

- The transport, the baits and the edition chip act on **what is on air** (owner's
  answer, 2026-11-03); the service waits behind it and Back restores its screen and
  edition.
- The strip's marker is the picker's own `On screen` component, not a new label: the
  thing wearing it is what the room sees, and while a goto is up no service row wears
  it.
- `Space` blanks whatever is on air, and Back keeps the words as they were left — the
  eye is one flag for one display.
- The find band is a layer, not a band (owner's note, 2026-11-03): the rest of the dock is
  covered while it is open, a click on the layer closes it, and `Backspace` on an empty field
  closes it — the same two gestures the projector's own Go To panel answers.
- While a go to is up the switch-service control is **disabled, not hidden** (the owner allowed
  either): the head keeps its width and the exit stays visible, and it returns with Back.
