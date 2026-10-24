# Preview: Hymn songbooks above a single separator, the rest A–Z

**Spec**: `specs/128-songbook-hymn-separator/spec.md`
**Route**: `/songs/` (also `/songs/book/<id>/`, `/songs/<song_id>/`)

## Run

```sh
cd ~/.hermes/worktrees/128-songbook-hymn-separator
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:59075/multimedia" \
  /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
  manage.py runserver 0.0.0.0:8795 --noreload
```

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| default | open `/songs/` | four hymn rows, one 2px rule, then the ordinary rows A–Z, no heading |
| filter, both sides matched | type `a` in *Filter songbooks* | both groups stay, separator stays between them |
| filter, hymn side empty | type `lagu` | separator gone; ordinary group starts flush |
| filter, ordinary side empty | type `kidung jemaat` | separator gone; hymn group alone |
| saved copy | disable the network, reload a Kidung route | the saved render draws the same two groups |
| current row | open any songbook | `aria-current` fill sits on its row in either group |

## Live preview or mockup

Live preview: the project's own routes, templates, stylesheet tokens and saved renderer. Screenshots in this
folder were taken from that running page at 1600 × 1000 and are evidence, not the preview.
