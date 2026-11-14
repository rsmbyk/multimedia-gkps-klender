# Quickstart: Stack Restart Policy

**Slice**: `specs/191-compose-restart` · Contracts: [`none`](contracts/none.md) · Data model:
[`data-model.md`](data-model.md) — not duplicated here.

Commands are run from the slice worktree. The venv lives in the main checkout
(`~/Projects/multimedia-gkps-klender/.venv/bin/python`); the database is the compose service.

## The file guard (runs today)

```sh
# 1. The targeted test — the two FR rows. SimpleTestCase never touches the
#    database, but Django's runner still sets one up, so point DATABASE_URL
#    at the compose Postgres (port via `docker compose port db 5432`).
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.test_docker_compose --keepdb

# 2. What compose itself now renders — every always-on service shows the policy.
docker compose config | grep -n 'restart'
```

Expected: the new test passes, and the rendered config shows `restart: unless-stopped` under
`web`, `db` and `media`.

## The runtime proof (manual — needs a daemon restart)

```sh
# 3. US1/SC-001: restart Docker Desktop (or reboot the machine), then:
docker ps                                    # web, db, media all `Up`
curl -s -o /dev/null -w '%{http_code}\n' "http://127.0.0.1:${WEB_PORT:-63404}/"   # 200

# 4. US2: stop on purpose, restart the daemon, nothing comes back.
docker compose stop
#    …restart the daemon…
docker ps                                    # no project container running
```

Step 3 is the one the slice exists for; it runs the next time the machine restarts, and the
out-of-band `docker update` repair of 2026-11-14 already demonstrated the mechanism with media.
