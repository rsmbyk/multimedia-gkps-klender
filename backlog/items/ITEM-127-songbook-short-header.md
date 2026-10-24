---
id: ITEM-127
status: in-review
title: 'Cite a song page''s songbook by its short name'
type: fix
priority: P2
effort: S
created: 2026-10-24
updated: 2026-10-24
spec: specs/126-songbook-short-header/spec.md
branch: feat/126-songbook-short-header
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/375
issue:
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-127: Cite a song page's songbook by its short name

## Summary

A song page's header spells its songbook out in full — `PELENGKAP KIDUNG JEMAAT 4` above the lyrics — while
the same page's second sidebar prints the compact reference on its selected row (`PKJ 4`), and every other
song surface in the app (the projector's Go To list, the OBS song dock, the verses view) uses the short name
too. The page that actually shows the song is the one place with two names for it. This slice makes the song
header — and the browser tab built from it — cite the songbook by its short name, mirrors the rule in the
saved renderer, and starts the repo's `docs/spec/` capability tree with what it folds.

## Notes

- Reported with a screenshot of a Pelengkap Kidung Jemaat song page: header `PELENGKAP KIDUNG JEMAAT 4`,
  selected sidebar row `PKJ 4`.
- An ordinary (non-hymn) songbook's page keeps its full name — its songs carry no numbers, so the name is the
  whole citation, and every ordinary songbook in the library has an empty short name.
- On a narrow stage the header stops wrapping: the full name took two lines at 768 px and 390 px, the short
  reference takes one.
- Accepted at gate 2 with the decision to start `docs/spec/reading.md` rather than record `n/a` again; the
  saved copy is `R2` inside that file, not a capability of its own.

## Acceptance sketch

- A hymn song page's header reads `PKJ 4`, `KJ 24A`, `HAL 101`; the tab follows.
- A hymn songbook without a short name falls back to its full name; an unnumbered song shows the reference alone.
- An ordinary songbook's page is unchanged, even if a short name is set.
- The saved page and the server page agree on the header and the title.
- `docs/spec/reading.md` exists and holds `R1` and `R2`.

## Links

- Spec: [`specs/126-songbook-short-header/spec.md`](../specs/126-songbook-short-header/spec.md)
- Capability: [`docs/spec/reading.md`](../../docs/spec/reading.md)
- Related items: ITEM-122 (saved reading parity), ITEM-124 (the header's typography), ITEM-125 (saved song
  page parity)
