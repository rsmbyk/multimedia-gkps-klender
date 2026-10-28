# Quickstart: a service entry draws no box until it is pointed at

**Slice**: `specs/142-entry-surface` · Contracts: [`none.md`](./contracts/none.md) · Data model:
[`data-model.md`](./data-model.md)

## Run it

```sh
cd ~/Projects/multimedia-gkps-klender-142
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8820 --noreload
```

- `/tatib/142/` — 24 text entries and 3 section breaks
- `/tatib/144/` — all five kinds: 1 text, 1 scripture, 4 songs, 3 media, 6 breaks

The DB password is the one in `docker-compose.yml`; `docker compose port db 5432` gives the port.

## Check it by hand

1. Park the pointer away from the list: no fills, no outlines anywhere, in light and dark.
2. Point at an entry: it fills with `--icon-hover-bg` (`rgba(31,31,29,.08)` / `rgba(255,255,255,.09)`).
3. Tab to an entry: the same fill. After closing a modal, no fill (quiet restoration).
4. On `/tatib/144/`, confirm a media row still reads as an object — 42px tile at `left: 13px`,
   filename, type line — and the section break still draws its rule and diamond.

## Run the checks

```sh
# the palette the slice must not disturb
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.test_design_tokens
# 6 tests, green

# the surface and the interaction states
DATABASE_URL="postgres://multimedia:<pw>@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test \
  tests.e2e.test_tatib_entry_controls tests.e2e.test_tatib_hover
```

`tests.e2e.test_tatib_hover::…::test_touch_controls_remain_visible_after_dismissal` is red on
`develop` too (carded as ITEM-153); the remaining failures belong to slice 143's add-bar geometry,
not to this slice — see `analysis.md`.

## Regenerate the static comparison

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/142-entry-surface/preview/build_preview.py
```

It reads the live page's markup and the stylesheets frozen at `ca71c850`, so the **Now** column keeps
showing the retired box.
