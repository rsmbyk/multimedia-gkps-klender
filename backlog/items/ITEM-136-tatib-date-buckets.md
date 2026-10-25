---
id: ITEM-136
status: in-progress
title: 'Group the Tata Ibadah list by age, and mark today'
type: feat
priority: P2
effort: S
created: 2026-10-25
updated: 2026-10-25
spec: specs/132-tatib-sidebar-date-buckets/spec.md
branch: feat/132-tatib-sidebar-date-buckets
pr:
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/391
closed_at:
closed_reason:
bump: patch
release_version:
---

# ITEM-136: Group the Tata Ibadah list by age, and mark today

## Summary

The dated Tata Ibadah list stops grouping by calendar month and groups by age — `Upcoming`, `Last 30 days`,
`Earlier this year`, `Older` — with today's services first inside `Upcoming`, each carrying a `Today`
badge. The operator dock's picker takes the same four groups and the same badge instead of its row tints,
and a saved page draws them too.

## Notes

- A month heading answered a question nobody asked of a list whose rows already print their own date, and
  it put a service from three days ago beside one from six weeks ago.
- The bucket window is days, not months: 0–30 days back is `Last 30 days`, 31 or more in the same year is
  `Earlier this year`. A rolling window has no honest month name, which is why the labels are `Upcoming` /
  `Last 30 days` / `Earlier this year` / `Older` and not month names.
- "Today" is the congregation's day in `Asia/Jakarta`, the same clock the media inventory uses; the project
  runs on UTC, and a service would otherwise leave `Upcoming` at 07:00 WIB.
- Three surfaces draw the list and all three agree: the server panel, the operator dock, and the saved-page
  renderer.

## Acceptance sketch

- The dated list shows the four headings in order, each only while it holds rows.
- A service dated exactly thirty days ago sits under `Last 30 days`; thirty-one days ago, same year, under
  `Earlier this year`.
- Inside `Upcoming`, today's rows come first, then the future farthest date first, and only today's rows
  carry the `Today` badge.
- The dock shows the same four headings and the same badge, and no longer tints a row.
- A saved `/tatib/` page groups and badges identically, on the day it is opened.

## Links

- Spec: [132](../../specs/132-tatib-sidebar-date-buckets/spec.md)
- Related items: ITEM-019 (spec 017 — the month header this replaces), ITEM-133 (empty-service tiles, done),
  ITEM-134 (Break retirement, done)
