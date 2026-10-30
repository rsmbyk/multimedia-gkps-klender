# Quickstart: Audio and video name their play/pause key

**Spec**: `specs/160-shortcuts-audio-video-groups/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` — Django's runner and Playwright 1.47
  with its Chromium build.
- A database URL no other worktree is using:
  `DATABASE_URL=postgres://multimedia:***@127.0.0.1:<db-port>/gkps160`. Page-rendering tests also
  need the plain static-files storage, or a `collectstatic` first (the local tree has no manifest).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-160
export PY=../multimedia-gkps-klender/.venv/bin/python
PW=$(grep -m1 'POSTGRES_PASSWORD' docker-compose.yml | sed 's/.*POSTGRES_PASSWORD: *//; s/"//g; s/ *$//')
DBPORT=$(cd ../multimedia-gkps-klender && docker compose port db 5432 | cut -d: -f2)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:${DBPORT}/gkps160"
```

## Run

```sh
$PY manage.py test multimedia.web.tests.ServiceProjectorTests \
  --keepdb --noinput
```

The new case is `test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own`; run it alone
with `... .ServiceProjectorTests.test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own`.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the sheet's groups and rows | the `Run` command | green after the template change; red before it (`Display` still holds the combined row, and no `Audio` heading exists) |
| the media contract that named the old row | `$PY manage.py test multimedia.web.test_media --keepdb --noinput` | green — the case now reads `Play/Pause` |
| the sheet's geometry | `$PY specs/160-shortcuts-audio-video-groups/preview/measure.py` | `today` 1123.4 × 676.1px, `after` 1094.4 × 676.1px, columns `[634.2, 634.2, 634.2]`, `scrollHeight` 675 at both window sizes |
| the preview by eye | open `specs/160-shortcuts-audio-video-groups/preview/preview.html` | the bar's `Today` / `After` toggle; `Audio` and `Video` are the middle column's third and fourth groups |
| the running page, after the merge | the compose projector at `http://localhost:63404/projector?service=<id>`, press K | the sheet shows `Audio` and `Video`; Space still plays and pauses the showing media |

## Not yet runnable

- The last row's live check, before the merge: the compose `web` service serves the `develop`
  checkout, so a worktree's template is not on it. Recorded as the `manual` row for SC-001 and
  SC-004.
- The heavy E2E suites (`tests/e2e/test_projector.py`, `tests/e2e/test_audio_display.py`,
  `tests/e2e/test_video_display.py`) are deferred to the push step by the owner's standing rule;
  between stages the targeted Django cases above are the run.
