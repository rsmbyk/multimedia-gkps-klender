# Quickstart: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`

## Prerequisites

- The repo's virtualenv, in the main checkout: `~/Projects/multimedia-gkps-klender/.venv`
- Playwright's Chromium for that venv (`~/.cache/ms-playwright/chromium-*`)
- PostgreSQL from the compose stack; its host port comes from `docker compose port db 5432`
  (59075 at the time of writing) and the password from `docker-compose.yml`
- No new dependency, no migration, no `collectstatic`: the change is a template line, a script line
  and one model sentence, and the dev server re-reads templates and static files per request

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-162

# the preview, rebuilt from the app's own rendered fragment (needs the dev server below)
python specs/162-song-verse-empty-state/preview/build_preview.py
```

## Run

```sh
# the slice running, against the local library
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8842 --noreload
```

Open `http://127.0.0.1:8842/tatib/149/`, press `+ Song`, search `lagu kosong`, and pick it.

The preview opens by itself: `specs/162-song-verse-empty-state/preview/preview.html`.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| A verse-less song is named, not mistaken for no song | `manage.py test tests.e2e.test_entries.EntryModalE2ETests --keepdb` | `test_a_song_with_no_verses_is_named_and_cannot_be_saved` passes: the trigger reads `This song has no verses`, is disabled, and Save answers with the song's own refusal |
| The no-song and with-verses lines are unchanged | same command | `test_the_song_pick_searches_and_the_verses_start_all_checked` and `test_single_verse_song_keeps_checked_verse_and_disables_picker` pass |
| The edit form says it before the script runs | `manage.py test multimedia.web.tests.ServiceEntryViewTests --keepdb` | `test_an_edit_form_for_a_verse_less_song_states_it_in_the_markup` passes |
| Both refusals keep their own sentence | `manage.py test multimedia.tatib.tests.ServiceEntryTests --keepdb` | `test_a_song_entry_keeps_at_least_one_verse` and `test_a_song_entry_with_no_verses_names_the_song` pass |
| The preview's numbers | `preview/build_preview.py` then open the file | the trigger is 38px tall in every row; the new line's summary box is 158.52×18.89, one line |

The runs above need `DATABASE_URL` pointing at a database name no other session is using — e.g.
`postgres://multimedia:***@127.0.0.1:59075/gkps162`, which creates and drops `test_gkps162`.

## Not yet runnable

- **The live picker with the real search.** It needs the running app and a song without verses in
  the database; the local library has seven (`lagu kosong` among them), so the dev server above is
  the way to see it by hand. The preview cannot fetch, so it shows the markup each state produces.
