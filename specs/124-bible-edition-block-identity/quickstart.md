# Quickstart: Keep a chapter's verse text when the reading page updates in place

**Spec**: `specs/124-bible-edition-block-identity/spec.md`

## Prerequisites

- The repository's virtualenv (`.venv/bin/python` in the main checkout) with `requirements.txt` and
  `requirements-dev.txt` installed, including Playwright and its Chromium build.
- The local database service running (`docker compose up -d db`).
- `DATABASE_URL` pointing at that service.

## Setup

```sh
# from the slice worktree
PORT=$(docker compose port db 5432 | sed 's/.*://')
export DATABASE_URL="postgres://multimedia:<password>@127.0.0.1:${PORT}/multimedia"
```

## Run

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8767 --noreload
```

Then open `/home/`, choose Alkitab, open Rut, open chapter 1, then chapter 2 — the verses stay on the
stage.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The reported path keeps its verse text | `manage.py test tests.e2e.test_reading.ReadingE2ETests.test_same_name_edition_blocks_keep_the_verse_text --keepdb` | 1 test, green |
| Neighbouring reading behaviour is unchanged | `manage.py test tests.e2e.test_reading.ReadingE2ETests.test_shell_navigates_in_place tests.e2e.test_reading.ReadingE2ETests.test_bible_sidebar_labels_follow_edition_and_reset_on_refresh tests.e2e.test_reading.ReadingE2ETests.test_sim_codes_titles_labels_and_fallback_follow_selected_edition tests.e2e.test_reading.ReadingE2ETests.test_bible_edition_survives_menu_switches_and_history tests.e2e.test_reading.ReadingE2ETests.test_the_translation_switch_fills_the_hovered_option tests.e2e.test_targeted_reading_updates tests.e2e.test_navigation_freshness --keepdb` | 15 tests, green |
| The saved reading view still matches the server page | `manage.py test tests.e2e.test_saved_render_parity --keepdb` | 3 tests, green |

## Not yet runnable

- Nothing — the slice runs against the existing local stack; no new service, fixture service, or browser
  binary is needed.
