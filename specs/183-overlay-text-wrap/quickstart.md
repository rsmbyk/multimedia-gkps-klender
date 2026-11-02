# Quickstart: the overlay's text wraps inside the box that owns it

**Spec**: [`spec.md`](./spec.md) · **Plan**: [`plan.md`](./plan.md) · **Data model**:
[`data-model.md`](./data-model.md) · **Contracts**: [`contracts/none.md`](./contracts/none.md)

Everything below runs from this slice's worktree (`~/Projects/multimedia-gkps-klender-183`), with the
main checkout's virtualenv (`~/Projects/multimedia-gkps-klender/.venv/bin/python`). The compose
Postgres is the only service needed; a throwaway database keeps the dev data untouched.

## 1 — A database of this slice's own

```sh
docker exec -e PGPASSWORD=multimedia multimedia-gkps-klender-db-1 \
  psql -U multimedia -d postgres -c 'CREATE DATABASE gkps183'
export DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/gkps183"
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py migrate --noinput
```

## 2 — The fixture the numbers come from

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py shell \
  < specs/183-overlay-text-wrap/preview/seed.py
```

Seven entries: a body with a 120-character run (the report), a pasted 140-character URL after the mark
`L.`, a long lyric, a passage with a long verse title, two short controls, and a 64-character entry
title. It prints the service id; every command below takes it as `--service`, and the probe and the
preview resolve each entry to its screen from the projector's own screen list.

## 3 — The acceptance tests (red first, then green)

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_obs_overlay_wrap
```

Nine cases. Removing the one declaration (`git stash push -- static/styles/design/obs-overlay.css`)
turns the wrapping cases red with the measured spill in the failure message; restoring it turns the
module green. `converge.md` records both runs, including the pass after the scope was widened.

## 4 — The review page

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8816 --noreload
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/183-overlay-text-wrap/preview/build_preview.py --service <id>
```

Then open `specs/183-overlay-text-wrap/preview/index.html`. It is static and needs no server:
everything it shows was captured from the page above.

## 5 — The measurements on their own

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/183-overlay-text-wrap/preview/probe.py --service <id> --size 1920x1080
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/183-overlay-text-wrap/preview/probe.py --service <id> --size 1920x1080 --normal
```

`--normal` restores the declaration, so the same six states are printed as the state before the slice
and after it; the numbers land in `scratch/shots/<after|before>-<size>.json`.
