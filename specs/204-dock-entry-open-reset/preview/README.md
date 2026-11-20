# Preview: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md`
**Shape**: `static`
**Open**: `specs/204-dock-entry-open-reset/preview/index.html` opened directly

## Run

```sh
# none: open the file directly.
xdg-open specs/204-dock-entry-open-reset/preview/index.html

# optional — any static file server, for the reload state's cookie fidelity (see below):
python -m http.server 8899 --bind 127.0.0.1 \
  --directory specs/204-dock-entry-open-reset/preview
# then http://127.0.0.1:8899/index.html

# rebuild from the product's own materials (needs the running stack for capture):
.venv/bin/python specs/204-dock-entry-open-reset/preview/capture.py   # real page + payloads
.venv/bin/python specs/204-dock-entry-open-reset/preview/build.py     # assemble index.html
.venv/bin/python specs/204-dock-entry-open-reset/preview/probe.py     # every state, measured
```

## What is real and what is stubbed

Real: the rendered `/obs/dock` markup (its picker buckets, rows, pills and runner skeleton),
`tokens.css`, `obs-dock.css`, `display-session.js`, `display.js` and `obs-dock.js` — byte copies
from `develop` (`ab46f384`), except **one added line** in the dock script: the drafted reset in
`openService()`, gated on `window.__openReset` so the same page can run today's rule. The
entry/screen islands are the ones `/projector?service=N` really serves for five local services
(155, 149, 142, 144, 145), captured verbatim in `fixtures/`.

Stubbed: the network only. `shim.js` answers `/projector?service=N` from those islands in the same
`json_script` shape, so the dock's own fetch → `DOMParser` → `JSON.parse` path runs unchanged. The
picker keeps the five captured services; every other row is removed by `build.py`.

**The fetch is unchanged by this slice** — it re-draws a list the dock already holds, and resets
page memory when a service is opened.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| picker at rest | open the page | five services in their real buckets; no block open anywhere |
| rest after an open | click a picker row | every header `aria-expanded="false"`, chevron right, block height 0 |
| hand-expanded | click a non-live entry's header | chevron turns down, block at its natural height (126 px for the passage at position 4 of 155) |
| **the reported leak** | expand position 4 in 155, then open 149 | `today`: position 4 of 149 stands open (70 px). `drafted`: nothing open |
| re-open the same service | Back, then click 155 again | `today`: position 4 still open. `drafted`: shut |
| keyboard open | mark a picker row with `↓`, press `Enter` | the same reset as a click — `measurements-enter.json` |
| multi-open | expand positions 2, 4, 9 in 155, then open 149 | `today`: `[1, 3]` open. `drafted`: `[]` |
| live entry | expand position 4, click its first screen row | block open, no chevron, row tinted, `aria-current="true"` |
| **the live exception** | with 155 on air, open 149, then 155 again | 149: nothing open (nothing live there). 155: only the live block open |
| crossing (unchanged) | hand-open position 7, then project position 1 | the hand-opened block stays open — spec 198's rule |
| re-read (unchanged) | hand-open a block, press *Re-read now* | the block stays open — spec 195's rule; this is not an open. The button bumps a revision marker the shim serves in the first entry's label, so the payload really differs and the dock really rebuilds (`rebuilds=13` in the measurements) — an unchanged payload would take the dock's own no-rebuild shortcut and prove nothing |
| reload | press *Reload* | every override gone; over http the on-air service resumes with only its live block open |
| empty service | open “Ibadah Minggu” (0 entries) | no rows, no error |
| long service + breaks | open “Ibadah Minggu” (27 entries) | break rows are hairlines with no chevron; the reset covers all 27 |
| reduced motion | `probe.py` runs a context with `reduced_motion="reduce"` | identical — the reset paints no morph at all |
| narrow | resize the window under 860 px | the rail stacks under the dock; the dock keeps its fluid layout |
| light theme | Back to the picker, click the appearance button | the same states in the light tokens |

The rail beside the panel reads back what is **painted** — `aria-expanded`, `is-open`, the inner's
measured height, `scrollTop` and the stored display state — and logs every click. After each open
it states what the open left standing: `non-live open []` is the drafted rule holding.

*Run the reported sequence* performs the reported clicks end to end (open 155 → expand position 4
→ open 149 → re-open 155) with the dock's own controls.

## Live or static

**Static**: one HTML page assembled from the project's real template output, class names,
stylesheets, tokens and scripts, opened directly — no server of its own, and no duplicate of the
project's dev server. The defect itself was reproduced **live** on the running stack
(`http://127.0.0.1:63404/obs/dock`, `develop` `ab46f384`); those numbers are in the spec's
Clarifications and in `../` scratch probes, and the preview reproduces the same sequence over the
captured payloads.

**What a static page cannot show:** anything that fetches. Here the fetch is stubbed with the real
payloads, so the list, its blocks and their states are the product's own; the Go To band's index
fetch, media bytes from the local companion, and the projector/overlay surfaces are not exercised.

**One browser caveat, measured:** over `file://` Chrome refuses cookies, so `display-session.js`
re-mints its session marker on every load and a stored display state reads as foreign after a
reload — the dock lands on the picker instead of resuming the on-air service. Over any static
`http://` server the cookie persists and the reload state is the product's: runner resumed, only
the live block open. Both runs are recorded (`measurements-file.json`, `measurements-http.json`);
the reload row above is the http one.

## What is not a preview

A screenshot, a static image and a recording are not previews. `shots/` holds the probe's
read-back screenshots as evidence beside the page, not in place of it.
