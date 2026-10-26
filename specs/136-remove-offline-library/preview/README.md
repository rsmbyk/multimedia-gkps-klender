# Preview: the app without the offline library, and the Go To's loading state

**Spec**: `specs/136-remove-offline-library/spec.md`
**Shape**: static previews at `specs/136-remove-offline-library/preview/`

- `after.html` — the real `/home/` reading shell with the offline feature removed: the rail's status
  button, its panel, the `Saved copy` label, the offline stylesheet and the three offline scripts.
- `projector-index-loading.html` — `G` opened before the Go To index has arrived: the panel is up,
  the field is locked, the row carries the spinner.
- `projector-selection-loading.html` — a result chosen and its chapter/song being fetched: the same
  panel state with the query and the chosen row, plus the corner spinner beside the shortcuts button.
- `projector-selection-error.html` — the fetch failed: the state restores, the row says so, the
  field is usable again.
- `projector-chapter-loading.html` — a chapter crossing inside a passage detour: the panel is closed
  and only the corner spinner is showing.

Every page comes from this worktree's own server — shell, rail, panels, stage, type, tokens,
stylesheets and words. The builder strips the scripts (so nothing rewrites the page) and applies the
proposal: the removal itself, plus the loading treatment.

## The proposal

The spinner is the app's own idiom (`.editor__loading-spinner`: 2px border, 800ms linear, off under
reduced motion), sized for this surface:

```css
.projector-find__spinner { width: 12px; height: 12px; }
.projector-find__row.is-loading .projector-find__count { display: none; }
.cue-loading { position: absolute; right: 74px; bottom: 25px; width: 14px; height: 14px; }
```

The row's spinner takes the count's place at the row's right end — the count is meaningless while
the content loads — so the suggestion line does not move. The corner spinner sits 8px left of the
shortcuts button (32px page inset + 34px button + 8px gap = `right: 74px`) and shares its vertical
centre (24px button, 14px spinner → `bottom: 25px`).

## States to look at

| File | State | What to look for |
| --- | --- | --- |
| `after.html` | reading shell, panel closed | rail foot holds the theme button alone; no offline button, no panel, no saved-copy label |
| `projector-index-loading.html` | `G` before the index | field locked, row reads `Loading search…` with the spinner at its right, `0 / 0` hidden |
| `projector-selection-loading.html` | choosing a result | `KJ 152` in the field, one row with the spinner, corner spinner beside the keyboard icon |
| `projector-selection-error.html` | the fetch failed | panel keeps its row, `Could not load — try again`, field usable, no corner spinner |
| `projector-chapter-loading.html` | crossing a chapter | no panel; only the corner spinner beside the keyboard icon |

## Rebuild and measure

```sh
# from this worktree, with the compose database reachable
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8769 --noreload
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/136-remove-offline-library/preview/build_preview.py
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/136-remove-offline-library/preview/probe_loading.py
```

`probe_loading.py` prints the reading rail before and after (foot height, button labels), and each
projector state's panel, row, spinner and corner geometry — the numbers quoted in the spec's
`## UI/UX`.

## What this preview cannot show

The fetch itself: the panel is posed in its loading state, because no page here runs the projector's
script (the index, the chapter request and the lock are behaviour, verified by the tests named in
`plan.md`). The corner cue's runtime text is the running page's, so the chapter preview shows the
cue as the server sends it, with the spinner in place.
