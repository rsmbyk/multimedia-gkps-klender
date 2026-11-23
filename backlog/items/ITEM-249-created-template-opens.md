---
id: ITEM-249
status: ready
title: 'A newly created Template does not open on the reading stage'
type: fix
priority: P1
effort: S
created: 2026-11-23
updated: 2026-11-23
spec: 234-open-created-template
branch: feat/234-open-created-template
pr:
issue: 609
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-249: A newly created Template does not open on the reading stage

## Summary

Creating a dated Tata Ibadah opens it immediately on the reading stage; creating a Template only
refreshes the sidebar and leaves the stage where it was. The operator has to click the new row a
second time. R46 currently records the list-refresh behaviour as intentional, so the change is a
modification of that requirement, not a missing condition.

## Notes

- The create handler in `static/web/reading.js` opens only `record_kind === 0`; a Template answers
  `record_kind === 1` from `editor_save` and falls through to the list refresh.
- The destination for a Template is `/tatib/<id>/?mode=template`, the URL copy-as-template already
  uses; `TatibView` also derives the mode from the record itself.
- Live base/slice measurements are in `specs/234-open-created-template/preview/README.md`.
- The existing E2E assertion `test_a_template_create_keeps_the_stage` is superseded by the new
  behaviour and is rewritten at Implement.

## Acceptance sketch

- Creating a Template from either Tata Ibadah list opens it at `/tatib/<id>/?mode=template`, with
  its name on the stage, its row current and the child pane open.
- The open is in place: no document reload, `data-nav` preserved, quiet focus on the new row.
- Dated creates, edits, refused creates, generate and copy flows land exactly as before.

## Links

- Spec: [234](../specs/234-open-created-template/spec.md)
- Related items: ITEM-240 (a created songbook or song opens as its row would)
