# Feature Specification: the dock's entry headers expand and collapse their own block

**Slice**: `specs/198-dock-entry-toggle`
**Branch**: `feat/198-dock-entry-toggle`
**Created**: 2026-11-16 · **Revised**: 2026-11-18 (full revision — SDD-25 re-entry at Specify)
**Status**: Accepted — Gate 1 (2026-11-18)
**Input**: the owner's request, 2026-11-18 — "revert everything back and start over. clicking on
the entry headers no longer display the first content inside it. it only expand/collapse the
entries, except for live-entry (it cant be collapsed). the entry headers will have corresponding
chevron depending on the state. operators need to click on the item inside specifically to jump"

This supersedes the 2026-11-16 request in full (circular icon-only button, row still projects).
The pre-revision pack and code were reverted to `341cf340` at the owner's direction; what the old
model said and why it changed is restated in Clarifications — never silently dropped.

## User Scenarios & Testing

### US1 — The header expands and collapses its entry's block, and never projects (P1)

**Why this priority**: one line of mental model changes everything else: a header is a door, not a
launch button. Before this slice an entry's block is open only while that entry is on air, and a
header click puts the entry on air. After it, any entry can be inspected in place with a click,
and clicking a header never moves what is on air.

**Independent Test**: open a service; click a non-live entry's header — its block morphs open over
230 ms and the display state never changes; click again — it closes. Click the live entry's
header — nothing happens at all.

**Acceptance scenarios**

1. **Given** a non-live entry whose block is closed **When** the operator clicks its header
   **Then** the block morphs open over 230 ms, `aria-expanded` becomes `true`, the inner's
   `aria-hidden` becomes `false`, and no display-state write is issued — nothing goes on air.
2. **Given** an entry the operator opened by hand **When** the operator clicks its header again
   **Then** the block morphs shut over 230 ms, `aria-expanded` becomes `false`, and again nothing
   is projected.
3. **Given** the live entry **When** the operator clicks its header **Then** nothing happens —
   the block stays open, `aria-current` stays on its row, no write is issued; the live entry
   cannot be collapsed.
4. **Given** an entry whose block the operator opened by hand **When** a crossing makes another
   entry live and `sync()` repaints **Then** its block stays open, and when it stops being live
   its stored state applies again without the operator touching anything.
5. **Given** several entries **When** the operator opens several blocks **Then** each toggles
   independently — multi-open is the model; no other block closes.

### US2 — The items inside are the jump targets (P1)

**Why this priority**: projection is the dock's air-moving verb. The revision moves its trigger off
the header onto the content the header reveals: one click deeper, but only for entries the
operator chose to open, and exactly the screen they clicked.

**Independent Test**: expand an entry, click one of its screen rows — that exact screen goes on
air. Click a header — nothing goes on air. The Next band and the transport still jump as before.

**Acceptance scenarios**

1. **Given** an expanded entry **When** the operator clicks a screen row inside its block
   **Then** that screen goes on air through the existing projection path — unchanged behaviour,
   `aria-current` moves to it.
2. **Given** a collapsed entry **When** the operator looks at its block **Then** the items are
   hidden and inert (`aria-hidden="true"`, `inert`) — there is nothing to click until the header
   opens it.
3. **Given** the live entry's Next band **When** the operator clicks it **Then** it projects its
   screen — unchanged.
4. **Given** any header **When** the operator clicks it **Then** no `gkps-display` write and no
   `OBS-*` message is issued — headers never project. This reverses the pre-revision rule that a
   row click projected the entry's first screen.

### US3 — The chevron shows the state; quiet answers for motion, breaks and reloads (P2)

**Why this priority**: the affordance has to be readable at a glance in a dark projection room,
must not offer a control that cannot act (the live row), and must not invent motion for a viewer
who asked for none.

**Independent Test**: a collapsed header shows a right-pointing chevron; an open one shows it
rotated down; the live row, a section break and an empty entry show none. With
`prefers-reduced-motion: reduce`, opening and closing swaps instantly. Reload: every hand-opened
block is gone; only the live block is open.

**Acceptance scenarios**

1. **Given** a collapsed, non-live entry with screens **When** the operator looks at its header
   **Then** a right-pointing chevron is painted at the header's trailing end — ink, via
   `currentColor`.
2. **Given** that block open **Then** the chevron is rotated 90° to point down; the flip is
   transitioned with `var(--ease)` (200 ms) and is instant under `prefers-reduced-motion: reduce`.
3. **Given** the live entry **Then** its header renders no chevron — its open block and selected
   tint carry the state (owner, 2026-11-18).
4. **Given** a section break or an entry whose block is empty **Then** its header renders no
   chevron and a click on it does nothing.
5. **Given** `prefers-reduced-motion: reduce` **When** the operator clicks a header **Then** the
   block swaps instantly — no `requestAnimationFrame` morph runs and no CSS `transition` applies.
6. **Given** a hand-opened block **When** the page reloads **Then** no state survives; the list
   paints with the base rule — blocks open only on the live entry.

### Edge Cases

- **When** an override is recorded on an entry and a crossing makes it live **Then** the override
  is inert for the duration of the live period (the block stays open); the departing live entry's
  stored state applies as soon as another entry goes on air.
- **When** the operator requests a toggle on an entry whose crossing morph is in flight **Then**
  the crossing owns that block until it settles; the request is recorded and the block lands in
  its effective state when the morph finishes — two hand-animations never write the same block's
  height at once.
- **When** a break row or an empty-block header is clicked **Then** nothing happens — no toggle,
  no projection, no write.
- **When** the entry is not live **Then** its header is the expand/collapse control and shows its
  chevron; the rest of the line is the same face as today, tint included.
- **When** the operator clicks a screen row inside an open block **Then** that screen goes on air
  and the block stays open (the live hand-off, not the click, decides what is open after a
  crossing).

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Every entry that has an inner block and is not the live entry SHALL render one chevron in its header line — trailing, inside the header button, a painted state indicator. The live entry, section breaks and empty-blocked entries SHALL render none. | `dock` (R14 new) |
| FR-002 | The header row SHALL be its entry's sole expand/collapse trigger: clicking it SHALL toggle only that entry's inner block — no `gkps-display` write, no `OBS-*` broadcast, no scroll or glide, no `aria-current` change — and SHALL never project. The live entry's header click SHALL do nothing (its block is locked open); a section-break or empty entry's header click SHALL do nothing. | `dock` (R14 new; R3 unaffected) |
| FR-003 | The chevron SHALL be an inline SVG stroke (viewBox `0 0 20 20`, `stroke: currentColor`, `stroke-width: 1.7`, round caps and joins), painted in ink via the header's `color`: right-pointing when the block is closed, rotated 90° down when open; the rotation SHALL be transitioned with `var(--ease)` (200 ms) and instant under `prefers-reduced-motion: reduce`. It SHALL NOT be a plus or minus glyph. | `dock` (R14 new) |
| FR-004 | Projection SHALL happen only from inside an open block (a screen row's click, the Next band), from the panel's bait chips, or from the transport. No header click SHALL ever project. This supersedes the pre-revision "row click projects the entry's first screen" rule. | `dock` (R14 new; R3 projection path unaffected) |
| FR-005 | Expansion and collapse SHALL morph `grid-template-rows` 0fr ↔ 1fr by hand over 230 ms with the same `easeInOut(t)` curve the crossing hand-off uses; `.is-morph` SHALL suppress the CSS transition during the morph; `prefers-reduced-motion: reduce` SHALL swap instantly. | `dock` (R14 new; crossing machinery, R3) |
| FR-006 | The effective open state of an entry's block SHALL be, while it is the live entry, open — no click can change it and its stored state is inert; while it is not live, its per-entry override when set, else closed. Overrides SHALL live in page memory only, SHALL NOT be persisted, and SHALL NOT be clobbered by a crossing's morph or by `sync()` repaints. | `dock` (R14 new; sync, R11) |
| FR-007 | Toggling a block SHALL NOT start, cancel or retarget a scroll or glide, SHALL NOT move the list cursor, and SHALL NOT change `aria-current` — expanding is peeking; no screen row inside gets selected by opening a block. | `dock` (R14 new; R9 unaffected) |
| FR-008 | The header button SHALL carry `aria-expanded` and `aria-controls` pointing at its entry's inner block; a closed block SHALL be `aria-hidden="true"` and inert; the header SHALL stay `tabindex="-1"` like every dock control and activation SHALL return focus to the panel; the row's `aria-current` semantics are unchanged. | `dock` (R14 new; R10 keeps the keyboard) |
| FR-009 | A toggle requested while that block's crossing morph is in flight SHALL let the crossing own the block until it settles; the request SHALL be recorded as the entry's override and the block SHALL land in its effective state when the morph finishes. | `dock` (R14 new; crossing machinery, R3) |
| FR-010 | An entry with nothing to open — a section break, or an entry whose inner block is empty — SHALL render no chevron, and its header click SHALL be a no-op. | `dock` (R14 new; break rule, `reading.md`/R3 unaffected) |
| FR-011 | The header's hover tint SHALL cover the whole header — the row's own face, chevron included (`background: var(--icon-hover-bg)` on the row); the live row SHALL keep `var(--sidebar-selected-bg)`. No separate line wrapper is needed: the chevron lives inside the row. | `dock` (R14 new) |

### Key Entities

- **Entry block override** — a per-entry tri-state held in page memory: `open`, `closed`, or unset
  (no override). Unset behaves as the base rule. The override is read at every paint and is inert
  while the entry is live. Session-scoped; never persisted.
- **Effective open state** — `live ? open : (override ?? closed)`; the single input to the inner's
  `is-open` class, `aria-hidden`, `inert`, and the header's `aria-expanded` and chevron rotation.
- **Header chevron** — a `<span>` (aria-hidden) inside `button.entryrow`, holding the SVG; its
  rotation follows the effective state; `hidden` while the entry is live.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The chevron renders on every non-break, non-empty, non-live entry's header — right-pointing at rest, rotated down when open; live, break and empty headers render none. | DOM count + computed styles; E2E |
| SC-002 | Clicking a header opens or closes the block with a 230 ms morph (instant under reduce), flips `aria-expanded`, `aria-hidden`, `inert` and the chevron's rotation, and leaves `aria-current` and the display state untouched — no write, nothing on air. | E2E (toggle test) + preview states |
| SC-003 | Clicking a screen row inside an open block projects exactly that screen — the projection path is bit-for-bit today's. | E2E existing `tests/e2e/test_obs_dock.py` + new toggle test |
| SC-004 | Clicking the live entry's header, a section break's header or an empty entry's header changes nothing — no write, no morph, no class change. | E2E (toggle test) |
| SC-005 | A block opened by hand stays open through crossings and `sync()` notices; a crossing never reopens a block the operator closed; reload forgets every override; the live entry never collapses and renders no chevron. | E2E (toggle test) |
| SC-006 | `tests.e2e.test_obs_dock` and `multimedia.web.test_obs_dock` pass, and the slice's toggle test fails against `develop`'s stylesheet/script for the toggle reason, not an import. | suite output |

## UI/UX

| | today (HEAD `13baf77f`) | this slice |
| --- | --- | --- |
| entry header | full-width `button.entryrow` (flex, min-height 38 px, padding 9 px 10 px, radius 9 px), row face paints `--icon-hover-bg` on hover; click projects the entry's first screen | same face and tint; click toggles the block and never projects; a chevron sits at its trailing end |
| chevron | — (none) | inline SVG, 15 × 15 px (viewBox `0 0 20 20`, stroke 1.7), ink via `currentColor` — right at rest, rotated 90° down when open; 200 ms `var(--ease)` flip, instant under reduce; `flex: none` at the row's trailing end, **vertically centred in the header** (`align-self: center` — the row aligns by baseline and the chevron has no text to baseline on); never a plus or minus glyph |
| live row | no chevron (nothing existed); selected tint; block open | no chevron — its open block and `--sidebar-selected-bg` tint carry the state; header click does nothing |
| break / empty header | click is a no-op (divider guard) | unchanged — no chevron, click stays a no-op (the pre-revision clamped projection of an empty header goes away with FR-002) |
| block visibility | open only while live; `is-open` set by `sync()` | per-entry: `live ? open : (override ?? closed)`; closed blocks stay `aria-hidden` + inert |
| block morph | crossing hand-off at 230 ms `easeInOut(t)`; CSS fallback 200 ms `var(--ease-timing)`; reduce: instant | unchanged; the header toggle uses the same 230 ms hand morph with `.is-morph`, instant under reduce |
| projection triggers | header row, screen rows, Next band, bait chips, transport | screen rows, Next band, bait chips, transport — headers removed |
| focus ring | none on dock controls (panel-focused, `tabindex="-1"` everywhere) | unchanged |
| sticky live row | pins the live entry at `top: -4px` | unchanged |
| list keys | arrows/step, Space, T, G, Esc — transport only; Enter inert in run view | unchanged — the toggle stays pointer-only (A9) |

The approved preview: `static preview at specs/198-dock-entry-toggle/preview/index.html` — every
state above reachable by hand (rest, hover, collapsed/expanded chevron, live row, break, empty,
reduce).

## Assumptions

- **A1 — chevron direction is the APG disclosure reading: right collapsed, down open.** The
  W3C APG Disclosure pattern words it exactly so ("right-pointing arrow or triangle" when hidden,
  "typically points down" when visible); Material/Apple-button families go down→up instead — a
  convention split, not a defect. Provenance: research (APG fetched2026-11-17).
- **A2 — toggles are session-scoped.** Overrides live in page memory; a reload repaints with the
  live-block rule; nothing is written to `localStorage` or to `gkps-display`.
- **A3 — the live entry is locked open and shows no chevron; any other entry is independent.**
  (Owner, 2026-11-16 and 2026-11-18.) Non-live entries toggle independently, several may open at
  once, and expanding selects nothing.
- **A4 — no scroll follows a toggle.** Toggling never glides or centres; the dock's scroll stays
  owned by live hand-offs and the operator's hand.
- **A5 — the header's accessible name stays the entry's title; the state rides `aria-expanded`.**
  (Owner, 2026-11-18 revision.) Supersedes the pre-revision "Expand entry N / Collapse entry N"
  verb-name, which belonged to the removed circle button; with the header itself as the control,
  the list stays navigable by title and the attribute carries the state — the APG accordion idiom.
- **A6 — media entries toggle** (their insides are screen rows); entries with an empty inner and
  section breaks do not — there is nothing for a chevron to act on.
- **A7 — the pin is untouched.** The sticky rule pins the live entry's header line as today; the
  live entry renders no chevron, so nothing rides the pin that did not before.
- **A8 — first chevron in the dock.** The dock has no right/down chevron at HEAD; this slice
  introduces the shape, drawn to the existing stroke vocabulary (`.iconbtn` SVGs).
- **A9 — no keyboard binding; pointer-only toggle.** The dock's keys are list-scoped (R7): in the
  run view the arrows/Space/T transport, Enter inert. The header stays `tabindex="-1"`, so no key
  reaches it — recorded as the dock's own pointer model, as the request draws it.
- **A10 — never persisted, never projected.** No `gkps-display` field, no channel message, no
  localStorage key; the dock's display state schema is untouched.
- **A11 — the whole header is the click target.** No hit slop, no separate button face: the row
  is the disclosure control (the WinUI reading of the pattern), which is what "clicking on the
  entry headers" asks for.
- **A12 — an entry with nothing to open is a dead control.** No chevron, no action. The
  pre-revision behaviour where an empty entry's header click projected a *clamped* neighbouring
  screen (an artifact of projecting `entry.start` regardless of content) disappears with FR-002.

## Clarifications

### Session 2026-11-18 (the revision)

- The owner's directive (verbatim) is the **Input** above: headers no longer display the first
  content inside; they only expand/collapse, except the live entry (it can't be collapsed);
  headers carry a chevron per state; operators click the item inside specifically to jump.
  Recorded in US1, US2, US3, FR-001…FR-004, FR-010, UI/UX.
- Q: how should the restart happen — revise the pack in place per SDD-25, or revert and rebuild?
  → A: **full revert, then rebuild** (owner's choice): code and records went back to `341cf340`
  and the pre-revision pack was deleted; this pack is written from zero. The four pre-revision
  amendments' substance is restated in this spec wherever it still stands (chevron painted, live
  locked, overrides, morph), so nothing the owner decided is lost — only the superseded wording.
- Q: what does the live entry's header show? → A: **no chevron on the live row** — its open block
  and selected tint carry the state; the header still renders no control because none can act
  (FR-001, US3 scenario 3).
- Superseded, kept in words, never silently dropped: the **circular icon-only button** model
  (2026-11-16 input; radius, hit-slop, ghost-face and hover-reveal decisions all belonged to it
  and are gone with it — A11 replaces them); **"the row still projects"** (old US2/FR-006/SC-003 →
  FR-004 now says headers never project); the **line-level hover wrapper** introduced to tint
  around the circle (FR-011: the row's own face tints again, chevron inside it, same visual
  extent); the **verb+number accessible name** (A5 superseded above); the **painted-chevron-on-
  ghost amendment** — moot, there is no circle face left to ghost.

No `[NEEDS CLARIFICATION]` markers remain, and no open decision is outstanding: the restart
approach and the live row's chevron were answered by the owner on 2026-11-18, and every other
question carried from the pre-revision sessions stands as recorded above.
