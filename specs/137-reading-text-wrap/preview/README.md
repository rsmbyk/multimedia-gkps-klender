# Preview: a reading page's text wraps at its pane

**Spec**: `specs/137-reading-text-wrap/spec.md`
**Shape**: static previews at `specs/137-reading-text-wrap/preview/`, plus a live route

Four pages, each as a pair built from the same server response:

| Pair | Page | What it carries |
| --- | --- | --- |
| `before-tatib.html` / `after-tatib.html` | `/tatib/149/` | the reported case: a 64-character title (the column's own limit), and a Text entry whose body is a pasted Drive link |
| `before-songs.html` / `after-songs.html` | `/songs/1817/` | the reported case: a song title that is one unbroken run plus a name |
| `before-bible.html` / `after-bible.html` | `/bible/1/1/` | a pericope heading and a verse, **both fixtures** (`data-fixture="1"`) — the live chapter has no long value |
| `before-search.html` / `after-search.html` | `/search?q=ibadah` | the first result's title and meta, **both fixtures** — the live rows are short |

The Bible and search fixtures run longer than the columns allow (a `Verse` title caps at 128, a
service or song name at 64), so the case is visible at desktop widths in the picture. The reachable
case is the 64-character one: a search row overflows below roughly 1000px, which the tests measure at
820 and 390. The Tata Ibadah and song pages use the live records — no fixture there.

`after-*` is the worktree as it stands: the rule is in `components.css`. `before-*` is the *same*
page with that rule's one declaration restored to `overflow-wrap: normal` — so the pair differs by
one property and not by two builds. Open either file directly in a browser.

Everything else is the project's own: shell, rail, sidebars, stage, type, colours, tokens and
stylesheets (pointed at `../../../static/`). Scripts are removed so nothing rewrites a panel, and
the shell is opened to `data-nav="open" data-ch="open"` — `data-read="off"` on the search page, so
its results list is the surface on screen.

**Live preview**: `http://127.0.0.1:8768/tatib/149/` and `/songs/1817/` from this worktree — the
real app, so the Preview modal (which the static page cannot open) is reachable there.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| The reported Tata Ibadah title | `before-tatib.html` | one line, painted out of the pane to the right; the document scrolls sideways |
| The same title, wrapped | `after-tatib.html` | 4 lines inside the 400px box, nothing past the pane, no sideways scroll |
| A body paragraph holding a URL | both Tatib files, under the title | `before`: 215px past the box; `after`: 2 lines inside it |
| The reported song title | `before-songs.html` / `after-songs.html` | 2 lines ending off-pane → 3 lines inside the pane |
| A Bible pericope heading | both Bible files, narrow the window below ~1300px | `before`: past the pane; `after`: wrapped |
| A search result | both Search files | `before`: the row's title runs 614px past the row; `after`: wrapped |
| A short title is unchanged | any `before`/`after` pair at 1440 | the title is one line and the same height in both |
| Truncation still truncates | the left-hand service list on either Tatib file | the long service name is still one line ending `…` |
| The Preview modal | live `http://127.0.0.1:8768/tatib/149/` → any entry's Preview | the pasted link wraps inside the dialog |
| The language toggle | live `/bible/1/1/` | TB / SIM keeps the line it takes today |

## Rebuild and measure

```sh
# from this worktree, with the compose database reachable
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py \
    runserver 0.0.0.0:8768 --noreload
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/137-reading-text-wrap/preview/build_preview.py
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/137-reading-text-wrap/preview/probe_wrap.py
```

`probe_wrap.py` opens every pair at 1440×900, 1280×800 and 390×844 and prints, per page: the
document's horizontal overflow, the title's line count and box height, and every text run still
painted past its box — the numbers quoted in the spec's `## UI/UX`.

`build_preview.py` serves the stylesheets from `_static/`; after editing `static/styles/`, run
`manage.py collectstatic --noinput` and restart `runserver`, or the preview keeps the old CSS.

## What this preview cannot show

The Preview modal is built by `preview.js` at click time, so a static page cannot open it; the live
route is the preview for that surface. Everything in this slice is layout, so nothing else is
missing: no server behaviour, no fetch and no saved copy is involved.
