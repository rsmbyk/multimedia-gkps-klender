# Plan 103: Local Media Library and service media entries

- **Status:** Accepted by owner on 2026-10-17
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-103
- **Bump:** minor
- **Visual previews:** [Media Library](./preview-library.html), [media entry form](./preview-entry.html)

## Why

Operators prepare a Tata Ibadah on projector laptops and already keep its files on those computers. Vercel cannot serve as the durable local file folder. Chrome and the OBS browser dock have separate browser storage, so each browser storing its own upload would duplicate work. A computer-level library makes the same bytes available to both browser contexts, while the service order keeps durable references even when a particular computer lacks the file. The owner approved the linked UI previews on 2026-10-17 and requested no file-content preview or projector rendering in this slice.

## Assumptions for this Draft

- The local companion runs as a separate process on each operator computer, is maintained in this repository, and stores files in an ordinary computer folder outside browser storage. The web app remains deployed on Vercel.
- A media reference is identified by SHA-256 of the bytes; the filename is display metadata, not identity. This is a product contract to review, not a shipped schema.
- The supported families are image, audio, video, PDF, and PowerPoint (`.ppt` / `.pptx`), with 200 MB as the maximum individual file size. The inspected content determines the family even if the filename extension is misleading.
- "No projector display yet" means advancing to a media entry clears previous projected content and leaves the projector content area blank. Its navigation controls may remain.
- "No file preview yet" means a media entry does not render its binary contents in the existing Preview modal. The stage still shows the entry's title, file type, filename, and missing state.
- 102 is already allocated by a parallel feature branch; 103 is reserved for this Draft. Recheck the IDs and integration base before opening a PR.

## Scope / edges

**In:**

- A cross-platform local companion, computer folder, local manifest, status, content verification, safe file import, removal, and cleanup.
- One top-level Media Library page for inspecting local files, usage references, filters, sorting, status, and per-computer retention settings.
- One `+ Media` creation flow on Tata Ibadah with Upload and Media Library tabs. Create a service media entry for any supported family inferred from content.
- Immutable file reference on each entry; Edit changes only the optional entry title. Deleting an entry leaves its local file available for later reuse.
- Missing-file state when an entry's fingerprint is absent locally. Removing local bytes leaves service entries intact.
- The agreed blank Preview/projector behavior for media entries, while preserving existing non-media projection.

**Out:**

- R2 publishing, inter-computer downloads, cloud expiry, or automatic recovery from another computer.
- Rendering image/audio/video/PDF/PPT/PPTX contents in Preview or on the projector; OBS behavior.
- Editing or replacing an existing entry's file reference. A different file requires a new entry.
- Importing more than one file in one media entry, remote URL imports, and server-side persistent binary storage.

## Approach

1. Add a server-side media identity/metadata record and a service-entry reference. Preserve entry order and existing kinds. Keep the entry's original display filename so a local rename does not change the service label.
2. Add a small companion in this repository that binds only to loopback, owns a user-visible local folder and index, computes SHA-256 while importing, validates size and content, and exposes narrowly scoped status/list/import/read/remove operations to both Chrome and OBS dock on the same computer. It must not expose arbitrary filesystem paths or broad cross-origin write access.
3. Use the companion for file bodies. The Vercel-hosted Django app stores metadata and entry references only. A file chosen from the existing library is linked without copying it again. A new upload is copied into the local folder before the service entry is saved; failure leaves no service entry pointing at an unconfirmed import.
4. Render the Media Library and entry form from the approved previews, including the missing-file state, type/unused filters, grouped date ordering, sort controls, and one-click navigation to referencing entries.
5. Reconcile local files against current service references and apply the per-computer unused-file retention policy. When the reference inventory cannot be confirmed, defer automatic deletion rather than incorrectly deleting a used file.
6. Ensure media entries clear projector content and do not display file content in Preview. Existing service navigation and non-media rendering continue to work.

## TDD and UI checks

- Domain/app: focused tests in `multimedia/tatib/tests.py`, `multimedia/web/tests.py`, and a new companion test module for hash identity, type validation, import/reuse, missing references, and retention.
- Browser E2E: focused media-entry/library tests and targeted `tests/e2e/test_projector.py` cases for blank media screens and non-media continuity.
- Platform checks: the same companion protocol and path handling on Windows, macOS, and Linux; Chrome and OBS dock connect to one computer-level folder.

## Risks

- This is a two-process feature. Installing/starting the companion and connecting it safely from a Vercel page need a concrete, reviewable implementation design, especially origin checks and a user-facing disconnected state. Do not silently fall back to browser storage.
- Browser MIME types and filenames are insufficient to identify file contents; the preview's signature checks are illustrative, not production validators. Supported formats need robust validation and malformed-file tests.
- A cross-computer service reference can exist before the local bytes arrive. The application must not mistake "missing here" for deletion of the shared entry.
- Cleanup must not use a stale service-reference list during network loss. Manual removal and automatic cleanup are separate decisions.
- Other feature branches may advance `develop` before this Draft is accepted. Refresh numbering, board links, migration numbering, and code integration points before implementation.
