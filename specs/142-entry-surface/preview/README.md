# Preview: a service entry draws no box until it is pointed at

**Spec**: `specs/142-entry-surface/spec.md`
**Shape**: `static` comparison of the four candidates, plus the live slice server
**Open**: `specs/142-entry-surface/preview/preview.html` directly, or live at
`/tatib/142/` (24 text entries and 3 breaks) and `/tatib/144/` (all five kinds)

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-142
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8820 --noreload
```

Open `http://127.0.0.1:8820/tatib/142/`. The static page is regenerated from that server:

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/142-entry-surface/preview/build_preview.py
```

## Why the stylesheet is frozen

`preview/assets/*.css` are `static/styles/design/*.css` as of `ca71c850` (develop, immediately
before this slice), copied by the build script — not linked. The comparison has to keep drawing the
spec 068 box in its **Now** column after the box has left the working tree; linking the live
stylesheet would turn **Now** into a second **Bare**.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| Now | open the page, top-left button | 24 faint rectangles: `background rgba(31,31,29,.012)`, ring `rgba(31,31,29,.08)` |
| A · Bare | press `A · Bare` | no paint anywhere; the entries separate on 32px of text gap |
| B · Rules | press `B · Rules` | a 1px hairline between entries — and the section break's 2px rule stops standing out |
| C · Gutter | press `C · Gutter` | `L :` / `J :` hang in a 37.6px margin; wrapped lines align under the words at x = 239.6 |
| D · Felt | press `D · Felt` | no ring; a 4% fill (9 of 255 levels) that can actually be seen |
| hover | press **Show hover** | the second entry fills with `--icon-hover-bg` — the one paint the adopted option keeps |
| dark | press **Dark** | the same six states with the dark palette |

The static page carries 24 entries of `/tatib/142/`, all text. The five kinds — text, scripture,
song, media and section break — are on the live server at `/tatib/144/`.
