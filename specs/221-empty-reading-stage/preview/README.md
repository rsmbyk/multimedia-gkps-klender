# Deleted-record empty stage preview

**Spec**: `specs/221-empty-reading-stage/spec.md`
**Shape**: static
**Open**: `specs/221-empty-reading-stage/preview/index.html` opened directly (file:// is fine)

## Run

```sh
# Open specs/221-empty-reading-stage/preview/index.html in a browser; no server is needed.
```

The page is the public reading shell captured from the served app on `/songs/book/17/` — real
templates, class names, tokens, stylesheets and bundled logo — with the stage article replaced by the
same `.read` article the proposed server state renders: the empty song view's `.entry__empty` block
with a generic 38px empty-screen icon above the 20px heading "Nothing open." and the subtitle "Choose a song or
service from the list." The new rules (`.entry__empty-icon` and the stage-centred block) are in a preview-only style block
and land in `components.css` at Implement. Preview-only links are stripped; the one script at the end
only switches the two states, the theme and the readout.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Before — search landing | Initial load, or **Before — search landing** | Today's post-delete landing: the logo, search field and empty results area fill the stage (`data-read="off"`, `data-home="landing"`). |
| After — nothing open | **After — empty reading stage** | The stage keeps reading mode (`data-read="on"`, `data-home="reading"`): `.read` holds a centred icon above "Nothing open." and the subtitle below it; no search field or logo. Both side panels stay where they were. |
| Dark theme | **Switch to dark theme** | The same two states with the project's own dark tokens. |
| Narrow / phone | Resize to 390×844 or 320×568 | The block stays centred in the stage; drawers and toolbar keep their existing geometry. |
| Wide | Resize to 720×900, 1440×900, 1920×1080 | The block stays centred in the stage at every width; no horizontal overflow. |

## Measured on the preview

| Viewport | Rail | First panel | Second panel | Stage | `.read` before | `.read` after | Search home before |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1440×900 | 80px at x=0 | 296px at x=80 | 416px at x=376 | 648px at x=792, h=900 | display none | 648×108 centred at y=396 | 520×796 at x=856, y=40 |
| 390×844 | off-canvas | off-canvas | off-canvas | 390px at x=0, h=844 | display none | 390×108 centred at y=368 | 354×704 at x=18, y=76 |

Inside the block: icon 38×38 at (1097, 396) desktop / (176, 368) narrow; heading 140×26 at y=444 /
y=416; subtitle 287×24 at y=480 / y=452. The block centre is exactly the stage centre (x=1116,
y=450) / (x=195, y=422).

`scrollWidth === innerWidth` in every state at 390, 720, 1440 and 1920. The after state adds one icon
rule only; the centred block, heading and subtitle reuse rules the empty song view already ships.

## Live or static

Static is appropriate here: the change affects which existing stage state is painted and which URL
reaches it; it adds no data, API or fetch. The state toggle uses the shell's own `data-read`/`data-home`
attributes and the project's own CSS rules, so what is shown is what those attributes paint. The
server-side flag, the delete POST and the history replacement are outside a static page and are
verified against the live app during implementation.
