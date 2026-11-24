# Quickstart: entry modal title band

**Spec**: `specs/240-entry-modal-title/spec.md` · **Contracts**: `contracts/none.md` ·
**Data model**: `data-model.md`

## Prerequisites

- The slice worktree at `~/Projects/multimedia-gkps-klender-240`, its collectstatic
  output refreshed after the CSS edit, and its local server running.
- The repository Python 3.12 environment with Django and Playwright; a local
  PostgreSQL database via `DATABASE_URL`. No credential is stored in the spec pack.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-240
python3 ~/.hermes/cache/scratch/gkps240/run.py collectstatic --noinput
python3 ~/.hermes/cache/scratch/gkps240/run.py runserver 0.0.0.0:8790 --noreload
```

The launcher is machine-local and reads the database URL from the compose web
container at run time. Hard-reload the browser tab after each static change.

## Run

```sh
# Live preview: open / first, click Tata Ibadah, open service pk 149.
xdg-open http://127.0.0.1:8790/tatib/149/

# Frozen before/after readouts, dark, 1440x900 and 390x844:
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/240-entry-modal-title/preview/probe.py
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Existing frame guard | `python3 ~/.hermes/cache/scratch/gkps240/run.py test tests.e2e.test_entry_modal_frame --keepdb` | green after the fix; `test_new_text_dialog_matches_new_media` reads `'0px' != '20px 26px'` on the base |
| New title E2E | `python3 ~/.hermes/cache/scratch/gkps240/run.py test tests.e2e.test_entry_modal_title --keepdb` | green after the fix; red on the base at 0px/1px offsets |
| Verse header guard | `python3 ~/.hermes/cache/scratch/gkps240/run.py test tests.e2e.test_verse_modal_header --keepdb` | one rule, title padding/border `0px` in all cases |
| Full browser suite | deferred to the push step per your standing preference | report only; do not run between pushes |

## Not yet runnable

- The new E2E module is written during Implement, not at Plan; its command is a path,
  not a claim that it has already passed.
- The probe needs a Python with Playwright and the local server; both are
  machine-specific and intentionally absent from the repo.
