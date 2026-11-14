# Preview — a preview's play shortcut paints nothing on the dialog's edge

**Static preview at `specs/159-preview-body-ring/preview/preview.html`** — open it directly; there is no
server and nothing is fetched. Regenerate with

```
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/159-preview-body-ring/preview/build_preview.py [url]
```

The dialog, the player and the body are the product's own markup, captured from a running page
(`/tatib/144/` by default) after the dialog drew its own content, so the filenames, the icons and the
controls are the product's, not a transcription. `assets/{tokens,components,fonts}.css` are frozen at
`24a6d6d2`, the commit this slice was cut from, because the **Now** panel has to keep drawing the
shipped ring after the fix reaches the working tree.

## What it shows

Three panels, one dialog at a time, over the arena the page owns:

- **Now** — the shipped code: the ring appears on the first key press and stays.
- **A** — the shortcut takes the ring away. A preview opened from the keyboard keeps it until the
  first space press.
- **B** — the body wears no ring from open until the reader reaches it with Tab.

**Adopted: A** — chosen from this page by the owner on 2026-10-29. B stays here as the record of the
alternative, not as a live option.

Each panel offers both open paths, both entries, and a live readout of `:focus-visible`, the computed
outline, the dialog's and body's boxes, and the player's state. The two candidate rules are the only
CSS this page adds:

```css
.preview__body.is-shortcut:focus-visible { outline: none; }   /* A */
.preview__body.is-quiet:focus-visible    { outline: none; }   /* B */
```

## What it cannot show

The companion's media bytes. The players here toggle a label instead of decoding anything, so no
`<video>` or `<audio>` source is set — the ring is the subject, and the browser's own focus rules
produce it, not the stub. Everything else is real: the dialog box, the body's padding, the controls,
the type.

## Measured

Headless Chromium, 1512 × 900, panel × entry × open path, read from the page's own readout:

| state | Now | A | B |
| --- | --- | --- | --- |
| pointer open | none | none | none |
| pointer open + space | **ring** | none | none |
| keyboard open | ring | ring | **none** |
| keyboard open + space | ring | **none** | none |
| Tab to the body | ring | ring | ring |
| click in the body, then space | ring | none | none |

The ring, when it is drawn: `2px solid rgb(28, 92, 60)` at offset `-2px`. Dialog and body are the same
box at every width — video `920 × 852` at (296, 24) and audio `620 × 256` at (446, 322) in a 1512 × 900
window; `384 × 607` and `384 × 248` at a 420px window, where Chrome's own dialog rule caps the 388px the
stylesheet asks for.
