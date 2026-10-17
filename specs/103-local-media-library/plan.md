# Plan 103: Local Media Library and service media entries

- **Status:** Accepted amendment (2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-103
- **Bump:** minor
- **Visual previews:** [Media Library](./preview-library.html), [media entry form](./preview-entry.html)

## Why

Operators use the same projector computers for the web app and OBS dock, and need one local copy of each media file that both browser contexts can reach. Running the companion in the existing Docker Compose stack avoids separate per-OS installation and folder setup. A Docker-managed named volume keeps the bytes and local index on that computer, while Vercel stores only file metadata and service-entry references.

## Assumptions for this amendment

- Keep the existing media identity, entry, library, and companion API behavior from the accepted Spec 103. Change how the companion is launched and where it persists its local data.
- Run the companion as a service in the existing Compose project, with a named volume mounted at a fixed in-container library root. The volume stores both media bytes and the SQLite index.
- Chrome and OBS's browser dock run on the host. They use `http://127.0.0.1:63174`; Docker's service DNS name is only for container-to-container traffic. This changes the companion's host endpoint from `47863`; API paths and payloads remain unchanged.
- The companion listens on its container interface, while Compose publishes port `63174` only on host loopback. Its origin allowlist includes the exact production origin and both local web origins, `http://localhost:<WEB_PORT>` and `http://127.0.0.1:<WEB_PORT>`, where `<WEB_PORT>` is the effective Compose web port (default `63404`).
- The operator sets `GKPS_MEDIA_PRODUCTION_ORIGIN` in the project-root `.env` on each projector computer. Compose combines it with both local origins and passes the resulting exact list to the companion as `GKPS_MEDIA_ALLOWED_ORIGINS`; the production value is the site's scheme and hostname (including a nonstandard port only if used), with no path or trailing slash. It is local Compose configuration, not a Vercel environment variable.
- Compose gives the companion a restart policy. It will start after the Docker engine starts, provided the operator has configured Docker Desktop / Engine to start at login and has not explicitly stopped or removed the service.
- Operators do not need the Docker volume's filesystem path. The connected status popup will show connection, file count, and total size, without a folder-location row.
- The named volume is local to one Docker host. Cross-computer transfer, cloud sync, and a backup/restore UI remain out of scope.

## Scope / edges

**In:**

- Add the local media companion to the existing Docker Compose stack.
- Persist the companion's file bytes and index in a named Docker volume at a configurable/fixed container root.
- Publish companion port `63174` only to `127.0.0.1` on the Docker host and update the browser clients to use that loopback URL.
- Configure the production origin in the project-root `.env` and let Compose combine it with both local origins (`localhost` and `127.0.0.1` at the effective `WEB_PORT`).
- Restart the companion when Docker starts after login, without a separate OS-native startup service.
- Remove the folder-location row from the connected status popup and stop returning the container path to the browser.
- Update companion, architecture, and Compose documentation to describe the Docker-managed library and volume lifecycle.

**Out:**

- Bind mounts to an OS-specific host folder, host-path detection, or a folder picker.
- Requiring operators to browse or edit files in Docker's volume directly.
- Backup/export, volume migration between computers, R2, or other cloud synchronization.
- Media Preview/projector rendering, PPT/PPTX slide display, or OBS-specific behavior.

## Approach

1. Add a `media` service to `docker-compose.yml` using the repository's Python image/build and the existing companion module. Configure its storage root to the named volume mount so the byte files and SQLite index share the volume.
2. Change the companion's browser endpoint from port `47863` to `63174`, updating the companion listener, browser clients, and tests together. Publish `63174` as `127.0.0.1:63174:63174`; allow the process to bind inside the container without exposing the port on other host interfaces. Keep API paths and payloads unchanged.
3. Require `GKPS_MEDIA_PRODUCTION_ORIGIN` in the project-root `.env`. Compose combines that exact production origin with `http://localhost:<WEB_PORT>` and `http://127.0.0.1:<WEB_PORT>` (default `63404`) and passes the list as `GKPS_MEDIA_ALLOWED_ORIGINS`; fail closed if the production origin is missing or malformed.
4. Add `restart: unless-stopped` (or equivalent documented behavior) so the service returns when Docker starts after login; `docker compose down` still requires a later `up` because it removes the container.
5. Remove the filesystem path from the status response and status popup. Retain connection state, file count, total size, and all existing disconnected behavior.
6. Add focused Compose/configuration and companion tests, then update the existing Spec 103 PR and its operator documentation.

## TDD and verification

- Companion tests: `multimedia/test_local_media.py` verifies the configured volume root, file/index persistence, origin enforcement, and verified reads.
- Compose tests: `tests/test_docker_compose.py` verifies the companion service, named volume mount, loopback-only `63174` port mapping, restart policy, production origin, and both local web origins at the configured port. Companion and browser-client tests verify the same endpoint port and unchanged API behavior.
- Browser E2E: `tests/e2e/test_media_library.py` verifies the connected status omits the path, still shows counts and size, and reports unavailable behavior when the companion is stopped.
- Run the targeted Django/companion tests, targeted media-library E2E, `docker compose config`, and `git diff --check`.

## Risks

- A Docker-managed volume is less directly browsable than a host folder; deleting the volume deletes the library. Documentation must distinguish ordinary `docker compose down` from `docker compose down -v`.
- Docker Desktop / Engine must be installed and started on each computer. Restart policy cannot start a Docker engine that is not running.
- The browser must reach the helper through host loopback. A Compose DNS name will not work in Chrome or the OBS dock, and publishing the port beyond loopback would violate the local-only boundary.
- A production origin is deployment configuration and must be an exact origin, without path or trailing slash. Do not guess or silently widen the allowlist.
