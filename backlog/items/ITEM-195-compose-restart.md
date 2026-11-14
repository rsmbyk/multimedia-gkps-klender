---
id: ITEM-195
status: in-review
title: 'The local stack stays down after a reboot'
type: fix
priority: P1
effort: S
created: 2026-11-14
updated: 2026-11-14
spec: specs/191-compose-restart/spec.md
branch: feat/191-compose-restart
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/504
issue: 503
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-195: The local stack stays down after a reboot

## Summary

The compose file gives only the media service a restart policy, so after a machine restart the
Docker daemon comes back and web and db stay exited (web exits 255 at daemon shutdown) until
someone starts them by hand. The request (2026-11-14, chat): the project's docker compose does not
start on system restart — fix it.

## Notes

- The machine's Docker daemon does start on boot (Docker Desktop's user service is enabled); only
  the containers lack a policy. Media already carries `restart: unless-stopped` and demonstrably
  returns on its own.
- The running containers on the owner's machine were repaired out-of-band on 2026-11-14 with
  `docker update --restart unless-stopped`; this slice writes the same policy into the compose file
  so a future `docker compose up` cannot drop it.
- `unless-stopped` is chosen over `always` so a deliberately stopped stack stays stopped.

## Acceptance sketch

- After a machine restart (or daemon restart), web, db and media are all running with no manual
  start, and the site answers on the published port.
- A stack stopped on purpose stays stopped across a daemon restart.

## Links

- Spec: [191](../specs/191-compose-restart/spec.md)
- Related items: ITEM-186 (spec 182, the launcher and the machine requirements the stack already
  records)
