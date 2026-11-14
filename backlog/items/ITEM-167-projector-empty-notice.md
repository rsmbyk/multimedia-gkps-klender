---
id: ITEM-167
status: done
title: 'The projector''s empty notice stays under a Go To passage or song'
type: fix
priority: P1
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/161-projector-empty-notice/spec.md
branch: fix/161-projector-empty-notice
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/444
issue: 440
closed_at: 2026-10-29
closed_reason: merged into develop via #444
bump: patch
release_version:
---

# ITEM-167: The projector's empty notice stays under a Go To passage or song

## Summary

A Tata Ibadah with no items projects the server-rendered sentence *"Nothing to show yet: this Tata
Ibadah has no items."* Opening a passage or a song from Go To paints it on a detour screen, but the
notice stays where it was — below the stage, so the congregation reads the empty-service sentence
under a projected verse. The notice is a sibling of the stage (`projector.html:55-57`) rather than one
of the screens, so the detour's `.is-active` never covers it and `renderDetour()`
(`static/web/projector.js:1148`) never touches it.

The same paragraph also survives a re-read that brings the service its first items: `reflow()`
(`projector.js:1372`) swaps the stage's screens and never re-syncs the notice.

## Notes

- Measured at 1920×1080 on `develop` (24a6d6d2), service 147 (no items): notice 755×38.4 at
  x 582.5, y 977.6, `display: block`, with the detour stage 1856×945.6 at y 32 — the notice begins
  exactly where the stage ends, 38.4px of painted copy under the words.
- Hiding it returns that 38.4px to the stage: 945.6 → 984 tall, the fitted detour 103 → 107px and
  its block re-centred 9.2px lower. Those are consequences of the space, not new values.
- Provenance: the owner's report against the projector page, with a screenshot of a hymn screen
  carrying the notice underneath.

## Acceptance sketch

- While a Go To detour is on the stage, the notice is not painted and takes no box; the detour fills
  the stage the notice was holding back.
- Closing the detour (Escape, or `Back to service`) restores the notice when the service is still
  empty.
- A re-read that brings the service its first screens takes the notice away in the same pass.
- The notice's own copy, 28px size, colour and centred position are unchanged wherever it shows.

## Links

- Spec: [161](../specs/161-projector-empty-notice/spec.md)
- Related items: ITEM-146 (the Go To that paints the detour), ITEM-144, ITEM-149
