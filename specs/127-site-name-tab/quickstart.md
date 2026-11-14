# Quickstart: The tab names the site, and the index's tab stops at the name

**Spec**: `specs/127-site-name-tab/spec.md`

## Serve the branch

```bash
cd ../multimedia-gkps-klender-127          # the slice worktree
DATABASE_URL=postgresql://multimedia:${PW}@127.0.0.1:$(docker compose -f ../multimedia-gkps-klender/docker-compose.yml port db 5432 | cut -d: -f2)/multimedia \
  ../multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8765 --noreload
```

Do not set `DJANGO_DEVELOPMENT_MODE` — it switches the settings module to SQLite, whose empty database
answers `no such table: bible_book`.

## Read the titles

1. **Index stops at the name.** Open `/`: the tab reads `Multimedia GKPS Klender`. The same for `/home/`
   and `/search` (no query).
2. **Every other page appends the name.**
   - `/bible/1/1/` → `Kejadian 1 — Multimedia GKPS Klender`; click the SIM edition → `1 Musa 1 — Multimedia GKPS Klender`.
   - `/songs/` → `Kidung — Multimedia GKPS Klender`; a hymn song → `PKJ 4 — Multimedia GKPS Klender`.
   - `/tatib/` → `Tata Ibadah — Multimedia GKPS Klender`; a service → `<service name> — Multimedia GKPS Klender`.
   - `/search?q=kasih` → `Results for “kasih” — Multimedia GKPS Klender`.
   - `/media-library/` → `Media Library — Multimedia GKPS Klender`.
3. **Nothing visible moved.** The page's heading, the search field's label, the logo's alt text and the
   rail's labels still read `GKPS Klender`.
4. **The saved copy agrees.** With the library synced, open a reading page from the sidebar: the title does
   not change when the online update replaces the saved page.

## Test

```bash
DATABASE_URL=… manage.py test multimedia.web --keepdb
```

Browser suites (`tests/e2e/`) run at the push step per the repo's test budget.
