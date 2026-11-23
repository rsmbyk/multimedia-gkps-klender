# Research: A song opened from the sidebar can edit its verses

**Spec**: `specs/230-song-verse-script-boot/spec.md`
**Unknowns remaining**: 0

## D001 — Which document boots `songs_verse.js`

- **Decision**: `reading/base.html`, once, through `{% static %}`, beside `reorder.js`.
- **Rationale**: the handler is delegated on `document`, so one execution at shell load serves
  every later swap. The live probe measured 0 script tags at `/` before and 1 after, and the
  dialog stayed closed; with the include in the shell, 1 tag at `/`, executed at 220–223ms in two
  runs, and the dialog opens after the same three clicks. Every other reading script is already
  booted here.
- **Alternatives considered**: re-executing the imported script on `shell:page` (needs a new
  loading path and a race with the swap); keeping the fragment include and calling an init
  function on the event (requires editing script internals, and there is no init to call);
  loading the script on first song arrival (adds a fetch to the click path). All lost to a
  single static include.
- **Provenance**: research — `applyPage` at `static/web/reading.js:1683` reconciles children;
  `reconcileChildren` at `:301` uses `document.importNode`, which does not execute scripts;
  `songs_verse.js:231` binds the click handler on `document`; `reading.js:1881` already dispatches
  `shell:page` for scripts that do need re-binding.

## D002 — Remove the fragment include rather than keep both

- **Decision**: delete the `<script src>` from `reading/song.html`.
- **Rationale**: a direct load would otherwise execute the file twice and bind two delegated
  click handlers; the E2E with the shell include alone shows one dialog and one editor request.
- **Alternatives considered**: keep the old tag as a fallback for cached pages — rejected
  because the file is static and versioned through the manifest, so there is no staleness case
  that a duplicate could cover.
- **Provenance**: research — the before tree already has a working direct load; the after tree
  must preserve it with exactly one script node.

## D003 — Verification shape

- **Decision**: Playwright E2E through `StaticLiveServerTestCase`; no new unit test.
- **Rationale**: the failure is produced by in-page navigation and script execution, neither of
  which a Django response test observes. The probe reproduces it on unmodified `develop` and
  passes on the slice; an E2E module keeps that evidence in the repo.
- **Alternatives considered**: a template assertion alone would test the include's presence,
  not that the button works; a JS unit test would need a DOM simulation of `reading.js` swaps.
- **Provenance**: research — repo custom in `docs/PROCESS.md` TDD scope; existing
  `tests/e2e/test_verse_modal_header.py` uses the same fixture pattern.

## D004 — Version level

- **Decision**: `patch` (1.36.15 → 1.36.16), applied at delivery, not now.
- **Rationale**: a behaviour fix under SemVer's `patch` mapping (VER-10); no interface change.
- **Alternatives considered**: `none` would hide a user-visible fix; `minor` would claim a new
  capability.
- **Provenance**: `docs/PROCESS.md` VER-03/VER-07/VER-10.

## Open

None. Phase 0 is complete; all decisions are settled.
