# Quickstart: passage search comboboxes

**Spec**: `specs/238-passage-search-pickers/spec.md`
**Plan**: `specs/238-passage-search-pickers/plan.md`

See `contracts/README.md` for the interface position and `data-model.md` for the state the
combos drive.

## Setup

The slice worktree is `~/Projects/multimedia-gkps-klender-238`, branch
`feat/238-passage-search-pickers`. The launcher reads the database URL from the compose web
container; no credentials are written into the repo.

```sh
cd ~/Projects/multimedia-gkps-klender-238
python specs/238-passage-search-pickers/preview/run.py collectstatic --noinput
python specs/238-passage-search-pickers/preview/run.py runserver 0.0.0.0:8792 --noreload
```

Hard-reload the tab after a static edit. The live preview is
`http://127.0.0.1:8792/tatib/151/`; drive `/` → Tata Ibadah rail → `111ojo` → `+ Passage`.

## Run

```sh
# Behaviour + geometry probe
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/238-passage-search-pickers/preview/probe.py

# Song-picker regression baseline
python specs/238-passage-search-pickers/preview/run.py test \
  tests.e2e.test_song_entry_pickers --keepdb --noinput

# New acceptance module (from tasks.md)
python specs/238-passage-search-pickers/preview/run.py test \
  tests.e2e.test_passage_search_pickers --keepdb --noinput
```

All commands are runnable now. Playwright Chromium is installed on this machine; if another
session holds the shared test database, pass a throwaway database name to the launcher.
