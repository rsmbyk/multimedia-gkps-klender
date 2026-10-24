# Quickstart: Match the Tata Ibadah date header to the songbook header

**Spec**: `specs/123-tatib-date-header-parity/spec.md`

## Serve it

From this worktree, with the project's local Postgres:

```sh
DATABASE_URL=postgres://… .venv/bin/python manage.py runserver 0.0.0.0:8766 --noreload
```

Stylesheets are served per request, so a CSS edit shows on reload; Python edits need a restart.

## Verify by hand

1. Open `/`, click **Tata Ibadah** in the rail, open the service dated **25 Oktober 2026** — the date sits
   above the title at the same size, weight, tracking, and colour as the song page's songbook header.
2. Open `/songs/1351/` beside it and compare the two eyebrows.
3. Narrow the window until the stage is under ~271px of header width: the **Project** button drops beneath
   the date on an 8px gap, the date keeps its size, and the page does not scroll sideways.
4. `/tatib/?mode=template` → open a template service: the `Tata Ibadah` label carries the same style.

## Verify with tests

```sh
# the two new browser pins and the existing centring pin
.venv/bin/python manage.py test \
  tests.e2e.test_reading.ReadingE2ETests.test_tatib_date_header_matches_songbook_header \
  tests.e2e.test_reading.ReadingE2ETests.test_tatib_date_header_reflows_at_a_narrow_stage \
  tests.e2e.test_reading.ReadingE2ETests.test_tatib_date_and_project_button_are_vertically_centered \
  --keepdb

# the header-text pins
.venv/bin/python manage.py test multimedia.web.tests.ReadingViewTests --keepdb
```
