# Spec: Local Media Library and service media entries

- **ID:** 103
- **Status:** Accepted amendment (2026-10-17)
- **Item:** ITEM-103
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Previews:** [Media Library](./preview-library.html), [media entry form](./preview-entry.html)
- **Bump:** minor

## Intent

Let operators attach a locally stored file to a Tata Ibadah once and use that same computer-level library from the web page and OBS dock. A service entry retains its file identity even when the file is absent on the current computer. This slice establishes storage, references, and operator visibility; it does not show file contents in Preview or on the projector.

## Scope

### In scope

- A local companion running in the existing Docker Compose stack, with media bytes and per-computer settings stored in a Docker-managed named volume on Windows, macOS, and Linux Docker hosts.
- Service media entries for images, audio, video, PDF, and PowerPoint (`.ppt`, `.pptx`).
- Upload from the service-entry Create form, or link a file already in the local Media Library.
- A top-level Media Library page for viewing local files, usage, missing/unused state, manual removal, and retention settings.
- A service-stage label and icon for each media entry, with a danger-color missing-file icon when its bytes are absent locally.
- Blank media-content behavior in the existing Preview and projector flows.

### Out of scope

- Cloud sharing, R2, download/sync between computers, cloud expiration, and recovery workflows.
- Binary playback or rendering of any media type in Preview, projector, or OBS.
- Changing an existing service entry's file, importing by URL, or storing binary files in Vercel Functions or deployment storage.

## Data and identity rules

- The server stores a media identity and metadata: SHA-256 of the complete bytes, byte count, detected family, and a display filename. It stores no binary payload in production. A service media entry refers to that identity and records the library filename chosen for that entry. A filename is not an identity key.
- The local companion indexes files by the same SHA-256. Adding identical bytes under a different name reuses one local copy and one Media Library row; the existing row keeps its original local filename and upload date. The new service entry uses that existing library filename, not the name of the duplicate upload. A local copy satisfies an entry only when its complete hash matches.
- Different byte content may have the same filename. It produces separate local rows and identities; importing a newer file with the same name never overwrites an earlier file. The library keeps both rows, distinguished by their size, upload date, and service uses.
- A Media service-entry kind is distinct from Text, Passage, Song, and Section break. Its detected family is Image, Audio, Video, PDF, or PowerPoint. One media entry has exactly one file reference and an optional title. Its title is limited by the current service-entry title length; if blank, the saved entry filename is shown as its heading.
- After creation, Edit changes only the title. The file identity, detected type, and saved filename are read-only. To use different bytes, create a new media entry and optionally delete the old entry.
- Deleting an entry does not delete local bytes. Removing bytes from the local library does not delete or rewrite any service entry. When the entry is opened on a computer without the matching bytes, it is missing *on that computer*.
- The maximum imported file size is 200 MB (200,000,000 bytes), applied before copying and checked again by the companion. Empty, unsupported, malformed, or unverifiable files are rejected without changing the current selection or creating a service entry.
- The content, not the filename extension or browser MIME report, determines image/audio/video/PDF/PowerPoint classification. A PDF named `.png` remains a PDF. The implementation must validate enough structure to distinguish PPT/PPTX from unrelated OLE/ZIP files and identify supported audio/video containers. The companion is authoritative; the browser may precheck for feedback.
- Imports use an atomic temporary write, hash/validation, then a verified move into the library. Failed or interrupted imports leave no visible library record or service entry. A name with path separators cannot escape the library folder.

## Local companion and connection

- The companion runs as a service in the existing Docker Compose stack. A named Docker volume stores both media bytes and the SQLite index at a fixed container path. The volume is local to the Docker host and shared by the app's browser contexts on that same computer. A service page opened on another computer correctly reports missing local bytes until that computer has its own copy.
- The companion's data root is the named volume mount; there is no OS-specific host path, bind mount, folder picker, or folder-location display. The local status response omits the container path. Operators manage files through the Media Library UI. Removing the named volume removes the local library; ordinary container recreation and `docker compose down`/`up` retain it.
- The browser calls `http://127.0.0.1:63174`. This replaces the previous `47863` endpoint; companion API paths and payloads remain unchanged. The companion listens on its container interface, and Compose publishes the port only on host loopback (`127.0.0.1:63174:63174`). The browser does not connect to the Compose service name. The local interface must authorize writes, restrict allowed web origins to exact configured origins, reject path traversal or arbitrary local-file requests, and only read verified library identities.
- The operator sets `GKPS_MEDIA_PRODUCTION_ORIGIN` in the project-root `.env` on each projector computer. This is the production app's exact scheme and host, without a path or trailing slash; it is local Compose configuration, not a Vercel environment variable. Compose combines it with `http://localhost:<WEB_PORT>` and `http://127.0.0.1:<WEB_PORT>`, where `<WEB_PORT>` is the effective Compose web port (default `63404`), and passes all three exact origins to the companion as `GKPS_MEDIA_ALLOWED_ORIGINS`. A missing or invalid production origin prevents the companion from starting; it must not fall back to a permissive origin.
- The companion service uses a restart policy so it returns when Docker starts after login. This assumes Docker Desktop / Engine itself is configured to start at login. A manually stopped/removed Compose service does not start until the operator runs `docker compose up` again.
- When the companion is unavailable, the status indicator is unavailable, local files cannot be imported/read/removed, and every media service entry shows `Local library unavailable` beside its saved type/filename label. Its type icon uses a muted color; even a previously missing entry does not use the danger icon until the companion reconnects and confirms absence. Existing text, song, and passage operations remain usable.
- The connected status popup reports connection, local file count, and total local byte size; it does not reveal the Docker volume path. It does not label a file "missing" merely because the helper is disconnected.
- When disconnected, the status popup keeps its heading and shows `Connection — Unavailable`. It hides the file count and total size, including any cached values.

## Create, edit, and missing rules

- The existing Tata Ibadah insertion surfaces add `+ Media` at the start, after an item, and in an empty service. Create uses the approved large modal: Upload and Media Library tabs, Upload first, date-grouped Media Library rows, no search in the picker, optional entry title, and Save/Cancel footer.
- Upload accepts one dropped file or one system-picked file. A selected upload replaces the drop prompt with detected type, name, size, and a button to choose another file. File failures appear in a custom dialog; the prior valid selection remains. The supported families and 200 MB limit are listed inside the empty drop area.
- The system file picker requests a filter for supported image, audio, video, PDF, PPT, and PPTX extensions. This is a browsing aid only: drag-and-drop and any file selectable through an OS `All files` option still go through content-signature inspection and the same validation rules. A misleading extension does not determine the detected family.
- After inspecting a valid upload, the companion checks its complete fingerprint against the local library. On a match, the selected-file area shows `Already in Media Library` and the existing library filename before Save. Saving reuses that row and uses the existing filename for the new entry's saved filename and untitled heading. No duplicate bytes or row are added.
- A Media Library row is selectable. Its selection and scroll position persist when switching tabs. The Upload tab has its own selection. Save is enabled only if the visible tab has a valid selection and uses that selection. No binary import occurs merely by browsing or switching tabs.
- Create persists the local import (if any) and server reference as one recoverable workflow. If local import succeeds but server save fails, the local file remains available for a retry or later reuse; there is no incomplete service entry.
- Edit opens a compact modal with title editing and a read-only file reference/status. It never offers a different file picker or replacement upload. The existing delete-entry action remains available outside the edit form.
- If a file is missing and no recovery path is available, the operator can delete that entry or create a new one. Attaching a different file to an existing entry is not a recovery path. A later copy of the *same* bytes may satisfy the original reference by hash without editing the entry.
- Existing service-entry ordering, editing permissions, and deletion behavior continue to apply.

## Media Library rules

- A top-level **Media Library** main-sidebar item opens a read/manage page. Files are added from Tata Ibadah creation, not from the library page; there is no Add files control or drop zone on that page.
- The page lists only files stored by the companion on this computer. Each row shows a type icon, filename, detected family, size, upload date, and Tata Ibadah uses. A use displays service name/date and, where present, its entry title in muted text separated by a middle dot. Uses are sorted by service date newest first. Clicking one navigates to that Tata Ibadah and scrolls to the referenced entry.
- A file with no current Tata Ibadah references is styled with a subtle unused tint and displays its deletion countdown. It stays reusable until manually removed or cleanup runs. The file list can filter by multiple families and by Unused; it shows the displayed/total count.
- Sorting offers upload date newest (default), upload date oldest, file size largest, and file size smallest. Date sorts group files by local upload date, using long Indonesian month names as the Tata Ibadah header does. Size sorts are ungrouped. File row separators are softer than the filter-row divider.
- An icon-only danger Remove action opens a confirmation. Removing a local copy leaves all service entries and server metadata intact; those entries become missing on this computer when the companion is connected. The confirmation states this effect.
- The settings modal offers unused-file retention of 3, 7, 30 (default), 90 days, or unlimited, stored separately per computer. An unused file's timer begins when it first becomes unused; using it again cancels that timer. Changing to a shorter setting never deletes affected files immediately: if an unused file's previously shown remaining time exceeds the new limit, its deadline becomes tomorrow (today is its last day). Unlimited cancels pending cleanup.
- Automatic cleanup removes only local bytes whose unused deadline passed and only after a fresh, successful reconciliation of references against the service database. Offline or stale reference data defers cleanup. No service entry is deleted by cleanup.

## Stage, Preview, and projector

- The service stage shows a type icon, the optional entry title (or saved filename when untitled), and a lower label. For titled entries, the lower label is `Type · filename`; for untitled entries it is only `Type`. The supported type names are Image, Audio, Video, PDF, and PowerPoint. A locally missing file uses the missing-file icon in the danger color; no large row warning or badge is added.
- File content is not rendered in the media entry's Preview in this slice. The Preview control may omit content for that kind; it must not imply the file can be played or shown. No PPT/PPTX slide renderer is included.
- When a projector advances to a media entry, it clears the prior projected content and leaves the content region blank. It does not display an image, playback control, PDF, filename placeholder, or PowerPoint slide. Projector navigation and non-media entries continue to work. A missing file does not change this blank result.

## UI details

The two linked HTML previews are the visual source of truth. They are planning artifacts, not implementation. Preserve their current geometry and states unless the owner approves a revision.

- **Library page:** top-level rail icon; centered content column with 40 px desktop top padding and 28 px small-screen top padding; 29 px desktop heading; 42 px settings/status buttons at top right. Status button has a green/red 9 px dot and opens a right-aligned popup. The connected popup shows connection, file count, and total size, with no folder path. Settings opens a centered modal. Both close on backdrop/outside click and Escape and use short scale/fade transitions; reduced-motion mode removes these animations.
- **Library controls:** type chips are 12 px pill buttons; the Unused chip is separated by a centered dot. Result count and custom sort control share the filter row. Active chips use the accent fill. The sort popup matches app menu styling. Hover, focus-visible, active/selected, empty, disconnected, and disabled states match the preview in light/dark themes.
- **Library rows:** 42 px square type-icon area, file text, and vertically centered 36 px icon-only danger remove button. Each Tata Ibadah reference is a separate line. Unused rows have a soft tint. Group dates use long Indonesian month names; file metadata uses the same date format. The shared app scrollbar is 5 px with no stepper buttons where supported.
- **Entry Create:** modal width up to 840 px, viewport margins at least 16 px, height up to 760 px/viewport minus 36 px, with a scrollable file list. A centered 320 x 42 px two-choice switch sits below the title. Upload has a large dashed drop area; selected-file state replaces all prompt content. The optional title and Save/Cancel footer remain visible below the selection area. At <=650 px viewport width, modal width is viewport minus 20 px, horizontal padding is 18 px, and the drop area remains at least 220 px tall.
- **Entry Edit:** compact ~490 px modal with title field and read-only file summary. Missing status appears inside that summary without a replacement action. Entry stage icons are SVG, with a danger-color missing icon. New and Edit media dialogs use short scale/fade transitions when opening and closing, including Cancel, backdrop click, Escape, and Save; reduced-motion mode removes the transitions. Error dialog is content-height, <=410 px wide, and has no line above its action button.
- **Interaction states:** library file selection is outlined/accented; Upload hover changes the button fill; dragging over the drop area changes its border/fill; Save is disabled until the visible tab selects a valid file. Returning to a previously selected library file smoothly scrolls to and briefly highlights its row; reduced-motion mode jumps directly without animation. Focus-visible outlines remain present for controls.

## Acceptance scenarios

### Scenario: Add media from this computer

- **Given** a connected companion and a valid file no larger than 200 MB
- **When** an editor drops or selects it in `+ Media`, optionally names the entry, and saves
- **Then** one verified local copy exists, one service entry refers to its hash, and the stage shows the entry title or saved filename with its detected type.

### Scenario: Filename does not decide file type or identity

- **Given** a valid PDF renamed with a `.png` suffix
- **When** it is selected for a new media entry
- **Then** content inspection identifies it as PDF and the service reference uses its SHA-256, without treating the suffix as an image.

### Scenario: Reject invalid import

- **Given** an unsupported, malformed, empty, or over-200-MB file
- **When** it is dropped or selected
- **Then** a custom dialog explains the failure, no new local record or service entry is created, and any prior valid selection remains.

### Scenario: Reuse a local file

- **Given** a file already stored in the local library
- **When** it is selected in the Media Library tab and a new entry is saved
- **Then** no second byte copy is made and the new entry refers to the same hash.

### Scenario: Upload identical bytes again

- **Given** a local file already has a Media Library row
- **When** the operator uploads the same bytes under either the same or a different filename while creating another entry
- **Then** the selected-file area identifies the existing library filename before Save; the companion reuses the existing bytes and row without resetting its upload date, and the new entry refers to the same hash and uses that library filename.

### Scenario: Tabs retain their own state

- **Given** a library file is selected and the list is scrolled to it
- **When** the editor switches to Upload and then back
- **Then** the library file is still selected, the list moves to that row, and Save reflects only the currently visible tab's valid selection.

### Scenario: Edit cannot replace bytes

- **Given** an existing media entry
- **When** it is edited
- **Then** only its optional title can change; the file reference and saved filename remain unchanged and read-only.

### Scenario: Missing local copy

- **Given** a service entry exists but its hash is not stored on this connected computer
- **When** the Tata Ibadah is opened
- **Then** its stage entry uses the danger-color missing icon, its edit dialog reports the absence, and the entry remains in the service order. Removing the entry and creating a new one remain separate user actions.

### Scenario: Local library unavailable

- **Given** a service contains media entries, including one previously known to be missing
- **When** the local companion cannot be reached
- **Then** each entry retains its saved title, type, and filename, shows `Local library unavailable` in muted text, and uses its normal type icon without a missing-file danger state. The edit dialog reports that availability cannot be checked. Once reconnected, each entry returns to its verified available or missing state.

### Scenario: Companion starts with the local Compose stack

- **Given** Docker Compose is configured with the production and local app origins
- **When** the operator runs `docker compose up -d` on the projector computer
- **Then** the Django service, database, and media companion run together, and Chrome and the OBS dock can reach the companion at `http://127.0.0.1:63174`.

### Scenario: Media survives companion recreation

- **Given** files and the SQLite index are stored in the named media volume
- **When** the companion container is restarted or the Compose stack is brought down and up without `-v`
- **Then** the same files, filenames, hashes, and retention settings are still available.
- **And** removing the named volume with an explicit destructive volume-removal command removes that computer's local library.

### Scenario: Allowed production and both local loopback origins

- **Given** the companion is configured with the exact production origin and both local origins at the effective Compose web port
- **When** the Media Library is opened from `http://localhost:<WEB_PORT>` or `http://127.0.0.1:<WEB_PORT>`
- **Then** it can connect to the companion through host loopback.
- **And** a request from any unlisted origin is rejected.

### Scenario: Connected status does not expose Docker storage path

- **Given** the companion is connected
- **When** the operator opens the status popup
- **Then** it shows connection, file count, and total size without a folder-location row or container filesystem path.

### Scenario: Remove local bytes without removing references

- **Given** a local file is used by one or more Tata Ibadahs
- **When** the operator confirms its removal from Media Library
- **Then** the local bytes disappear, server entries remain, and those entries report missing on this connected computer.

### Scenario: Unused-file cleanup

- **Given** a file has no current Tata Ibadah references and the companion has freshly reconciled references
- **When** its configured unused deadline passes
- **Then** only the local file is removed. Changing to a shorter limit gives affected files through today; unavailable reference data prevents automatic deletion.

### Scenario: Media does not project yet

- **Given** a projector is showing a non-media service entry
- **When** navigation advances to a media entry
- **Then** the previous content is cleared and the projector content region is blank; navigation still works and a following non-media entry renders normally.

## Traceability

- Domain/app tests: `multimedia/tatib/tests.py` (media identity, immutable reference, blank projector screen), `multimedia/web/test_media.py` (metadata registration, entry save, reference inventory), and `multimedia/test_local_media.py` (deduplication, content inspection, verified reads, retention, configured root, and allowed origins).
- Compose tests: `tests/test_docker_compose.py` (companion service, named-volume mount, loopback-only port `63174`, restart policy, production origin, and both local loopback origins); companion/browser tests also verify that clients use `63174` consistently.
- E2E: `tests/e2e/test_media_library.py` (connected/disconnected library, picker state, duplicate upload, entry creation, missing state) and `tests/e2e/test_projector.py::ProjectorE2ETests.test_media_navigation_clears_projector_then_text_resumes`.
- Implementation: `multimedia/local_media.py`, `multimedia/tatib/models.py`, `multimedia/web/reading/{entries,views}.py`, `multimedia/web/templates/reading/{media_library,_entry_form,tatib,base}.html`, and `static/web/media-{entry,library,stage}.js`.
