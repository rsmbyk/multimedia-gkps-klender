# Quickstart — spec 253

See [`data-model.md`](./data-model.md) for the stored record and [`contracts/none.md`](./contracts/none.md)
for the (absent) external interface.

## Local run

```
cd ~/Projects/multimedia-gkps-klender-253
../multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_use_template_progress --keepdb
```

The E2E module uses Django's `StaticLiveServerTestCase` with Playwright, the same lane as
`tests/e2e/test_tatib_templates.py`. The venv lives in the main checkout; the worktree's `manage.py`
runs with it.

## Preview

```
cd specs/253-use-template-progress/preview
python3 build_preview.py
../<repo venv>/bin/python probe.py
```

Opening `index.html` in a browser gives the interactive states listed in `preview/README.md`.
The generated page is self-contained; do not hand-edit it.

## Commands not yet runnable

None at Plan — both commands above name files produced at Implement and are expected to fail until
then. No new dependency is needed.
