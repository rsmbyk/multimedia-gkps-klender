---
id: ITEM-270
status: speccing
title: 'Use template progress survives a close'
type: feat
priority: P2
effort: M
created: 2026-11-28
updated: 2026-11-28
spec: 253-use-template-progress
branch: feat/253-use-template-progress
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-270: Use template progress survives a close

## Summary

Closing the Use template modal today discards every settled slot. The operator should be told that
leaving keeps the work and that it can be resumed; progress should be kept per template so two
templates do not overwrite each other.

## Notes

- Owner decisions: sessionStorage (lost when the browser session closes), written continuously on
  every change, and cleared after a successful Create.
- Keyed by the template id already on the dialog as `data-generate-tatib`.
- `generate.js` close paths: Cancel, backdrop click and the `cancel` event (Esc).
- R36 already promises the template is byte-identical after generating or abandoning; this adds
  client-only state without touching the record.
- Static preview and measured numbers: `specs/253-use-template-progress/preview/README.md`.

## Acceptance sketch

- Settle a slot, close, reopen the same template: the slot is settled again.
- Open a second template: it starts empty; the first one's progress is intact.
- A dirty close shows a confirmation that says the progress is saved and can be resumed later.
- A successful Create clears the saved progress for that template.

## Links

- Spec: [253-use-template-progress](../specs/253-use-template-progress/spec.md)
- Related items: —
