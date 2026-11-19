# Preview: the dock centres its live entry only when asked

**Spec**: `specs/200-dock-centre-triggers/spec.md`
**Shape**: `static` — one self-contained page assembled from the product's own markup, classes and
`styles/design/obs-dock.css`
**Open**: `specs/200-dock-centre-triggers/preview/index.html` opened directly, or dropped into the
desktop chat's preview pane

## Run

```sh
none: open the file directly   # index.html is self-contained (no server, no external asset)
python3 preview/build.py       # rebuild index.html after editing panel.html / preview.js / preview.css
~/Projects/multimedia-gkps-klender/.venv/bin/python preview/probe.py   # the numbers in spec's UI/UX
python3 preview/build_tune.py  # rebuild tune-built.html after editing tune.html / tune.js / tune.css
```

## Motion tuning harness — `tune-built.html`

A second, self-contained page for finding a comfortable duration/curve pair. Two panes replay the
same ~460 px move on real dock rows; each has its own duration slider, easing select and preset
chips. **Play both** runs them together, the **Slow** buttons stretch time 2×/4× without changing
the curve, and each pane prints elapsed time, scrollTop, instantaneous px/s and a speed trace.
Space plays, `r` resets. Presets: current 190, brisk 260, gentle 320, smooth 400, sine 400,
slow 500. The product's current candidate is 400 ms soft in-out — half sine, half quintic
smootherstep — which is the *smooth 400* preset.

`index.html` is generated. Its stylesheet is a verbatim copy of `tokens.css` + `obs-dock.css` at the
branch's commit, inlined by `build.py` so the page can never drift from them silently — re-run the
build after touching either. Self-contained because the chat's preview pane loads a page as
`srcdoc` in a sandboxed frame, where a relative `<link>`/`<script>` never resolves.

`?idle=<ms>` shortens the idle clock (default 15 s) so a probe can walk the condition matrix in
seconds; the harness uses 800 ms.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| the new control | look at the transport row | a crosshair between Previous and Next, the same 40 × 40 navbtn face |
| following | press Next three times with the dock showing the service on air | "mode: following" and the live row lands 0 px off the pane's centre on each step |
| browsing | scroll the list, then press Next or Back | "mode: browsing"; the live row changes but `scrollTop` does not |
| back to following | press the centre control, click an item or the sticky Next band, or let the idle elapse fire | "mode: following"; the next advance centres again |
| sticky Next band from browsing | scroll, then click the sticky "Next" band | "mode: following"; the live pointer moves to the next entry, its first row is marked, and that row centres |
| browsing by expansion | click another entry's header, then press Next or Back | "mode: browsing"; the list stays put |
| centred by the control | press it with the live row off the middle | the list glides until the live row's centre is on the pane's centre (~190 ms, no bounce) |
| centred by an item click | click any row inside an open block | that row goes on air and the list centres it |
| the live row out of view | "Scroll the live row out of view" | the list stays where it is — no automatic centring |
| the idle elapse | leave it alone for 15 s with every condition true | the list glides the live row back |
| held by a condition | tick "a layer is open", or "another entry's header is open", or untick the display / the browsed service | the idle elapse passes and nothing moves |
| the clock ignores a moving pointer | move the pointer across the dock mid-count, without pressing | "N s of stillness left" keeps falling and the elapse still centres |
| the clock restarts on a scroll or a click | turn the wheel, click the page, or press and hold a button | the count jumps back to 15 s; a held button suspends it ("held") and restarts it on release |
| nothing else moves the list | press Previous / Next / the edition chip / the eye | `scrollTop` in the readout does not change |

## What this preview is not

It is not the product: the entry list is a fixture (a 34-entry service), the six conditions are
controls on the page rather than the dock's own DOM, and the "mode: following / browsing" line is a
preview-only readout — the dock itself has no mode indicator. Crossing advances snap the blocks
instead of running the product's 230 ms morph, so the preview proves where the list lands, not the
crossing's motion. It shows the control's placement and face at real size, the list's own glide, and
every state the decision turns on.
