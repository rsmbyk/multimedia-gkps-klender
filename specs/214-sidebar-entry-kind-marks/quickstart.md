# Quickstart: a contents row marks its entry's kind

**Spec**: `specs/214-sidebar-entry-kind-marks/spec.md` · **Contracts**: `contracts/toc-markup.md` ·
**Data model**: `data-model.md` (n/a — no stored state)

## Run it

From the slice worktree. The venv lives in the main checkout; the database is the compose service.

```sh
cd ~/Projects/multimedia-gkps-klender-214
export DATABASE_URL="$(docker exec multimedia-gkps-klender-web-1 printenv DATABASE_URL \
  | sed 's/@db:5432/@127.0.0.1:59075/')"
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8777 --noreload
```

`collectstatic` is not optional: static files are served from `_static/` through a manifest, so a CSS
edit without it leaves the page on the old rules.

## Look at it

`http://127.0.0.1:8777/tatib/<service id>/` — a dated service holding a legacy text row, a passage, a
song, a media file, and section breaks. A template page (`?mode=template` in the sidebar, or a
template's own route) supplies the fill-in and choice rows with their corner badges.

## Verify the spec's numbers

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/214-sidebar-entry-kind-marks/preview/probe.py
```

The preview is regenerated from the project's real tokens, CSS and row markup with:

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
    specs/214-sidebar-entry-kind-marks/preview/build_preview.py
```

## Tests

```sh
# the rendered marks, in the existing reading-view module
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
    multimedia.web.tests.ServiceEntryViewTests --keepdb

# the new browser suite: geometry, states, both surfaces
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
    tests.e2e.test_sidebar_kind_marks --keepdb

# the contracts this slice must not disturb
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
    tests.e2e.test_toc_number_centering tests.e2e.test_text_wrap \
    tests.e2e.test_stage_kind_marks --keepdb

# the slot badge's own stage rules
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
    multimedia.web.tests.SlotKindBadgeTests tests.e2e.test_tatib_templates --keepdb
```
