---
id: ITEM-101
status: done
title: 'Brighten the translation label after flipping a Go To passage'
type: fix
priority: P2
effort: S
created: 2026-10-16
updated: 2026-10-16
spec: 101
branch: fix/101-goto-translation-flash
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/351
archived_at:
archive_reason:
bump: patch
release_version: 1.13.3
---

# ITEM-101: Brighten the translation label after flipping a Go To passage

## Summary

A passage opened through the projector's Go To rebuilds its corner cue on every TB/SIM flip, and the rebuilt label lost the brighten immediately — the operator saw only the momentary press colour. The label now keeps the same about-one-second highlight a service passage cue has, through one shared helper.

## Acceptance sketch

- T or a click on the label of a Go To passage brightens it for about one second, then it returns to rest.
- A flip during the hold toggles back and restarts the hold.
- A verse whose other edition has no text does nothing — no flip, no brighten.
- The service passage keeps its own flip and brighten, now through the same shared helper.

## Links

- Spec: [101](../../specs/101-goto-translation-flash/spec.md)
- Plan: [101](../../specs/101-goto-translation-flash/plan.md)
- PR: [#351](https://github.com/rsmbyk/multimedia-gkps-klender/pull/351)
