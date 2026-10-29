---
id: ITEM-155
status: in-progress
title: 'The Media Library and the transfer history group by age'
type: feat
priority: P2
effort: M
created: 2026-10-28
updated: 2026-10-28
spec: specs/146-media-and-transfer-age-buckets/spec.md
branch: feat/146-media-and-transfer-age-buckets
pr:
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/417
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-155: The Media Library and the transfer history group by age

## Summary

The Media Library list stops drawing one heading per upload day and groups by age — `Last 30 days`,
`Earlier this year`, `Older` — the Tata Ibadah list's own buckets (spec 132). The Transfers dialog, which
has no grouping at all today, takes the same ladder plus two recent rungs: `Last 24 hours` and
`Last 7 days`. One shared browser rule decides both, so the three lists cannot name the same age
differently.

## Notes

- A per-day heading answered a question the row's meta line already answers (`Image · 28 Oktober 2026 ·
  7 KB`); eight files drew four headings, one of them over a single row. Under age they draw one.
- The Media Library takes three buckets, not four: an upload's timestamp is never in the future, so there
  is no `Upcoming`, and a file uploaded today is the newest row of `Last 30 days`.
- The transfer ladder's first two rungs are rolling windows measured from the moment the dialog draws,
  and a transfer is dated by when it started — the only instant an active transfer has.
- Bucket keys: `last-30-days`, `earlier-this-year`, `older` on both surfaces, plus `last-24-hours` and
  `last-7-days` on the transfer history.
- The rail's progress flyout keeps its shape: active rows and the seen divider, no headings.

## Acceptance sketch

- The Media Library draws its three headings in order, each only while it holds rows, and no date-shaped
  heading anywhere.
- A file uploaded exactly thirty days ago sits under `Last 30 days`; thirty-one days ago, same year, under
  `Earlier this year`.
- A transfer started 23 hours ago sits under `Last 24 hours`; two days ago under `Last 7 days`; eight days
  ago under `Last 30 days`.
- An active transfer draws above the finished rows of its own bucket.
- A size sort draws no headings; an ascending date sort reverses the shelves.
- The three shared labels read identically on `/media-library/`, its Transfers dialog and `/tatib/`.

## Links

- Spec: [146](../../specs/146-media-and-transfer-age-buckets/spec.md)
- Related items: ITEM-136 (spec 132 — the Tata Ibadah list's own buckets, done), ITEM-019 (spec 017 — the
  month header 132 replaced)
