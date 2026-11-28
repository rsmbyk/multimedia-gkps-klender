# Quickstart: Enter accepts a delete confirmation

**Spec**: `specs/256-enter-confirms-delete/spec.md`

## Prerequisites

- Slice worktree at `~/Projects/multimedia-gkps-klender-256`, main checkout at
  `~/Projects/multimedia-gkps-klender` with `.venv/bin/python`.
- Compose `db` service running; the `gkps256` database is created by `serve.py` if absent.
- Playwright Python and its Chromium browser for the E2E pins.

## Setup

```sh
# from the slice worktree; both helpers read the DB credential at run time
# and never write it to disk
.venv/bin/python specs/256-enter-confirms-delete/preview/serve.py   # background
```

## Run

Open `http://127.0.0.1:8768/` from the home URL and click through to any delete confirmation; press
Enter with focus away from its Delete button. `serve.py` reseeds `gkps256` on each start and calls
`collectstatic`, so restart it after editing anything under `static/`.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Four E2E pins | `.venv/bin/python specs/256-enter-confirms-delete/preview/run-tests.py tests.e2e.test_enter_delete_confirm` | `Ran 4 tests` … `OK` |
| Before/after observables | `.venv/bin/python specs/256-enter-confirms-delete/preview/probe.py <tag>` | one JSONL row per surface; baseline 0 activations, tagged-after 1 |
| JS syntax | `node --check static/web/enter-delete.js` | no output, exit 0 |
| No stray markers | `grep -rn 'NEEDS CLARIFICATION' specs/256-enter-confirms-delete` | no match |

## Not yet runnable

- None. The two helper scripts and the test module are present and have been run.
