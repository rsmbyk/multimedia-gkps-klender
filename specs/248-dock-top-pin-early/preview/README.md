# Preview — spec 248 (earlier top pin)

**Live preview**: `http://127.0.0.1:8793/obs/dock` — this worktree's own code with the change
applied, served by `serve.sh` against the real compose DB.
**Before build**: `http://127.0.0.1:63404/obs/dock` — the compose `web` container, unmodified
`develop`, same DB. The change is state on a live list, so a static replica cannot show it.

## Driving the states

1. Open the dock and click the first service row in the picker.
2. Click a deep entry with a long block (entry 26 in the first service) and click its first screen
   row so it is on air. The header may be below the fold; that is fine.
3. Scroll the runner list down slowly with the wheel:
   - **Before**: the live label stays in flow until the whole block clears the top, then a pinned
     copy appears. Between those points the header is already clipped but no pin has taken over.
   - **After**: the moment the header's own top reaches the top edge, a faithful copy takes over
     and the real header stops painting underneath it. The copy sits exactly where the sticky
     header was, so the takeover has no hop.
4. Keep scrolling: the copy stays at the top edge, the NEXT band stays at the bottom, and the
   bottom pin keeps its own behaviour.
5. Click the pinned copy: the list glides back to the live row, the screen on air does not change,
   and following returns. Hand-scrolling back gives the edge to the native header on that frame.
6. Enable `prefers-reduced-motion: reduce` and repeat step 3: the pin lands in the same paint.

## Commands

```sh
./serve.sh                                     # worktree code on 8793 (collectstatic + runserver)
$VENV python probe_boundary.py http://127.0.0.1:63404 before-boundary.json
$VENV python probe_boundary.py http://127.0.0.1:8793 after-boundary.json
```

## Measured (probe_boundary.py, 420 × 860, dark, 1×; first service, entry 26 live)

| Reading | develop (63404) | slice (8793) |
| --- | --- | --- |
| First pin visible at scrollTop | 1164 | **1056** |
| Live block top at takeover | -110 px | **-2 px** |
| Live block bottom at takeover | -2.31 px | 105.69 px |
| Real header top at takeover | -40.31 px (off) | **0 px** (at edge) |
| Pin top / bottom | 0 / 38 px | 0 / 38 px |
| Pin label | `26Entri 26` | `26Entri 26` (exact) |
| Frames sampled | 490 | 490 |
| Real header while pinned | visible, but already off-screen | **hidden (covered), so never a second header** |
| Boundary mismatches | 0 (old rule) | 0 (new rule) |
| Takeover hop | — | 0 px (pin top = header top at takeover) |
