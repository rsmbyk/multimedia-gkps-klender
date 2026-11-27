# Preview: rail fetch feedback

`combined.html` is the draft for this slice: the reading shell from spec 243's accepted static
preview in dark mode at 1440×900, with a 152px control bar carrying the driver.

## States

| State | How to reach | Expected readout |
| --- | --- | --- |
| Idle | open the page | status idle, no bar, no lock |
| Loading | click the Search or Media Library rail tile, or the matching toolbar button | svg opacity `0.45`, `aria-disabled=true`, stage `aria-busy=true`, bar 3px at stage y=0, destination-shaped placeholder present (Search results, Search home via the "home" toggle, or Media Library) |
| Settled | wait for the chosen delay | tile unlocked, bar hidden, placeholder replaced by the real destination |
| Reduced motion | set `prefers-reduced-motion: reduce` and replay | bar sweep stops, lock and placeholder remain |
| Quick response | choose Instant (0ms) | pending state may not paint, no residue |

The three earlier candidate pages (`option-a.html`, `option-b.html`, `option-c.html`) are kept
for the record and reachable from `index.html`; arrow keys and the toolbar links move between
pages.

## Rebuild and verify

```bash
python3 build_previews.py
~/.hermes/skills/software-development/obs-browser-surfaces/scripts/verify-chat-preview-frame.py combined.html
~/Projects/multimedia-gkps-klender/.venv/bin/python probe.py
```

`probe.py` writes screenshots to `shots/` (gitignored) and prints the measured values quoted in
the spec's `## UI/UX`. The pages are static simulations of a delayed fetch; no application
code is changed by this preview.
