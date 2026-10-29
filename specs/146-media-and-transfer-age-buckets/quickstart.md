# Quickstart: the Media Library and the transfer history group by age

**Slice**: `specs/146-media-and-transfer-age-buckets`

Data model: [`data-model.md`](./data-model.md) · Interface: [`contracts/README.md`](./contracts/README.md) ·
Traceability: [`plan.md`](./plan.md)

## The preview

```sh
open ~/Projects/multimedia-gkps-klender-146/specs/146-media-and-transfer-age-buckets/preview/preview.html
```

Opened directly (`file://`); it needs no server. Fixtures and the companion's real snapshot are both in the
page, behind the `DATA` control. States and what to look for:
[`preview/README.md`](./preview/README.md).

## The slice's own suite

```sh
cd ~/Projects/multimedia-gkps-klender-146
DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/gkps146" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_media_age_buckets --keepdb
```

- `gkps146` is a throwaway database name: Django creates `test_gkps146`, so this run never collides with
  another slice's suite on the same Postgres. It names a different database, not a different server — a
  second suite running on the same Postgres still slows this one down, because both flush between tests.
- Playwright (Python) and its Chromium are already installed in the main checkout's `.venv`; the suite is
  a `StaticLiveServerTestCase`, so no dev server is started by hand.
- `UserWarning: No directory at: …/_static/` is expected: the browser suites override
  `STATICFILES_STORAGE` to read `static/` directly, so no `collectstatic` is needed for them.

## The repository's suites this slice must not break

```sh
DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/gkps146" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test multimedia.web tests --keepdb
```

The browser suites are heavy and, per the owner's workflow, run at the push step rather than on every pass;
the nine red-on-`develop` tests listed on the board are not this slice's to fix.

## The live page

`/media-library/` draws its rows from the loopback companion, which accepts only two origins —
`http://localhost:63404` and `http://127.0.0.1:63404` — and that port is the running compose stack on
`develop`. To click through this branch live, that `web` service has to be pointed at this worktree (or the
suite's routed fixtures used instead); the static preview is the gate-1 substitute.
