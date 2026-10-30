# Contracts: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md`

## Interfaces exposed by this slice

`none` — this slice adds no endpoint, no route, no message and no exported function. The overlay is a page the
operator points OBS at; everything it paints is derived from data another surface already serves.

## Not exposed

The distinction matters, so the interfaces this slice *consumes* are named here and left out of any contract file,
because they are owned elsewhere and this slice changes neither:

| Interface | Owner | Shape this slice reads | Changed here |
| --- | --- | --- | --- |
| `projectorEntryData` (island on `/obs/source/projector`) | reading views, spec 119 | `[{type, label, start, end}]` | no |
| `projectorData` (island, same page) | reading views | `{screens: [{blank, header, lines[], entry_index, translations}]}` | no |
| `gkps-display` in `localStorage` + `BroadcastChannel('gkps-service-display')` | the dock, spec 119 | `{service, screen, on, translation}` | no |

One field *is* added inside the second row's payload — each screen line gains `mark` and `words` beside its `text`
(FR-010). It is a widening of an internal island, not a published interface: the projector page ignores the new keys,
and the payload's existing `text` is untouched.
