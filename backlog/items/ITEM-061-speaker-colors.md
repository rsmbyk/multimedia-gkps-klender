---
id: ITEM-061
status: in-review
title: 'Color liturgy speakers as a congregation cue'
type: feat
priority: P2
effort: M
created: 2026-10-12
updated: 2026-10-12
spec: specs/059-speaker-colors/spec.md
branch: feat/059-speaker-colors
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/312
archived_at:
archive_reason:
bump: minor
release_version: 1.5.0
---

# ITEM-061: Color liturgy speakers as a congregation cue

## Summary

The projection screen faces the congregation. Leader lines are only a cue, so they
stay dimmer than the ordinary off-white. Congregation lines stay that off-white.
A joined line is one they read and say, so it stays readable and its color marks
it as theirs, still quieter than the off-white.

## Notes

- Approved preview: `specs/059-speaker-colors/preview.html` (2026-10-12).
- Leader: dark `#9C8463`, light `#866B50`. Joined: dark `#8EC2CC`, light `#2B5A64`.
  Ordinary text stays `--ink`. Projector header stays `#FFD166`.
- Leader labels share one voice: `L`, Liturgis, Litrugis, bare `P`, Paragenda,
  Pendeta, Pandita, Pdt, Pelayan, Pemimpin, Parambilan.
- Everyone else, including J, K, Jemaat, Kuria, Bapa, Inang, and Namaposo, uses
  the ordinary color. Two of those on one screen is an operator habit (a blank
  line splits the screen), not another color.
- Songs, scripture, and the sidebar are unchanged.
- Renumbered from a local ITEM-059 draft: `develop` already uses ITEM-059 and
  ITEM-060.

## Acceptance sketch

- On the projector, a `P:` line is `#9C8463` and a `J:` line is `#F5F3EE`.
- A `P+J:` line is `#8EC2CC` on the projector and `#2B5A64` on the light page.
- An unmarked line keeps the previous voice inside the same item.
- A song or a verse stays the ordinary text color.

## Links

- Spec: [specs/059-speaker-colors/spec.md](../../specs/059-speaker-colors/spec.md)
- Related items: ITEM-060 (built-in projection blanks, the screens this colors)
