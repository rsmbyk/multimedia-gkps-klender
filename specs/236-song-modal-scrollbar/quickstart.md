# Quickstart: song entry modal scrollbar

**Spec**: `specs/236-song-modal-scrollbar/spec.md`

## Prerequisites

- The worktree's slice branch checked out; the repository's Python environment with Django and
  Playwright available.
- A local PostgreSQL database reachable through `DATABASE_URL`, and a Chromium browser installed
  for Playwright. Credentials are deliberately not written into repo artifacts.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-236
# Point DATABASE_URL at a throwaway database (see the repo's local dev notes); the slice shares
# the machine's Postgres with other worktrees, so do not reuse the default test database.
```

## Run

```sh
# Static preview, no server needed: open in a browser tab.
xdg-open specs/236-song-modal-scrollbar/preview/index.html

# Rebuild it after editing snippets or CSS copies, then re-check the chat frame:
python3 specs/236-song-modal-scrollbar/preview/build_preview.py
python3 ~/.hermes/skills/software-development/obs-browser-surfaces/scripts/verify-chat-preview-frame.py \
  specs/236-song-modal-scrollbar/preview/index.html --width 900
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Chat-frame preflight | `python3 …/verify-chat-preview-frame.py …/preview/index.html --width 900` | `PASS`, 1 inline stylesheet, 0 external subresources |
| Targeted E2E | `<venv>/python manage.py test tests.e2e.test_song_modal_scrollbar --keepdb` | all tests in the new module pass; base fails the gutter assertions with `5px` |
| Full browser suite | deferred to the push step per the owner's standing preference | report only; do not run between pushes |

## Not yet runnable

- The targeted E2E command is written with a `<venv>` placeholder and requires a local
  `DATABASE_URL`: the interpreter path and the database credentials are machine-specific and are
  intentionally not stored in the spec pack. Fill them from the local environment before running.
- The preview verifier needs a Python with Playwright installed; `python3` on a machine without it
  must be replaced by that interpreter.
