# Research: Back clears the Go To from the cue over an empty stage

## Decisions

### D001 — Clear in `renderCue()`, not in a caller

The three ways out of a Go To over zero screens all call `renderCue()`: `leaveDetour()` → `render()`,
the dock's Back → the `{type:'goto'}` message → `applyGoto()` → `paintIdle()` (no service) or
`render()` (empty service), and `rereadSession()` → `paintIdle()`. Clearing in any one caller would
miss the others; the empty branch of the dispatcher sees all of them.

**Rationale**: one place owns the cue's DOM, so one place owns its reset.

**Alternatives**: clear in `leaveDetour()` (rejected — misses dock Back and idle re-read); clear in
`paintIdle()` (rejected — misses `render()` when the service id is still set).

### D002 — Reset the whole Go To part of the cue, not just the label

`renderDetourCue()` writes five places: `#cue-prefix`, `#cue-baits`, `#cue-progress`, `#cue-next`'s
`on`/arrow classes and `#cue-next-name`. Emptying only the prefix would leave clickable baits and a
`back to service` button for a Go To that no longer exists.

**Rationale**: the empty state is the template's original cue — separator only.

**Alternatives**: remove the cue element (rejected — it is the operator's service-entries button and
shortcuts surface too); hide the whole cue (rejected — the popup sheet's open rules depend on it).

### D003 — Pin both Back origins plus the pre-Go To state

Three E2E cases: projector Back with no service, projector Back over an empty service, dock Back
with no service. Each asserts no label, no flip, no baits, no Back text and `#cue-next` hidden.

**Rationale**: the finding covers both empty situations and both control surfaces.

**Alternatives**: a single combined test (rejected — one behaviour per case, and the two fixtures
differ in which path through `applyGoto()` they take).

### D004 — Reuse the empty notice as the single idle-state marker

`syncEmptyNotice()` already computes whether the stage holds nothing and no detour is up. It now
toggles an `empty-stage` body class there; CSS hides `.cue-separator` and disables `.mouse-zones` on
that class. A Go To clears the class while it paints, so its spec 227 cue is untouched.

**Rationale**: one source of truth; no second listener, no duplicated screen count.

**Alternatives**: a separate `render()` branch (rejected — `syncEmptyNotice()` runs after adopt,
re-read and detour changes too); a class set from the dock channel (rejected — the projector owns
its own stage).

### D005 — Disable the zones, not the screen or the cue's buttons

`pointer-events: none` on `.mouse-zones` removes the previous/next/hide/show cursor icons and their
clicks, while the fullscreen capture listener still sees `#projectorScreen` underneath. The cue's
service-list button, `.keys` and find band are deliberately left alone. `revealCursor()` returns
early while `empty-stage` holds and `syncEmptyNotice()` clears any pending `cursor-hidden` class,
so the pointer stays visible with its normal cursor.

**Rationale**: the owner wanted every phantom mouse function gone except fullscreen, with the
projector's own controls still reachable.

**Alternatives**: hide the whole HUD (rejected — it would remove the buttons he asked to keep);
`cursor: none` overrides (rejected — they would also mask the fullscreen cursor).

### D006 — `[hidden]` needs an author rule for the next button

The UA's `[hidden] { display: none }` loses to the author's `.cue-next { display: inline-flex }`, so
setting `cueNext.hidden = true` left the button — and its lone 12.8 × 12.8 right-arrow icon — painted.
One `.cue-next[hidden] { display: none; }` rule fixes it everywhere the next control is hidden, not
just in the empty state, and mirrors the existing `.cue-baits[hidden]` rule.

**Rationale**: the attribute is the state; CSS must honour it.

**Alternatives**: remove the arrow node in `renderCue()` (rejected — the DOM contract stays and the
populated path needs the same button); inline style (rejected — duplicates the state in JS).

## Provenance

- `static/web/projector.js:909–930` — the detour branch and the empty return.
- `static/web/projector.js:1593–1601, 2052–2064` — `leaveDetour()` and `paintIdle()`.
- `tests/e2e/test_goto_shared_state.py` — the spec 227 fixtures and the shared-state seam.
- Red run: 3 failures, each `AssertionError: '<label>' != ''` with `goto: null` and no detour.
  Green run: 28 tests in the two goto modules, `OK` in 100.736s. Live probe: after Back the cue
  reads `·`, prefix empty, zero baits, `backHidden: true`.
- Revision red run: 3 cases, four failures — cue text `· != ''` (both empty situations), zone
  `pointerEvents: auto != none`, `cursor-hidden` present. Green after the HUD change: 3 cases in
  9.746s. Loaded lane of 39 tests: 38 pass; `test_quiet_controls_support_keyboard_and_mouse_jumps`
  fails identically on unmodified `develop` (33 tests, same assertion), so it is a pre-existing
  load-sensitive case, not a regression.
- Live HUD probe at 8765 (1280×800): `innerText ''`, separator `display: none`, zone
  `pointerEvents: none`, `cursor-hidden false`, body cursor `auto`, keys and service button
  `pointerEvents: auto`, fullscreen entered on click.
