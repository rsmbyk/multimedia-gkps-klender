# Preview: the Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` (revision 2)
**Shape**: `static` — one page, the product's own markup, tokens and stylesheets
**Open**: `specs/152-transfer-scrollbar-edge/preview/preview.html` directly

## Run

```sh
# none: open the file directly. The stylesheets it draws with are copies:
python3 specs/152-transfer-scrollbar-edge/preview/build_preview.py   # refresh them from the base commit
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/152-transfer-scrollbar-edge/preview/probe.py                  # re-measure, refresh shots/
```

`assets/{fonts,tokens,components}.css` are `static/styles/design/*.css` as of `24a6d6d2` (develop, the
base commit), copied by the build script rather than linked, so the **Today** column keeps drawing
develop's rules after this slice's two rules land in the working tree. `shots/` is what `probe.py`
writes and is not committed — run it to regenerate the screenshots the convergence record cites.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| fifteen rows, the report | open the page | left: the 5px bar stops 22px short of the right border and 23px short of the bottom one; right: it is against both |
| the content | same state, compare the two columns row by row | the names, the glyph column, the age headings and both content edges sit on the same x in both columns |
| the scroll's end | scroll either list to the end | left: the thumb's bottom stops 23px above the border; right: it reaches the border, its rounded tip cut by the 12px corner — and in both columns the last row keeps the same 22px above the border |
| two rows | press `2 rows` | no bar in either column, no lane reserved, and the rows are still on the same x |
| dark theme | press `Dark` | the same distances; the bar is `--scroll-thumb` `#45413A` |
| narrow | narrow the window below 1260px | the columns stack; each dialog takes `calc(100vw - 32px)` and the bar still meets both edges |
| the numbers | read the table under the dialogs | the list's right and bottom edges inside the dialog, the lane width, and the content insets, per column |

## What the page does not show

The rows are written into the page rather than fetched from the companion, and the dialog is placed
in the flow instead of being opened with `showModal()`. It therefore does not exercise the rail
button, the `session`/`viewed` logic, or the companion's payload. The rail-opened state draws no age
headings (spec 146, FR-014); the page's rows are the library-opened state, which is the one in the
report.

It also cannot report the painted bar: it has no DOM. `probe.py` reads it from the screenshot, in a
**headed** Chromium — the headless build on this machine paints overlay scrollbars, reports a 0px lane
and draws no thumb at all (`--headless` reproduces that, for the record). Each column is measured
twice: at rest, and with its list scrolled to the end, which is where the thumb's bottom is visible.

## Live check

The same dialog on the running app, from the worktree:

```sh
cd ~/Projects/multimedia-gkps-klender-152
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8832 --noreload
```

Open `http://127.0.0.1:8832/media-library/`, press the Transfers button in the page's toolbar, and
look at the bar's right edge and its bottom end. The dialog needs a list taller than
`max-height: min(86vh, 46rem)` to draw a bar at all — at a 760px-tall window, nine transfers are
enough.
