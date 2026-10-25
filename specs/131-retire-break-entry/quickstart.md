# Quickstart: The Break kind retires, and the breaks already written stay

**Spec**: `specs/131-retire-break-entry/spec.md`

## Serve the branch

```bash
cd ../multimedia-gkps-klender-131          # the slice worktree (addressed from the main checkout)
DATABASE_URL=postgresql://multimedia:***@127.0.0.1:$(docker compose -f ../multimedia-gkps-klender/docker-compose.yml port db 5432 | cut -d: -f2)/multimedia \
  DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
  ../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8803 --noreload
```

## Read the four surfaces

1. **An add row.** Open a Tata Ibadah with items (`/tatib/<id>/`), hover an item: `+ Passage`, `+ Song`,
   `+ Text`, `+ Media` — four buttons, no `+ Break`.
2. **The start bar and the empty service.** A service with no items shows four 52px tiles (Passage, Song, Text,
   Media), centred, 238px wide; the row has no empty fifth slot.
3. **An existing break.** A service that still holds one draws its full-width divider, keeps its sidebar row,
   and hovers to show Delete only (no Edit).
4. **Delete it.** Delete the divider, confirm: it leaves the stage and the sidebar, the order closes up, the
   request is `POST /editor/entry/<pk>/delete/ → 200`.

## Ask the endpoints directly

With a service id (`TATIB`) and a session cookie + CSRF token from the browser:

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST \
  "http://127.0.0.1:8803/editor/entry/new/save/?tatib=$TATIB" \
  -H 'X-Requested-With: fetch' -H "X-CSRFToken: $CSRF" -b "csrftoken=$CSRF; sessionid=$SESSION" \
  --data 'kind=3&after=start'          # 404, and the service gains no row

curl -s -o /dev/null -w '%{http_code}\n' -X POST \
  "http://127.0.0.1:8803/editor/entry/$BREAK_PK/save/" \
  -H 'X-Requested-With: fetch' -H "X-CSRFToken: $CSRF" -b "csrftoken=$CSRF; sessionid=$SESSION" \
  --data 'kind=3&title=x'              # 404, and the row is unchanged
```

`GET /editor/entry/new/?kind=section_break&tatib=$TATIB` and
`GET /editor/entry/$BREAK_PK/edit/` are `404` too.

## Test

```bash
DATABASE_URL=… manage.py test multimedia.web --keepdb
DATABASE_URL=… manage.py test tests.e2e.test_tatib_section_break tests.e2e.test_entries \
  tests.e2e.test_reorder tests.e2e.test_edit_request_feedback --keepdb
```

The remaining browser suites run at the push step, per the repo's test budget.
