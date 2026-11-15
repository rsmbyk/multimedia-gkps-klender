# Quickstart — spec 195

Worktree: `~/Projects/multimedia-gkps-klender-195` (branch `fix/195-hotfix-batch`). The venv lives in the main checkout.

## Serve the slice

```bash
cd ~/Projects/multimedia-gkps-klender-195
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

Static files: after editing `static/`, run `~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput` (Whitenoise manifest), then restart the server.

## Targeted tests (run in between; the full suite runs at push)

DB: host port from `docker compose port db 5432` (run in the main checkout), password from `docker-compose.yml`, then:

```bash
DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:<port>/gkps195 \
  ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test multimedia.web.tests \
  --keepdb
```

(The throwaway `gkps195` database avoids colliding with any parallel session's `test_multimedia`.)

## The six click paths

1. **US1** — hover a Today row in the Tata Ibadah sidebar: badge hidden while controls are up, back at rest.
2. **US2** — Edit a Tata Ibadah: title left, Copy as template right (34px), rule under the row; clicking opens the confirmation.
3. **US3** — sidebar → click a template (stage swap) → + New Tata Ibadah from template → Next → click **Date**: calendar opens. Reload the page by URL and repeat: opens the same way.
4. **US4** — open a service → add song entry → pick song, check verses → Save: entry created, stage names "Bait 1, 3"-style numbers. Empty checklist → refusal stays. Reopen for edit: same-looking checklist, summary in numbers.
5. **US5** — put a song screen on air (`/obs/source/overlay` + dock): a lyric whose lines wrap shrinks to two visual lines; one that fits keeps the accepted size.
6. **US6** — service on air in the overlay; edit one of its entries **in a different browser**; the overlay repaints within ~10 s; the dock follows. Same-browser: the repaint is immediate on save.
