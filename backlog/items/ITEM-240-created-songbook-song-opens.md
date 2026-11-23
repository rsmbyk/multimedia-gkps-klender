---
id: ITEM-240
status: done
title: 'A newly created songbook or song does not open'
type: fix
priority: P2
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 225-open-created-songbook-song
branch: feat/225-open-created-songbook-song
pr: 592
issue:
closed_at: 2026-11-23
closed_reason: merged into develop (PR #592)
bump: patch
release_version:
---

# ITEM-240: A newly created songbook or song does not open

## Summary

After a successful sidebar create, the new row appears in its list but nothing is selected and the
stage stays put. Measured on the base commit at 1440×900: after creating a songbook,
`currentBook=null` and `data-ch=closed`; after creating a song in an open book, `currentSong=null`,
`#readName=""` and `data-read=off`. Opening either row by hand gives `currentBook="38"` with
`data-ch=open`, or `/songs/<id>/` with the title on the stage. The create should land on those same
states without a second click.

## Notes

- The save response already carries `id`, `kind` and `created`; no server change is needed.
- The shell's existing `lists` navigation is a songbook row click; `song` is a song row click.
- Spec 209 already opens a created Normal service on the stage; that path stays as it is.
- Owner decision 2026-11-23: "opened" means as if the new row were clicked — songbook selected with
  its songs listed, song on the reading stage.
- Out of scope: edits, verse saves, Tata Ibadah paths, hymn books, and any new look.

## Acceptance sketch

- A created songbook becomes current in the panel with its song list open, in place.
- A created song opens on the stage: URL, heading, current row and `data-read` match the click state.
- No reload, no panel-state change; edits, refusals and other record kinds keep today's behaviour.

## Links

- Spec: [225-open-created-songbook-song](../../specs/225-open-created-songbook-song/spec.md)
- Related items: ITEM-170 (spec 209, created service opens on stage)
