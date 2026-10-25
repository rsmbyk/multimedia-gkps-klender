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

It opens 1440×900, 1280×800, 1024×700 and 390×844 and prints, per size: where the block's centre sits in the
reading area, how far its top clears the header, whether the five tiles share one `y`, whether each is square,
and the smallest tile's side.

Expected on the branch:

| Viewport | Block centre | Clear of header | Tiles |
| --- | --- | --- | --- |
| 1440×900 | 26.2% of the area | 132.8px | 5 × 52px, one row |
| 1280×800 | 26.5% | 31.4px | 52px, 3 + 2 |
| 1024×700 | 29.9% | 12.0px | 52px, 3 + 2 |
| 390×844 | 26.2% | 80.7px | 52px, 3 + 2 |

The quarter mark is 25%; the few points over are the 12px floor pad the body carries so the block never sits
flush under the header when the half-height band collapses to the block's own size.

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
