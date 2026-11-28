# Spec 255 preview — saved-draft indicator

Self-contained page assembled from the repo's `tokens.css` and `components.css` plus the real
`read__project` button markup. Open `index.html`; the toggle compares the saved and no-draft states.
`build_preview.py` rebuilds it; `probe.py` measures all three variants in both states.

## Measured (1000×900 viewport, dark, 2× device pixels)

| Variant | Width when saved | Mark | Accessible name |
| --- | --- | --- | --- |
| A — corner dot | 135.8 px (unchanged) | 7×7 at +124.8, +4 | “Use template, draft saved” |
| B — label suffix | 217.6 px (+81.8) | none | “Use template · draft saved” |
| C — inline dot | 147.8 px (+12) | 6×6 at +15, +14 | “Use template, draft saved” |

All three are 34 px tall. Probe: PASS, zero console errors. Chat-frame verifier: PASS.

## States

1. **Saved draft ON** — every variant shows its mark and names the saved draft.
2. **No draft** — every variant is the plain button; no mark, name “Use template”.
3. **Chosen at Gate 1** — **A**, corner dot. B and C stay in the page for comparison.