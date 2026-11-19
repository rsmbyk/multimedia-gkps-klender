# Research: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md` (Accepted, Gate 1 2026-11-18)
**Unknowns remaining**: 0

## D001 — Where the following mode lives

- **Decision**: one page-memory variable in `static/web/obs-dock.js`, `following = true` on load.
  It is neither written to `gkps-display` nor broadcast nor persisted.
- **Rationale**: FR-011 fixes the initial state; the mode is an operator's relationship with this
  dock's list, not a fact about what is on air. The display record is read by the projector and
  overlay, which have no list and no use for the flag; every surface restoring state from storage
  shouldn't inherit a dock-local UI choice.
- **Alternatives considered**: a field in `gkps-display` (makes three surfaces parse a value they
  ignore, and forces a writer for every mode change); `localStorage` (needs session semantics like
  spec 184's stamp and makes a reload inherit "browsing", contradicting FR-011).
- **Provenance**: research — `obs-dock.js` `dock = {…}` is already page-memory; `display.js:101`
  `write()` is the only state writer and all three surfaces share the record.

## D002 — How an advance is recognised without tagging every writer

- **Decision**: `sync(state)` keeps the previous `{service, screen, goto}` in page memory. It treats
  a notice as an **advance** iff `service` is unchanged, `goto` is unchanged (and null), and
  `screen` changed. On an advance it calls `scheduleCenter()` **only when `following`**. The first
  sync after load has no previous record and centres nothing (FR-011, FR-014).
- **Rationale**: this is the only discriminator that covers both the dock's own writers and an
  advance made in another window, while excluding every FR-014 event: `hide`/resume keeps `screen`,
  a re-read keeps `screen`, a reload starts fresh, opening a service changes `service`, a go to
  changes `goto`, and closing a layer writes nothing.
- **Alternatives considered**: a transient flag set at each of the ~17 projection call sites
  (misses external advances and drifts as call sites are added); centre on every notice while
  following (reintroduces the display-switch and re-read centring the owner asked to remove).
- **Provenance**: research — `step()`/`stepUnit()`/`projectScreen()` all converge on `gkpsDisplay.screen`
  or `.show`, and `gkpsDisplay.subscribe(sync)` at `obs-dock.js:1831` is the single fan-in.

## D003 — The crossing morph must be able to run without the scroll

- **Decision**: `startMorph(out, in, node, outEffectiveOpen, carry)` gains a fifth argument. When
  `carry` is true (following) it drives `scrollTop` from the arriving row's live layout position on
  the same 230 ms `easeInOut` curve, as today. When false (browsing) it animates only the two block
  heights. `morphState` records `carry`, and `finishMorph()` calls `centerRow(node)` only when the
  morph carried the scroll. D002's glide is skipped while a morph owns the blocks.
- **Rationale**: today `startMorph` always scrolls and `finishMorph` always re-centres
  (`obs-dock.js:707`); without a guard, a key-driven crossing would move the list in browsing mode,
  breaking FR-006. Keeping one morph avoids two competing height animations on the same `.entryinner`.
- **Alternatives considered**: skip `startMorph` entirely in browsing (then a crossing's block
  heights pop, reintroducing the two-phase look the owner rejected); animate scroll separately
  (a second motion, and the capture/inert ownership in `finishMorph` would be wrong).
- **Provenance**: research — `startMorph` at `:640`, `finishMorph` at `:690`, call at `:1268`.

## D004 — The 15 s clock and what restarts it

- **Decision**: a single ~100 ms `setInterval` with `lastActivity` and a `holding` flag. Listeners
  on `wheel`, `pointerdown`, `pointerup`, `pointercancel` and `keydown` at document level mark
  activity; a still or moving pointer with no button down marks nothing. While `holding`, each tick
  refreshes `lastActivity`. Conditions are read again at the tick where the threshold crosses, and
  a successful centre sets `following = true` and restarts the count.
- **Rationale**: matches the narrowed clock rule and makes FR-008's "read at fire time" literal;
  the interval also gives the same place to re-check FR-007's six conditions without another timer.
- **Alternatives considered**: a `setTimeout` reset on each event (a held press would still time
  out unless separately tracked, and the conditions would be read when armed); `pointermove`
  (explicitly rejected by the owner).
- **Provenance**: owner decision — "mouse activities to only scrolls and clicks (including holding
  down the buttons such as dragging)"; accepted preview `preview/preview.js` implements the same
  clock and its probe verifies it.

## D005 — What ends following

- **Decision**: `wheel` on `runBody` and `toggleBlock()` opening a **non-live** entry's block set
  `following = false`. A `sync()`-driven repaint never does.
- **Rationale**: the owner's exact rule — "scrolling and expanding another entries exits the
  following mode". The live header is already inert as a toggle (spec 198 R14), so "another entry"
  needs no extra test. A repaint during a crossing must not end following, or every advance would
  drop out of the mode it just used.
- **Alternatives considered**: any `aria-expanded` change (would fire on the live hand-off);
  any click in the list (an item click is a re-entry, so it would cancel itself).
- **Provenance**: owner decision (2026-11-18) + `runBody` wheel listener at `:781`, `toggleBlock`
  at `:764`.

## D006 — The sticky Next band is already the next entry

- **Decision**: keep `projectScreen(Number(nextBand.dataset.screen))` in the `entryList` click
  handler. `updateBand()` sets that dataset to `next.start` of the first non-divider entry after the
  live one, so the pointer jump and the first-row mark come from existing code. Add only
  `following = true` on that path. Transport Next/Back continue through `step()` and touch no mode.
- **Rationale**: the owner's correction — "the sticky next band … also jumps the pointer to the next
  entry"; the transport buttons "keep whatever the current following mode". No new projection path.
- **Alternatives considered**: a separate band handler (would duplicate `focusPanel()` and risk a
  second write); advancing one *screen* (the band names the next entry, not the next lyric).
- **Provenance**: owner correction + `updateBand()` at `:786`, click handler at `:1330`.

## D007 — Cancelling a glide is independent of the mode

- **Decision**: `cancelPendingCenter()` keeps cancelling `glideFrame` on `wheel`/`pointerdown` but
  never writes `following`. D005's wheel listener is a separate listener on the same event.
- **Rationale**: FR-010 requires a hand on the list to win; FR-012 requires that same hand to end
  following. Two concerns, one event — not one listener doing both jobs.
- **Alternatives considered**: fold both into `cancelPendingCenter` (couples glide cancellation to
  the mode and would run on programmatic calls to `cancelPendingCenter` from `startMorph`).
- **Provenance**: research — `:774–782`.

## D008 — Geometry and scroll invariants are untouched

- **Decision**: keep `overflow-anchor: none` on `.dock__body`, the same-frame scroll clamp in
  `sync()`, `layoutTop()`'s non-sticky-parent rule, the 190 ms quadratic ease-out glide, the 230 ms morph, and
  the reduced-motion instant branches. The new control adds no CSS: `.navbtn` at 40 × 40, radius
  10, 17 px SVG and stroke 1.8 already produce the gate-1 numbers.
- **Rationale**: the accepted preview measured those numbers from the real stylesheet; changing
  them would invalidate `## UI/UX` after gate 1 (SDD-26 forbids a spec growing after Accept).
- **Alternatives considered**: a custom `centrebtn` class (a second design language, and a new
  set of numbers to approve).
- **Provenance**: gate-1 preview probe + `obs-dock.css` `.navbtn` at `:741`, `.dock__body` at `:209`.

## D009 — The control's disabled state and go-to target

- **Decision**: `centreBtn.disabled = !liveRowExists` painted in `sync()`. `liveNode()` is extended
  to fall back to `#offBody .offrow[aria-current="true"]` when `entryList` has no live screen row,
  so US1/AC5's go-to case centres the go to's marked row.
- **Rationale**: the control has no meaning when nothing is live, and a go to replaces the service
  rows with its own block but still has a marked row to centre.
- **Alternatives considered**: disabling the control during a go to (rejected by US1/AC5); using
  `dock.stops` (page-memory, not the painted mark).
- **Provenance**: spec US1/AC4–AC5; `liveNode()` at `:612`, `offBody` build at `:1048`.

## D010 — Verification lanes

- **Decision**: one new Playwright E2E file `tests/e2e/test_obs_dock_follow.py` (Django
  `StaticLiveServerTestCase`, fixtures in `setUp`, ORM assertions after the browser closes), plus
  two inspection items on markup/styles and three manual checks in `quickstart.md`. The idle test
  waits the real 15 s; no production timing hook is added (the `?idle=` override lives only in the
  static preview).
- **Rationale**: mode transitions and scroll positions are observable only in a browser; a test
  hook would verify the hook rather than the dock (spec 198 D011's same reasoning).
- **Alternatives considered**: unit-testing a pure `shouldCentre(state, prev)` helper (would cover
  D002's arithmetic but not the mode transitions, and requires extracting code solely for the test);
  a shortened production clock via query string (a back door in shipped code).
- **Provenance**: repo TDD deviation — user-visible acceptance is Playwright E2E; existing dock
  suites under `tests/e2e/`.

## Open

None.
