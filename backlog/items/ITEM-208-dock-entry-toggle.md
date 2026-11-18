---
id: ITEM-208
status: done
title: "Dock entry headers expand and collapse their block; items do the jumping"
type: feat
priority: P2
effort: L
created: 2026-11-18
updated: 2026-11-18
spec: specs/198-dock-entry-toggle/spec.md
branch: feat/198-dock-entry-toggle
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/532
issue: 531
closed_at: 2026-11-18
closed_reason: merged into develop (PR #532)
bump: minor
release_version:
---

# ITEM-208: Dock entry headers expand and collapse their block; items do the jumping

## Summary

A full restart of the dock's entry list (the owner's 2026-11-18 directive): a header click no longer projects
the entry's first screen. It only expands or collapses that entry's own block. Projection moves to the item
rows inside an open block. Each eligible header carries a chevron for its state — right-pointing at rest,
rotated down when open, centred vertically in the line. The live entry's header has no chevron and cannot be
collapsed; a section break or an empty entry has no chevron and ignores clicks. Hand-opened blocks survive a
live-entry crossing and forget on reload; reduced motion swaps instantly.

## Notes

- Owner input, verbatim: "revert everything back and start over. clicking on the entry headers no longer
  display the first content inside it. it only expand/collapse the entries, except for live-entry (it cant be
  collapsed). the entry headers will have corresponding chevron depending on the state.operators need to click
  on the item inside specifically to jump"
- Owner answers the same day: full revert then rebuild; no chevron on the live row; chevrons centred
  vertically in the headers; branch fast-forwarded onto develop; Gate 2 "tick and accept all".
- Superseded decisions (kept in words in the spec, not in the code): the circular icon-only control, the
  verb+number accessible name, the line-level hover wrapper, and header-click projection itself.
- Converge: 81 E2E tests green in a real seven-suite run; the fast lane's 20 reds are pre-existing (identical
  set on a stashed clean baseline); `check` and `makemigrations --check` are green. FR-011's live-hover clause
  executes as "keeps the selected family of fill, never the generic hover face" — the baseline hover CSS is
  untouched (plan.md:79, approved preview).
- Minor bump 1.33.0 applied at Fold. Nothing committed, nothing pushed (GIT-06/GIT-07); the card stays in
  Speccing for the owner to promote, so no anchor issue is needed yet (BRD-10).

## Acceptance sketch

- A header click only toggles its block — no display write, no selection, no scroll; a click on an item inside
  projects exactly that item.
- A chevron on every non-break, non-empty, non-live header; none on the live, break or empty rows; it points
  right at rest and down when open, centred vertically in both states.
- The live header is locked open; break and empty headers are inert.
- Hand-opened blocks survive a crossing and forget on reload; reduce motion swaps instantly with no morph.

## Links

- Spec: [198](../specs/198-dock-entry-toggle/spec.md)
- Related items: ITEM-207 (spec 197 — the dock's bucket-head pin above this list), ITEM-119 (spec 119 — the
  dock itself).
