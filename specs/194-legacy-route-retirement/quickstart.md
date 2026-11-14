# Quickstart: Retired Addresses

**Slice**: `specs/194-legacy-route-retirement` · Contracts: [`routes.md`](contracts/routes.md) ·
Data model: [`data-model.md`](data-model.md) — not duplicated here.

Commands run from this worktree. The venv lives in the main checkout
(`~/Projects/multimedia-gkps-klender/.venv/bin/python`); the database is the compose service in that
checkout, published on `127.0.0.1:59075` (`docker compose port db 5432`).

```sh
export DATABASE_URL=postgresql://multimedia:multimedia@127.0.0.1:59075/multimedia
PY=~/Projects/multimedia-gkps-klender/.venv/bin/python
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The retirement, the archive, the blank page and the reading addresses (FR-001–FR-009, FR-011, SC-001–SC-005) | `$PY manage.py test multimedia.web.tests.RetiredWebRouteTests --keepdb` | every test green |
| The note is a watermark until hovered (FR-006a) | `$PY manage.py test tests.e2e.test_retired_routes --tag=e2e --keepdb` | green with Playwright's Chromium installed; skipped cleanly without it |
| Nothing else regressed | `$PY manage.py test --exclude-tag=e2e --noinput` | pre-existing failures only (ITEM-137/139/140/141/144/153/156/174/175/184/185 are red by design) |
| The whole retirement by hand | `$PY manage.py runserver 8123` in one shell, then the loop below | one 302 per address, destination as `contracts/routes.md` says |

## The by-hand loop

```sh
base=http://127.0.0.1:8123
for path in /home /home/ /manage /manage/songs/12/ \
            /obs/bible/dock /obs/bible/dock/ /obs/songs/dock /obs/tatib/dock \
            /obs/bible/source /obs/songs/source /obs/tatib/source /obs/project/source \
            /obs/project/settings /archive/ /archive/home/ /archive/manage/songs/12/ \
            /archive/songs/ /archive/songs/books /archive/obs/songs/source /archive/nowhere/; do
  printf '%-30s ' "$path"
  curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' "$base$path"
done

# One hop, not two: the archived manage address never names /manage.
curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' "$base/archive/manage/songs/12/"

# The blank page: 200, no-store, no script, no image.
curl -sI "$base/obs/blank" | grep -i 'HTTP/\|cache-control'
curl -s "$base/obs/blank" | grep -c '<script\|<img'     # 0

# The reading addresses still answer 200.
for path in / /songs/ /songs/152/ /tatib/; do
  curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' "$base$path"
done
```

## Not yet runnable

- **The slice's own suite** (`RetiredWebRouteTests`, `tests/e2e/test_retired_routes.py`) does not
  exist until T002 and T010 write it; until then those two commands report `ModuleNotFoundError`.
  They are the exact commands the tasks run, kept here so the proof and the work cannot drift.
- **The OBS proof** (`manual` row): needs OBS with a scene holding an old browser source, and a
  person watching the program out. No command stands in for it.
- **The production smoke** (`manual` row): the deployment URL is not in the checkout
  (`.vercel/project.json` is absent), so the owner supplies the host; the same `curl` loop applies
  once it is known.
- **The E2E note test** runs only where Playwright's Chromium is installed (`playwright install
  chromium`); without it the module skips with its reason, which is not a failure.
