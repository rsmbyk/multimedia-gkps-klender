# Quickstart: Back clears the Go To from the cue over an empty stage

Worktree `~/Projects/multimedia-gkps-klender-228`; venv in the main checkout. Point `DATABASE_URL`
at a throwaway database (Django creates `test_<name>`), derived from the compose `web` service's own
URL with the host set to `127.0.0.1:59075`.

```sh
RAW=$(docker exec multimedia-gkps-klender-web-1 printenv DATABASE_URL)
export DATABASE_URL=$(python3 - "$RAW" <<'PY'
import sys
from urllib.parse import urlsplit, urlunsplit, quote
u = urlsplit(sys.argv[1]); netloc = '%s:%s@127.0.0.1:59075' % (
    quote(u.username or '', safe=''), quote(u.password or '', safe=''))
print(urlunsplit((u.scheme, netloc, '/gkps233', '', '')))
PY
)
PYBIN=~/Projects/multimedia-gkps-klender/.venv/bin/python
$PYBIN manage.py test \
  tests.e2e.test_goto_shared_state.GotoSharedStateE2ETests.test_back_clears_a_passage_cue_when_no_service_is_open \
  tests.e2e.test_goto_shared_state.GotoSharedStateE2ETests.test_back_clears_a_song_cue_when_the_service_has_no_entries \
  tests.e2e.test_goto_shared_state.GotoSharedStateE2ETests.test_a_dock_back_clears_the_projector_cue_with_no_service \
  --noinput
$PYBIN manage.py test tests.e2e.test_goto_shared_state tests.e2e.test_dock_goto --noinput
```

Live preview: `runserver 0.0.0.0:8765 --noreload` from the worktree, then
`$PYBIN specs/228-goto-cue-back-reset/preview/probe.py --base http://127.0.0.1:8765`. The probe
starts a Go To from the dock with no service, presses Back and prints the cue before and after.
