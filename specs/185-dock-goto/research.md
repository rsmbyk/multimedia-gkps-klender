# Research: the dock's Go To

**Spec**: `specs/185-dock-goto/spec.md`
**Unknowns remaining**: 0

## D001 — The return place is the state's own `screen` and `translation`, not a copy inside `goto`

- **Decision**: `goto` carries only what is on air — `{kind, song_id, index}` for a song,
  `{kind, book_id, chapter, verse, translation}` for a passage. The service's place to come back to
  stays in the top-level `screen` and `translation`, which no goto act writes.
- **Rationale**: FR-015 says the service's own screen and edition SHALL NOT change until Back, and
  FR-008 says Back restores exactly what stood before. Two fields frozen for the goto's whole life
  are that promise by construction; a duplicated `return` could disagree with them, and the plan
  would then need a rule for which copy wins. `static/web/display.js:96-132` already writes every
  verb from `state.service`/`state.screen`/`state.translation`, so keeping them untouched is the
  smaller change than teaching each verb to skip a field.
- **Alternatives considered**: `goto.return = {screen, translation}` (a second home for one fact,
  and a repair path when they diverge); a separate storage key (breaks FR-013 and the one-state
  rule); moving the service to a `service` sub-object (rewrites spec 119's pinned shape for no
  gain).
- **Provenance**: research — FR-001's "the service's own return place" is read as the state
  carrying it in those two fields, which is what the accepted text says of the state, not of the
  goto object.

## D002 — One new channel message, `{type: 'goto', goto}`, for every goto change

- **Decision**: starting, stepping, flipping and ending a goto all post the same message type with
  the whole goto (or `null`), and every surface re-reads the state on it.
- **Rationale**: `static/web/display.js:17-24` documents five message types whose payloads are
  narrow (`show`, `hide`, `release`, `flip`, `update`). A goto has four mutations; four message
  types would each need a reader branch, and a surface that missed one would paint a stale
  position. One type with the full pointer keeps every reader a re-read, which is how the overlay
  already works (`obs-overlay.js:292-300` syncs on any message).
- **Alternatives considered**: `show` with an `detour` flag (overloads a verb whose meaning is "a
  service screen is on air"); three messages (`goto-start`, `goto-step`, `goto-end`) with payload
  shapes to keep in step.
- **Provenance**: research.

## D003 — Each reader fetches the payload it paints; the state never carries words

- **Decision**: the projector, the overlay and the dock fetch `/projector/goto/song/<id>/` or
  `/projector/goto/chapter/<book>/<chapter>/` themselves, `cache: 'no-store'`, when the state's
  goto names one they do not already hold.
- **Rationale**: FR-001 and SC-005 forbid text in the state; the payloads already exist and are
  shaped exactly as each surface paints them (`multimedia/web/reading/goto.py`). The dock already
  fetches the same chapter to step inside it (FR-006), so the three readers share one request
  shape, not three.
- **Alternatives considered**: storing the painted lines in `gkps-display` (megabytes, and the
  state would stop being a pointer); a server-side projection state (the whole design is
  browser-local).
- **Provenance**: research.

## D004 — The dock loads the index on the first `G`, not with the page

- **Decision**: `projector-library.js` is injected on the first `G` (or the head's control) and
  `load()` runs then; the band shows `Loading search…` until it resolves.
- **Rationale**: the index is 29 KB gzipped (spec 136's measurement) and a dock that is opened and
  never searched should not pay for it. US1/AC1 says the index is read once, at the moment the band
  opens, which is this decision; the spec fixes no earlier moment.
- **Alternatives considered**: loading at dock boot (a request on every dock open, and the same
  29 KB for a surface that may never search); a server-rendered list in the template (stale the
  moment a song is added).
- **Provenance**: research.

## D005 — The block is the list's live content, drawn with the dock's own row vocabulary

- **Decision**: while a goto is up, `#entryList` holds the goto's block — a pinned header (label,
  `Back`) and the goto's own rows, full-bleed from the list's 8 px padding — and the service's rows
  are not drawn at all.
- **Rationale**: approved in the preview (`preview/index.html`, states *Song on air* and *Passage
  on air*) and measured there: header 384 × 43 at the dock's 400, rows 28.8 px, the current row
  carrying the live tint. A banner above the service rows was the alternative and was rejected in
  review: it leaves two lists claiming to be what is on air.
- **Alternatives considered**: a banner plus the service list underneath; a third view (the owner
  asked the dock not to grow one).
- **Provenance**: owner decision at gate 1 (the preview's *Go To block* anatomy).

## D006 — The dock's transport acts on what is on air

- **Decision**: `step`, `stepUnit`, `edgeOf`, the bait chips and `flipEdition` read the state's
  goto when there is one, and write to it; `blankBtn` toggles `on` for whatever is on air.
- **Rationale**: the owner's answer at clarify — *"step the Go To"* — and FR-015. The transport is
  already the surface's only stepper (`obs-dock.js:836-878`); teaching it one more target is
  smaller than a second set of controls.
- **Alternatives considered**: modal arrows (two steppers in one 400 px band); modifiers (the
  operator's hands are on arrows mid-service).
- **Provenance**: owner decision, recorded in the spec's `## Clarifications`.

## D007 — The projector's `detour` becomes a payload cache keyed by the state

- **Decision**: `projector.js` keeps its `detour` variable, but it is now the fetched payload for
  the state's current goto — refetched when the state names a different song, chapter or edition —
  and it is never the source of truth for *which* screen is up. `openDetour` writes the state
  before it paints; `leaveDetour` writes `back`.
- **Rationale**: FR-010 keeps the projector's panel, cue, loading lock and Back behaviour, and those
  are built on the payload shape (`projector.js:1321-1437`). Reusing that rendering with the state
  as its input keeps the look and removes the private memory in one move.
- **Alternatives considered**: re-fetching on every render (a request per keypress); a shared
  payload store in the state (forbidden by D003).
- **Provenance**: research.

## D008 — `moveTo` ends a goto, like `show`

- **Decision**: any act that puts a service screen on air — `show(service, screen)` from the dock or
  a reading page, and `moveTo(screen)` from the dock's picker — clears `goto`.
- **Rationale**: FR-009 names `show`; FR-015 forbids the service's screen changing underneath a
  goto, so a `moveTo` that kept the goto would either move the service invisibly (the defect this
  slice exists to end) or leave two pointers disagreeing. Ending the goto is the one reading that
  satisfies both.
- **Alternatives considered**: refusing `moveTo` while a goto is up (a dead control, and the dock's
  arrow keys would silently do nothing).
- **Provenance**: research — a reading of FR-009 governed by FR-015.

## D009 — The session stamp is inherited, not extended

- **Decision**: `read()` keeps its `GKPSDisplaySession.owns(stored)` gate and `goto` rides inside
  the same object; nothing new is stored.
- **Rationale**: FR-003 says the goto is stamped "like the rest of the state". `display.js:42-56`
  already returns the empty state when the stamp does not match, so a goto cannot survive a
  restart — and the slice needs no new code for that promise.
- **Alternatives considered**: a second marker for the goto (two lifetimes to keep in step).
- **Provenance**: research; spec 184 (`display-session.js`).

## D010 — Capability homes: `display-state/R2` new, `projector/R1`+`R5` and `overlay/R1` modified, `docs/spec/dock.md` created

- **Decision**: Fold adds `R2` to `docs/spec/display-state.md`, modifies `projector/R1` and `R5`
  and `overlay/R1` in place, and creates `docs/spec/dock.md` carrying the dock's goto rules
  (`R1`–`R4`). The dock's older rules stay where they are (`docs/spec/reading.md` R33 and the picker
  buckets).
- **Rationale**: the accepted spec's requirement table names `new: dock`, so the dock's goto needs a
  capability home of its own. Moving `reading/R33` and the picker rules out of `reading.md` would
  rewrite accepted text this slice does not change, and Fold cannot invent intent.
- **Alternatives considered**: folding the dock's goto into `reading.md` as `R34+` (contradicts the
  accepted table and buries the Go To under a reading capability); one capability per surface
  rewritten wholesale (out of scope).
- **Provenance**: research; the overlap is stated in `dock.md`'s header at Fold.

## Open

<!-- empty: Phase 0 is finished -->
