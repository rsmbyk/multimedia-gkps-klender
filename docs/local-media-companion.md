# Local Media Library companion

The companion runs in the project's Docker Compose stack and stores media bytes
and its SQLite index in a Docker-managed named volume. It serves both the local
Chrome browser and OBS's browser dock through host loopback, so no Python
process needs to be started separately and no host folder needs to be chosen.

## First-time setup on a projector computer

1. Install Docker Desktop (Windows or macOS) or Docker Engine with the Compose
   plugin (Linux), and configure Docker to start when you log in.
2. Get the project checkout on that computer and copy `.env.example` to `.env`
   in the project root.
3. Set `GKPS_MEDIA_PRODUCTION_ORIGIN` in `.env` to the exact production site's
   origin: scheme and hostname (and port only if the site uses a nonstandard
   port), with no path or trailing slash. For example:

   ```dotenv
   GKPS_MEDIA_PRODUCTION_ORIGIN=https://multimedia.example.org
   ```

   This is local Compose configuration, not a Vercel environment variable. The
   value must match the origin in the production browser address bar.
4. Start the stack from the project root:

   ```sh
   docker compose up --build -d
   ```

   Compose starts Django, PostgreSQL, and the media companion. The companion's
   allowed origins include the configured production origin and both local
   origins at the effective `WEB_PORT` (`63404` by default):
   `http://localhost:<WEB_PORT>` and `http://127.0.0.1:<WEB_PORT>`.

Once the stack is running, the production site and local web app can use the
Media Library. The browser reaches the helper at `http://127.0.0.1:63174`.
Compose binds that port to host loopback only; do not expose it through a proxy
or a public network interface. The companion also checks the request host,
exact browser origin, and a session token for writes. A browser may ask for
permission to access a local network service; allow it for the configured app
origin.

## Starting it later

If the stack is running, the companion is already available. When Docker starts
after login, Compose's `unless-stopped` restart policy brings the companion
back automatically, provided it was not explicitly stopped. If the containers
were removed with `docker compose down`, run `docker compose up -d` again. To
rebuild after updating the project, use `docker compose up --build -d`.

## Storage and removal

Compose creates a named volume called `<compose-project>_media_library_data`.
It keeps the file bytes and `index.sqlite3` together across container restarts,
image rebuilds, and ordinary `docker compose down` / `docker compose up` cycles.
Operators manage files through the Media Library page; they do not need to
browse the volume or know its path. The status popup shows connection, file
count, and total size when connected, without disclosing a folder location.

Removing only the companion volume permanently deletes that computer's local
Media Library. `docker compose down -v` removes all volumes for this Compose
project, including both the media library and the local PostgreSQL database.
Do not use it as a routine restart command. Cloud sync, volume migration, and
backup/restore controls are not part of this version.

## Availability and file behavior

If the companion is stopped or the browser cannot connect to it, the status
shows `Connection — Unavailable`; counts and size are hidden. Service entries
remain saved and show `Local library unavailable` because file availability
cannot be checked. When connected, the app verifies each file against its
SHA-256 identity. The companion checks content signatures, enforces the 200 MB
limit, stores files by fingerprint, and keeps the first library filename for
identical bytes. Removing a file from this computer does not delete the service
entry. Unused-file cleanup runs only after a complete server reference
inventory is received.

The first version stores images, audio, video, PDF, PPT, and PPTX files. It does
not render file contents in Preview, the projector, or OBS.
