---
id: ITEM-140
status: backlog
title: 'The projector keeps data-showing=true when display-off is asked for'
type: fix
priority: P1
effort: S
created: 2026-10-25
updated: 2026-10-25
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-140: The projector keeps data-showing=true when display-off is asked for

## Summary

Two browser tests that switch a playing audio or video entry off expect the projector's `<body>` to reach
`data-showing="false"`; it stays `"true"` for the whole five-second window, with `data-current-screen="2"`
and `data-display-channel="gkps-service-display"` set. Either the display-off path stopped clearing the
showing state, or the projector now reports a different attribute and the tests are reading the old one —
the slice that fixes this has to decide which, from the running page.

## Notes

- Reproduced on `develop` `ffa5c340`: identical two failures, same assertion, so it is not a slice's
  regression.
- Failing tests: `tests/e2e/test_audio_display.py::AudioDisplayE2ETests::test_untitled_preview_and_projector_idle_display_off`
  and `tests/e2e/test_video_display.py::VideoDisplayE2ETests::test_navigation_and_display_off_stop_and_reset_video`.
- The failing locator resolves to
  `<body data-adopt data-showing="true" data-service data-current-screen="2" data-display-channel="gkps-service-display" class="projector …">`,
  so the page is running the shared browser-local display state (spec 119), not the older per-page path.

## Acceptance sketch

- With a media entry playing, "display off" leaves the projector in its off state within the test's
  timeout, and the attribute the test reads is the one the projector writes.
- The same check holds for a text entry, so the rule is not specific to media.

## Links

- Spec: —
- Related items: ITEM-002 (projection source as display + controls), ITEM-119 (the unified dock)
