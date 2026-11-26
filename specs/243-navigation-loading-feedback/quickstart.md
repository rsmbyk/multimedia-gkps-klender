# Quickstart — spec 243

**Spec**: `specs/243-navigation-loading-feedback/spec.md`

## Preview

Accepted static preview: `specs/243-navigation-loading-feedback/preview/index.html`.
Open it as a file so the toolbar works; `preview/grid-v14.png` is the contact
sheet. The earlier rounds are `preview/index-v1.html` … `index-v13.html`.

After implementation, drive the same states on the slice's dev server:

```bash
cd ~/Projects/multimedia-gkps-klender-243
DATABASE_URL='postgresql://multimedia:***@127.0.0.1:<db-port>/gkps243' \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 127.0.0.1:8777 --noreload
```

Derive `<db-port>` from the running compose stack (`docker compose port db 5432`);
never write the real password into a file. After touching `static/`, run
`collectstatic --noinput` and hard-reload the tab.

## Tests

Use a throwaway database so another session's `manage.py test` cannot collide:

```bash
cd ~/Projects/multimedia-gkps-klender-243
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
DATABASE_URL='postgresql://multimedia:***@127.0.0.1:<db-port>/gkps243' \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_navigation_pending --tag=e2e --noinput -v 2
DATABASE_URL='postgresql://multimedia:***@127.0.0.1:<db-port>/gkps243' \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_navigation_freshness --tag=e2e --noinput -v 1
```

The first module is new in this slice and holds the ten targeted E2E cases in
`plan.md`. The second is its sibling: the rail-to-page path must still paint
the server's current page without a document reload. The full browser matrix
is deferred to the push step.

Measurement helpers for the preview stay in `preview/probe14.py` and
`preview/inspect_placeholder.py` (venv Python with Playwright). The chat-frame
check before any inline preview is
`~/.hermes/skills/software-development/obs-browser-surfaces/scripts/verify-chat-preview-frame.py`.
