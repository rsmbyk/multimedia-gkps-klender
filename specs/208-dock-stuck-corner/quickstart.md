# Quickstart: the live entry header's corners follow its pin state

## Live preview

From the slice worktree:

```bash
cd specs/208-dock-stuck-corner/preview
./serve.sh            # http://127.0.0.1:8767/obs/dock
```

Open the **11 Oktober** service, open entries 2 and 3 by hand, make **HAL 5** live, then scroll.
Hard-reload (Ctrl+Shift+R) after a code change — the dev server serves static with only
`Last-Modified`.

## Tests

```bash
./run-tests.sh tests.e2e.test_dock_stuck_corner                       # the 12 pins
./run-tests.sh tests.e2e.test_obs_dock tests.e2e.test_dock_open_reset \
  tests.e2e.test_obs_dock_follow tests.e2e.test_dock_text_wrap \
  tests.e2e.test_dock_stuck_corner                                   # full dock regression
```

`run-tests.sh` inherits the compose web container's own `DATABASE_URL` and rewrites only the host,
port and database name to `gkps208`, so no credential is written to a file. The suite needs the
Playwright browser and the venv at `../../../../.venv` (the main checkout).
