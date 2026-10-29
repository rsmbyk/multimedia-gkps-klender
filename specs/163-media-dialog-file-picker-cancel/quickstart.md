# Quickstart: dismissing the file picker leaves the New media dialog open

**Spec**: `specs/163-media-dialog-file-picker-cancel/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Playwright and its Chromium builds already
  installed).
- A database URL no other worktree is using:
  `DATABASE_URL=postgres://multimedia:<password>@127.0.0.1:<db-port>/gkps163`.
- For the live check only: this worktree's own server on port **8814**, because the media companion admits
  that origin and refuses others (`GKPS_MEDIA_ALLOWED_ORIGINS`; measured: `8768` → 403, `8814` → 200).

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-163
export PY=../multimedia-gkps-klender/.venv/bin/python
PW=$(grep -m1 'POSTGRES_PASSWORD' docker-compose.yml | sed 's/.*POSTGRES_PASSWORD: *//; s/"[[:space:]]*$//')
DBPORT=$(cd ../multimedia-gkps-klender && docker compose port db 5432 | cut -d: -f2)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:${DBPORT}/gkps163"
```

## Run

```sh
$PY manage.py test tests.e2e.test_media_library.MediaLibraryE2ETests.test_dismissing_the_file_picker_leaves_the_new_media_dialog_open --keepdb --noinput
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the dismissal case | the `Run` command above | red before the fix (the dialog is gone after 400 ms), green after it |
| a chosen file survives | the same command with `…::test_a_dismissed_picker_keeps_the_chosen_file` | red before, green after |
| the library selection survives | the same command with `…::test_a_picker_dismissal_keeps_the_library_selection` | red before, green after |
| Escape still closes | the same command with `…::test_escape_still_closes_the_new_media_dialog` | green before and after — it fails only against the wrong fix (deleting the listener) |
| the module | `$PY manage.py test tests.e2e.test_media_library --keepdb --noinput` | no case changed by this slice (its pre-existing reds are the board's, not this branch's) |
| the live route, by hand | `$PY manage.py runserver 0.0.0.0:8814 --noreload`, then `http://localhost:8814/tatib/149/` → *New media* → *Choose file to upload* → dismiss the system picker | the dialog stays open with its title; Escape on the dialog then closes it |
| the live route, by probe | `$PY specs/163-media-dialog-file-picker-cancel/preview/picker_probe.py --url http://localhost:8814/tatib/149/` | `OK — a dismissed picker leaves the dialog, its title and its file; Escape still closes it`, exit 0 |

## Not yet runnable

- Nothing. Unlike slice 150, the live route is reachable before the merge: the companion admits
  `http://localhost:8814`, and a real PNG was inspected and chosen through the page while specifying.
