# Quickstart: Empty song paints one Add verse control

**Spec**: `specs/224-empty-song-add-verse-row/spec.md`

## Targeted tests

From this worktree, with the compose DB published at 127.0.0.1:59075:

```sh
bash specs/224-empty-song-add-verse-row/preview/test.sh
```

`test.sh` reads the web container's `DATABASE_URL` at runtime, points Django at the throwaway
database `gkps224` so no other worktree's test run collides, and runs
`multimedia.web.reading.test_verse_add_gate` and `tests.e2e.test_song_empty_placement` with
`--keepdb`. The placement module opens an empty song and an empty Tata Ibadah and compares their
`.entry__empty-title` tops at 1440×900 and 900×700. It never prints the credentials.

## Live check

```sh
bash specs/224-empty-song-add-verse-row/preview/serve.sh
.venv/bin/python specs/224-empty-song-add-verse-row/preview/probe.py
```

Open `http://127.0.0.1:8770/songs/1731/` (no verses) and `/songs/1387/` (three verses).
The probe writes `preview/measurements.json` and screenshots in `preview/shots/`.

## Static preview

Open `specs/224-empty-song-add-verse-row/preview/index.html` directly; use the state switcher.
Rebuild it from the live pages with `preview/build.py` when the served markup changes.
