# Quickstart: a slot states the kind it resolves to

**Spec**: `specs/213-slot-kind-badge/spec.md` · **Contracts**: `contracts/stage-markup.md` ·
**Data model**: `data-model.md` (n/a — no stored state)

## Run it

From the slice worktree. The venv lives in the main checkout; the database is the compose service.

```sh
cd ~/Projects/multimedia-gkps-klender-213
export DATABASE_URL="$(docker exec multimedia-gkps-klender-web-1 printenv DATABASE_URL \
  | sed 's/@db:5432/@127.0.0.1:59075/')"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8777 --noreload
```

`collectstatic` is not optional: static files are served from `_static/` through a manifest, so a CSS
edit without it leaves the page on the old rules.

## Look at it

`http://127.0.0.1:8777/tatib/151/` — template *111ojo*, six slots covering all four kinds
(song ×3, passage, text, media).

## Verify

```sh
# the numbers the spec's ## UI/UX carries
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/213-slot-kind-badge/preview/probe_adopted.py

# the four glyphs at 1x, plus their pixel maps and pairwise differences
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/213-slot-kind-badge/preview/probe_glyphs.py
```

## Tests

```sh
# the behaviour this slice adds, in the existing template-page module
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
    tests.e2e.test_tatib_templates --keepdb

# the mark rail it must not disturb (spec 144)
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
    tests.e2e.test_stage_kind_marks --keepdb

# the legacy no-kind row, which the local data cannot produce
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
    multimedia.web.tests --keepdb
```

Run E2E against a throwaway database when another session may be testing at the same time: name one in
`DATABASE_URL` (`.../gkps213`), so Django builds `test_gkps213` and no other run touches it.

## Build the preview pages again

Both are generated from the running server, so they must be rebuilt after a template or stylesheet
change:

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/213-slot-kind-badge/preview/build_compare.py    # the A/B/C comparison
```
