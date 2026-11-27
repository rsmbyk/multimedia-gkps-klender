# Preview: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md`
**Shape**: static (with a live comparison route)
**Open**: `specs/224-empty-song-add-verse-row/preview/index.html` opened directly

## Run

The static page needs no server: open `index.html`. To rebuild it from the live pages and
re-measure the current product:

```sh
bash specs/224-empty-song-add-verse-row/preview/serve.sh   # worktree on 127.0.0.1:8770
.venv/bin/python specs/224-empty-song-add-verse-row/preview/build.py
.venv/bin/python specs/224-empty-song-add-verse-row/preview/probe.py
```

The harness reads the compose database at 127.0.0.1:59075 and serves this worktree's code;
`serve.sh` obtains its credentials from the web container at runtime.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| empty — placed (proposed) | default, or button in the top-right switcher | one `Add verse` inside the invitation; its title at y≈254, level with the Tata Ibadah empty title |
| empty — gate only | switcher button | one button, invitation back at the top of the body (y=153.9) — shows what the template fix alone would do |
| empty — before (current) | switcher button | two identical `Add verse` buttons, the stray one on its own 38px row above the invitation |
| three verses (unchanged) | switcher button | three verses and one `Add verse` row at the bottom, exactly as the live page paints it |
| live before | `http://127.0.0.1:8770/songs/1731/` | the current duplicate on the real server-rendered page |
| live with verses | `http://127.0.0.1:8770/songs/1387/` | the unchanged after-the-last-verse row |
| live reference | `http://127.0.0.1:8770/tatib/145/` | the Tata Ibadah empty title at y=253.5 that the song state matches |

## Live or static

**Static** here is the live page's real markup and real stylesheet captured from the two
routes; the four read-body fragments sit in `<script type="text/plain">` blocks and the
switcher only swaps them; the placed state also enables a `<style>` block carrying the candidate
quarter-band CSS. The proposed fragments are the current ones with exactly the `.verse-add` element
removed — the template gate being reviewed, not a restyled imitation. `build.py` re-captures from
the live server so the preview cannot drift from the product.

**What a static page cannot show:** anything that fetches — the server-side `{% if %}` itself,
the write endpoints and uploaded media. The live routes above and `probe.py` cover those; the
measurements are saved in `preview/measurements.json` and screenshots in `preview/shots/`.

## What is not a preview

A screenshot, a static image and a recording are not previews.
