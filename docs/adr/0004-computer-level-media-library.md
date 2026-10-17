# ADR 0004: Store service media in a computer-level library

- Status: Accepted for Spec 103
- Date: 2026-10-17

## Context

Operators usually prepare and project Tata Ibadah from the same laptops. Chrome and the OBS dock use different browser profiles, so browser storage would require separate uploads. Vercel's deployment filesystem is not durable media storage. The first slice needs file identity, local reuse, and missing-file visibility; projection of the file contents is deferred.

## Decision

Run a small Python companion on each operator computer, bound to loopback. It owns one data folder per operating-system user and a SQLite index. Chrome and the OBS dock access the same process and folder. The browser imports bytes directly to the companion, which validates content, computes SHA-256, writes atomically, and deduplicates by hash. Django stores metadata and immutable service-entry references, but no binary payload. Each companion accepts only explicitly configured app origins and requires a token for writes. The page reconciles local inventory with current server references before cleanup.

The default folders are `%LOCALAPPDATA%\GKPS Klender\Media Library` on Windows, `~/Library/Application Support/GKPS Klender/Media Library` on macOS, and `$XDG_DATA_HOME/gkps-klender/media-library` or `~/.local/share/gkps-klender/media-library` on Linux. Operators start the companion as described in [the companion guide](../local-media-companion.md).

## Consequences

Media entries can be shared as references across computers while local bytes remain computer-specific. Losing or stopping the companion makes local availability unknown without deleting service entries. A later cloud transfer can distribute bytes with the same hash without changing those references. Operators must run and maintain the companion separately from the Vercel site, and browsers may need local-network access permission.
