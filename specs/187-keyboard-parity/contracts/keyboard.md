# Contract — the keyboard grammar the two surfaces share

**Spec**: `specs/187-keyboard-parity/spec.md` · **Surfaces**: the dock (`static/web/obs-dock.js`,
`obs_dock.html`), the projector (`static/web/projector.js`, `projector_controls.html`)

The dock and the projector name one act the same way and mean the same thing by it. This table is the
contract; each surface's own sheet is a view of it.

## The chords

| Chord | Dock, runner | Dock, picker | Projector |
| --- | --- | --- | --- |
| `→` `↓` `PgDn` / `←` `↑` `PgUp` | next / previous screen | — | next / previous screen |
| `Shift` + those | next / previous bait | — | next / previous bait |
| `Ctrl` or `⌘` + those | next / previous entry | — | next / previous entry |
| `Home` / `End` | first / last screen of the unit on show (the live bait in a song, the live entry otherwise) | — | same |
| `Shift+Home` / `End` | the live entry's first / last bait; nothing on an entry with none | — | same |
| `Ctrl`/`⌘+Home` / `End` | the service's first / last entry | — | same |
| `Ctrl` or `⌘` + `PgUp`/`PgDn` | left to the browser (tabs) | — | left to the browser |
| `G` | the Go To band | the Go To band | the Go To band |
| `K` | the dock's shortcut sheet | the dock's shortcut sheet | the projector's shortcut sheet |
| `Space` | display / hide the service's words | — | play/pause a recording, else show/hide the words |
| `T` | flip TB / SIM | — | flip TB / SIM, or fit width / height on a media screen |
| `Esc` | held 900 ms: back to the picker; closed on the tap: band, sheet | the tap closes the band or the sheet; nothing else | close the layer, leave a go to; a held `Esc` leaves fullscreen |
| `↑` `↓` | (in a band) cycle results | move the pick | (in a band) cycle results |
| `Enter` | (in a band) open the match | open the marked service | (in a band) open the match |
| `Backspace` | (in a band, empty field) close | — | (in a band, empty field) close |

## The go to's own chords

| Chord | Passage go to | Song go to |
| --- | --- | --- |
| plain arrows | next / previous verse (no request inside the loaded chapter) | next / previous screen |
| `Shift` + arrows | next / previous chapter (one fetch per crossing) | next / previous bait |
| `Ctrl`/`⌘` + arrows | next / previous book (one fetch per crossing) | nothing |
| `Home` / `End` | first / last verse | the live bait's first / last screen |
| `Shift+Home` / `End` | first / last chapter | first / last bait |
| `Ctrl`/`⌘+Home` / `End` | first / last book | nothing |

## Obligations

- **One meaning.** A chord in this table acts as written on both surfaces; a surface that cannot
  perform an act (the dock has no media, the projector has no picker) says so with a dash, never with
  a different act.
- **One wording.** A row whose shortcut the projector's sheet also has wears the projector's own label,
  verbatim, and stands in the projector's own order inside its group (`FR-008`). The dock's five
  dock-only rows — *Move the Pick*, *Open the Service*, *Back to Services (hold)* — are the only ones
  worded for the dock.
- **One row per direction.** `next` and `previous`, `first` and `last` never share a row; the `or`
  between caps joins keys that do the same thing and nothing else.
- **The guard.** While a go to's payload is being fetched or a chapter/book step is in flight, no key
  and no pointer act changes what is on air; the block's header reads `Loading…` (`FR-009`).
- **The band keeps the keyboard.** While the band is open the dock's field holds the focus; the panel
  takes it back when the band closes (`FR-015`).
