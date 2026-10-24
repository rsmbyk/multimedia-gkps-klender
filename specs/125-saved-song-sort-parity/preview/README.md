# Preview: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`
**Route**: `/songs/<hymn song>/` — measured on `/songs/1390/` (NKB 1, "Hai Kristen, Nyanyilah")

## Run

```sh
# from this worktree, against the local stack (see docs/PROCESS.md and docker-compose.yml)
.venv/bin/python manage.py runserver 0.0.0.0:8768 --noreload
```

The saved view needs the library synced once in the browser that runs it: open `/home/`, wait for the
offline status control to settle, then use the sidebar paths below.

## States to click through

| State | How to reach it | What to look for |
| --- | --- | --- |
| server page (the target) | open `/songs/1390/` directly | no sort control beside "Filter songs…"; the field spans 339 px |
| saved page, online (the defect) | home → Kidung → NKB → first song | the sort control is painted for about 220 ms (38 × 38 px) and the field narrows to 293 px, then both revert |
| saved page, offline | the same clicks with the network unavailable | the control stays visible — the saved frame is the final one |
| ordinary songbook (must not change) | home → Kidung → Lagu → a song | the control stays visible before and after the online update |

Measured 2026-10-24 on `localhost:8768`, develop plus this slice's draft: `#songSort` visible
`hidden=false`, width 38 px, `#songFilter` 293 px; settled `hidden=true`, width 0, `#songFilter` 339 px.
Frame sampling on `requestAnimationFrame` recorded the visible window between 3130 ms and 3350 ms after
the sidebar click.

## What is not a preview

A screenshot, a static image and a recording are not previews. The preview is the **running** screen,
built from the project's own components and tokens — here, the server-rendered page for the same route,
which is already the reference spec 122 fixed.
