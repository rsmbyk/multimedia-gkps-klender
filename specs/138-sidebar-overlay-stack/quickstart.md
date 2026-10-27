# Quickstart: the sidebars are a drawer stack

**Slice**: `specs/138-sidebar-overlay-stack`
Contracts: [`contracts/shell-state.md`](./contracts/shell-state.md) · Data: [`data-model.md`](./data-model.md)

Everything runs from the slice's worktree, against the compose database.

```sh
export DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/multimedia"
PY=/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python
```

## The rendered shell — Playwright E2E

```sh
$PY manage.py test tests.e2e.test_drawer_shell --keepdb
```

*Not yet runnable: the module is written in Implement (`tasks.md` T002–T014), so it does not exist
at gate 2.*

The modules this slice must not disturb:

```sh
$PY manage.py test tests.e2e.test_reading tests.e2e.test_navigation_freshness \
  tests.e2e.test_song_label_typography --keepdb
```

## The prototype, from this branch's own server

```sh
$PY manage.py collectstatic --noinput                 # Whitenoise serves _static/
$PY manage.py runserver 0.0.0.0:8772 --noreload       # 8772 is this slice's port
$PY specs/138-sidebar-overlay-stack/preview/build_prototype.py
$PY specs/138-sidebar-overlay-stack/preview/probe_prototype.py
```

These already ran at Preview and produced `preview/prototype-*.html`, the numbers in `## UI/UX`, and
the screenshots under `preview/shots/`. After Implement they can be rebuilt unchanged — the shell
will then carry the behaviour itself, and the prototype's `proto.css`/`proto.js` become redundant
probes rather than the source of the behaviour.

## What to look at

| Surface | Path | Expectation |
| --- | --- | --- |
| The reported 768px window | `http://127.0.0.1:8772/tatib/149/` at 768 wide | open a drawer: the stage stays 688px and the drawer floats over it |
| A stack | same, second level | the child covers the parent exactly |
| The 425px window | same at 425 wide | the toolbar, the menu drawer, full-width drawers, no strip |
| The desktop | same at 1440 wide | unchanged push columns |
| A service on a phone | same at 425, open a service | the drawer closes onto the page; no contents drawer is offered |
