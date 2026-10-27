---
id: ITEM-151
status: in-review
title: 'The stage''s entry links read as text until hovered'
type: chore
priority: P2
effort: S
created: 2026-10-27
updated: 2026-10-27
spec: specs/140-stage-link-affordance/spec.md
branch: feat/140-stage-link-affordance
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/410
issue: 409
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-151: The stage's entry links read as text until hovered

## Summary

Every entry title on a Tata Ibadah stage is a link, and since spec 056 it wears the theme's link
colour — forest green in light, royal blue in dark — with a resting underline. A service page
therefore reads as two colours, and every song and passage title looks like a call to action whether
or not the operator is pointing at it.

The titles become heading ink with no line at rest; the underline is the whole affordance and appears
on hover, and on keyboard focus so the cue is not mouse-only.

## Notes

- Owner request with a screenshot of `/tatib/144/`: "make the link texts similar to appear in normal
  color and only get underlined if being hovered".
- Retires the colour half of spec 056 (`--link` on `.entry__jump`); the token stays because the media
  library's "used by" links still wear it.
- The 3px underline offset is taken from the search result hover cue, not invented.
- The entry controls moved into a column of their own at the owner's direction: they sat over the
  title, so a hover-only cue could not reach it. The column is sized to the reading pane — labels
  from 700px of pane, icons below — because a 1440px window with both sidebars open leaves 400px.

## Acceptance sketch

- At rest every entry title is `#1F1F1D` light / `#F5F3EE` dark with `text-decoration-line: none`.
- Hovering one title underlines it 3px under the text and leaves its colour alone.
- Reaching it with the keyboard draws the same underline.
- The controls never cover a title; the labels give way to icons on a narrow pane and each button keeps
  its name for assistive technology.
- Search results, the media library's links, sidebar rows and the editor are unchanged.

## Links

- Spec: [140](../specs/140-stage-link-affordance/spec.md)
- Related items: ITEM-058 (the link colour this retires), ITEM-147 (the wrap the underline follows)
