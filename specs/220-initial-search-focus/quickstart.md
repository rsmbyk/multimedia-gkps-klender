# Quickstart: reproduce the numbers and run the tests

**Slice**: `specs/220-initial-search-focus` · worktree `~/.hermes/worktrees/220-initial-search-focus/multimedia-gkps-klender`

## Run the shell

```sh
# The compose stack publishes the public site on 63404 (main checkout) — or run this worktree:
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

The landing is at `/`, `/search/`, `/bible/`, `/songs/`, `/tatib/`; results at `/search/?q=<query>`.

## Run the tests

```sh
# Throwaway database so a parallel slice's run cannot collide:
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:<port>/gkps220" \
  /home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_reading.ReadingE2ETests.test_the_empty_search_landing_takes_focus \
  tests.e2e.test_reading.ReadingE2ETests.test_the_search_rail_opens_a_focused_landing \
  tests.e2e.test_reading.ReadingE2ETests.test_results_never_take_focus \
  tests.e2e.test_reading.ReadingE2ETests.test_submitting_from_the_landing_moves_focus_out \
  tests.e2e.test_reading.ReadingE2ETests.test_reading_routes_never_take_search_focus \
  --noinput
```

`--keepdb` on a second run; the page-rendering tests need
`override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')` or a
`collectstatic` first.

## Read the numbers

```sh
# In a browser at the shell, at 1440x900 and 390x844:
#   document.activeElement.id                       -> "searchQuery" on the landing, never on results
#   document.getElementById('searchQuery').getBoundingClientRect()
#   document.documentElement.scrollHeight === innerHeight
```

The preview reproduces the same values from the file:

```sh
xdg-open specs/220-initial-search-focus/preview/index.html
```

## Deliver

```sh
VERSION=1.36.5   # bump: patch
# CHANGELOG.md: one line under ## [Unreleased] ### Fixed
# docs/spec/reading.md: R15 modified (focus clause), R50 added — Fold
```