---
id: ITEM-139
status: backlog
title: 'Three offline projector E2E tests error with ERR_INTERNET_DISCONNECTED'
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

# ITEM-139: Three offline projector E2E tests error with ERR_INTERNET_DISCONNECTED

## Summary

Three browser tests that take the page offline and then open the projector die on the navigation itself:
`Page.goto: net::ERR_INTERNET_DISCONNECTED at http://localhost:<port>/projector?service=<id>`. Playwright's
offline emulation applies to loopback too, so the projector page never loads and the assertion underneath
is never reached. The behaviour under test — a saved service still projecting with Django down — is
therefore unproven by the suite that exists for it.

## Notes

- Reproduced on `develop` `ffa5c340` under the same environment, same command, same database: identical
  three errors, so it is not any one slice's regression.
- Failing tests: `tests/e2e/test_offline_library.py::OfflineLibraryE2ETests::test_saved_content_and_projector_survive_disconnection`,
  `tests/e2e/test_pdf_display.py::PDFDisplayE2ETests::test_saved_projector_renders_pdf_while_django_is_offline`,
  `tests/e2e/test_powerpoint_display.py::PowerPointDisplayE2ETests::test_saved_projector_renders_slides_while_django_is_offline`.
- Both offline modules already need a way to load the *document* while the *network* is unavailable —
  either by intercepting every non-loopback request (`context.route`) instead of `set_offline(True)`, or
  by serving the shell from the browser's cache. Which of the two is the honest reading of "offline" for
  this product is the open question for the slice.

## Acceptance sketch

- The three tests run green on a machine with no network access to anything but loopback.
- A test that must be offline proves the page loaded from the saved copy, not from the server.

## Links

- Spec: —
- Related items: ITEM-117, ITEM-118, ITEM-122 (saved rendering)
