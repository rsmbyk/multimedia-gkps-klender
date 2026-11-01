# Contract — the launcher command

Two scripts implement one contract: `docker/up.sh` (POSIX `sh`, macOS and Linux) and `docker/up.ps1`
(Windows PowerShell 5.1+). An operator may use either, and the rest of the stack must not know which
one started it.

## Invocation

```
docker/up.sh  [command] [args...]        # macOS, Linux
docker\up.ps1 [command] [args...]        # Windows PowerShell
```

- No arguments → `docker compose up -d`.
- The first argument names a compose command (`up`, `down`, `build`, `logs` …), so
  `docker/up.sh --build` is read as `up -d --build` and `docker/up.sh down` as `down`.
- `--print` → `docker compose … config`, printed to standard output, nothing started. It exists so a
  reviewer can see the mounts without running the stack.

## Environment

| Variable | Read | Effect |
| --- | --- | --- |
| `GKPS_FONTS_DIR` | passed through untouched | the operator's directory; `.env` still wins as it does today |
| `TMPDIR` / `TEMP` | yes | where the generated override is written |

## Files written

`${TMPDIR:-/tmp}/gkps-host-fonts.yaml` — a minimal compose file holding the discovered read-only
mounts, rewritten on every run, readable after the run for inspection. It is never committed and never
read by the application.

## Exit behaviour

- A directory that is absent or unreadable is skipped; it never fails the run.
- A missing Docker or Compose surfaces Docker's own message and its own non-zero exit code.
- The launcher adds no output of its own except the `--print` case and one line naming how many font
  directories it mounted.

## Guarantee kept by the base file

`docker-compose.yml` remains runnable on its own: `docker compose up` starts the same three services
with the operator's directory mounted and no host fonts. The launcher is additive, never required.
