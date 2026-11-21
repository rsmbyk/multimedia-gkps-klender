---
id: ITEM-233
status: backlog
title: 'A start from an image older than the Dockerfile says nothing'
type: fix
priority: P2
effort: S
created: 2026-11-21
updated: 2026-11-21
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump: none
release_version:
---

# ITEM-233: A start from an image older than the Dockerfile says nothing

## Summary

`docker\up.ps1` runs `up -d`, which reuses whatever image exists. An operator who pulls a `Dockerfile`
change and starts again keeps the old image and reads the same failure as before the change, with no
signal that a rebuild was needed — which is exactly what happened right after spec 216 landed.

## Notes

- Observed 2026-11-21: the fix was correct and merged, and the machine still failed because the image
  predated it. The operator had no way to tell from the launcher's output.
- A warning is cheap only if the comparison is cheap: the `Dockerfile`'s modification time against the
  image's creation time, read through `docker image inspect`, with `docker compose build` named.
- It must not change the start's exit status, and must not run when the start failed.

## Acceptance sketch

- A start whose image predates the `Dockerfile` prints one line naming `docker compose build`.
- A start from a freshly built image prints nothing.
- The exit status is the start's, on both paths.

## Links

- Related items: ITEM-231 (spec 216), ITEM-232 (spec 217, the same report's other half)