# Quickstart: A passage cue carries its current and end verse

**Spec**: `specs/229-cue-verse-counter/spec.md`

## Prerequisites

- The slice worktree `~/Projects/multimedia-gkps-klender-229`; the venv in the main checkout at
  `~/Projects/multimedia-gkps-klender/.venv/bin/python`.
- The compose `db` container publishing 5432 as 59075 on this machine. Point `DATABASE_URL` at a
  throwaway database so Django creates `test_<name>` and no other session collides.

## Setup

```sh
RAW=$(docker exec multimedia-gkps-klender-web-1 printenv DATABASE_URL)
export DATABASE_URL=$(python3 - "$RAW" <<'PY'
import sys
from urllib.parse import urlsplit, urlunsplit, quote
u = urlsplit(sys.argv[1]); netloc = '%s:%s@127.0.0.1:59075' % (
    quote(u.username or '', safe=''), quote(u.password or '', safe=''))
print(urlunsplit((u.scheme, netloc, '/gkps229', '', '')))
PY
)
PYBIN=~/Projects/multimedia-gkps-klender/.venv/bin/python
```

## Run

```sh
cd ~/Projects/multimedia-gkps-klender-229
$PYBIN manage.py test multimedia.web.tests.ServiceProjectorTests --noinput
$PYBIN manage.py test tests.e2e.test_projector.ProjectorE2ETests tests.e2e.test_goto_shared_state --noinput
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Payload fields | `ServiceProjectorTests` | scripture screens carry `verse`, the entry carries both bounds |
| Service cue | the three new `test_projector.py` cases | `3/5 → 4/5 → 5/5`, `3/3`, zero counters on non-scripture |
| Go To cue | the new `test_goto_shared_state.py` case | `1/3 → 2/3 → 3/3`, end changes with the chapter, flip inert |
| Cue geometry | `test_corner_cue_parts_share_the_bottom_band_vertical_center` | all parts centred at `height − 32px` at 1366×768 and 1920×1080 |
| Static preview | `http://127.0.0.1:8771/specs/229-cue-verse-counter/preview/index.html` | Before/After frames and stepping buttons render with the real CSS |

## Not yet runnable

- The Vercel production deploy: no preview deployment is part of this slice.
