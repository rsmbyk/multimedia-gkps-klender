# Keyboard parity — the dock's preview (spec 187)

One page:

| Page | What it is |
| --- | --- |
| `index.html` | the dock's picker and runner, its Go To, the go to standing alone, and the `K` sheet — states, keys, measurements |

**It is a self-contained single file** — every stylesheet and script inlined, the two fonts as
base64 data URIs — because the desktop chat's `::preview{file=…}` frame does not load a page by URL:
it reads the file's text and sets it as an iframe's `srcdoc` with `sandbox="allow-scripts"` and no
`allow-same-origin`. In that opaque origin a relative `<link>` or `<script src>` never resolves, so a
page that works when opened directly renders as bare markup in the chat. `build.py` produces the
bundle from the source `.css` / `.js` beside this file (and from `static/`), which stay the authors.

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python specs/187-keyboard-parity/preview/build.py
~/Projects/multimedia-gkps-klender/.venv/bin/python specs/187-keyboard-parity/preview/probe.py
```

The probe walks every state, asserts the behaviours below, writes `shots/` (gitignored) and prints
the numbers `## UI/UX` quotes.

## What to click

The bar above the dock switches the state, the width (320 / 400 / 520), the height (800 / 1000 / 1200) and the theme.

| State | What it shows |
| --- | --- |
| **Service** | the runner at rest: the service's own place is the live row, its block open, the transport with the edition chip and arrows |
| **Picker** | the dock's service picker as the live one draws it: the head with the logo and refresh/theme, the grouped list (last 30 days, earlier this year) |
| **Go To** | the find band open as a layer: the dock behind it dimmed by `--backdrop`, `NKB 4` typed, one tinted suggestion, `1 / 1` |
| **No match** | `zzzz`: the row says `No matching passage or song` and Enter does nothing |
| **Loading** | the index still in flight: the field is disabled, the row says `Loading search…`, the count is `0 / 0` |
| **Song on air** | a Go To song as the list's live block, and nothing else |
| **Passage on air** | the same block with its 48 verse rows and the edition chip |
| **Words hidden** | the same song with the words blanked: the eye reads `Show words` |
| **Go to alone** | this slice's new state: a go to with no service — the head reads `Go To` and no date, the block names the song, the switch control stays usable |
| **Fetching** | a chapter step in flight: the block header reads `Loading…`, no rows, both arrows disabled |
| **Shortcuts** | `K`'s sheet over the runner: 32 rows in five groups, one per direction, in the projector's own wording and order; `K`, `Esc` or a click on its 8 px frame closes it |
| **Picker + shortcuts** | the same `K` over the picker: 34 rows in six groups, the picker's own two (`↑` / `↓`, `Enter`) leading, since only the picker has them |

In the page itself: `G` opens the find band (over the service or the picker), typing answers from
the product's own lookup, `Enter` puts the suggestion on air, `↑`/`↓` cycle results; `Esc`, a click
on the dimmed area, or `Backspace` on an empty field each close it. `K` opens and closes the sheet;
while it is open no other key acts. The arrows step what is on air, `T` flips a passage's edition,
`Space` blanks it, and `Back` returns the service to the screen and edition it stood on.

## Numbers (400 × 800, dark; measure with the probe)

| Part | Measured |
| --- | --- |
| head (every state) | 65.1 px tall, three 38 px controls (find · switch · display) |
| go to alone | head's title line `Go To`, the date line `display: none`, the switch control **not** disabled; the block takes the list from y 65.1 |
| fetching | block header `Loading…`, 0 rows, `prev`/`next` disabled |
| sheet panel | **384 × 784 at (8, 8)** — the dock inset 8 px; `--rail-bg`, 1 px `--divider` border, 12 px radius, shadow `rgba(0, 0, 0, .34) 0 18px 40px` |
| sheet head | 49 px tall inside the border; title `KEYBOARD` 10.5 px/650, letter-spacing .08em, `--head-ink`; close control 30 × 30, 8 px radius, its right edge flush with the keycap column at x 377 |
| sheet body | 382 × 733 at (9, 58); on the runner **5 groups, 32 rows**, on the picker **6 groups, 34 rows** — the picker's own two lead it, every row carries one direction only, and each shared row wears the projector's label, in the projector's order; the first group's heading at y 68 |
| grouping heading | 10 px/650, letter-spacing .7 px, `--head-ink`; **16 px above**, 3 px below |
| row | 354 × **30 px**, 10 px between the label and the chords, 4 px of air above and below the cap |
| row label | 12.5 px/400 in the ink, one line, ellipsized |
| keycap | **22 × 22 px** (the projector's cap at the dock's scale), word keys 44 px, space bar 66 px, 4 px radius; letter text 11 px/400, word text 10.5 px; the space cap carries the projector's `␣` open-box mark at 14 px, stretched 1.3× wide (not the word `Space`), its box centred with 4 px of air above and below; fill `#2A2722` and edge `#4A463F` in dark, `#D4D2CB` with an ink-30 % edge in light, inset top highlight |
| the separator | between rows: a 1 px hairline, ink 12 %, drawn as an inset shadow so it costs no height — the projector's own `.row + .row` |
| the separator | between alternatives in a row: the word `or`, 11 px/650 `--head-ink`, 4 px each side — the projector's own |
| the scrollbar | the app's own (spec 087): 5 px thumb, `border-radius: 999px`, `--scroll-thumb` (hover `--scroll-thumb-hover`), transparent track; `scrollbar-width`/`scrollbar-color` only behind `@supports not selector(::-webkit-scrollbar)`. An overlay bar: it paints while the body scrolls, as the dock's list does |
| sheet at width | no row overflows at 320 / 400 / 520; at 320 the narrowest rows wrap their chords under the label |
| sheet height | **1117 px** of content on the runner, **1206 px** on the picker: 384 / 473 px to scroll in an 800 px dock, 184 / 273 at 1000, and at 1200 the runner fits (1133 px body) while the picker still scrolls 73 |
| short dock | body 1117 / 453 at a 520 px dock — the sheet scrolls, it does not clip |
| motion | the panel rises 180 ms (`translateY(6px) scale(.99)` → none) on `--ease-timing`; the frame fades over 160 ms; reduced motion gets a cut |

## What this page cannot show

- **Fetches.** A static page cannot read `/projector/goto/index/`, `/chapter/…` or `/song/…`. The
  lookup is the product's own module (`static/web/projector-library.js`, loaded unchanged) answered
  from a captured index; choosing a result paints from a captured payload. Only `NKB 1`, `NKB 2`,
  `NKB 43`, `KJ 152` and `Matius 5` carry content here — any other result shows the product's own
  `Could not load — try again` row, because that is what a fetch that is not served produces.
- **The Esc hold.** A hold is a gesture, not a look: the sheet's `Back to services (hold)` row is the
  visible part; the 900 ms timing is asserted in the slice's E2E, not here.
- **The picker's behaviour.** Its markup is the live dock's own, captured whole (head, refresh and
  theme controls, 116 services including the dev database's test rows); the preview switches to it to
  show the sheet's fifth group. Its keys — `↑` / `↓`, `Enter` — are not wired here.
- **The projector and the overlay.** Their look does not change; a service-less go to paints there by
  their own rules, which a static page cannot exercise.

## The data and how to refresh it

`build.py` writes `index.html` from the captured payloads:

| File | Captured from |
| --- | --- |
| `service.json` | `/projector?service=142` — 27 entries, 51 screens, real liturgy |
| `index.json` | `/projector/goto/index/`, sliced to four songs and `Matius` |
| `songs.json` | `/projector/goto/song/{1390,1391,1434,667}/` |
| `chapter.json` | `/projector/goto/chapter/40/5/` — `Matius 5`, both editions |
| `picker.html` | `/obs/dock` — the picker section verbatim (its logo inlined at build), 116 services |

`build.py` writes `panels.js` (one copy of that data) and `index.html`. Re-capture, then run it.
