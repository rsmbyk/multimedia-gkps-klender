# Preview: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md`
**Shape**: `static` — one page, the product's own markup, tokens and stylesheets
**Open**: `specs/153-preview-tabs-row/preview/preview.html` directly

## Run

```sh
# none: open the file directly. The stylesheets it draws with are copies:
python3 specs/153-preview-tabs-row/preview/build_preview.py    # refresh them from the base commit
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/153-preview-tabs-row/preview/probe.py                   # re-measure, refresh shots/
```

`assets/{fonts,tokens,components}.css` are `static/styles/design/*.css` as of `24a6d6d2` (develop, the
base commit), copied by the build script rather than linked, so the **Today** column keeps drawing
develop's rules after this slice's rules land in the working tree. `shots/` is what `probe.py` writes
and is not committed — run it to regenerate the screenshots the convergence record cites.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| the report's song | open the page | left: title ellipsized at 570px with the tabs on its row; right: title at 660px, tabs on their own row, one rule under them |
| which side of the tabs the rule falls on | press `Rule above the tabs` | right column only: the title band regains its rule and the tabs float between it and the lyrics — the rejected shape |
| no verse tabs | scroll to *A preview with no verse tabs* | both columns identical: 704×52 header, rule under the title, body at 52px |
| the focus on open | press `Today's dialog` / `The After dialog` | readout names the element that took focus: `button.preview__tab` today, `div.preview__body` after. Focus the button and press `Enter` to see the keyboard case, where today's tab — not the after's body — paints a ring |
| dark theme | press `Dark` | the same numbers with `--divider` `#3A362F`; no other change |
| a phone | narrow the window to 390px (or read `probe.py`'s `390` block) | today: the tabs wrap onto a second line inside the header (89.8px); after: a 95px header block with the tabs on their own row |

## What the page does not show

Neither column is server-rendered: the page clones the payload `tatib.html` emits for the song in the
report — `.preview__song` plus three verse tabs — and lifts it the way `preview.js` does. It does not
exercise the pane, the trigger, or the payload's own data. The two demo dialogs copy the two lines of
`preview.js`'s open path (`showModal()`, then `content.focus()` in the After variant); the product's
script is not loaded twice on one page.

## Live check

The same dialog on the running app, from the worktree:

```sh
cd ~/Projects/multimedia-gkps-klender-153
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8831 --noreload
```

Open `http://127.0.0.1:8831/tatib/144/` and press Preview on the song entry whose title starts
`Buku Ende HKBP`.
