---
id: ITEM-210
status: in-review
title: 'The dock centres its live entry only when asked'
type: feat
priority: P2
effort: M
created: 2026-11-18
updated: 2026-11-19
spec: specs/200-dock-centre-triggers/spec.md
branch: feat/200-dock-centre-triggers
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/535
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-210: The dock centres its live entry only when asked

## Summary

The runner re-centres its live entry on every display-state notice: a screen step, an entry step, a
display toggle, a go to, a saved-change re-read, a session refresh, a load. The owner asked to keep
that *following* behaviour for a service left alone, and to give the operator a way to take the list
over. The dock now has two modes. In **following** (the default) an advance — forward or backward,
within an entry or across one — keeps the live row centred, even with other entries open or the
words hidden, as long as the dock shows the service on air. **Scrolling the list or expanding
another entry** drops into **browsing**, where advances no longer move the list. Three things return
it to following: the new control between Previous and Next, a click on an item inside an entry
(which includes the sticky Next band), and a successful 15 s idle re-centre. The transport's Next
and Back buttons are plain advances and keep whatever mode is current.

## Notes

- Today: `sync()` → `scheduleCenter()` on every notice, `centerRow()`/`glideScroll()` (190 ms
  ease-out), and the 230 ms crossing morph which carries its own scroll
  (`static/web/obs-dock.js`).
- The idle case has six conditions, read at the moment the timer fires: runner view · browsed
  service is the one on air · display on and no go to · no layer open · no other entry's block open
  · the live row entirely outside the scrollport.
- Precedent to weigh: spec 196's "snap back when the entry is off screen" was reverted unmerged;
  this is not that rule — it fires only after 15 s idle, and it centres rather than edge-aligns.
- Settled: a key-driven crossing centres while the dock is following and does not while it is
  browsing. The named actions are re-entries to following, not the only times the list moves.

## Acceptance sketch

- The new control sits between Previous and Next, is disabled with nothing live, centres on
  press (instant under reduced motion), and puts the dock back into following.
- An item click centres the row that just went on air and re-enters following; the sticky Next band
  also jumps the live pointer to the next entry and marks its first row.
- Following centres on every advance, including across entries, with open blocks and with the
  display off; a go to on air suspends it. The transport's Next and Back buttons never change the
  mode. Clicking the sticky Next band does re-enter following — it is an item click.
- A scroll or another entry's header ends following; the next advance then leaves the list still.
- 15 s idle centres only with all six conditions true, and re-enters following.

## Links

- Spec: `specs/200-dock-centre-triggers/spec.md`
- Related items: ITEM-208 (spec 198 — headers toggle, items jump), ITEM-207 (spec 197 — the pinned
  bucket head)
