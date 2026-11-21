---
id: ITEM-224
status: backlog
title: 'A speaker token alone on its line is not read as a speaker'
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
bump:
release_version:
---

# ITEM-224: A speaker token alone on its line is not read as a speaker

## Summary

The liturgy classifier reads a speaker only when words follow the mark on the same line. A token
written alone — `Paragenda:`, `P:`, `Bapa:`, `Narator:` — is treated as ordinary text, so it and
every line under it stay ordinary: no voice, no colour, no words column. This is the other shape
the liturgy data uses, and it is not the owner's screenshot case (there the mark and words share
the line).

## Notes

- `read_mark`'s colon rule requires `\S.*` after the colon; `_DOT_RE` requires the same.
- Scanning the local legacy snapshot (`db.sqlite3`, 2,952 text rows) found 23 token-only lines:
  `Paragenda:`, `Bapa:`, `Namaposo:`, `Inang:`, `P:`, `Narator:`, `Haganupan:`, `Haganup:`,
  `Majelis:`, `Pelajar:`, `Paingkatkon:`.
- A fix needs the classifier to mark the token line and the overlay to paint a mark with no words
  as a row in the mark column, so the following lines have a column to hang from.
- Out of scope for spec 211; that slice is the continuation layout for an inline mark.

## Acceptance sketch

- `Paragenda:` alone reads as a leader mark; the following unmarked lines carry the leader voice.
- The overlay paints the token in the mark column, its words cell empty, and the following lines
  hang at that column.
- A colon sentence ("Maka jiwaku pun memuji-Mu:") and a reference ("Lukas 6:27") stay unmarked.

## Links

- Spec: [specs/059-speaker-colors/spec.md](../../specs/059-speaker-colors/spec.md)
- Related items: [ITEM-223](./ITEM-223-overlay-turn-hang.md), [ITEM-061](./ITEM-061-speaker-colors.md)
