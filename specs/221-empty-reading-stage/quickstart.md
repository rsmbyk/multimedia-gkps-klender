# Quickstart: an empty reading stage after deleting the open record

**Spec**: `specs/221-empty-reading-stage/spec.md` · **Design**: [data-model](data-model.md),
[contracts](contracts/none.md).

## Reproduce the reported behaviour

On a served app with editing allowed, open a non-hymn song from its songbook, hover its row, click
trash and confirm. Today the stage flips to the search landing on the songbook list. With the slice
applied the stage keeps reading mode and shows "Nothing open." with the hint.

## Commands

```sh
# From the slice worktree (~/Projects/multimedia-gkps-klender-221):
../multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_deleted_stage --keepdb

# Serve the slice's own code (port chosen free; use --noreload):
../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8771 --noreload

# Static preview: open in a browser, no server needed:
specs/221-empty-reading-stage/preview/index.html
```

The E2E module is runnable once Implement lands it; before that the command is not-yet-runnable and
the preview is the material to click through. Tests use Django's runner with Playwright and skip when
the browser is unavailable. A full `collectstatic` is not needed for the E2E class because it
overrides `STATICFILES_STORAGE`; a manually served page needs one after any `static/` change.
