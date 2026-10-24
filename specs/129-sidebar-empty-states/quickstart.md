# Quickstart: The sidebars say which nothing they show

**Spec**: `specs/129-sidebar-empty-states/spec.md`

## Serve the branch

```bash
cd ../multimedia-gkps-klender-129          # the slice worktree (addressed from the main checkout)
DATABASE_URL=postgresql://multimedia:***@127.0.0.1:$(docker compose -f ../multimedia-gkps-klender/docker-compose.yml port db 5432 | cut -d: -f2)/multimedia \
  ../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8801 --noreload
```

Do not set `DJANGO_DEVELOPMENT_MODE` — it switches the settings module to SQLite, whose empty database
answers `no such table: bible_book`.

## Read the four states

1. **Empty sections.** Open a Tata Ibadah with no entries: the second column shows a list glyph,
   `No sections yet.` and `Add the first item to start preparing the service.`, centred on the pane.
2. **Empty songs.** Open a songbook with no songs: a music glyph, `No songs yet.`, centred the same way.
3. **A miss.** Open a service that has sections, type `zzz` in *Filter sections…*: the glyph becomes a
   magnifier with a cross, the title reads `No matching sections.` and the hint `Try a different search.`;
   clear the field and the block goes away.
4. **The first column.** On `/bible/`, `/songs/` or `/tatib/`, type `zzz` in the first column's filter: it
   names its own list (`No matching books.` / `No matching songbooks.` / `No matching Tata Ibadah.`).

## Measure the centring

```bash
../multimedia-gkps-klender/.venv/bin/python specs/129-sidebar-empty-states/preview/probe_empty_states.py
```

Each line prints `state`, `title`, `iconFor`, and `dvCenter`/`dhCenter` — the block's ink against its pane's
centre, in CSS pixels. All four states read `0`.

## Test

```bash
DATABASE_URL=… manage.py test multimedia.web --keepdb
DATABASE_URL=… manage.py test tests.e2e.test_reading.ReadingE2ETests.test_sidebar_empty_states_are_centred_and_typed --keepdb
```

The rest of the browser suites (`tests/e2e/`) run at the push step per the repo's test budget.
