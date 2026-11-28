# Preview — dock entry-kind icons

**Live**: `http://127.0.0.1:8771/obs/dock` (worktree `~/Projects/multimedia-gkps-klender-250`, dark, 420×800 at 1×). Open the page, click a service in the picker, then a header to open or project a block.

States to review:

1. **Mixed kinds** — service 144 (`Ibadah Minggu`): book on the passage, play-frame on media, note on songs, rules on text; the break rows stay bare. `shots/mixed-kinds-dark.png`.
2. **Text-only, 60 rows** — service `Ibadah Pace Probe`: the same 16px rule mark on every row, chevrons trailing at the same x. `shots/text-rows-dark.png`.
3. **Open header** — click any header: the chevron rotates 90°; the mark does not move or rotate.
4. **Live header** — click a screen row inside an open block: the chevron hides, the mark stays at the row edge in `--ink`.
5. **Both pins** — scroll a live block past either edge: the pinned clone carries the same single mark as its source header.
6. **Multi-line headers, service 149** (`hhhh…`, 25 Oktober 2026): the text URL wraps to 2 lines (row **57.1px**) and the media filename wraps to 4 (row **96.3px**). `shots/multiline-text-and-media-dark.png`.
7. **Multi-line headers, service 144** (`Ibadah Minggu`): rows 2, 4, 7 and 8–10 — a long song title wraps to 2 title lines plus its Bait line (row **77px**), a long media filename wraps to 3 (row **76.7px**), a song + Bait row is **56px**. `shots/multiline-song-and-media-dark.png`, `shots/wrapped-media-and-song-dark.png`, `shots/wrapped-media-and-bait-rows-dark.png`. The mark stays at 361–377px with the same 10px gap to the chevron.

On every wrapped row measured, the mark and the chevron sit at **0px off the row's centre** — the whole multi-line row, not just its first line.

`probe.py` prints the measured mark/chevron boxes and painted colour from the live page:

```
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/250-dock-entry-kind-icons/preview/probe.py \
  http://127.0.0.1:8771/obs/dock 144
```

Screenshots in `shots/` are gitignored; the probe and this note ship with the spec pack.
