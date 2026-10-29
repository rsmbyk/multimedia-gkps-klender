# Preview: the Transfers list draws each boundary once

**Spec**: `specs/149-transfer-separator-seam/spec.md`
**Shape**: `static` — one page, the product's own markup, tokens and stylesheets
**Open**: `specs/149-transfer-separator-seam/preview/preview.html` directly

## Run

```sh
# none: open the file directly. The stylesheets it draws with are copies:
python3 specs/149-transfer-separator-seam/preview/build_preview.py   # refresh them from the base commit
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/149-transfer-separator-seam/preview/probe.py                  # re-measure, refresh shots/
```

`assets/{fonts,tokens,components}.css` are `static/styles/design/*.css` as of `05379336` (develop, the
base commit), copied by the build script rather than linked, so the **Today** column keeps drawing
develop's rules after this slice's two rules land in the working tree. `shots/` is what `probe.py`
writes and is not committed — run it to regenerate the screenshots the convergence record cites.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| nine rows, the report | open the page | the seam after `side-view-silhouette…`: **two** lines 10.5px apart on the left, **one** 2px line on the right |
| the dialog's bottom edge | same state, look at the bottom of each dialog | left: the last row's border 4px above the dialog's border; right: 22px of padding, no line near the border |
| fifteen rows | press `15 rows` | left: six rows paint **outside** the dialog, over the page; right: the list scrolls, nothing leaves the dialog |
| dark theme | press `Dark` | the same numbers with `--divider` `#3A362F`; no other change |
| the numbers | read the table under the dialogs | separator count, distance between the seam's lines, and the list's overshoot, per column |

## What the page does not show

The list is the page's own data (the nine transfers of the report, plus six older ones), not a
fetch: it does not exercise the companion, the rail button, or the `session`/`viewed` logic that
decides *whether* a divider is drawn. The divider is placed where the report had it, after the
second row.

## Live check

The same dialog on the running app, from the worktree:

```sh
cd ~/Projects/multimedia-gkps-klender-149
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8830 --noreload
```

Open `http://127.0.0.1:8830/media-library/`, upload a file, and press the transfers button in the
rail once the upload completes.
