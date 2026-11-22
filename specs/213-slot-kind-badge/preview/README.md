# Preview: a slot states the kind it resolves to

**Spec**: `specs/213-slot-kind-badge/spec.md`
**Shape**: `live` (the change applied to the running page) plus a `static` comparison page
**Open**: `http://127.0.0.1:8777/tatib/151/` — template *111ojo*, six slots — and
`specs/213-slot-kind-badge/preview/compare.html` opened directly

## Run

```sh
# from the slice worktree, with the compose db published on 59075
export DATABASE_URL="$(docker exec multimedia-gkps-klender-web-1 printenv DATABASE_URL \
  | sed 's/@db:5432/@127.0.0.1:59075/')"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8777 --noreload
```

The comparison page is built from the running server and needs no server of its own once written:

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python specs/213-slot-kind-badge/preview/build_compare.py
```

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| default (dark) | open `/tatib/151/` | six badges, one per slot: note, note, book, note, lines, frame |
| light | switch the app's theme | the disc turns to `#F7F5F1`, the glyph to `rgb(100,99,87)` |
| hovered | point at a slot row | the disc takes the row's own tint — no hole punched in the fill |
| modal origin | open a slot's Edit modal | the row keeps its fill and the badge stays legible |
| keyboard focus | Tab to a slot's Edit control | same as the modal origin |
| no options | the choice whose options were emptied | the badge is still drawn; `No options yet` sits below |
| untitled slot | a slot with an empty title | the badge is drawn beside the kind label alone |
| the three sizes | `compare.html` | A 11px, **B 13px — adopted**, C 15px, each at 1× and its 1× pixels at 8× |
| responsive | resize to 900 × 380 and to 390 wide | nothing wraps that did not wrap before; the badge stays inside the row |

## The choice, and what it was made against

**B (13px disc, 10px glyph) is adopted** — the owner chose it at gate 1 from three candidates built on
the real rows. A (11px) was built first and rejected: at true 1× pixels its 8.5px glyph is an unnamed
blob. C (15px) is the clearest of the three but its disc is wider than the 14.8px dashed frame it sits
on and eats that corner whole. `compare.html` keeps all three visible, B marked `adopted`, so a later
reader sees what was decided and against what.

## What this preview cannot show

A slot whose `fill_kind` is missing (a legacy row) — the local database has none. Its behaviour is
stated in FR-007 and is exercised by a unit test instead.

## Live or static

**Live** is served from the project: its own route, components and tokens, running. The change is in
the worktree, so the page itself shows it.

**Static** is the comparison page: one HTML file assembled from the served page's own markup, the
project's three real stylesheets inlined, and the badge at three sizes, opened directly. It exists to
make a *choice* visible; the live page is the preview of the adopted one.
