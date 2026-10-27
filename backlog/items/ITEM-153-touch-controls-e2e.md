---
id: ITEM-153
status: backlog
title: 'The touch-controls E2E cannot reach the preview control'
type: fix
priority: P1
effort: S
created: 2026-10-28
updated: 2026-10-28
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-153: The touch-controls E2E cannot reach the preview control

## Summary

`tests/e2e/test_tatib_hover.py::TatibHoverE2ETests::test_touch_controls_remain_visible_after_dismissal`
errors on a 390×844 touch context. Playwright retries the tap action 62 times, each round waiting for
the element to become visible, enabled and stable, and ends with **"element is not visible"**.

Found while running `tests.e2e.test_tatib_hover` + `tests.e2e.test_tatib_entry_controls` for spec 142,
35/36 otherwise green. The failure is **identical on unmodified `develop`** — run there on its own with
one test, same 62 retries, same error — so it predates that slice.

## What is known, and what is not

- Known: the error is a `tap` that never becomes actionable, in the one test that uses a phone context
  (`viewport 390×844`, `is_mobile`, `has_touch`). The test taps `#panelCollapse`, `#chCollapse`, then
  the first entry's `[data-preview-open]`, then dismisses the modal with `page.touchscreen.tap(5, 5)`.
- Not yet known: **which** of those taps is the one that never resolves, and why. It has not been
  narrowed further, so the cause is not claimed here.

## Why it matters

The test is the only proof that the entry controls stay visible on a touch screen after a modal is
dismissed — the behaviour the `(hover: none)` exemptions in spec 032/033 exist for. While it errors,
that behaviour is unproven on any branch, so a real regression there would be invisible.

## Links

- Failing test: `tests/e2e/test_tatib_hover.py` (the test named above)
- Neighbours: ITEM-139, ITEM-140, ITEM-141, ITEM-144 — the other E2E tests known red on `develop`
