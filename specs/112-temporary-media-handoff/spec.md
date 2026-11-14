# Spec: Temporary media handoff

- **ID:** 112
- **Status:** Accepted
- **Item:** ITEM-112
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** minor

## Intent

An operator can make a local media file available to another computer for seven days. A computer running the local companion acquires missing online files for services dated today or later, verifies them, and exposes readable progress and history. Existing media entries remain references to immutable content identities.

## Scope

### In scope

- Individual Share action and online state for each local Media Library file.
- Companion-managed uploads and downloads with local durable progress, cancellation where offered, and transfer history.
- Transfer activity in Media Library and a temporary main-sidebar button.
- A Tata Ibadah media-status dialog and date-based automatic or manual download.
- R2 object availability, seven-day expiry, verification, and cleanup contract.
- R2 bucket, token, Django deployment configuration, cleanup scheduling, and connection verification.

### Out of scope

- Displaying media contents in entry Preview or Projector, converting PDF/PPT/PPTX, sharing an entire service in one action, and replacing an entry's immutable file reference.

## Domain rules

1. **Identity.** A media identity is its existing SHA-256 fingerprint, with expected byte count and detected family. One identity has at most one active cloud object. Two service entries may reference the same identity. A different filename never causes a new object or changes identity. The first library filename remains the displayed filename when identical bytes are reused.
2. **Share.** Only a local, verified file may be shared. Start one whole-object upload request (no multipart/resume). The service issues a short-lived, write-scoped permission for that identity; R2 credentials never reach the browser or companion. Availability remains false until completion is verified against identity and size. Successful verification starts a seven-day availability window. Sharing an already-online identity is idempotent and does not silently extend expiry. If the URL expires, the upload is cancelled, interrupted, or any other failure occurs, record failure/cancellation; do not retry or request new authorization automatically. The operator may explicitly Share again from byte zero. A failed/aborted PUT must not be advertised as an available object.
3. **Online expiry.** Store a server-authoritative expiry timestamp. At or after it, online availability and download authorization are false. Remove the cloud object; delayed physical cleanup must not keep it usable through the application. Show remaining days in the Media Library while online. Local copies and media entries survive online expiry. The server must handle a missing or corrupt cloud object as unavailable and correct stale metadata.
4. **Companion ownership.** The existing local companion performs byte transfer; its SQLite index in the named Docker volume also stores job direction, identity, start/end timestamps, byte progress, status (`in progress`, `completed`, `failed`, `cancelled`), and failure detail for diagnostics. Browser closure neither cancels nor loses known jobs. Reopening reads current status/history from the companion. A companion/container restart cannot resume a single interrupted request: mark such a job failed and allow a new explicit attempt. Transfer history belongs to the current computer and is not a global account log. Progress never exceeds total bytes; terminal jobs are immutable history records.
5. **Downloads and retry.** Deduplicate concurrent downloads by identity, including references in several services. Write to a temporary local file, verify byte count and SHA-256, then atomically expose it in the existing Media Library. A partial/mismatched download is never available. An unavailable or expired cloud object is not downloadable. Manual downloads may be cancelled; automatic downloads cannot be cancelled from the service dialog. Every failed automatic attempt is recorded, then retried from byte zero with exponential backoff (initial 5 seconds, doubling to a 5-minute cap, with jitter); the retry loop has no attempt-count limit while a today/future reference exists and the source remains online. Persist the next-attempt time in the companion so browser closure/restart does not reset the backoff. A transient lost connection pauses retries until connectivity returns; expiry/removal of the online copy or loss of eligible references ends the retry loop. Never create overlapping attempts for the same identity. A failed attempt appears in history while the current state is `Retrying` with the next-attempt time accessible to assistive technology.
6. **Automatic eligibility.** On app open/reconnection, reconcile missing media identities against all accessible Tata Ibadahs dated today or later in the app's service timezone (`Asia/Jakarta` unless repository timezone configuration establishes another canonical zone). Download each missing online identity once at a time. A local copy cannot be deliberately removed while any service dated today or later references it; this prevents an immediate delete-and-reacquire loop. Past or undated services do not trigger automatic acquisition. The app need not discover new remote shares in the background while no app tab has opened; already-started companion jobs and their retry schedules keep running. Opening the Media files dialog shows current state but is not required to trigger reconciliation.
7. **Missing/unavailable.** A media entry remains attached to its identity when no local or online bytes exist. Its existing missing-file treatment remains; the status dialog shows both local and online unavailability. Neither deleting a local file nor online expiry removes the Tata Ibadah entry.
8. **History order and sessions.** Active jobs precede finished jobs, active sorted by start time newest first, finished by end time newest first. The transient sidebar button appears when a transfer begins; its appearance establishes a session boundary. During activity, it opens an active-only view. When all jobs end, it opens a finished view separating jobs completed since that appearance (`Just finished`) from older history (`Earlier transfers`) with a line. It disappears after that finished view is closed. A new job before acknowledgement remains in the same session; a job after disappearance starts a new session. History remains available through Media Library regardless of sidebar visibility.
9. **Protected local copies.** If any Tata Ibadah dated today or later references an identity, its local copy cannot be manually deleted or removed by unused-file cleanup. The companion must reject delete requests using a fresh, complete reference inventory, not just a stale browser-side check; if the inventory cannot be verified, fail closed for deletion and explain why. Past or undated references do not block deletion. The entry itself can still be edited (title only) or removed under existing rules. Once no qualifying reference remains, the ordinary deletion/unused retention rules apply.

## R2 configuration and operations

- **Bucket:** Provision a dedicated, private R2 bucket in the **Standard** storage class, with no `r2.dev` public access or public custom domain. Use deterministic object keys under `temporary-media/<sha256>`; never put user-supplied filenames in keys. The bucket name is configuration, not a hard-coded account resource. The same bucket serves production and local Django during development unless the operator explicitly configures a separate development bucket; use a separate key prefix for development to avoid collisions with production.
- **Credentials:** Create an R2 S3 API token scoped to this bucket with Object Read & Write permission. Keep its Access Key ID and Secret Access Key only in server-side secrets. Define `GKPS_R2_ACCOUNT_ID`, `GKPS_R2_BUCKET`, `GKPS_R2_ACCESS_KEY_ID`, `GKPS_R2_SECRET_ACCESS_KEY`, and optional `GKPS_R2_ENDPOINT` (needed for a jurisdiction-specific bucket) as Django server settings. Document placeholders in `.env.example`, load them into the local Django Compose service, and set corresponding encrypted Vercel environment variables for production. Do not expose them through template context, API responses, browser JavaScript, the local companion, images, or committed `.env` files. Fail closed and show online-sharing unavailable if configuration is missing or invalid; local Media Library remains usable.
- **Direct transfer:** Django signs operation- and object-specific PUT/GET URLs using those server credentials. The companion sends bytes directly to the R2 S3 endpoint over HTTPS; browser and Vercel functions do not relay the file body. No R2 bucket CORS rule is needed for the companion's non-browser HTTP request. The upload URL has a bounded lifetime sufficient for the 200 MB single PUT; expiry produces a failed job as defined above. The companion can obtain or renew a GET permission for retries while the identity remains online; a permission must never outlive its seven-day online expiry. The URL or renewal capability is scoped to that object, persisted only in the companion's named volume, never exposed as a reusable browser link or long-lived R2 key. The service denies new URLs at the seven-day cutoff; already-issued signed URLs cannot be instantly revoked.
- **Verification and cleanup:** Before marking an upload online, the server checks that the expected object exists at the expected key and byte count; the companion already knows the local SHA-256, and recipients independently verify downloaded bytes. Do not equate an R2 ETag with SHA-256. A server-side scheduled cleanup deletes expired objects and reconciles stale records; configure its schedule/authorization for production and a runnable management command for local/operational use. Configure an eight-day bucket lifecycle expiry as a safety backstop for orphaned objects, while application availability ends seven days after verified completion. Physical deletion may lag the cutoff; the status and API must not claim availability during that interval.
- **Setup verification:** Provide a configuration/health command that checks bucket access without printing secrets, then an opt-in end-to-end smoke test with a small temporary object: upload, HEAD, signed GET, byte verification, delete, and confirmation that it is gone. Document exact Cloudflare dashboard setup, token scope, Vercel and Compose variables, cleanup schedule, lifecycle rule, expected costs/free-tier limits, and rollback/credential rotation. Do not enable sharing in production until this check passes.

## UI details

The [interactive preview](./preview.html) is the visual reference for light and dark themes. Its demo controls and sample transfers are preview-only.

- **Media Library layout:** Put the icon-only Transfers button immediately left of Settings in the header. Each file row keeps balanced side and vertical padding (`14px` desktop, `12px` at ≤700px); place the cloud control immediately left of the existing icon-only Delete button. A 36×36 px outlined neutral Share button, 36×36 px outlined danger Delete button, and passive cloud-check status differ visibly. The online state shows remaining days in a muted 10px caption below its icon. No progress percentage appears beneath the ring.
- **Tata Ibadah references in Media Library:** Sort dated uses by service date, newest first. Within the same Tata Ibadah/date, preserve the order in which its entries appear. If different Tata Ibadahs have the same date, order those Tata Ibadahs by title, then preserve each one's entry order. Put undated Tata Ibadahs after every dated one, sorted by Tata Ibadah title and then their entry order. Use a stable ID tie-breaker for equal titles. Render each dated reference as one link in the exact order `Tata Ibadah title (10 Okt 2026) · Entry title or filename`; omit the parenthesized date for an undated Tata Ibadah. The link opens the Tata Ibadah scrolled to that entry. Use the entry's optional title as its label; when blank, use that entry's saved `media_filename`, even if it differs from the Media Library's canonical display filename. Keep the entry label muted within the link, but make the entire line clickable and focusable. Links for services before today's date use normal ink color; links for today/future keep the accent color. Undated links use normal ink color. Compare dates in the app's service timezone, and preserve underline on hover/focus for all links.
- **Protected delete:** When a file is needed by a service dated today or later, hide its Delete button and remove it from keyboard/accessibility navigation, but preserve the button's 36×36 px grid space (`32×32px` at ≤700px) so horizontal alignment matches other rows. Do not show a popup or empty-looking button. When no qualifying reference remains, show the normal Delete button again. A concurrent service-date/reference change still requires companion-side rejection.
- **Progress and controls:** Use a 40×40 px circular ring with an opaque 32×32 px center (even 4px ring), not a hover fill that alters ring geometry. During upload its center is an X cancel button, with a conventional hover highlight confined to the center. During manual download the center is likewise cancellable. Automatic download uses a passive download glyph, without cancel affordance. Label icon-only controls and availability icons accessibly; expose progress numerically to assistive technology.
- **Transfer dialog:** Maximum width `700px`, maximum height `min(84vh, 760px)`, 13px radius; scrollable body with existing app scrollbar treatment. Header padding `20px 24px 17px`, body horizontal padding `24px`, footer `13px 24px 18px`. No top-right X. Footer Close, Escape, and backdrop dismiss it. Active rows show directional icon, filename, `In progress`, a 4px progress bar, percent and bytes transferred/total; omit a separate file-size line. Finished rows show icon, filename, size, and Completed/Failed/Cancelled only. Do not show start/end time, direction words, or failure-reason text. Header entry shows active first and finished second; omit a `Finished` heading if there are no active jobs. When empty, show a quiet empty state.
- **Main sidebar:** Put the 44×44 px Transfers button just before offline status (`40×40px` at ≤700px). Active icon reflects upload-only, download-only, or both; 7px yellow dot means any active job. When all session jobs finish, use the same generic Transfers icon as the Media Library header, with a green dot if all succeeded or red if any failed/cancelled. While active, its dialog displays active jobs only. After completion, its dialog shows the session partition described above and the button disappears when that dialog closes.
- **Tata Ibadah:** Show `Media files` to the left of Project only if at least one media entry exists. Its dialog lists every media entry in Tata Ibadah order, including repeated references. Each row displays type icon, entry title if present otherwise canonical filename, file family and size, then **download action/progress → online availability → local Media Library availability**. Online and local indicators are icon-only with accessible names. Missing+online+today/future shows uncancellable automatic progress; missing+online+past/undated shows a download button which becomes a cancellable progress ring. Missing+offline has no download action. Existing entry/projector display stays blank for file contents.
- **Colors and typography:** Reuse current app tokens for ink, muted text, dividers, canvas, green success, neutral controls, and danger. Online/local available icons use success green; missing local uses established danger; online unavailable is neutral. Transfer labels use 13px names, 11px metadata/status. The preview's type icon boxes are 38×38 px desktop and 34×34 px at ≤700px.
- **Responsive:** At ≤700px, dialogs use up to `88vh`, `17px` horizontal padding, and compact file/status grids. Long filenames truncate with ellipsis without pushing indicators off-screen. The modal remains keyboard navigable and focus returns to its launcher on dismissal.
- **Motion:** Dialog scale `.97 → 1` with fade in `190ms` and reverse in `150ms`; scrim fades on the same timing. Disable animations under `prefers-reduced-motion: reduce`. Live progress updates must not retrigger entry animation.

## Acceptance scenarios

### Scenario: Share one content identity

- **Given** a locally verified file referenced by two entries, with no online object
- **When** the operator selects Share and the companion completes a verified single upload
- **Then** both entries resolve the same online identity, the library shows online status and seven-day countdown, and one cloud object is available.

### Scenario: Upload fails or browser closes

- **Given** an upload in progress
- **When** its browser tab closes
- **Then** the companion keeps transferring and a newly opened tab shows its actual progress/history.
- **When** the signed URL expires or the companion restarts mid-request
- **Then** the job ends failed, online remains unavailable, no automatic retry occurs, and explicit Share can start again from zero.

### Scenario: Automatic acquisition and verification

- **Given** a missing local identity is online and used in a Tata Ibadah dated today or later
- **When** the app opens or reconnects on this computer
- **Then** the companion starts at most one download for that identity, the service dialog shows passive progress, and the library marks it available only after byte count and SHA-256 match.

### Scenario: Past or undated service

- **Given** its identity is missing locally but online
- **When** the service is past or undated
- **Then** no automatic download begins; the service dialog offers manual download with a cancellable progress state.

### Scenario: Protected local copy

- **Given** a local identity is referenced by a Tata Ibadah dated today or later
- **When** its Media Library row is shown
- **Then** the Delete button is hidden while its grid space remains, the companion rejects deletion requests, and unused-file cleanup preserves it.
- **When** the last today/future reference becomes past or is removed
- **Then** normal manual deletion and unused-file retention become available again.

### Scenario: Untitled Media Library reference

- **Given** a file is referenced by an entry without a title, whose saved filename differs from the library display filename
- **When** its usage list is shown in Media Library
- **Then** the reference line reads `Tata Ibadah title (10 Okt 2026) · saved filename` with its actual title/date, and clicking anywhere on that line opens the service at that entry.

### Scenario: Past reference link color

- **Given** a Media Library file is used by services before and after today's date
- **When** its usage list is shown
- **Then** past-service links use normal ink color, today/future links use accent color, and both remain fully clickable and keyboard-focusable.

### Scenario: Usage-list order

- **Given** one file is referenced by multiple entries in the same dated service, by another dated service, and by undated services
- **When** its Media Library usage list is shown
- **Then** dated services appear newest first; same-service entries retain their appearance order; equal-date services sort by title; undated services come last by title, each retaining its entry order.

### Scenario: Persistent automatic retry

- **Given** a today/future service has a missing local identity that remains available online
- **When** automatic download fails repeatedly
- **Then** each failed attempt enters history, only one attempt runs at a time, and the companion keeps retrying with capped backoff across browser closure and companion restart until verification succeeds or eligibility/online availability ends.

### Scenario: Transfer views and sidebar session

- **Given** upload and download jobs have started and older history exists
- **When** the sidebar button is opened during activity
- **Then** it shows only active jobs, a combined icon, and a yellow dot.
- **When** all session jobs end and the button is opened
- **Then** it shows just-finished jobs above a divider and earlier jobs below, with a green dot for all-success or red if any failed/cancelled; closing hides the sidebar button while the Media Library dialog retains history.

### Scenario: Online expiry

- **Given** an uploaded identity reaches seven days
- **When** a computer checks its availability or requests download
- **Then** it is unavailable and download permission is denied, while existing local copies and service entries remain.

## Traceability

- Domain/app tests: `multimedia/test_local_media.py` covers protected deletion, durable retry plans, and R2 URL restrictions; `multimedia/web/test_media.py` covers reference ordering, the service dialog, manifest eligibility, share completion, and stale R2 objects.
- Browser check: isolated Chromium opened a worktree-local Django server, verified the service and transfer dialogs, and observed no page errors. The live R2 path still requires a configured bucket smoke test.
- Implementation: `multimedia/media_handoff.py`, `multimedia/local_transfers.py`, the existing companion and Django media endpoints, `static/web/media-handoff.js`, `static/web/media-library.js`, Tata Ibadah templates, shared styles, Docker/production configuration, and `docs/local-media-companion.md`.

## Owner review points

- Automatic discovery begins on app open/reconnection; already-started transfers survive tab closure. A completely closed browser does not discover newly shared references on its own.
- Local copies needed by a service dated today or later are protected from manual deletion and unused-file cleanup; past and undated services do not protect them.
- Failed automatic downloads retry without an attempt limit, but with capped backoff, while a qualifying reference and online source remain.
