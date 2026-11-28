# Quickstart: Cloud Run writes pass CSRF

Run from this worktree. The venv lives in the main checkout.

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-251
DJANGO_DEVELOPMENT_MODE=True DJANGO_ALLOWED_HOSTS='*' \
  /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.test_cloudrun_csrf --noinput -v 2
```

Expected: `test_a_forwarded_https_request_is_accepted` is red before the setting lands and green after;
`test_without_the_proxy_header_the_https_origin_is_rejected` is green in both states.

Live probe (non-destructive — the PK does not exist):

```python
# GET /editor/songbook/new/ with a cookie jar, then POST to
# /editor/songbook/999999999/delete/ with the CSRF token and
# Origin: https://<live host>. 403 means the fix is not deployed; 404 means CSRF passed.
```

Full reproduction and the two live hostnames are in
[`spec.md`](spec.md) and the diagnosis recorded on 2026-11-28.
