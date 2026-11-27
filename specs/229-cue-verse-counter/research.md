# Research: A passage cue carries its current and end verse

**Spec**: `specs/229-cue-verse-counter/spec.md`
**Unknowns remaining**: 0

## D001 — Where the service passage's two numbers come from

- **Decision**: add `verse_start` and `verse_end` to the projector's scripture **entry**, and a
  `verse` field to each scripture **screen**; read `screen.verse` for the current number and
  `entry.verse_end` (falling back to `verse_start`) for the end.
- **Rationale**: both values already exist on the `ServiceEntry` row and in the loop that builds
  `_scripture_screens()`. Parsing `Matius 5:3` out of a rendered header would break on a verse
  title (headers are `reference\ntitle`) and on a missing translation, where there is no header.
- **Alternatives considered**: parse the header text in JS (fragile, rejected); add a second
  endpoint for the range (new interface for data already in the payload, rejected).
- **Provenance**: research — `multimedia/web/reading/views.py:1707–1735, 1782–1801`.

## D002 — Where the Go To chapter's last verse comes from

- **Decision**: read the last `verses[].n` of the edition in use (`detour.translation`, then `TB`,
  then the first edition) from the `editions` map already held in the detour.
- **Rationale**: the chapter payload carries every verse of every edition, so the end number
  follows a chapter crossing, an edition flip and a local step without a fetch. Using the
  displayed edition keeps the count consistent with what is on the stage when editions differ.
- **Alternatives considered**: use the Go To index's chapter verse count (a different source
  that could disagree with the loaded chapter, rejected); store a new state field (rejected —
  the detour already holds the data).
- **Provenance**: research — `static/web/projector-library.js:250–285`,
  `multimedia/web/reading/goto.py:90–116`.

## D003 — How the counter sits in the existing cue without moving anything

- **Decision**: append a `<span class="cue-verse">n/n</span>` **inside** the existing label span,
  with the same `' · '` text separators the reference and flip already use. No new flex child, no
  CSS rule and no new control.
- **Rationale**: `#cue-prefix` is `display: inline-flex` with `gap: .2em`; a third flex child would
  add a second gap and change the measured box that 24px-band tests pin. Keeping the counter in
  the label preserves the existing spacing exactly and gives E2E a stable selector.
- **Alternatives considered**: a sibling span (changes the gap, rejected); plain text alone
  (unselectable for read-back, rejected); a CSS `::after` (cannot take live data, rejected).
- **Provenance**: research + gate-1 owner decision — `static/styles/design/projector.css:350–364`,
  `specs/229-cue-verse-counter/spec.md` `## UI/UX`.

## D004 — Test lanes

- **Decision**: one Django unit test for the payload fields in `multimedia/web/tests.py`; service
  cue E2E in `tests/e2e/test_projector.py`; Go To cue E2E in `tests/e2e/test_goto_shared_state.py`.
- **Rationale**: the payload is server-rendered and testable without a browser; the two cue paths
  are owned by the two E2E modules that already build their fixtures and drive the real render.
- **Alternatives considered**: a JS unit runner (none installed, rejected); a new E2E module
  (duplicates two fixtures, rejected).
- **Provenance**: research — `multimedia/web/tests.py:2819`, `tests/e2e/test_projector.py:82`,
  `tests/e2e/test_goto_shared_state.py:48`.

## Open

<!-- empty when Phase 0 is finished; anything here blocks Phase 1 -->
