# Quickstart

Commands for this slice only. The contract they exercise is
[`contracts/stage-markup.md`](./contracts/stage-markup.md); the entities are in
[`data-model.md`](./data-model.md) — neither is repeated here.

## The stage's server

```sh
cd ~/Projects/multimedia-gkps-klender-144
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8830 --noreload
```

`/tatib/144/` is the fixture service: one passage, four songs, one text entry, three media files.

## The tests

```sh
cd ~/Projects/multimedia-gkps-klender-144
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/gkps144" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_stage_kind_marks --noinput
```

- A **throwaway database name** (`gkps144`) keeps this run off the shared `test_multimedia` that another
  session may be using; Django creates and drops `test_gkps144` itself.
- `--keepdb` is fine once it exists and no other run holds it.
- The module needs no `override_settings(STATICFILES_STORAGE=…)`: its assertions are geometry and paint
  from stylesheets the live server serves, not hashed asset URLs. If a page-rendering assertion is added
  later, add that decorator — the suite's convention.

Adjacent modules worth re-running once, because they measure the same rows:

```sh
… manage.py test tests.e2e.test_tatib_entry_controls tests.e2e.test_text_wrap \
  tests.e2e.test_media_library --noinput
```

## The preview, if the geometry moves again

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/144-passage-song-icons/preview/build_preview.py
```

Reads `http://127.0.0.1:8830/tatib/144/`, freezes the stylesheets at `05379336`, writes
`preview/preview.html` and `preview/compare.html`. It is a record of gate 1, not a build step — nothing
imports it.
