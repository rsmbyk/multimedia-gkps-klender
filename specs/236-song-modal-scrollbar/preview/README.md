# Preview — spec 236

`index.html` is a self-contained static preview: open it directly (`file://`), in a
browser tab, or in the chat preview. It is assembled from the product's own materials —
the real rendered `#editorModal` markup captured from the running app (`snippets/`) and
the worktree's `static/styles/design/` CSS copied verbatim into `css/before/` and
`css/after/`. All four stylesheets are inlined into the single HTML file by
`build_preview.py`: the chat's `::preview` frame loads the file as `srcdoc` in an
opaque-origin sandbox, so any relative `<link>` would fail there.

The only product declaration changed is in `css/after/components.css`:

```css
.editor { … overflow: clip; }
```

The before column loads the same patched stack but scopes that one declaration back
to the base value (`auto`) so both states can be compared on one page. `preview.css`
only lays the dialogs out in normal flow (`position: relative`) and adds the readouts;
it does not change their box internals. `build_preview.py` regenerates `index.html`
from the snippets and stylesheet copies.

## States

| State | How to reach it | What to read |
| --- | --- | --- |
| New song — before / after | top-left / top-right panel | before: 5px scrollbar gutter, dialog `246/256px` (10px overflow), `overflow-y:auto`; after: `0px` gutter, `overflow-y:clip`, same box |
| Edit song with verses — before / after | lower panel in each column | `410/410px`, no gutter in either state — this state was already clean |
| Dark / light | **Switch to light** button (default dark) | same geometry and no-dialog-scroll rule in both themes |
| Narrow / tall | resize the browser so the `86vh` cap engages | `.editor__content` remains the scrollport; the dialog's own edge stays clean |

## Verified measurements (1366×900, dark theme)

| Panel | dialog client / scroll height | gutter (`offsetWidth − clientWidth`) | computed `overflow-y` |
| --- | --- | --- | --- |
| `new-before` | 246 / 256px | 5px | `auto` |
| `edit-before` | 410 / 410px | 0px | `auto` |
| `new-after` | 246 / 256px | 0px | `clip` |
| `edit-after` | 410 / 410px | 0px | `clip` |

The before New-song numbers match the live app on the base commit exactly; the live
Edit-song panel likewise measured `410/410px`. `scrollHeight` still reports 256px
after the fix — clipped overflow continues to count — so the acceptance observable is
the missing gutter and the computed `overflow`, not a smaller `scrollHeight`.

## Chat-frame preflight

Rebuild and re-check before every `::preview` use:

```sh
python3 specs/236-song-modal-scrollbar/preview/build_preview.py
python3 ~/.hermes/skills/software-development/obs-browser-surfaces/scripts/verify-chat-preview-frame.py \
  specs/236-song-modal-scrollbar/preview/index.html --width 900
```

Current result: **PASS** — 1 inline stylesheet / 1100 rules, 0 external subresources,
both dialogs styled and placed as in a browser tab. The first build used four `<link>` tags
and failed here with 0 rules, which is exactly what broke in chat; never repeat that.
