# Research: opening a service starts its entry blocks shut

**Spec**: `specs/204-dock-entry-open-reset/spec.md`
**Unknowns remaining**: 0

## D001 — The reset lives in `openService()`, the one explicit-open path

- **Decision**: clear `entryOverrides` at the top of `openService()`
  (`static/web/obs-dock.js:418`), before `dock.service` is reassigned and before
  `entryList.replaceChildren()` (`:435`) and `loadServiceData()` (`:438`).
- **Rationale**: `openService` has exactly three call sites, and all three are explicit opens —
  `openCursorRow()` (`:392`, the picker's `Enter`), the picker's click handler (`:1435`), and
  `resumeOnAir()` (`:2032`, the on-load open of the service on air). The re-read paths do not go
  through it: `refreshService()` (`:472`) and the 10 s timer (`:2013`) call `loadServiceData()`
  directly, so a clear placed in `openService` cannot reach them. Measured consequence: the
  preview's drafted rule leaves a hand-opened block open across a re-read (`[0, 6, 9]` before and
  after) and across a crossing (`[0, 6]`), while every open paints `[]`.
- **Alternatives considered**: clear in `renderList()` (`:321`) or `loadServiceData()` (`:442`) —
  rejected, both run on every re-read and would shut the operator's blocks every ten seconds,
  contradicting `dock/R13`. Clear on `setView('pick')` (Back) — rejected: the picker is also
  reached by a go-to ending (`sync()` `:1311`), and the open, not the exit, is the moment a
  different list is drawn; clearing at the exit would also leave the map stale for the go-to's
  own return to the runner.
- **Provenance**: research (code reading of every call site) + measurement
  (`preview/measurements-http.json`).

## D002 — Clear the map, do not key it by service

- **Decision**: keep `entryOverrides` a `Map<index, boolean>` and empty it on an open.
- **Rationale**: the request is "it should be reset", not "remembered per service". A
  `Map<serviceId, Map<index, boolean>>` would preserve each service's inspection state and show it
  again on re-open — the opposite of the accepted behaviour, and it would grow for the whole
  session. A composite string key without a clear has the same defect plus an unbounded map.
- **Alternatives considered**: per-service memory (rejected — contradicts US1-AC2); a generation
  counter compared at paint time (rejected — more state than the one `clear()` it replaces, with
  no observable difference).
- **Provenance**: owner decision at gate 1 (2026-11-19), on the drafted reading.

## D003 — The live entry needs no exception in the reset code

- **Decision**: no special case. `effectiveOpen(index)` (`:556`) asks `liveEntry()` (`:543`)
  first, and `liveEntry()` derives from the display state's service and screen against
  `dock.service` — never from the override map.
- **Rationale**: clearing the map therefore cannot collapse a live block, and a live entry's
  block is open in the service that is on air whether or not an override ever existed for it.
  Measured: with position 4 on air in service 155, opening 149 paints `[]` (nothing live there)
  and returning to 155 paints `[3]` with `live=[3]`, no chevron, `aria-current="true"`.
- **Alternatives considered**: re-record the live index as an override after the clear — rejected,
  it would make the block stay open after the entry stops being live, which is the leak in another
  form.
- **Provenance**: research (code reading) + measurement (`measurements-http.json`,
  `measurements-open-write.json`).

## D004 — No animation cancellation is added

- **Decision**: leave `morphState`, `toggleMorphs`, `glideFrame` and `centerFrame` untouched.
- **Rationale**: the slice changes which blocks stand open, not how an open animates. Across 10
  measured opens the new list carried 0 `.is-morph` frames, `scrollTop` never left 0, the stored
  display state was byte-identical and 0 channel messages were sent. A switch attempted 60 ms into
  a crossing moved the scroll no further (0 across 900 ms into a 27-entry list, three attempts).
  Those attempts could not confirm a morph was in flight — `is-morph` is absent when the departing
  block is live and the arriving block was hand-opened — so this is a no-regression observation,
  not a morph measurement, and it is recorded as such in the spec's edge cases.
- **Alternatives considered**: cancel every in-flight animation on open — rejected as unrequested
  work with no measured defect; Converge would type it `unrequested`. If a jolt is later measured,
  it is its own card.
- **Provenance**: research + measurement (`preview/probe_open_write.py`,
  `measurements-open-write.json`).

## D005 — A new targeted E2E module, red first on `develop`

- **Decision**: `tests/e2e/test_dock_open_reset.py`, following `test_obs_dock_follow.py`'s shape —
  `StaticLiveServerTestCase`, `@tag('e2e')`, `skipUnless(HAS_PLAYWRIGHT)`,
  `@override_settings(STATICFILES_STORAGE=…StaticFilesStorage)`, two services built in `setUp`
  (one long enough to hold position 4 and more, one shorter), fixtures created before the browser
  starts.
- **Rationale**: the repo's practice is one module per concern (spec 197 →
  `test_dock_bucket_head.py`, spec 200 → `test_obs_dock_follow.py`), and `test_obs_dock.py` already
  carries spec 198's 20-plus pins at 1036 lines. The behaviour is browser-local, so the unit lane
  (`multimedia/web/test_obs_dock.py`, "routes and first paint only") cannot reach it.
- **Alternatives considered**: append to `test_obs_dock.py` — rejected, mixes concerns and makes
  the red-first run against `develop` noisier; a unit test — rejected, the state lives in the page.
- **Provenance**: research (the two sibling modules read in full).

## D006 — `bump: patch`

- **Decision**: `patch`. `VERSION` at the branch base (`ab46f384`) is `1.34.4`; the delivery commit
  re-reads the base and takes the next patch then (VER-04), so the number is not written here.
- **Rationale**: a defect in shipped behaviour, no new capability, no interface or model change.
  Calibrated against the neighbourhood: spec 197 `patch` (fix), spec 202 `patch` (fix), spec 198
  `minor` (a new operator-facing capability), spec 200 `minor` (a new control and mode).
- **Alternatives considered**: `minor` — rejected, nothing new is offered to the operator;
  `none` — rejected, the operator sees a behaviour change.
- **Provenance**: research (sibling `plan.md` Bump lines) + VER-10.

## D007 — The preview is static, running the product's own script

- **Decision**: one page assembled from the rendered `/obs/dock` markup, byte-copied
  `tokens.css`/`obs-dock.css`/`display-session.js`/`display.js`/`obs-dock.js`, and the captured
  `projectorEntryData`/`projectorScreenData` islands of five real services; only `fetch` is stubbed,
  and the dock script carries the drafted line gated on a flag so one page runs both rules.
- **Rationale**: the slice changes what the already-fetched list does, so a static page over the
  real payload is honest (SDD-06) and needs no second dev server; a live "after" would require
  implementing before gate 1. `diff` confirms the copied script differs by exactly the three
  drafted lines and the CSS not at all.
- **Alternatives considered**: a hand-drawn mockup — rejected, it would re-interpret the dock; a
  live worktree server with the fix applied — rejected, that is implementation before the gate.
- **Provenance**: research + measurement; recipe recorded in the agent's dock skill.

## D008 — A toggle in flight cannot reopen the new list

- **Decision**: no guard needed for a morph in flight at the moment of an open.
- **Rationale**: `openService` detaches the old list with `entryList.replaceChildren()`; a pending
  `finishToggleMorph` (`:845`) paints only the detached inner it holds, and `effectiveOpenFor`
  reads that node's own id. The new list is built by `renderList()` and painted by `sync()` from
  the cleared map, so it is drawn shut in the same frame. Measured: 0 morph frames in the new list
  across 10 opens.
- **Alternatives considered**: cancel every pending toggle frame on open — rejected per D004.
- **Provenance**: research (code reading) + measurement.

## Open

None.
