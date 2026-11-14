# Quickstart — the rail's marks and the stage's own

**Spec**: `specs/151-rail-icons/spec.md` · **Plan**: `specs/151-rail-icons/plan.md`

## Run the tests

The venv lives in the main checkout; the database is the compose service on `127.0.0.1:59075`. Name a
throwaway database so a concurrent run in another worktree cannot hold the same `test_*` database:

```bash
export PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
export DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/gkps151

$PY manage.py test tests.e2e.test_rail_marks --noinput      # this slice
$PY manage.py test tests.e2e.test_stage_kind_marks --noinput # spec 144's, must stay green
```

`--keepdb` is safe once the throwaway database exists; `--noinput` rebuilds it from scratch.

## Run the slice by hand

```bash
$PY manage.py runserver 0.0.0.0:8765 --noreload
```

Then open `http://127.0.0.1:8765/tatib/<id>/` at 1440×900 and look at the rail: Bible, Kidung, Tata
Ibadah, Media Library. Switch the theme with the rail's bottom button. Resize to 1024px (64px rail,
20px marks) and to 425px (the menu drawer). For the empty stage's tiles, open a Tata Ibadah with no
entries.

Static files are served from `_static/` through `CompressedManifestStaticFilesStorage`: after editing
anything under `static/`, run `$PY manage.py collectstatic --noinput` and restart, or the page keeps
the old `media-stage.js`.

## Regenerate the preview

```bash
$PY specs/151-rail-icons/preview/build_preview.py           # reads the live app on :63404
$PY -m http.server 8831 --bind 127.0.0.1 -d specs/151-rail-icons/preview
```

`http://127.0.0.1:8831/preview.html` — the top bar switches each slot to its alternative; **Dark**
flips the theme.

## What to look for

| Check | Where |
| --- | --- |
| The rail's Bible is a book **with a cross**, and a passage row draws the same path | rail, then a stage row |
| The Tata Ibadah rail mark is a **clipboard**, not a page | rail beside a PDF chip |
| The song row and the rail draw the same **beamed pair** | stage row, rail, empty stage's Add Song tile |
| An audio file is a **waveform**, distinct from the song | a stage holding a song and an audio file |
| No box moved | 44px buttons, 24px glyphs, 20px kind mark at +24, 42px chips, 56/80px rows |
