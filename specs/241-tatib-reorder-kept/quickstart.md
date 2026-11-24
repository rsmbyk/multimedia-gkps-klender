# Quickstart — spec 241

**Spec**: `specs/241-tatib-reorder-kept/spec.md`

## Preview

Live: `http://127.0.0.1:8791/tatib/322/`, served from this worktree with the uncommitted fix:

```bash
cd ../multimedia-gkps-klender-241
source ../multimedia-gkps-klender/.venv/bin/activate
DATABASE_URL='postgresql://multimedia:multimedia@localhost:59075/multimedia' \
  python manage.py runserver 127.0.0.1:8791 --noreload
```

See `preview/README.md` for the states to drive by hand.

## Tests

```bash
cd ../multimedia-gkps-klender-241
source ../multimedia-gkps-klender/.venv/bin/activate
python manage.py collectstatic --noinput
DATABASE_URL='postgresql://multimedia:multimedia@localhost:59075/multimedia' \
  python manage.py test tests.e2e.test_reorder --tag=e2e --noinput -v 2
DATABASE_URL='postgresql://multimedia:multimedia@localhost:59075/multimedia' \
  python manage.py test tests.e2e.test_song_sort_retained --tag=e2e --noinput -v 1
DATABASE_URL='postgresql://multimedia:multimedia@localhost:59075/multimedia' \
  python manage.py test multimedia.web.tests --noinput -v 1
```

`tests/e2e/test_reorder.py::ReorderE2ETests` links to the contracts and data model above for the
endpoints and entities it drives. The one red unit test in `multimedia.web.tests` and the red
E2E cases in `test_reading.py` / `test_entries.py` reproduce unchanged on unmodified develop.
