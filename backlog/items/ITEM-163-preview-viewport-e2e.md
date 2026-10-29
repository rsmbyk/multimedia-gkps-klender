---
id: ITEM-163
status: backlog
title: 'Three preview E2E tests cannot hover their entry after the viewport shrinks to 900×380'
type: fix
priority: P2
effort: S
created: 2026-10-29
updated: 2026-10-29
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-163: Three preview E2E tests cannot hover their entry after the viewport shrinks to 900×380

## Summary

`test_the_preview_header_stays_put_while_the_body_scrolls`, `test_short_preview_arrow_keys_do_not_scroll_the_page`
and `test_clicking_long_preview_text_allows_arrow_key_scrolling` set a 900×380 viewport and then call
`_open_preview()`. Below 1272px the sidebars are drawers over the page (spec 138), and the chapter drawer
the pane had open at 1440 stays open over it — so Playwright's `item.hover()` is retried 62 times and
times out with *"`#chBody` … intercepts pointer events"*.

## Notes

Reproduced on unmodified `develop` at `24a6d6d2`, in the main checkout, with the three cases run alone:
three errors, 101s. Not caused by any slice in flight. The likely fix is the fixture's viewport timing —
the context is created at 1440×900 and resized afterwards, so the pushed sidebars become open drawers
mid-test — rather than the drawer behaviour itself.

## Acceptance sketch

- The three cases reach their entry at 900×380 without a pointer retry loop.
- Every other preview case in `tests/e2e/test_entry_preview.py` is unchanged.

## Links

- Spec: —
- Related items: ITEM-153, ITEM-159 (the other E2E reds on develop)
