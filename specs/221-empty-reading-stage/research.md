# Research: an empty reading stage after deleting the open record

**Spec**: `specs/221-empty-reading-stage/spec.md` (Accepted, Gate 1 2026-11-22)
**Date**: 2026-11-22 · **Unknowns remaining: 0**

## Decisions

### D001 — Carry the state as `?stage=empty` on the parent list

- **Decision**: the post-delete URL is the existing parent list with `stage=empty` appended as a query
  parameter (`/songs/book/36/?stage=empty`, `/songs/?stage=empty`, `/tatib/?stage=empty` and
  `/tatib/?mode=template&stage=empty`). The flag is appended only when the deleted record was on stage.
- **Rationale**: the parent list is already the accepted destination (R41); a query flag makes the
  state reloadable, visible in `history`, and clearable by the ordinary links on the lists. `?mode=`
  is already used this way on `/tatib/`, so no new routing grammar is introduced.
- **Alternatives**: a dedicated route (a new URL and template for a pure render state); a
  `sessionStorage` flag (survives reload but not a fresh tab, and is invisible to Back); client-only
  DOM surgery (a reload would fall back to the search landing, which is the reported defect).
- **Provenance**: owner request plus the served reproduction; existing `?mode=template` precedent in
  `multimedia/web/templates/reading/tatib.html` and `static/web/reading.js`.

### D002 — One view helper decides the empty render; no new route or endpoint

- **Decision**: a module-level predicate in `multimedia/web/reading/views.py` reads
  `request.GET.get('stage') == 'empty'`. `BookIndexView`, `BookDetailView` and `TatibView` pass that
  boolean to `_shell()` as `read_on` and choose `home_state` `'reading'` instead of `'landing'`, and
  add `read_name` / `read_hint` context. Existing `ch` and `nav` values stay as they are.
- **Rationale**: the three views are exactly the parent lists the delete flow can land on; the server
  owns the render state, so a fresh load and an in-page arrival receive the same markup.
- **Alternatives**: a new view/URL per parent list (extra routes for one boolean); deciding it in JS
  (would break reload); adding a field to a record (state belongs to the page, not the model).
- **Provenance**: `multimedia/web/reading/views.py:2350–2512` (the three views) and `:98` (`_shell()`).

### D003 — The copy is rendered by the base template, after the child's `read_body` block

- **Decision**: `reading/base.html` suppresses the reading header when `read_hint` is set and
  renders the empty song view's `.entry__empty` block inside `#readBody`: the owner-selected 38px
  empty-screen glyph above `.entry__empty-title` "Nothing open." and `.entry__empty-hint` with the
  subtitle. One new `.entry__empty-icon` rule sizes the glyph; the other classes already exist.
- **Rationale**: appending after the block means the three list templates need no edits and a child's
  own body (Tata Ibadah items) is unaffected; those templates render nothing when no record is open.
- **Alternatives**: a new `reading/empty.html` partial included by each view (extra file and context);
  a bespoke empty-state component with new type rules (unnecessary — the empty song view already gives
  the approved type, and only the icon needs a size rule).
- **Provenance**: `multimedia/web/templates/reading/base.html:443–455`, `components.css:1127`, `:1498`;
  Gate 1 revision and its recorded wording assumption.

### D004 — The delete flow only adds the flag when the record was on stage

- **Decision**: in `static/web/editors.js`, `submitDelete()` computes `wasOnStage(kind, id)` first;
  when true, `parentListUrl(kind)` is extended with `stage=empty` (using `?` or `&` according to
  whether the URL already has a query) and passed to `window.gkpsNavigate(url, {kind:'refresh',
  replaceUrl:true})` as today. Off-stage deletes keep their `shell:sidebar-delete` path and URL.
- **Rationale**: one branch already distinguishes the two cases; the history replacement and the list
  refresh are already correct there.
- **Alternatives**: always appending the flag (ordinary list refreshes would turn into reading
  states); replacing the navigation with `location.href` (a full reload loses the shell's in-place
  transition and focus behaviour).
- **Provenance**: `static/web/editors.js:305–364`, `static/web/reading.js:1482–1530, 1672–1693`.

### D005 — The shell's existing stage reconciliation paints the new state

- **Decision**: no stage-specific JS. `applyPage()` already copies `data-read`, `data-home` and the
  whole `.stage` subtree from the fetched document and calls `refreshStageRefs()`, so the server's
  title and hint arrive with the swap.
- **Rationale**: the preview toggles exactly those two attributes and gets the approved pixels; no
  second source of stage copy is introduced.
- **Alternatives**: setting `#readName`/`#readBody` in JS (duplication and a stale state on reload).
- **Provenance**: `static/web/reading.js:1672–1693, 1824–1841`; `specs/221-empty-reading-stage/preview/index.html`.

### D006 — The empty stage reports nothing on stage

- **Decision**: the empty render leaves `read_kind` unset, so `readKind()` returns `''`,
  `stageSection()` returns `null`, and `gkpsStage()` reports no section, tile or song. The URL in
  `stageInfo` updates through the normal `applyPage()` path.
- **Rationale**: a subsequent delete must not be mistaken for an on-stage delete, and the idle
  collapse timer must not run against a stage that holds no record.
- **Alternatives**: copying the deleted record's `data-kind` (would make the shell claim a record is
  still on stage and misroute the next delete).
- **Provenance**: `static/web/reading.js:89–100, 1832–1836, 2113–2118`.

### D007 — Verification is Playwright E2E plus inspection

- **Decision**: one new E2E module, `tests/e2e/test_deleted_stage.py`, with `StaticLiveServerTestCase`,
  the repo's `STATICFILES_STORAGE` override and Playwright skip pattern. Tests cover the song,
  service, template and songbook deletes, reload/history, off-stage deletes and the measured geometry.
  Refused-delete and R41's superseded clause are verified by inspection.
- **Rationale**: repo TDD convention makes user-visible acceptance a Playwright E2E; endpoint guards
  and unchanged shell behaviour already have coverage elsewhere.
- **Alternatives**: unit-testing the view predicate (would not prove the stage swap or the URL).
- **Provenance**: `docs/PROCESS.md` TDD repo block; `tests/e2e/test_editor.py:1–70`; spec 220's plan.

### D008 — Bump: patch

- **Decision**: declare `bump: patch`; apply `VERSION` `1.36.6 → 1.36.7` and one `### Fixed` line in
  the pre-merge commit, never before.
- **Rationale**: a bug fix with no interface or data change.
- **Alternatives**: none (minor/major would claim an API or feature change).
- **Provenance**: `VERSION`, `CHANGELOG.md`, C-SDD-VER.
