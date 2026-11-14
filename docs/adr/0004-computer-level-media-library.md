# ADR 0004: Store service media in a computer-level library

- Status: Accepted for Spec 103; amended 2026-10-17
- Date: 2026-10-17

## Context

Operators usually prepare and project Tata Ibadah from the same laptops. Chrome and the OBS dock use different browser profiles, so browser storage would require separate uploads. Vercel's deployment filesystem is not durable media storage. The first slice needs file identity, local reuse, and missing-file visibility; projection of the file contents is deferred.

## Decision

Run the Python companion as a service in the existing Docker Compose stack on each operator computer. A Docker-managed named volume stores file bytes and the SQLite index at `/var/lib/gkps-media`; there is no host bind mount or OS-specific folder setup. Chrome and the OBS dock reach the same process through `http://127.0.0.1:63174`. Compose publishes that port on host loopback only. The browser imports bytes directly to the companion, which validates content, computes SHA-256, writes atomically, and deduplicates by hash. Django stores metadata and immutable service-entry references, but no binary payload. Each companion accepts only explicitly configured app origins and requires a token for writes. The page reconciles local inventory with current server references before cleanup.

The operator sets the production site's exact origin in `GKPS_MEDIA_PRODUCTION_ORIGIN` in the project-root `.env`. Compose adds both local app origins at the effective `WEB_PORT` and passes the exact allowlist to the companion. A missing or malformed origin prevents startup. Docker's restart policy starts the companion after Docker Engine starts at login; Docker itself must be configured to launch at login. Setup and volume lifecycle are documented in [the companion guide](../local-media-companion.md).

## Consequences

Media entries can be shared as references across computers while local bytes remain computer-specific. Losing or stopping the companion makes local availability unknown without deleting service entries. A later cloud transfer can distribute bytes with the same hash without changing those references. Ordinary `docker compose down` and container recreation preserve the volume; explicitly removing the named volume deletes the local library. Docker Desktop / Engine must start at login for the restart policy to take effect. Browsers may need local-network access permission.
