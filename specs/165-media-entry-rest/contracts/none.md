# Contracts: a media entry ends on a rest like every other entry

**Spec**: `specs/165-media-entry-rest/spec.md`

**None** — no URL, endpoint, request body, response shape or stored data changes. The projector's page
carries its screens in embedded JSON islands, and the dock reads them back; that seam is recorded here
because two of the project's own scripts share it, and this slice moves one value across it.

## The screen island (unchanged shape, one more entry per media row)

`/projector?service=<id>` embeds `#projectorScreenData` (`json_script`) — a list of screen objects — and
`#projectorEntryData` — a list of entry ranges. `static/web/obs-dock.js` fetches that page and parses
both islands (`fetchService`).

```js
// screen — the keys a media entry's group now carries
{blank: false, header: '', lines: [], image_sha256: '<sha>', entry_index: n}   // image
{blank: true,  header: '', lines: [], entry_index: n}                          // the rest after it

// entry — the same object, its range one screen longer
{type: 'media', label: 'random.jpg', untitled: true, start: n, end: n + 1, baits: [], translation: ''}
```

**The invariant this slice adds to the seam**: a non-break entry's `end` names its last screen, and for
every entry kind that screen has `blank: true`. `obs-dock.js` reads `screen.blank` to draw the `Rest` row
and `entry.start`/`entry.end` to build its step list, so nothing in the script needs to change — the
contract it already relies on simply holds for media entries now.
