---
id: ITEM-018
status: in_review
title: 'Use a custom date picker for Tata Ibadah forms'
type: feat
priority: P1
effort: M
created: 2026-10-07
updated: 2026-10-07
spec: specs/016-tatib-custom-datepicker/spec.md
branch: feat/026-live-projection-editing
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/275
archived_at:
archive_reason:
bump: patch
release_version: 1.0.0
---

# ITEM-018: Use a custom date picker for Tata Ibadah forms

## Summary

Replace the native date field in Tata Ibadah create/edit forms with a dependency-free custom calendar that supports keyboard use, clearing, and ISO date submission.

## Notes

- Owner decision: do not use the browser-native date picker.
- Keep date optional for recurring templates.
- Keep the form's server-side date contract and verify re-rendered modal forms after validation errors.

## Acceptance sketch

- Create/edit use a custom keyboard-accessible calendar, submit ISO dates, support clearing, and contain no native `input[type=date]`.

## Links

- Spec: [016 — Use a custom date picker for Tata Ibadah forms](../../specs/016-tatib-custom-datepicker/spec.md)
- Related items: ITEM-006 (sidebar editors), ITEM-017 (Tata Ibadah form fields)
