# Preview — spec 208 (dock stuck corner)

**Live preview**: `http://127.0.0.1:8767/obs/dock` — the worktree's own code with the fix
applied, served by `serve.sh` against the real compose DB (the team's services).
**Before build**: `http://127.0.0.1:63404/obs/dock` — the compose `web` container, unmodified
`develop` at `c385a194`, same DB. The change is state tracking on the live list, so a static
replica cannot show it; both builds are the real code path.

## Driving the states

### The corner fix (US1–US3)

1. Open the dock, click the second service row (the 1 November service holding **HAL 1**,
   7 baits / 21 screens — any long song works).
2. Click **HAL 1**'s header to open its block, then click its **first screen row** — the song
   goes on air, the header sits in flow with round corners.
3. Press **ArrowRight** repeatedly to bait 7 (or **Shift+End** once). The list glides, the
   header pins flush at the list's top edge. Let it rest — no hand scroll.
   - **Before**: pinned, top corners still round (9 px). **After**: pinned, flat top (0 px).
4. Press **Ctrl+Home** — crosses to the first entry, whose header lands in flow.
   - **Before**: in flow, top corners square (0 px). **After**: in flow, round (9 px).
5. Any hand scroll reconciles both builds — the control that proves the toggle itself works.
6. With the header pinned, click a closed header **above** the live entry: its block opens and
   pushes the live header down. Before keeps the flat top; after rounds it with no scroll.

Every state is reachable by hand; the keyboard acts never pre-scroll the list.

### The bottom pin (US4)

1. Open the **11 Oktober** service (12 entries). Open entries 2 (HAL 238) and 3 (HAL 234) by
   hand, then make **HAL 5** (entry 11) live — its header lands far below the view. The **NEXT
   band** is always visible and pinned at the bottom edge; the live header's **pin** clips in only
   when the header's bottom reaches the NEXT band's top — no earlier, so it doesn't add a second
   header-height of chrome while the header is still clear (too tall). At that boundary the clone
   sits exactly over the real header.
2. Scroll until HAL 5's header's bottom reaches the NEXT band's top: a faithful copy of the header
   (number + name + Bait subtitle + chevron, flat bottom / round top corners) **abuts directly
   above the NEXT band** — the two stacked bands, no gap, no double. It stays as the header passes
   off and is fully below.
3. **Click the pin**: the list glides back to the live screen row (centre-control act) — the screen
   on air does not change, following returns, the pin disappears as the header comes back into view.
4. The NEXT band is a list-level slot, so it is never caged by its block: it is **always shown**
   while a next entry exists, regardless of that row's position. The runner list fills the
   scrollport (`min-height:100%`, flex-bottom slots, no body bottom padding) so the band pins flush
   at the edge **even when the whole list fits** (1920×1200: 1033–1068 px = the edge), not dangling
   after the last row with a gap below.
   With the **last** entry live there is no NEXT entry, so the band is hidden and the pin (while
   the header is off) takes the edge itself.

## Commands

```sh
./serve.sh                                   # worktree code on 8767 (collectstatic + runserver)
./run-tests.sh tests.e2e.test_dock_stuck_corner          # the twelve pins (throwaway test_gkps208)
./run-tests.sh tests.e2e.test_obs_dock tests.e2e.test_dock_open_reset \
               tests.e2e.test_obs_dock_follow tests.e2e.test_dock_text_wrap   # regression
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python probe.py http://127.0.0.1:63404 shots/before
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python probe.py http://127.0.0.1:8767 shots/after
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python probe_bottom.py http://127.0.0.1:8767 shots/bottom
```

## Measured (probe.py, 420 × 860, dark, 1×; HAL 1, 21 screens)

| State | Build | Δ top (px) | `.is-stuck` | Top radius |
| --- | --- | --- | --- | --- |
| First screen, in flow | both | 172 | absent | 9 px |
| Advance to bait 7, at rest | develop | 0 (pinned) | **absent** | **9 px** |
| Advance to bait 7, at rest | slice | 0 (pinned) | present | 0 px |
| One hand scroll (control) | both | 0 (pinned) | present | 0 px |
| Ctrl+Home to entry 1, at rest | develop | 4 (in flow) | **present** | **0 px** |
| Ctrl+Home to entry 1, at rest | slice | 4 (in flow) | absent | 9 px |

Per-frame during the advance (class must equal geometry's verdict on every frame):
develop **328 / 328 pinned frames mismatched** (404 sampled); slice **0 / 328** (405 sampled).

Raw screenshots: `shots/before/`, `shots/after/` (a-pinned, control-pinned, b-inflow).

## Verification log

- **Red on develop** (worktree at `c385a194`, before the fix): all six pins fail on their own
  assertions — pinned Δ 0 px / no class / 9 px; in-flow Δ 4 px / class / 0 px; hand-toggle
  Δ 789 px / class / 0 px with zero scroll events; 38 glide frames pinned with no class;
  old live row keeps the class across the crossing; reduced motion pinned with no class.
- **Green on the slice**: 6/6 (`run-tests.sh tests.e2e.test_dock_stuck_corner`).
- **Regression** (the four dock modules, 55 tests): 54 green + 1 pre-existing machine-local
  red — `test_the_chevron_marks_the_state_and_the_eligible_rows`, a pointer race recorded as
  ITEM-220: the unmodified base fails 4 of 5 alone runs (the slice's JS stashed), the slice
  3 of 5; a diagnostic timeline caught the pointer on the live header wearing the live-hover
  tone (`color(srgb 0.34149 0.36 0.409569)`) the pure-token wait can never match. CI green
  through spec 206. Not caused by this slice; the product behaviour is FR-011's.
  **Final pass on the presented code: 55/55 green** — the race is intermittent and drew green.
  **Combined pack (fix + bottom pin): 66/66 green** across the four dock modules and
  `test_dock_stuck_corner` (11 pins).
- The toggle-morph frame reads the pin geometry **before** its height write (clean layout at
  frame start, no forced mid-frame flush); the glide paths read after the write so the corners
  match the geometry on every sampled frame.
- **The bottom pin (US4)**: five more pins red on the strip-less tree (strip absent —
  `stripVisible: false`, the click test errors on the null node) → 11/11 green with the strip.
  Two geometry lessons built into the design: the slot is **list-level** (inside the live li
  it would share the band's sticky cage and could not pin while the whole block is below the
  view — measured: the band itself sits at its li's top, off-screen, in that state), and the
  strip's inset sits above the band's **measured top** (in the shallow partial-cut window the
  band cannot sit flush either). Real-data probe: strip flush at 0 px / radius 0 px fully off;
  strip bottom == band top (−13.88 px) partial; 0/47 mismatched frames on both click-glides;
  display state byte-identical; live row 0.48 px off centre (deep entry) / end clamp (last
  entry); following returns.
