---
id: ITEM-233
status: in-review
title: 'A launcher start that cannot reach the companion says nothing about why'
type: fix
priority: P2
effort: S
created: 2026-11-21
updated: 2026-11-21
spec: 218
branch: fix/218-restart-log
pr: 575
issue: 573
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-233: A launcher start that cannot reach the companion says nothing about why

## Summary

`docker\up.ps1` runs `up -d`, which reuses whatever image exists. An operator who pulls a `Dockerfile`
change and starts again keeps the old image and reads the same failure as before the change, with no
signal that a rebuild was needed — which is exactly what happened right after spec 216 landed.

## Notes

- Observed 2026-11-21: the fix was correct and merged, and the machine still failed because the image
  predated it. The operator had no way to tell from the launcher's output.
- An image-age comparison (Dockerfile mtime against `docker image inspect`) was rejected at Specify:
  the format and timezone differ per shell, and GNU `date -d` is absent on macOS. The companion's own
  last log line is exact evidence and covers every cause, not only a stale image.
- Still advisory: it must not change the start's exit status, and must not run when the start failed.

## Acceptance sketch

- A start whose companion is not running prints the companion's own last line and names
  `docker compose build`.
- A healthy companion is asked for no log.
- The exit status is the start's, on both paths.

## Links

- Related items: ITEM-231 (spec 216), ITEM-232 (spec 217, the same report's other half)