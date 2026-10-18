# Plan 113: Enable Media Library sharing in a fresh session

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-113
- **Bump:** patch

## Why

When an operator opens Media Library directly in a fresh browser session and clicks **Share online**, Django rejects the permission request because the page did not set a CSRF cookie. The browser then tries to parse Django's HTML 403 page as JSON and displays an unexpected-token alert. No upload starts.

## Scope / edges

**In:** Make the Media Library page set the CSRF cookie used by its existing same-origin share request. Preserve CSRF validation on the share endpoint and cover fresh-session behavior.

**Out:** Changing companion authorization, Cloudflare/R2 permissions, upload behavior, transfer UI, and general error-message handling for unrelated HTML responses.

## Approach

Use Django's existing `ensure_csrf_cookie` mechanism on the Media Library page view, following the pattern already used on the Tata Ibadah page. Keep the `/media-library/cloud/<sha>/begin/` endpoint CSRF-protected; the browser's existing share helper will continue sending the cookie value in `X-CSRFToken`.

## TDD

- Domain/app tests: `multimedia/web/test_media.py` with a CSRF-enforcing Django client. Verify a fresh Media Library GET sets the cookie, a POST with that token reaches the share view, and a POST without a valid token remains rejected.
- E2E: `tests/e2e/test_media_library.py` direct-open/share regression using a fresh browser context and mocked companion/R2 permission responses.

## Risks

- Do not exempt the share endpoint from CSRF. The fix must make the browser obtain the expected token while retaining Django's existing write protection.
