# Spec: Enable Media Library sharing in a fresh session

- **ID:** 113
- **Status:** Accepted
- **Item:** ITEM-113
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

Allow an operator to share a Media Library file after opening that page directly in a fresh browser session. Django must receive a valid CSRF token on the existing share-permission request so it can return the expected JSON response and the companion can begin the upload.

## Scope

### In scope

- Set the CSRF cookie when serving the Media Library page.
- Keep the share-permission POST protected by Django CSRF middleware.
- Verify the direct-open and share flow with Django and browser tests.

### Out of scope

- Companion API authorization or transfer changes.
- R2 credential, bucket, expiry, or permission changes.
- Changes to transfer progress or other Media Library layout.
- General handling for non-JSON responses from unrelated endpoints.

## Domain rules

- A GET of `/media-library/` in a fresh session must make the CSRF cookie available to same-origin page scripts.
- The existing Share online POST must send the matching token through `X-CSRFToken` and pass normal Django CSRF validation.
- The share endpoint remains protected: a missing or invalid CSRF token is rejected and does not create a share or transfer.

## Acceptance scenarios

### Scenario: Share from a fresh Media Library visit

- **Given** an operator opens `/media-library/` directly in a browser session with no prior CSRF cookie, and a local file is available to share
- **When** the operator clicks **Share online** and the permission request is otherwise valid
- **Then** the page supplies the CSRF cookie, the share POST includes its matching token, the server returns JSON, and the companion starts the upload without a browser JSON-parsing alert

### Scenario: Keep CSRF protection on sharing

- **Given** a share request has no valid CSRF token
- **When** it is posted to the share-permission endpoint
- **Then** Django rejects it and no cloud-share record or companion upload is started

## Traceability

- Domain/app tests: `multimedia/web/test_media.py` (fresh-page CSRF cookie and protected share POST)
- E2E: `tests/e2e/test_media_library.py` (direct-open Share online from a fresh browser context)
- Implementation: `multimedia/web/reading/views.py` (`ensure_csrf_cookie` on the Media Library page)
- Verification: `multimedia/web/test_media.py::MediaLibraryCsrfTests` and
  `tests/e2e/test_media_library.py::MediaLibraryE2ETests.test_share_online_from_fresh_library_page_sends_csrf_token`
