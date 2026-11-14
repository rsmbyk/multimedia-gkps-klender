# Plan 112: Temporary media handoff

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-112
- **Bump:** minor

## Why

Media bytes currently live in each operator computer's Media Library. A service created on one computer can therefore contain references that are missing on another. Operators need an explicit, temporary way to share individual files and a reliable way to acquire them before a future service, while seeing transfer progress even after closing a browser tab.

## Scope / edges

**In:** Per-file seven-day online sharing, R2 bucket/credential and deployment configuration, verified downloads to the existing local library, durable companion-owned transfer activity, Media Library and sidebar transfer views, and Tata Ibadah media status with date-based automatic download.

**Out:** Projector or entry preview rendering, PPT/PPTX presentation, permanent cloud storage, peer-to-peer transfer, bulk share commands, and a general-purpose cloud file manager.

## Approach

Use the existing SHA-256 media identity across local copies and cloud objects. The Django service owns authoritative cloud availability/expiry metadata and grants narrowly scoped temporary R2 operations; the local companion owns byte transfers, cancellation, progress, and this computer's history in its named volume. The browser controls and observes companion jobs, while the service page reconciles references for today/future services. Keep cloud credentials out of browser and companion configuration. Treat the [approved interactive preview](./preview.html) as the visual reference, with domain behavior governed by [spec.md](./spec.md).

Provision one private R2 Standard bucket for temporary media. Configure bucket-scoped S3 credentials on the Django server in Vercel and the local Django Compose service, with matching non-secret account/endpoint/bucket settings. Neither the companion nor the browser gets long-lived keys. Include a verified deployment smoke test and an expiry cleanup job with a bucket lifecycle backstop in this same spec. The account owner supplies the Cloudflare account and creates/authorizes the bucket-scoped token; no secret value goes in Git.

The Draft assumes reconciliation begins when the application opens or reconnects on that computer. Already-started jobs continue after its tabs close. This does not promise discovery of newly shared files while the app has never been opened on that computer. Files used by a service dated today or later cannot be deleted locally. Undated and past-service files may be deleted; undated services require manual download. Failed automatic downloads keep retrying with bounded backoff while the source is online and the service remains eligible. These consequences are explicit review points for the owner.

## TDD

- Domain/app tests: identity/deduplication, authorization and expiry, single-request failure, transfer persistence and recovery, verified atomic download, date eligibility and ordering.
- E2E: Media Library Share/Cancel/Online, transfer modal and sidebar session transitions, Tata Ibadah automatic/manual download and status across light/dark and narrow layouts.

## Risks

- A single 200 MB request cannot resume after a signed URL expires or the companion process stops. Show failure and let the operator start a new upload from zero.
- Cloud metadata and actual R2 object state can diverge. Never mark online until upload completion is verified; treat expired or missing objects as unavailable.
- Local companion can continue known jobs without a tab, but newly discovered service references need an app reconciliation trigger unless a separate authenticated background poller is designed.
- The seven-day cutoff must be enforced in metadata/read authorization even if provider-side physical deletion is delayed.
