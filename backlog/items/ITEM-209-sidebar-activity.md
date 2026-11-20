---
id: ITEM-209
status: done
title: "The first sidebar's idle interval counts every scroll and waits fifteen minutes"
type: fix
priority: P2
effort: M
created: 2026-11-18
updated: 2026-11-18
spec: specs/199-sidebar-activity/spec.md
branch: fix/199-sidebar-activity
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/534
issue: 533
closed_at: 2026-11-18
closed_reason: merged into develop (PR #534)
bump: patch
release_version: 1.35.0
---

# ITEM-209: The first sidebar's idle interval counts every scroll and waits fifteen minutes

## Summary

Spec 072 accepted "scrolling in the main rail or first panel" as activity that restarts the
idle interval. The listener for `scroll` was attached to `#panel`, but the element that
actually scrolls in the first sidebar is its descendant `#panelBody` — and `scroll` does not
bubble. So that one event never reaches the handler: dragging the panel's scrollbar is scrolling
the operator can do for a minute without the timer noticing, and the panel collapses mid-drag.
The other five events (`pointerdown`, `pointermove`, `keydown`, `focusin`, `wheel`) do fire.

Widened at the owner's word to 072's other half: the interval must restart **when an interaction
that held the collapse ends**. Only the expiry re-check did that, so a reorder drag or a dialog
closed before expiry left the old deadline standing and the panel could collapse seconds after the
operator let go.

At the owner's word the wait itself moves too: fifteen minutes instead of sixty seconds. The rule,
its surfaces, its guards and its collapse states stay exactly as 072 accepted them — only the
number changes, in one constant, with no setting exposed.

## Notes

- Owner input, verbatim: "can you make sure it is captured from the intended events? i dont want
  any unknown behavior here", then, on the first gate-1 pack, "widen it" — fold the drag-end
  restart into this slice instead of a card of its own. Then: "also increase the timer to 15
  minutes".
- "Intended" is spec 072's own sentence — pointer use, keyboard use, focus changes, or scrolling
  in the main rail or first panel — not a new activity model. This slice restores that sentence
  and makes its boundary explicit and pinned: the second sidebar (`#chapters`), the reading stage
  and dialogs stay outside it, each with a test rather than a comment.
- The fix direction is a capture-phase listener on `.rail` and `#panel`: capture sees descendant
  scrolls, which also covers a scrollbar drag (it emits only `scroll`, no `wheel`).
- The gap is invisible to the wheel path, which is why the existing suite is green: `wheel` fires
  over the panel and already resets. No E2E covers the scroll event.
- Deliberate exclusion carried over from 072, now pinned: the second sidebar does not restart the
  interval.
- The delay is `IDLE_COLLAPSE_DELAY` in `static/web/reading.js`; 072's own scope excluded "a new
  persistent timeout setting or a notification about auto-collapse", and this slice keeps that out.

## Acceptance sketch

- Dragging the first panel's scrollbar after 30 s idle restarts the interval — the panel is still
  open at 14 min 59 s and collapses at 15 min after the drag.
- Wheel and keyboard scrolling keep restarting it, as today.
- Releasing a reorder drag before the interval expires restarts it — the panel is still open
  14 min 59 s after the release and collapses at 15 min.
- Scrolling the second sidebar or the reading stage for the whole interval does not restart it; the
  panel collapses on schedule.
- A modal or dialog still defers rather than resets; a focused control still holds the interval, and
  the end of any of those interactions gives a full interval.
- The wait is fifteen minutes: a page loaded and left alone collapses at 15 min, not at 60 s, and
  nothing in the UI offers to change the number.
- The 720 px narrow cut-off, the guards around the timer and every visible state are unchanged.

## Links

- Spec: [199](../specs/199-sidebar-activity/spec.md)
- Anchor issue: [#533](https://github.com/rsmbyk/multimedia-gkps-klender/issues/533) — backfilled at
  Implement. PR: [#534](https://github.com/rsmbyk/multimedia-gkps-klender/pull/534), squashed into
  `develop`. `release_version` stays empty until a release names it.
- Related items: ITEM-075 (spec 072 — the idle collapse rule this restores), ITEM-106 (spec 128 —
  Kidung/Tata Ibadah have no mini state).
