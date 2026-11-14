# Preview: a Tata Ibadah sidebar row is three lines, ellipsized

**Spec**: `specs/135-tatib-sidebar-row-clamp/spec.md`
**Shape**: static previews at `specs/135-tatib-sidebar-row-clamp/preview/`

- `cases.html` — **every display the cap can produce**, one row per case, at the real panel width
  (415px) and at the narrow width a 390px window gives it (313px). Built by `build_cases.py`.
- `after.html` — the real `/tatib/144/` page with its own rows re-marked: the clamp in situ.

Open `after.html` in a browser. It is the real `/tatib/144/` page taken from this worktree's own
server — shell, rail, panels, stage, type, tokens and stylesheets — with three edits: its scripts
removed (so nothing rewrites the panel), every contents row re-marked into the proposed single
clamped block, and two fixture rows appended for the cases the live service does not carry.

The proposal itself is the `<style>` block the builder appends, plus the row markup:

```html
<span class="songrow__t songrow__t--song">
  <span class="songrow__heading">…</span>
  <span class="songrow__verses">Bait 1-3</span>
</span>
```

A text row is the same clamped block with its lines separated by `<br>`. A song keeps its heading and
its `Bait …` line as two blocks inside the box, so the heading can be clamped to two lines while the
`Bait …` line stays third. No `<br>` between them: it would add a fourth line.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| A song with a 64-character title | row 1 (`a…581. Sangap di Jahowa`) | heading on two lines, `Bait 1-3` third |
| A song with a short heading | rows 2, 10, 12 (`HAL 7`, `HAL 1`) | heading, then `Bait …` |
| A title that must not be cut at 60 | row 17 (fixture, 64 characters) | the whole title, ending `Setia`, on two lines |
| A body longer than three lines | row 16 (fixture) | three lines ending in `…` |
| A wrapped title | row 8 (the audio file) | two lines, no ellipsis |
| One-line rows | rows 3–5 (passage, two media) | one line, no ellipsis |
| A legacy row | row 6 (`VOTUM, INTROITUS, DOA`) | title, then its first body line, italic |
| Selected row | click any row | same height, tinted |
| Narrow window | resize to 390×844 | the panel is 313px; a 64-character title takes three lines |

## Rebuild and measure

```sh
# from this worktree, with the compose database reachable
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8769 --noreload
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/135-tatib-sidebar-row-clamp/preview/build_preview.py
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/135-tatib-sidebar-row-clamp/preview/build_cases.py
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/135-tatib-sidebar-row-clamp/preview/probe_rows.py
```

`probe_rows.py` prints, per viewport, the panel's width and each row's label height, row height,
computed line-height, clamp and whether its content is taller than its box — the numbers quoted in
the spec's `## UI/UX`.

## What this preview cannot show

The server sends the text the row draws, so the literal `…` a *long body* earns is the builder's
fixture, not the server's own (the code is unchanged at gate 1). The draft's re-render after a save,
the drag copy and the saved-library page are behaviour, not layout, and are verified by the tests
named in `plan.md`.
