# Preview — spec 242 (dock top pin)

**Live preview**: `http://127.0.0.1:8793/obs/dock` — the worktree's own code with the change
applied, served by `serve.sh` against the real compose DB (the team's services).
**Before build**: `http://127.0.0.1:63404/obs/dock` — the compose `web` container, unmodified
`develop`, same DB. The change is state on the live list, so a static replica cannot show it.

## Driving the states

1. Open the dock, click the **first service row** in the picker, and wait for the runner.
2. Pick a deep entry with a long block (entry 26 in that service works) and click its first
   screen row, so it is on air.
3. With the list at the top, the live header is far **below** the fold — the spec 208 **bottom
   pin** is visible on both builds. The new top pin is hidden.
4. Scroll to the bottom of the list (`End` on the scrollbar, or a wheel gesture). The live
   entry's whole block is now above the fold:
   - **Before**: the live label is gone; nothing is pinned at the top.
   - **After**: a faithful copy of the live header stands flush at the top edge — number, name,
     subtitle, chevron, selected face, flat top / round bottom. The NEXT band and the bottom pin
     behave exactly as before.
5. Click the pinned copy: the list glides back to the live row, the screen on air does not change,
   and following returns. The copy disappears on the frame the real header takes the edge back.
6. Hand-scroll back as an alternative: the copy yields to the native sticky header, never showing
   alongside it.

Every state is reachable by hand. Reduced motion can be checked by enabling the OS/browser
setting and repeating step 4 — the pin paints in the same paint.

## Commands

```sh
./serve.sh                                    # worktree code on 8793 (collectstatic + runserver)
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python probe_top.py http://127.0.0.1:63404 shots/before
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python probe_top.py http://127.0.0.1:8793 shots/after
```

## Measured (probe_top.py, 420 × 860, dark, 1×; service 1, entry 26 live)

| State | Build | Top pin | Top offset | Radius (top/bottom) | Label |
| --- | --- | --- | --- | --- | --- |
| Header in view, list at top | develop | no | — | — | — |
| Header in view, list at top | slice | no | — | — | — |
| Live block wholly above, list at bottom | develop | **no** | — | — | — |
| Live block wholly above, list at bottom | slice | yes | 0 px from the scrollport edge | 0 px / 9 px | `26 Entri 26` (exact match) |

- Bottom pin: visible at the top-of-list state on both builds, hidden at the above-fold state on
  both — the two pins never compete.
- Click of the slice's pin: **25 sampled frames, 0 mismatched** between visibility and the
  block's geometry; display state byte-identical; live row **0.48 px** from the centre; following
  `true`.
- Raw screenshots: `shots/before/`, `shots/after/` (`top-pin.png`, `after-click.png`).
