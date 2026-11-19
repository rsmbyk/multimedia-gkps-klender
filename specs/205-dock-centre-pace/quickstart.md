# Quickstart — spec 205 (dock centre pace)

Links: [data-model.md](data-model.md) · [contracts/](contracts/README.md) (none) ·
[spec.md](spec.md) · [preview/README.md](preview/README.md).

## Run the live preview (already running from this worktree)

```sh
# slice server on 8765 (started from this worktree with the compose DB):
#   DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:59075/multimedia \
#   ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
# after editing static/: collectstatic --noinput, then restart (manifest storage).
open http://127.0.0.1:8765/obs/dock        # after
open http://127.0.0.1:63404/obs/dock       # before (compose web, develop)
```

Open **Ibadah Pace Probe**, click a screen row, hold ArrowDown.

## Measure

```sh
cd specs/205-dock-centre-pace/preview
~/Projects/multimedia-gkps-klender/.venv/bin/python probe.py --url http://127.0.0.1:8765 --label after
~/Projects/multimedia-gkps-klender/.venv/bin/python probe.py --url http://127.0.0.1:63404 --label before
```

## Targeted tests (between gates; full suite at the push step)

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-205
PW=$(grep -oP 'POSTGRES_PASSWORD:\s*\K\S+' docker-compose.yml | head -1)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:59075/gkps205"
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_obs_dock_follow --keepdb --noinput
```

A throwaway database name (`gkps205`) avoids the shared `test_multimedia` another session may hold.
The new pace test is red on develop (400 ms) and green on the slice (200 ms); prove red by stashing
the `obs-dock.js` change, running, then popping.