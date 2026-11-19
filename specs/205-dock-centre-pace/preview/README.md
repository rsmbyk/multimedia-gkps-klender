# Preview: the dock's re-centring keeps pace with fast advancing

**Spec**: `specs/205-dock-centre-pace/spec.md`
**Shape**: `live` — the real dock served from this worktree. The change is motion on the live list
(the glide and the crossing morph), so a static replica cannot show it; the preview is the product's
own `/obs/dock` running the slice's code.

## Open

```sh
# the slice dev server (already running on 8765 from this worktree):
http://127.0.0.1:8765/obs/dock
# develop ("before") for comparison, served by the compose web container:
http://127.0.0.1:63404/obs/dock
```

Open **Ibadah Pace Probe** (the 60-entry fixture), click any screen row to put it on air, then hold
ArrowDown to advance fast. The centre control (crosshair between Previous and Next) re-centres on
demand. Compare the two URLs side by side: the slice's list keeps up with fast stepping; develop's
lags and swings.

## Measure

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python probe.py --url http://127.0.0.1:8765 --label after
~/Projects/multimedia-gkps-klender/.venv/bin/python probe.py --url http://127.0.0.1:63404 --label before
```

`probe.py` prints the single-move curve and the rapid-advance metrics (mean live-row offset, max
frame step, reversals, settle) and writes raw frames to `shots/` (gitignored). The numbers in
`spec.md`'s UI/UX come from these runs.

## Sampling pitfall (why the probe reads the way it does)

A persistent in-page rAF **or** setTimeout loop started via Playwright `evaluate_handle` reads a
**frozen** `scrollTop` in this headless Chromium — even a direct `scrollTop = 500` write is invisible
to it, while individual fresh `evaluate` reads are live. So every frame in `probe.py` is its own
fresh `evaluate` that sleeps in-page first, then reads in the resolving task. A probe that samples
with a long-lived loop reports zero motion and reads as "the glide is dead" when it is not.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| single centring | scroll the list away, press the crosshair | the live row glides to the middle over ~200 ms, no bounce |
| fast advancing | hold / repeat ArrowDown with the service on air | the row stays near the middle; less lag and smaller swings than develop |
| a crossing | ArrowDown from an entry's last screen into the next | expand, collapse and scroll move as one motion on the same pace |
| hand toggle | click a non-live entry's header | its block morphs over 230 ms on its own ease — unchanged |
| reduced motion | OS/browser reduce-motion on | every centring is an instant jump |

## What this preview is not

It is the product's own dock, not a replica — but the fixture is a synthetic 60-entry service, and
the per-crossing collapse-clamp reversal is still present (this slice changes the glide pace, not
that mechanism).