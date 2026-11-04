# Contract — the display state, with a goto

**Spec**: `specs/185-dock-goto/spec.md` · **Module**: `static/web/display.js`

This is the delta to the shape `docs/spec/display-state.md` R1 and spec 119's domain rules pinned.
One field, three verbs' meaning, one message.

## Stored shape

```
gkps-display = {
  service: <id|null>, screen: <n>, on: <bool>, translation: <'TB'|'SIM'|null>,
  at: <ms>, session: <string|null>,
  goto: null | {
    kind: 'song',    song_id: <id>, index: <n>
  } | {
    kind: 'passage', book_id: <id>, chapter: <n>, verse: <n>, translation: 'TB'|'SIM'
  }
}
```

- `screen` and `translation` are the **service's** place. While `goto` is non-null nothing writes
  them (FR-015); Back is `goto: null` and they are what every surface then paints (FR-008).
- `goto.translation` is the **shown** edition of the passage, which is not necessarily the
  service's `translation`.
- A stored value whose `goto` cannot be parsed is read as `goto: null`; the rest of the state is
  read as it is today.

## Verbs

| Verb | With no goto | With a goto on air |
| --- | --- | --- |
| `show(service, screen)` | the service's screen goes on air | the goto ends and the service's screen goes on air (FR-002, FR-009) |
| `moveTo(screen)` | the service's screen moves | the goto ends first (D008) |
| `hide()` | words off, the place kept | words off, the goto's place kept (US4/AC3) |
| `release()` | nothing on air | the goto ends with the service (US4/AC2) |
| `flip(translation)` | the service's edition | the goto's edition — the service keeps its own (FR-002, FR-015) |
| `goTo(goto)` | the goto starts at the given position | replaces it |
| `stepGoto(position)` | no-op | moves the goto's `index` (song) or `verse` (passage) |
| `back()` | no-op | `goto: null`; the service is on air exactly as it stood (FR-008) |

Every one of these writes once (`at` renewed, session stamped) and posts one message.

## Messages on `gkps-service-display`

| Message | Meaning |
| --- | --- |
| `{type: 'goto', goto: <Goto|null>}` | **new.** The goto started, moved, flipped or ended; readers re-read the state |
| `{type: 'show', service, screen}` | unchanged |
| `{type: 'hide'}` | unchanged (now also covers a goto's words) |
| `{type: 'release'}` | unchanged (now also ends a goto) |
| `{type: 'flip', translation}` | unchanged; the translation named is that of whatever is on air |
| `{type: 'update'}` / `{type: 'state'}` | unchanged |

A reader that receives `goto` re-reads `gkps-display` rather than trusting the payload: the write
that posted it is already stored, and two surfaces writing at once settle on the later state
(spec's concurrent-start edge case).

## Reader obligations

- **The dock** (`obs-dock.js`): paints the block from `goto` plus the payload it fetches; its
  transport writes the goto; `Back` calls `back()`.
- **The projector** (`projector.js`): keeps `detour` only as the payload for the state's current
  goto; `G` calls `goTo`; Back calls `back()`; a goto arriving over the channel stops a playing
  recording and paints (FR-012).
- **The overlay** (`obs-overlay.js`): paints a song goto as the caption, a passage goto as the
  plate, nothing when `on` is false or the goto is gone (FR-011).
- A surface opened or reloaded mid-goto reads the goto on its first paint (FR-014).

## Fetching

`/projector/goto/index/` — the lookup index, once per dock page, on the first `G`.
`/projector/goto/chapter/<book>/<chapter>/` — one chapter, both editions; a verse step inside it is
local.
`/projector/goto/song/<id>/` — one song's screens and baits.
All three `cache: 'no-store'`, all three existing (spec 136). No endpoint is added (FR-013).
