# Quickstart

## Run it

```bash
# from the worktree, with the compose database
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:$(docker compose port db 5432 | cut -d: -f2)/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8802 --noreload
```

An empty service on the local database: `/tatib/145/` (25 Oktober 2026). A service that holds items, for the
no-regression check: `/tatib/144/`.

## Take the four measurements

```bash
.venv/bin/python specs/130-empty-service-tiles/preview/probe_empty_stage.py http://127.0.0.1:8802/tatib/145/
```

It opens 1440×900, 1280×800, 1024×700 and 390×844 and prints, per size: the gap between the header's bottom
edge and the block, the gap between the block and the bottom of the window, whether the five tiles share one
`y`, whether each is square, and the smallest tile's side.

Expected on the branch:

| Viewport | Gaps above / below | Tiles |
| --- | --- | --- |
| 1440×900 | 318.6 / 318.7 | 5 × 52px, one row |
| 1280×800 | equal | 52px, 3 + 2 |
| 1024×700 | equal | 52px, 3 + 2 |
| 390×844 | equal | 52px, 3 + 2 |

## Existing behaviour that must not move

```bash
for port in 8801 8802; do  # 8801 = the branch before this slice
  .venv/bin/python specs/130-empty-service-tiles/preview/probe_empty_stage.py \
    http://127.0.0.1:$port/tatib/144/ --layout-only
done
```

Both must print the same header height, the same 30px header margin and the same 8px body margin.

## The tests

```bash
DATABASE_URL=... DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
.venv/bin/python manage.py test \
  tests.e2e.test_entries.EntryModalE2ETests.test_an_empty_service_centres_a_row_of_square_icon_buttons \
  tests.e2e.test_entries.EntryModalE2ETests.test_an_empty_service_invites_the_first_item \
  tests.e2e.test_saved_render_parity \
  tests.e2e.test_offline_library.OfflineLibraryE2ETests.test_empty_saved_tatib_shows_add_media_after_sidebar_navigation_offline \
  --keepdb
```
