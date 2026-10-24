# Preview: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md`
**Route**: `/songs/<id>/` — the preview build is running at `http://localhost:8768`

## Run

```sh
# from this worktree
PORT=$(cd ~/Projects/multimedia-gkps-klender && docker compose port db 5432 | sed 's/.*://')
export DATABASE_URL="postgres://multimedia:<password>@127.0.0.1:${PORT}/multimedia"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8768 --noreload
```

The preview is the app's own song page with this slice's two-line change applied — no mockup, no stand-in
template. The change is in the citation both renderers already compute: the server view
(`multimedia/web/reading/views.py`, `SongDetailView`) and the saved renderer (`static/web/offline-render.js`,
`songPage()`).

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| hymn song, short name present (the change) | `/songs/1013/` — PKJ 4 | header reads `PKJ 4`; the tab reads `PKJ 4 — GKPS Klender`; the sidebar's selected row already read `PKJ 4` |
| hymn song with a sub-number | `/songs/531/` — KJ 24a | header reads `KJ 24A` — the sub-number treatment is unchanged |
| hymn song, another songbook | `/songs/101/` — Haleluya 101 | header reads `HAL 101` |
| ordinary songbook (must not change) | `/songs/1905/` — Lagu | header reads `Lagu`, exactly as before |
| narrow stage | any of the above at 390 px and 768 px | the header is one line where the full name took two |
| saved copy, online | `/home/` → sync → Kidung → PKJ → any song | the saved page and the server page show the same header before the online update |
| saved copy, offline | the same clicks with the network unavailable | the saved header stays `PKJ 4` |

## Measured (2026-10-24)

`#readEyebrow` on `/songs/1013/`, type unchanged at 16.5px / 600 / 1.65 (27.225px) / 1.98px tracking:

| Width | Today (develop, `:63404`) | This build (`:8768`) |
| --- | --- | --- |
| 1440 | `Pelengkap Kidung Jemaat 4` — 292.64 × 27.22 px, one line | `PKJ 4` — 49.56 × 27.22 px, one line |
| 1280 | 292.64 × 27.22 px, one line | 49.56 × 27.22 px, one line |
| 768 | 243.22 × 54.44 px, **two lines** | 49.56 × 27.22 px, one line |
| 390 | 290 × 54.44 px, **two lines** | 49.56 × 27.22 px, one line |

Saved-vs-server agreement, checked through `GKPSOfflineRender.render()` against the same routes:

| Route | Saved | Server |
| --- | --- | --- |
| `/songs/1013/` | `PKJ 4` | `PKJ 4` |
| `/songs/531/` | `KJ 24A` | `KJ 24A` |
| `/songs/1905/` | `Lagu` | `Lagu` |

## What is not a preview

A screenshot, a static image and a recording are not previews. This preview is the running page, served by
the project's own development server, with the slice's change in the code path that renders it.
