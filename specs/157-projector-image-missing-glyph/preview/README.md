# Preview: the projector's image placeholder

**Spec**: `specs/157-projector-image-missing-glyph/spec.md`
**Shape**: `static` — one page, the product's own screen markup, tokens and stylesheet
**Open**: `specs/157-projector-image-missing-glyph/preview/preview.html` directly

## Run

```sh
# none: open the file directly. The stylesheets it draws with are copies:
python3 specs/157-projector-image-missing-glyph/preview/build_preview.py   # refresh them from the base commit
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/157-projector-image-missing-glyph/preview/probe.py                  # re-measure, refresh shots/
```

`assets/{fonts,tokens,projector}.css` are `static/styles/design/*.css` as of `24a6d6d2` (develop, the
base commit), copied by the build script rather than linked, so the **Today** column keeps drawing
develop's rules. `shots/` is what `probe.py` writes and is not committed.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| image loaded | open the page (the default) | left: the picture **and** the slashed-frame glyph 80px to its right; right: the picture alone, on the stage's middle |
| bytes failed (404) | press `Bytes failed (404)` | both: the glyph alone, 80×80, dead on the middle — this is the state the glyph exists for and both columns already draw |
| before the fetch settles | press `Before the fetch settles` | left: the glyph, although nothing has failed yet; right: an empty stage |
| the numbers | read the table under the boards | glyph `display`, whether it carries `hidden`, both boxes, the image's centre against 960 |

## What the page does not show

The image is a drawn 1600×900 frame, not the library's own file, and the states are set by the four
lines of `renderImageScreen` (`static/web/projector.js:211`) run directly — the page does not fetch
`http://127.0.0.1:63174/v1/files/<sha>`, so it does not exercise the companion, the `AbortController`,
the object URL, or the screen's morph. It also draws one screen, so the corner cue and the move between
screens are absent.

Each board is a real `.projector__screen` at 1920×1200, scaled to 45% so two fit side by side; the
readout divides the measured boxes back by that scale, so its numbers are the display's own.

## Live check

The same screen on the running app, from the worktree:

```sh
cd ~/Projects/multimedia-gkps-klender-157
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8833 --noreload
```

Open `http://127.0.0.1:8833/projector?service=<id>` for a service holding an image, press Space and
step to the image screen. With the companion running the picture is alone; stop the `media` container
and step back to it for the glyph.
