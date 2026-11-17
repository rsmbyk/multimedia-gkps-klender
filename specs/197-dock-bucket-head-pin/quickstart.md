# Quickstart: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`

## Prerequisites

- Python 3.12 with the repo's venv (`../multimedia-gkps-klender/.venv/bin/python` from a worktree).
- The compose database reachable: `docker compose port db 5432` (59075 on this machine).
- Playwright's Chromium installed (`playwright install chromium`).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-197
export DATABASE_URL='postgres://multimedia:multimedia@127.0.0.1:59075/multimedia'
../multimedia-gkps-klender/.venv/bin/python manage.py collectstatic --noinput
```

`collectstatic` is needed for the page to serve the changed stylesheet locally: the project uses
`CompressedManifestStaticFilesStorage`, so the hashed copy in `_static/` is what `{% static %}` resolves to.

## Run

```sh
../multimedia-gkps-klender/.venv/bin/python manage.py runserver 127.0.0.1:8767 --noreload
```

Open `http://127.0.0.1:8767/obs/dock` at 449×604 (dark theme) and scroll the picker past the first bucket.
The developed page answers the same route on `:63404` for comparison.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The strip above a pinned head holds no row | `document.elementFromPoint(x, pickBody.top + 2)` while a head is pinned | `H3.group__head` (on develop: `BUTTON.servicerow`) |
| The head starts at the scroller's top | head's `getBoundingClientRect().top − pickBody.top` | `0.0` (develop: `4.0`) |
| The label keeps its place | the same difference measured on the head's text at `scrollTop` 0 and pinned | one number, `14.0` |
| The air between buckets | next label's top − previous group's last row's bottom | `26.0` (develop: `10.0`) |
| The suite | `../multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_dock_bucket_head --keepdb` | 5 tests, all pass |
| Nothing else moved | `git -C . diff develop -- static/styles/design/obs-dock.css` | three declarations, all inside the picker's rules |

## Not yet runnable

- Nothing. Every command above runs against the worktree as it stands.