# Preview: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`
**Shape**: `static`
**Open**: `specs/162-song-verse-empty-state/preview/preview.html` — open the file directly

## Run

```sh
# rebuild from the app's own rendered fragment (needs a dev server on :8842)
python specs/162-song-verse-empty-state/preview/build_preview.py

# or from a saved fragment, with no server
python specs/162-song-verse-empty-state/preview/build_preview.py --fragment /tmp/frag162.html
```

Then open `preview.html` in a browser. `shots/` holds the two full-page renders the numbers in
`spec.md` were read from (`preview-desktop.png` 1440×1000, `preview-420.png` 420×1000).

## States to click through

Four rows, each pairing the same form as **Today** and **Proposed**:

| State | How to reach it | What to look for |
| --- | --- | --- |
| no song | row 1 — both columns | `Pick a song first`, disabled, in both columns |
| a song with verses | row 2 — both columns | `All verses`, enabled, three checked boxes, in both columns |
| a song with no verses | row 3 — compare the columns | left `Pick a song first`; right `This song has no verses`; both disabled; the trigger is 38px tall in both |
| the save refusal | row 4 — compare the columns | left `Keep at least one verse in the service.`; right `This song has no verses: pick another song.` |
| responsive | resize below 860px | the two columns stack; the line stays one line (the field is 356px wide, the line 158.52px) |

## Live or static

**Static**, and it has to be for the pre-gate state: the fragments are the server's own render of
`/editor/entry/new/?kind=song&tatib=149`, wrapped in the real `<div class="editor">` shell with the
real `tokens.css` and `components.css`, so every class, size and colour is the product's. What the
page does not show is what fetches: the song list and the verse checkboxes are drawn by script in the
product, and here the two states that need them (a song picked, a song picked with verses) carry the
markup that script would produce.

After the slice is implemented the same states are reachable live at
`/tatib/149/` → `+ Song` (the song list is fetched there).
