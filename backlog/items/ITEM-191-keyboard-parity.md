---
id: ITEM-191
status: in_progress
title: 'The dock and the projector share one keyboard grammar'
type: feat
priority: P2
effort: M
created: 2026-11-04
updated: 2026-11-05
spec: specs/187-keyboard-parity/spec.md
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-191: The dock and the projector share one keyboard grammar

## Summary

The dock and the projector already share the arrow grammar — plain steps screens, `Shift` steps
baits, `Ctrl` steps entries — but part company everywhere else: `Home`/`End` jump to the ends of the
whole service on the dock and to the ends of the entry (or bait) on show on the projector; the dock
has no `K` sheet, its `Esc` returns to the picker on a tap, its `G` is refused on the picker, its go
to cannot cross a chapter or a book, its picker moves on six keys, it has no fetch guard, and the
projector ignores `⌘`. This slice gives both surfaces one table.

A go to started from the picker stands alone: the owner's ruling is that choosing a result there puts
it on air with no service underneath, so the display state gains a go to that names no service.

## Notes

- Source: the owner's list of 2026-11-04 and his answer to the picker question.
- Later additions — the Home/End scope (FR-012), the two sheets' grouping and wording (FR-013, FR-014),
  and the find band's refocus (FR-015) — are implemented **with the slice, after gate 1 and gate 2**;
  the owner declined to build any of them ahead of the gates.
- The dock's table exists only as a comment today (`static/web/obs-dock.js:14-25`); the projector's is
  a sheet (`K`).
- A service-less go to reaches the state module (`display.js` refuses it today) and both readers —
  the overlay paints nothing without a service (`obs-overlay.js:350`).
- The dock's sheet is one scrolling column, not the projector's three: the dock is 320–520 px wide.

## Acceptance sketch

- A tap of `Esc` in the runner does nothing; a 900 ms hold shows the picker.
- `G` on the picker opens the band; choosing there writes `service: null` plus the go to, and `Back`
  returns the dock to the picker with every surface idle.
- The dock's go to crosses chapters and books on the projector's own chords, fetching once per crossing.
- The picker moves on `↑`/`↓` only.
- `Home`/`End` act on the entry — or the bait — on show, as the projector's do; `⇧` does nothing on an
  entry with no baits, and `⌘` reaches the service's ends.
- `K` opens the dock's shortcut sheet on either view; `Esc`, `K` or the scrim closes it.
- No key or click changes what is on air while a go to fetch is in flight.
- `⌘` acts as `Ctrl` on the projector, and `⌘`+letter stays with the browser.

## Links

- Spec: [187](../specs/187-keyboard-parity/spec.md)
- Related items: ITEM-189 (the dock's Go To, spec 185), ITEM-188 (the session boundary, spec 184)
