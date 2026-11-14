# Quickstart: a reading page's text wraps at its pane

**Slice**: `specs/137-reading-text-wrap`
Contracts: [`contracts/none.md`](./contracts/none.md) · Data: [`data-model.md`](./data-model.md)

Everything runs from the slice's worktree, against the compose database.

```sh
export DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/multimedia"
PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
```

## The rendered geometry — Playwright E2E

```sh
$PY manage.py test tests.e2e.test_text_wrap --keepdb
```

*Not yet runnable: the module is written in Implement (`tasks.md` T002–T011), so it does not exist
at gate 2. The suite needs a browser and the compose database; the repository's E2E modules run
through `StaticLiveServerTestCase` and skip cleanly when Playwright is absent.*

The neighbouring modules this slice must not disturb:

```sh
$PY manage.py test tests.e2e.test_reading tests.e2e.test_song_label_typography \
  tests.e2e.test_media_library --keepdb
```

## The preview, from the slice's own server

```sh
$PY manage.py collectstatic --noinput            # Whitenoise serves _static/, not static/
$PY manage.py runserver 0.0.0.0:8768 --noreload  # 8768 is this slice's port
$PY specs/137-reading-text-wrap/preview/build_preview.py    # before/after pairs, four pages
$PY specs/137-reading-text-wrap/preview/probe_wrap.py       # the numbers in ## UI/UX
$PY specs/137-reading-text-wrap/preview/shoot.py            # screenshots, two viewports
```

The first three already ran at Preview and produced `preview/before-*.html`, `preview/after-*.html`
and the spec's numbers. After Implement they can be rebuilt unchanged — the rule is in the app, so
the `after` page is simply the live route.

After editing `static/`, `collectstatic` and a restart are both required: WhiteNoise serves from
`_static/` and caches the manifest at startup.

## What to look at

| Surface | Path | Expectation |
| --- | --- | --- |
| The reported Tata Ibadah page | `http://127.0.0.1:8768/tatib/149/` | the title wraps inside the pane; no sideways scroll |
| The reported song page | `http://127.0.0.1:8768/songs/1817/` | the title wraps; no sideways scroll |
| A Bible chapter | `http://127.0.0.1:8768/bible/1/1/` | headings and verses wrap at narrow widths |
| The Preview modal | the service page → any entry's Preview | the pasted link wraps inside the dialog |
| The unchanged app, for contrast | `http://127.0.0.1:63404/tatib/149/` (compose, `develop`) | the same title runs past the pane and the document scrolls sideways |
