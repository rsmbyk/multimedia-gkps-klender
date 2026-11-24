# Preview — Media Library filter-pill hover

Live preview: <http://127.0.0.1:8767/media-library/>

Open `/` and click the Media Library rail (the task's own navigation path). The
served page is the real code path from this worktree with the hover rule applied
in `static/styles/design/components.css`; `DEBUG` makes static files read from
source, so a hard reload picks up CSS edits.

If the server is down, from `~/Projects/multimedia-gkps-klender-239` run:

```
DJANGO_DEVELOPMENT_MODE=true ../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8767 --noreload
```

## States to try

| State | How to reach it | What to look at |
| --- | --- | --- |
| Rest | Pointer away from the filter row | Transparent pill, `--divider` border |
| Hover | Point at Images, Audio, Video, PDF, Slides or Unused | `--icon-hover-bg` fill and `--focus` border, same 63.36 × 30 px box |
| Pressed | Click a pill, then point at it | Accent fill unchanged by hover |
| Focus-visible | Tab to a pill | Existing 2px `--focus` outline with 2px offset |
| Dark | Toggle the theme control, repeat hover | White 9% fill and blue `--focus` border |
| Narrow | Resize to 390px | Filter row wraps as before |

`probe.py` measures the shipped page and a second copy of the same page with the
rule deleted from its CSSOM, so the before/after numbers in `../spec.md` come
from the same markup and tokens:

```
../multimedia-gkps-klender/.venv/bin/python specs/239-media-filter-pill-hover/preview/probe.py
```
