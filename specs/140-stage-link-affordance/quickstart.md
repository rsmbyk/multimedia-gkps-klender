# Quickstart: The stage's entry links read as text until hovered

**Spec**: `specs/140-stage-link-affordance/spec.md`

## Prerequisites

- Python 3.12 with the repository virtualenv at `~/Projects/multimedia-gkps-klender/.venv`.
- The compose database published on `127.0.0.1:59075` (`docker compose up -d db` in the main
  checkout); its dev password is the one `docker-compose.yml` carries.
- Playwright's Chromium installed for that virtualenv.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-140
export DATABASE_URL="postgres://multimedia:multimedia@127.0.0.1:59075/multimedia"
export DJANGO_SECRET_KEY=dev-insecure-local-only-change-me
```

## Run

```sh
../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8773 --noreload
```

Open `http://127.0.0.1:8773/tatib/144/` and hover a song title.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the new behaviour, both themes and states | `manage.py test tests.e2e.test_reading.ReadingE2ETests.test_stage_entry_links_read_as_ink_until_hovered --keepdb` | pass |
| the surrounding reading suite | `manage.py test tests.e2e.test_reading --keepdb` | pass |
| the token pair still guards a live use | `manage.py test tests.test_design_tokens --keepdb` | pass |
| the media library keeps its link colour | `manage.py test tests.e2e.test_media_library --keepdb` | pass |

The page-rendering suites need
`override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')` or a
`collectstatic` first, as the repository's other E2E modules already arrange.

## Not yet runnable

Nothing. Every command above runs on the slice branch.
