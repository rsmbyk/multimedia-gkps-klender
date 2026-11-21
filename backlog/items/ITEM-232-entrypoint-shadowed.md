---
id: ITEM-232
status: ready
title: 'The web service still runs the checkout’s CRLF entrypoint, because the bind mount replaces the image’s'
type: fix
priority: P0
effort: S
created: 2026-11-21
updated: 2026-11-21
spec: 217
branch: fix/217-entrypoint-shadowed
pr:
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-232: The web service still runs the checkout's CRLF entrypoint, because the bind mount replaces the image's

## Summary

Spec 216 stripped `docker/entrypoint.sh` at build time, but `docker-compose.yml:25` mounts the
checkout over `/app`, so `web` executes the host's copy — still CRLF on a Windows machine — and dies at
`set -e` exactly as before. Reported after the fix landed: "the media and web are not running. also
the media still showing `docker/entrypoint.sh: 2: set: Illegal option -`".

## Notes

- Measured on the real image: without the mount it runs (`OK`, exit 0); with the checkout mounted at
  `/app` it prints `docker/entrypoint.sh: 2: set: Illegal option -` and exits 2. The image's copy has
  0 CR bytes, the mounted tree's has 19.
- `media` has no bind mount, so its failure in the same report is the other half: `docker\up.ps1` runs
  `up -d`, which reuses the image built before spec 216. That trap is filed as ITEM-233.
- The fix is a path: the runtime entrypoint must live outside the mounted tree.

## Acceptance sketch

- The image run with a CRLF checkout mounted at `/app` reaches its command, exit 0.
- The `ENTRYPOINT` names a path that does not begin `/app/`.
- `web` and `media` both stay `Up` from a CRLF checkout.

## Links

- Spec: `specs/217-entrypoint-shadowed/spec.md`
- Related items: ITEM-231 (spec 216, the strip this corrects), ITEM-233 (the stale-image trap)