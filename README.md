# Multimedia GKPS Klender

Worship multimedia for GKPS Klender — Bible, songs, service order (Tata Ibadah),
and bookmarks, plus live OBS projection sources.

- Product: [`docs/PRODUCT.md`](docs/PRODUCT.md)
- Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Process: [`docs/PROCESS.md`](docs/PROCESS.md)

## Run locally with Docker

Requires Docker with the Compose plugin.

```sh
docker compose up --build
```

Then open <http://127.0.0.1:63404/>.

- `db` is PostgreSQL 16; `web` runs Django's development server with the repo
  bind-mounted for autoreload. Migrations run automatically on start.
- The stack publishes high host ports (`63404` for web, `59075` for db) so it
  avoids the crowded `8000` / `5432` used by other local apps. If either port is
  already taken, copy [`.env.example`](.env.example) to `.env` and change
  `WEB_PORT` / `DB_PORT` — no tracked file needs editing.
- To run the app without Docker, use Python 3.12 with a reachable
  `DATABASE_URL` (see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)).
