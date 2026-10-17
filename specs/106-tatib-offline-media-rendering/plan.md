# Plan 106: Keep media entries visible in saved Tata Ibadah pages

- **Status:** Accepted (2026-10-17)
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-106
- **Bump:** patch

## Why

Opening a Tata Ibadah through the main menu can use the browser's saved-page renderer. That
renderer currently drops media-specific entry metadata and only renders the four older add
actions. As a result, media entries lose their type icon and the `+ Media` / `Add Media`
actions, even though a full refresh shows them. The saved and server-rendered paths should
show the same service-entry controls and file identity.

## Scope / edges

**In:**

- Carry the media entry kind, fingerprint, and file family through the offline service chunk.
- Render the same media icon and file identity as the Django Tata Ibadah page when the saved
  renderer opens a service.
- Include `+ Media` in the add rows and `Add Media` in the empty-service actions when editing is
  enabled in the saved shell.
- Preserve the existing local-library unavailable/missing distinction after in-place navigation.

**Out:**

- Media upload, storage, fingerprint, or recovery behavior.
- Media preview or projector rendering.
- Changes to the service-entry design or to other entry types.
- Changing whether editing is available offline or changing save behavior.

## Approach

Use the existing Tata Ibadah template as the rendering contract. Include only the media
metadata needed to reproduce that view in the public offline service chunk; never include file
bytes. Extend the saved renderer to emit the media row attributes/icon and media add actions,
then let the existing `media-stage.js` availability check update the icon state on `shell:page`.
Keep the offline chunk revision tied to the newly serialized metadata so saved copies refresh.

## TDD

- Domain/app tests: `tests/test_offline_sync.py` for media metadata in a service chunk.
- E2E: `tests/e2e/test_offline_library.py` for in-place navigation to a service with media and
  an empty service, verifying parity with direct server rendering.

## Risks

- A stale saved chunk must be replaced after the serialized shape changes; verify its revision
  changes and the offline sync fetches the updated payload.
- The offline chunk is public reading data. Include only the existing media reference metadata,
  never the local file bytes or companion credentials.
