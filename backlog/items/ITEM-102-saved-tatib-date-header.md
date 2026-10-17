---
id: ITEM-102
status: done
title: 'Show the Tata Ibadah date header in the saved-copy reading path'
type: fix
priority: P2
effort: S
created: 2026-10-17
updated: 2026-10-17
spec: [102](../../specs/102-saved-tatib-date-header/spec.md)
branch: fix/102-saved-tatib-date-header
pr: https://github.com/rsmbyk/multimedia-gkps-klender/pull/352
archived_at:
archive_reason:
bump: patch
release_version: 1.13.4
---

# ITEM-102: Show the Tata Ibadah date header in the saved-copy reading path

## Summary

Opening a dated Tata Ibadah by clicking the sidebar replaces the date above the title with
`TATA IBADAH`; a full refresh then shows the date. The in-place navigation renders the page from
the saved offline library, whose renderer sets the eyebrow to the section label and never writes
`service.date`, so both the first render and the online refresh show the fallback. The server
path (spec 017) is correct, and the existing tests miss it because the click-through test never
readies the offline library, and the offline test class has only an undated service.

## Notes

- Reported by the owner on 2026-10-17: "when you open a tata ibadah by clicking on the sidebar,
  the dates at the top is replaced with 'TATA IBADAH' instead of the dates. but, when you refresh
  the page, it changed to its date."
- Owner to correct if wrong: this is read as a parity fix of accepted spec 017, not a new rule.

## Acceptance sketch

- A dated service opened from the panel reads `23 Agustus 2026`, before and after the background
  refresh.
- An undated service keeps `Tata Ibadah`.
- A dated service under `?mode=template` keeps its date.
- A full page load is unchanged.

## Links

- Spec: [102](../../specs/102-saved-tatib-date-header/spec.md)
- Plan: [102](../../specs/102-saved-tatib-date-header/plan.md)
- Related items: [ITEM-019](./ITEM-019-tatib-full-month-header.md) (spec 017 — the header rule),
  [ITEM-095](./ITEM-095-offline-library-sync.md) (spec 092 — the saved-copy renderer)
