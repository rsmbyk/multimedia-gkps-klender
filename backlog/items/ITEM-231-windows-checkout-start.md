---
id: ITEM-231
status: in-review
title: 'The stack never starts from a checkout made on Windows'
type: fix
priority: P1
effort: S
created: 2026-11-21
updated: 2026-11-21
spec: 216
branch: fix/216-windows-checkout-start
pr: 571
issue: 570
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-231: The stack never starts from a checkout made on Windows

## Summary

On a fresh Windows computer, `docker\up.ps1` ends with `Error response from daemon: Container … is
restarting, wait until the container is running` and no site. Git for Windows checks text files out
with CRLF by default and the repo pins no line endings, so the image is built with a CRLF
`docker/entrypoint.sh`; `/bin/sh` then refuses it at `set -e`, the container exits 2, and
`restart: unless-stopped` loops `web` and `media`. Reported from a fresh machine (2026-11-21).

## Notes

- Reproduced on the image: the repo's own entrypoint, rewritten with CRLF and run inside the `media`
  container, prints `set: Illegal option -` and exits 2.
- Nothing on Linux reproduces it, so the suite cannot catch it — the fix has to make the image
  independent of how git wrote the file.
- The launcher makes the diagnosis worse: its post-start font check runs under
  `$ErrorActionPreference = 'Stop'`, so a `docker compose exec` against a restarting container throws
  `NativeCommandError` and aborts the script instead of printing its own message.
- The reporting checkout predates `spec 192`'s launcher (the check sits at `up.ps1:60`, current
  `develop` has it at 74); the entrypoint is unchanged either way.

## Acceptance sketch

- A CRLF `docker/entrypoint.sh` in the build context still starts the stack, launcher or plain
  Compose.
- `git check-attr eol` reports `lf` for the shell scripts and `unspecified` for `up.ps1`.
- A start whose companion is restarting prints one line naming `docker compose logs media` and exits
  with the status `up` returned.

## Links

- Spec: `specs/216-windows-checkout-start/spec.md`
- Related items: ITEM-186 (spec 182, the launchers and the font mounts), ITEM-195 (spec 191, the
  restart policy that turns the crash into a loop), ITEM-196 (spec 192, the post-start font check)
