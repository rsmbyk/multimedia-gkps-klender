---
id: ITEM-174
status: backlog
title: The drawer backdrop stays over the page and swallows every pointer in the browser suite
type: fix
priority: P1
effort: M
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

# ITEM-174: The drawer backdrop stays over the page and swallows every pointer in the browser suite

## Summary

`<div id="drawerBackdrop" class="drawer-backdrop">` is left covering the reading page, so Playwright's
`item.hover()`, a rail-button click and the pickers' menus all time out with "subtree intercepts pointer
events". Three modules cannot prove anything until it is fixed: `test_entry_pickers` (21 errors),
`test_entry_preview` (3) and `test_immediate_editor_open` (2 errors).

## Notes

- Reproduced on `3e005688^` (develop without spec 155) with a single case each:
  `test_entry_pickers.EntryPickerE2ETests.test_song_picker_filters_songs_by_songbook_name`,
  `test_entry_preview.EntryPreviewE2ETests.test_short_preview_arrow_keys_do_not_scroll_the_page`.
- The first of those also reproduces on `3e005688` (develop with spec 155), so this is not that slice:
  the interception is in the drawer shell, and spec 151's rail/drawer work is the neighbourhood to read.
- The failure text is always the same shape: `- <div id="drawerBackdrop" class="drawer-backdrop"></div>
  intercepts pointer events`, retried 60+ times.
- `test_immediate_editor_open...test_sidebar_editor_forms_open_immediately_and_ignore_repeat_activation`
  fails on its own assertion (`expected 'New Tata Ibadah'`), also on `3e005688^`; it may share the cause.

## Acceptance sketch

- `tests.e2e.test_entry_pickers`, `test_entry_preview` and `test_immediate_editor_open` reach their
  targets with no backdrop interception.
- The drawer still dims and blocks the page while a drawer is actually open.

## Links

- Spec: none yet
- Related items: ITEM-168 (rail icons), ITEM-148 (drawer shell)
