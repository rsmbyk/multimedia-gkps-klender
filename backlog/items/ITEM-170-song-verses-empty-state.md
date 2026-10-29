---
id: ITEM-170
status: ready
title: 'The song entry says "Pick a song first" when a song with no verses is already picked'
type: fix
priority: P1
effort: S
created: 2026-10-29
updated: 2026-10-29
spec: specs/162-song-verse-empty-state/spec.md
branch: fix/162-song-verse-empty-state
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-170: The song entry says "Pick a song first" when a song with no verses is already picked

## Summary

In the New song modal, picking a song that carries no verses leaves the Verses field reading
`Pick a song first` — the same line it shows when nothing is picked — and the field is disabled with
no explanation. Saving then answers `Keep at least one verse in the service.`, which reads as if the
person had removed the verses. The owner's report, with a screenshot of the modal on
`lagu kosong`: *"when a song does not have any verse, state it clearly"*.

The verses endpoint answers `{"verses": []}` for such a song, so the picker has zero checkboxes and
the script cannot tell "no song yet" from "song with no verses" — both fall in the same branch
(`static/web/entries.js:673`).

## Notes

- Seven songs in the local library currently have no live verses (pks 1774, 1852, 1886, 1905, 1906,
  1879, 1731), so the state is reachable by picking a song, not only by editing data.
- Measured on the live page (worktree 162, `/tatib/149/`, New song, 1440×900): trigger text
  `Pick a song first`, `disabled`, 0 checkboxes, Save enabled, save error `Keep at least one verse in
  the service.`
- The first paint of an edit form is server-rendered, so the same line has to be right in the
  template and not only after the script runs.

## Acceptance sketch

- A picked song with no verses states that the song has none; the field stays disabled.
- No song picked still reads `Pick a song first`; a song with verses is untouched.
- A save refusal names the song rather than the missing checks.

## Links

- Spec: [`specs/162-song-verse-empty-state/spec.md`](../specs/162-song-verse-empty-state/spec.md)
- Related items: ITEM-137 (a sidebar E2E on old empty copy)
