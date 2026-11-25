# Quickstart — spec 242

See [contracts.md](./contracts.md) (none) and [data-model.md](./data-model.md) (no change).

```sh
# Live preview (worktree code, real compose DB); no credentials are printed
cd ~/Projects/multimedia-gkps-klender-242
./specs/242-dock-top-pin/preview/serve.sh        # serves /obs/dock on 127.0.0.1:8793

# Targeted evidence — before and after builds
./.venv/bin/python specs/242-dock-top-pin/preview/probe_top.py http://127.0.0.1:63404 specs/242-dock-top-pin/preview/shots/before
./.venv/bin/python specs/242-dock-top-pin/preview/probe_top.py http://127.0.0.1:8793 specs/242-dock-top-pin/preview/shots/after

# New acceptance module (throwaway gkps242 database; reads the compose DB password at runtime)
./specs/242-dock-top-pin/preview/run-tests.sh tests.e2e.test_dock_top_pin
```

The preview server must be started from the worktree; port 8793 was free when the slice was cut.
`run-tests.sh` is added during Implement (it follows spec 208's runner verbatim with the database
name changed) and is runnable at that point; the two probe commands above are runnable now.
