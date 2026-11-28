# Preview: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md`
**Shape**: `static`
**Open**: `specs/258-live-reading-freshness/preview/index.html`

## Run

none: open the file directly. It links the repo's real `tokens.css`, `fonts.css` and `components.css` by relative path.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Current page | default | controls at full opacity, no badge |
| Invalidated | click `Invalidated` | badge at the top centre, Reload button, all page controls muted in place |
| Sidebar insert | click `Sidebar insert` | new row animates into its list position |
| Dark | click `Dark` | all three states with the product's dark tokens |

The preview keeps hover-only controls visible so their disabled state can be reviewed; the product still reveals them on hover or focus.

## Measured with the repo's Playwright

`probe.py` (run with the main checkout's `.venv/bin/python`) writes `shots/probe.json` and screenshots:

- 1440×900: badge 289×48 at (576, 64), Reload button 64×30. The 64px offset is preview-only — the product's candidate rule is `top: 12px`, clear of this page's toolbar.
- Disabled add control: 58×28 at (778, 177), opacity 0.45, cursor `not-allowed`; its box does not move between current and invalid states.
- Row insertion: 303×38, `animation: 0.18s cubic-bezier(.2,.8,.2,1)`; in-page rAF sampling sees opacity 0 and `translateY(-6px)` at the start, reaching opacity 1 and no transform by ~250 ms.
- Light and dark produce the same geometry; colour comes from the existing tokens.
