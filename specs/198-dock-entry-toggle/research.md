# Research — spec 198 (the 2026-11-18 revision)

Every decision carries provenance. Nothing here was decided from recollection; each reads the code
at `13baf77f`, the accepted preview, or a fetched primary source. Unknowns remaining: **0**.

## D001 — The chevron is a child of the header button; no wrapper, no sibling control

**Decision**: `entryRowContent` (or `renderList`, see D002) appends
`<span class="entrychev" aria-hidden="true"><svg …/></span>` as the last child of the existing
`button.entryrow`. The row becomes `justify-content`-neutral with the chevron pushed trailing by
`margin-left: auto`, `flex: none`. No `.entryrowline` wrapper, no separate button, no overlay.
**Rationale**: FR-011 says it outright — "No separate line wrapper is needed: the chevron lives
inside the row" — and it buys three things at once: the row's own hover face
(`.entryrow:hover { background: var(--icon-hover-bg) }`, `obs-dock.css:386`) paints behind the
chevron with no new rule; the sticky live-row pin (`.entryrow[aria-current="true"]`,
`obs-dock.css:390`) is untouched because no element joined the row's context; and the whole
header stays one hit target (A11 — the row *is* the disclosure control). A chevron inside a
`<button>` is legal HTML (only interactive descendants are barred), so unlike the pre-revision
circle there is no nesting question to answer.
**Alternatives**: the pre-revision `.entryrowline` sibling wrapper (rejected by FR-011 — a second
hover/pin context for zero gain); an absolutely-positioned chevron (fights the row's padding and
the sticky context, same arguments as the old circle overlay); a `::after` on the row (cannot
rotate a pseudo-element that holds an SVG cleanly across the a11y-free boundary — aria-hidden is
free on a real span).
**Provenance**: `obs-dock.js:148-215` (`entryRowContent`), `:295-307` (`renderList`),
`obs-dock.css:369-386` (`.entryrow`, `:hover`), `:390` (sticky), spec FR-001/FR-011, A11;
preview `preview/index.html` (`.entrychev` as built and probed).

## D002 — Eligibility at build; presence and live-lock at every `sync()` repaint

**Decision**: the chevron is built only when the entry actually has an inner: `renderList` calls
`buildInner(entry)` (`obs-dock.js:301`) and appends the chevron to the row only when `inner` came
back non-null — so breaks (guard at `:251`) and empty blocks (`:274`, no children → null) never
get one, at build time, from the one fact that knows. `sync()`'s existing per-`li` pass
(`:1118-1133`) then enforces the live half each repaint: the `li` marked `data-live="true"` gets
`chev.hidden = true`, every other eligible row `chev.hidden = false`; the same loop paints
`aria-expanded` from the effective state (D003). `sync()` runs after every `renderList()`
(`loadServiceData`), so first paint, service switches and spec 195's 10 s re-reads all re-derive
both facts.
**Rationale**: emptiness is known only where the inner is built, and liveness changes far more
often than rows — deciding presence only at build would strand a chevron on a row that just went
on air. `sync()` already walks every `li` and already sets `li.dataset.live`, so the rule costs
two assignments in a loop that exists. `hidden` (not `display: none` in CSS alone) keeps the DOM
honest with FR-001's "renders none" and removes the span from hit-testing outright.
**Alternatives**: decide everything at build (strands the live chevron — crossings flip liveness
without a rebuild); a MutationObserver (a watcher for what `sync()` already computes); CSS-only
`[aria-current="true"] .entrychev { display: none }` (works, but leaves `aria-expanded`'s painter
and the presence rule in two places forever).
**Provenance**: `obs-dock.js:250-276` (`buildInner`), `:295-307` (`renderList`), `:1118-1133`
(`sync` inner paint), spec FR-001/FR-010, US3 scenarios 3-4.

## D003 — Effective open state: `live ? open : (override ?? closed)`

**Decision**: `var entryOverrides = new Map()` — entry index → `true` (open) / `false` (closed),
absent = unset. `effectiveOpen(index)` = the entry is live ? `true` :
(`entryOverrides.get(index) ?? false`), liveness read from the same `current` fact `sync()` already
computes per `li`. Three painters and nowhere else read it: `sync()`'s inner loop (replacing
today's `toggle('is-open', current)` at `:1126`), `finishMorph`'s settle paint (D010), and
`toggleBlock` (D004). `aria-expanded`, `aria-hidden`, `inert` and the chevron's presence all ride
the same value.
**Rationale**: one effective-state input is the only way crossings, repaints and hand toggles
cannot disagree; FR-006 pins it and US1 scenario 4 pins the override surviving a crossing. The map
is keyed on the service's entry index — stable across `sync()` re-reads of the same service.
Overrides are page memory only: never serialized, never written, never broadcast (A2/A10).
**Alternatives**: a `gkps-display` field (display state is display-only — A10 forbids); a
localStorage key (same, plus A2); tri-state arity including the live lock (live is never eligible
to toggle at all — D002 removes it, so the third state buys nothing); repainting from overrides in
`finishMorph` only (today `finishMorph` hardcodes out-closed/in-open — the exact SC-005 bug).
**Provenance**: `obs-dock.js:1118-1133` (sync paint), `:606-624` (`finishMorph` hardcode),
spec FR-006, Key Entities, US1 scenarios 4-5, A2/A10.

## D004 — The toggle morph is the crossing's curve applied to one block

**Decision**: `toggleBlock(index)` records the override, then — unless
`prefers-reduced-motion: reduce` — hand-morphs that one block: measure the body's height, animate
`grid-template-rows` from 0fr to the measured height (and back) over **230 ms** with the same
`easeInOut(t)` the crossing uses (`obs-dock.js:561-563`), adding/removing `.is-morph`
(`obs-dock.css:477`) so the CSS transition never fights the rAF frames; on the last frame the
class pair is painted from the effective state and the inline style dropped. Under reduce: swap
instantly — no rAF, no inline height (the `reduceMotion.matches` branch idiom already at `:588`).
No `centerRow`, no `glideScroll`, no cursor move — FR-007/A4 forbid any scroll or glide.
**Rationale**: one motion vocabulary — the crossing already ships the curve, the class, the
reduce branch and the body-height measure; the header toggle extends those primitives to the
one-block case. The CSS `grid-template-rows` 200 ms transition (`obs-dock.css:465`) stays as the
no-JS fallback only; during motion `.is-morph` suppresses it (same rule as the crossing).
**Alternatives**: the CSS transition alone (different curve, class-flip ends, not the spec's hand
morph); `max-height` (jank at the ends); animating to `auto` without a measure (impossible);
reusing `startMorph` with a null partner (it centres the arriving row — FR-007 forbids scroll).
**Provenance**: `obs-dock.js:561-604` (curve, duration, reduce branch), `obs-dock.css:463-488`,
spec FR-005/FR-007, UI/UX "block morph" row, A4.

## D005 — A toggle clicked mid-crossing records its override; the crossing owns the block

**Decision**: in the toggle branch, before morphing: if `morphState` names this `li`'s inner (as
its `out` or `inn`), record the override and return — no second animation touches that height.
`finishMorph` (changed by D010) paints both blocks from the effective state at settle, so the
recorded request lands exactly when the morph ends. A toggle on any *other* `li` during a crossing
morphs immediately.
**Rationale**: two hand-animations must never write the same block's height; the spec's edge case
says the crossing owns the block until it settles and the request is recorded. Deterministic, one
branch, and the ≤230 ms "nothing happened yet" is the honest outcome — the settle paint applies it.
**Alternatives**: cancel the crossing and run the toggle (abandons the live hand-off mid-air);
queue every toggle behind `finishMorph()` unconditionally (hides unrelated rows' responsiveness);
reject the click (hostile and silent).
**Provenance**: `obs-dock.js:565-567` (`startMorph` finishes an in-flight morph first),
`:606-624`, spec Edge Cases (mid-crossing), FR-009.

## D006 — Accessibility: the header button itself carries the state; the title stays the name

**Decision**: no new control exists, so the attributes ride `button.entryrow` itself:
`aria-expanded` bound to the effective state, `aria-controls="entryinner-<index>"` — `buildInner`
gains `inner.id = 'entryinner-' + index`. The accessible name is **not** rewritten: the row's
content (title/number) stays the name and `aria-expanded` carries the state — the APG accordion
idiom, per A5 (owner, 2026-11-18, superseding the pre-revision verb-name). `tabindex="-1"` is
already on the row (`obs-dock.js:151`); activation calls `focusPanel()` — the dock invariant that
every control yields the keyboard back to the panel. `aria-current` semantics untouched.
**Rationale**: FR-008 pins all four facts; the dock's existing pattern is `tabindex="-1"` +
`focusPanel()` after every activation (`:1173,1179,1187`). `aria-controls` needs an id the inner
does not have today.
**Alternatives**: an `aria-label` verb ("Expand entry n" — superseded by A5, and it would drift
from `aria-expanded`); dropping `aria-controls` (the attribute is free and names the target);
making the row focusable (violates R10's panel-keeps-keyboard model).
**Provenance**: `obs-dock.js:149-153` (button, `tabindex=-1`), `:250-276` (inner, id to add),
`:311-313` (`focusPanel`), spec FR-008, A5, A9; R10 in `docs/spec/dock.md`.

## D007 — The icon: a stroked right-chevron, rotated 90°, never a plus or minus

**Decision**: inline `<svg viewBox="0 0 20 20"><polyline points="7 4 13 10 7 16"/></svg>`,
`fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap/linejoin: round`, painted
**15 × 15 px** (FR-003's viewBox/stroke; UI/UX's size), `color: var(--ink)` inherited from the
row. Closed: no transform (points right). Open: `transform: rotate(90deg)` on the svg, transitioned
`transform var(--ease)` — `--ease` is `200ms cubic-bezier(.32,.72,.28,1)` (`tokens.css:48`) — and
instant under `prefers-reduced-motion: reduce`. SC-004's glyph prohibition is verified by sweep:
no `+`, `−`, `×` glyph enters `obs-dock.css` or `obs-dock.js`.
**Rationale**: FR-003 pins shape, stroke, motion and the prohibition; the dock's icon vocabulary
is exactly these stroked SVGs (`.iconbtn`); a chevron is the dock's first (A8) and the APG
disclosure reading is right-collapsed/down-open (A1).
**Alternatives**: a Unicode `▸`/`▾` (browser-dependent rendering, off the currentColor grid);
CSS mask/background-image (ships an asset to paint 15 px); plus/minus (forbidden by FR-003 —
reads as "add", not "show").
**Provenance**: spec FR-003, SC-004, A1, A8; `tokens.css:48-54`; `obs-dock.css` `.iconbtn`
stroke vocabulary; preview as approved.

## D008 — Vertical centring: `align-self: center` on the chevron, because the row is baseline-aligned

**Decision**: `.entryrow` lays out with `align-items: baseline` (`obs-dock.css:371`). The chevron
span carries no text, so the browser synthesizes its baseline from its border-box bottom and the
span sits low. The fix is one declaration: `.entrychev { align-self: center }` — the chevron
centres on the row's cross axis regardless of line-box state, verified by probe: **offset from
row centre = 0 px** on collapsed and expanded rows (`/tmp/opencode/probe_chevron_center.py`, run
in the container against the preview).
**Rationale**: the owner asked for it explicitly (2026-11-18: "make sure the chevron is centred
vertically in the headers"); the probe is the evidence, carried into the spec's UI/UX row and
pinned again at Implement by a bbox assertion in the chevron E2E test (not CSS hope alone).
**Alternatives**: `align-items: center` on the row (moves every baseline-aligned text child —
number, title, verses — a visible regression across the whole list); `padding-top` fudge (breaks
at the 38 px min-height and any font change); `position: relative; top: 50%; transform: translateY
(-50%)` (couples with the rotation transform the same property must carry).
**Provenance**: `obs-dock.css:369-385`, spec UI/UX chevron row (records `align-self: center` and
the reason), probe output 2026-11-18.

## D009 — The projection rewire: expand, then click the item; semantics-neutral on both trees

**Decision**: every E2E site that clicked `.entryrow` **to project** (17 sites across 7 files —
`test_display_session.py:90,264,351`, `test_display_session_refresh.py:71`,
`test_dock_goto.py:265,292,346`, `test_dock_keys.py:258,377,407,456`,
`test_obs_overlay.py:121,265,283,319`, `test_obs_overlay_wrap.py:143`,
`test_obs_dock.py:102`) becomes two clicks: the header (expand), then the first `.screenerow`
inside that `.entryli[data-index]` (project). Where a suite has a `_project` helper the change is
one place; the inline sites follow the same shape.
**Rationale**: under FR-004 a header click never projects, so the old single click cannot move
what is on air — but the rewired pair is **semantics-neutral on both trees**: on `develop` the
header click projects the entry (opening its block as live) and the screen-row click re-projects
the same first screen; on the new tree the header expands and the screen-row click projects.
Either way the helper's contract ("this entry is on air") lands identically, so the rewire can run
Foundational — before the handler change — and the suite never sits red between phases.
Playwright's auto-wait covers the 230 ms expand (the screen row becomes visible only when the
block has height).
**Alternatives**: project via `gkpsDisplay.write` directly (bypasses the very path SC-003 says is
bit-for-bit); keyboard transport (changes what the tests exercise); rewire after the handler
change (leaves seven suites red mid-run for no benefit).
**Provenance**: the 17 grep sites above; `obs-dock.js:1168-1188` (handler);
`test_obs_overlay_wrap._project` already takes a `screen=` param and steps with ArrowRight
(`tests/e2e/test_obs_overlay_wrap.py:137-154`); spec US2, FR-004, SC-003.

## D010 — `finishMorph` must adopt the effective state; two guards keep crossings honest

**Decision**: `finishMorph` today hardcodes `out` closed / `inn` open (`obs-dock.js:615-620`).
It paints both from `effectiveOpen` instead, with two guards learned in the pre-revision run:
**`keepOutOpen`** — a departing block whose override is `true` is not collapsed by the crossing
(it stays open, it just stops being live), and **`inWasOpen`/arrival rule** — the arriving block
is always open (live ⇒ open) but its *stored* override is left untouched, so departure later
applies it. `sync()`'s inner loop keeps its `morphing` guard (`:1125`) so the settle paint is the
single writer at the end of a crossing.
**Rationale**: without this, a crossing reopens a block the operator closed and closes one they
opened — the exact SC-005/FR-006 violation. The pre-revision implementation shipped these guards
and the crossing suite stayed green; the diff is reused at Implement
(`/tmp/opencode/spec-198-v1/code-198-working.diff`).
**Alternatives**: repaint only in `sync()` (it deliberately skips in-flight inners — the settle
frame would land wrong); drop the guards (the documented bug).
**Provenance**: `obs-dock.js:606-624` (hardcode), `:1118-1133` (skip guard), spec FR-006/FR-009,
SC-005, Edge Cases; pre-revision converge record (`/tmp/opencode/spec-198-v1/tasks.md` T010).

## D011 — Bump: `minor`

**Decision**: `VERSION` 1.32.2 → **1.33.0**; `CHANGELOG.md` gains an `[Unreleased]` line at Fold.
Declared here for Gate 2; applied only pre-merge per VER-04.
**Rationale**: a new operator-facing capability (the header toggle + chevron) with no breaking
change to any surface — SemVer's definition of minor. Not `patch` (a visible new control is more
than a fix), not `major` (the panel, the projector and the display-state schema are untouched).
**Alternatives**: `patch` (understates the addition); `none` (invisible in the release record —
what the versioning part exists to prevent).
**Provenance**: `VERSION` (`1.32.2`), `CHANGELOG.md` (`[Unreleased]` holds spec 197's Fixed lines; ours adds the Added line at Fold), spec's new-capability
framing (R14 new).

## Noted, accepted, not re-litigated

- **Renumbering re-keys overrides** (D003): an edit that adds/removes entries above a peeked one
  re-keys the map. Session-scoped by A2 — a reload forgets anyway; the 10 s re-read of a static
  service re-keys nothing.
- **A rebuild mid toggle-morph** detaches the old inner; the frames run on detached nodes
  (harmless) and the `sync()` that immediately follows repaints the effective state
  (`loadServiceData` → `renderList` → `sync`). The override map survives the rebuild.
- **FR-005's literal "0fr ↔ 1fr"** is looser than the mechanism: the hand morph animates *measured
  pixels* on `grid-template-rows` (as the crossing does). Behavioural content is fully bound; the
  wording is Gate-1 accepted and may be tightened at Converge (carried as analysis A1).
- **The chevron build's live-half assertion** in the live-header test is vacuous until the chevron
  build task lands later in the run; the final full-suite run pins it for real. Recorded so no one
  mistakes the intermediate green for evidence.
