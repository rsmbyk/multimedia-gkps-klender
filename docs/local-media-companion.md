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

## PowerPoint conversion and fonts

A PowerPoint file is converted to a PDF by the companion's own LibreOffice when
the projector first asks for it. How faithful that is depends on two things in
the image: the LibreOffice version, and the faces the deck is set in. Both ship
with the image, so nothing needs installing for the usual decks — Calibri,
Cambria, Arial and Times New Roman are drawn in metric-compatible substitutes
(Carlito, Caladea, Liberation), which keep every word where the deck puts it.

Some decks also use fonts that ship only with Microsoft Office — `Britannic
Bold` and `Berlin Sans FB Demi` are the usual two. They cannot be included in
the image, but they can be supplied once on each computer:

1. Put the font files in `~/.local/share/gkps-fonts` (or in the directory
   `GKPS_FONTS_DIR` names, if your `.env` sets it).
2. Restart the companion: `docker compose up -d media`.

The companion re-scans that directory on start, and a deck converted before the
fonts arrived is converted again the next time it is projected — the derivative
is keyed on the renderer's version and its fonts, not on the file alone. If the
directory is missing or empty, conversion works as before.

To see what the image currently draws for each family, run:

```sh
docker compose exec media python -m multimedia.slide_fonts
```

## Temporary online sharing with Cloudflare R2

Create a private R2 Standard bucket and an R2 S3 API token restricted to that
bucket with Object Read & Write. In Vercel Production set
`GKPS_R2_ACCOUNT_ID`, `GKPS_R2_BUCKET`, `GKPS_R2_ACCESS_KEY_ID`, and
`GKPS_R2_SECRET_ACCESS_KEY` on the Django deployment. Set the same variables in
a computer's local `.env` only when its local Django server needs to share or
retrieve files through R2. The companion never receives these credentials: it
receives a signed URL for one file from Django and transfers bytes directly to
R2. Keep the bucket private; do not enable a public `r2.dev` URL.

Local Compose writes under `temporary-media/development/` in the configured
bucket. Production uses `temporary-media/` unless `GKPS_R2_PREFIX` overrides
it. For a shared bucket, set production to `temporary-media/production` so
both deployments have separate cleanup scope. The SQLite companion volume
keeps transfer history and unfinished retry plans when browsers close. A
companion process restart marks interrupted transfers failed. On the next
visit, the browser refreshes the list of eligible today/future files. Missing
files still available online download automatically; past and undated services
show a manual download action. An automatic failure retries with backoff from
five seconds to five minutes until the file succeeds or online access expires.

An upload has one attempt. When its one-hour signed URL expires or a network
error occurs, the transfer is marked failed and the operator can share the
file again. The server marks a file online only after R2 confirms the expected
size. The receiving companion verifies the SHA-256 fingerprint before adding
the file to its local library. Online availability expires seven days after a
successful upload. Configure an R2 object lifecycle rule for the temporary
prefix to delete objects after eight days as a backstop; ensure the rule is
scoped to that prefix, since lifecycle configuration replaces bucket rules.
Django's `/media-library/cloud/cleanup/` Vercel Cron endpoint removes expired
objects and metadata daily. Set a random `CRON_SECRET` in Vercel Production;
Vercel sends it as a bearer token when invoking the cron endpoint. If this is
not set, the endpoint refuses cleanup and only the R2 lifecycle rule clears
objects. Cloudflare's R2 free tier is not an unlimited budget: monitor stored
GB, request counts, and egress policies in the R2 dashboard.

For a credential rotation, create a new bucket-scoped R2 S3 API token, update
the four Vercel values and any local `.env` values, deploy/restart Django, and
then revoke the old token. Browser tabs and companions do not need the raw
secret. For a smoke test, use a non-sensitive small file: share it from one
computer, wait for the online indicator, open a today/future service using it
on a second computer, confirm the downloaded fingerprint and transfer history,
then run the cleanup command in a staging environment after advancing an
expired test share. Keep the production cleanup job and bucket lifecycle rule
pointing only at the intended prefix.

Run `python manage.py check_media_r2` from the Django environment to check
bucket access without printing credentials. Run `python manage.py check_media_r2
--smoke` before enabling production sharing: it writes, reads, verifies, and
deletes one small object under the configured prefix. The smoke test is
opt-in because it mutates the bucket.

In the Cloudflare dashboard, open R2 object storage → the private bucket →
Settings → Object lifecycle rules, add an expiration rule for the exact
`GKPS_R2_PREFIX` followed by `/`, and set deletion after eight days. Review
existing rules before saving. Bucket lifecycle management needs Cloudflare
bucket-management permission in addition to the bucket-scoped S3 object token;
that object token alone is not a way to configure the rule.
