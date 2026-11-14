---
id: ITEM-197
status: in-review
title: 'Project button on the song and Bible pages'
type: feat
priority: P1
effort: S
created: 2026-11-14
updated: 2026-11-14
spec: specs/193-reading-project-button/spec.md
branch: feat/193-reading-project-button
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/510
issue: 507
closed_at:
closed_reason:
bump: minor
release_version:
---

# ITEM-197: Project button on the song and Bible pages

## Summary

The song and Bible chapter pages have no way to put what is on stage onto the projector. The
request (2026-11-14, chat): add a project button on the songs and Bible verses pages that opens the
chapter or song as a Go To detour and opens the projector window if none is open.

## Notes

- The machinery already exists: `display.js`'s `goTo` verb (spec 185) writes the Go To pointer, the
  projector applies a stored Go To on boot and over the channel, and the named `gkps-projector`
  window is reopened by spec 141's control. This slice adds the third trigger surface and its
  window act.
- The Tata Ibadah page's project group is the anatomy to port (`.read__project`), minus the toggle:
  this control has no Stop state — the projector's Back ends the detour.

## Acceptance sketch

- A song page and a chapter page each draw a Project control in the stage header; clicking it puts
  that song/chapter on the projector as a Go To detour and brings the `gkps-projector` window
  forward (opening it when closed).
- No control on book pages without a chapter, verse-less songs, saved pages, or below 720px.
- An adopted service survives underneath; Back returns to it.

## Links

- Spec: [193](../specs/193-reading-project-button/spec.md)
- Related items: ITEM-189 (spec 185, the dock's Go To the pointer shape comes from), ITEM-150
  (spec 141, the named projector window)
