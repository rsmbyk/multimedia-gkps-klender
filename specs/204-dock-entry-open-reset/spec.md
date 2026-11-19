# Feature Specification: Opening a service starts its entry blocks shut

**Slice**: `specs/204-dock-entry-open-reset`
**Branch**: `fix/204-dock-entry-open-reset`
**Created**: 2026-11-19
**Status**: Accepted — Gate 1 (2026-11-19) · Gate 2 (2026-11-19, all 25 checklist items ticked on
the owner's word)
**Input**: the owner's request, 2026-11-19 — "when you expand an entry in dock (lets say entry at
position 4), when you open another (or even the same) entry, the same position entry(s) also gets
expanded. it should be reset (exception for the live-entry)"

A defect in shipped work (spec 198, `dock/R14`), so it is a slice of its own. The request names the
event as "open another (or even the same) entry"; the reproduced defect is an *open of a service*
from the picker, which is the only event that draws a different list at the same positions
(A2 records that reading, and the one question put to the owner timed out — A1 holds the
recommendation and is offered for reopening at gate 1).

## User Scenarios & Testing

### US1 — An open starts every block shut but the live one (P1)

**Why this priority**: the operator opens a service to run it, not to inherit the previous
service's inspection state. A block standing open at position 4 of a service nobody touched reads
as a selected entry, and the dock's whole list model says only the live entry is selected.

**Independent Test**: open service A, click the header of position 4, open service B — every block
in B is shut. Re-open A — every block in A is shut. Project position 4 in A, open B, return to A —
position 4's block is open because it is live, and nothing else is.

**Acceptance scenarios**

1. **Given** a service whose position 4 block the operator opened by hand **When** the operator
   opens a different service from the picker **Then** every entry block in the newly opened service
   is shut (`aria-expanded="false"`, no `is-open`, height 0), except a live entry's if one is live
   there.
2. **Given** the same hand-opened block **When** the operator opens the *same* service again
   **Then** the list is drawn with every non-live block shut — the open is a fresh start, not a
   return to the previous inspection state.
3. **Given** several blocks opened by hand (positions 2, 4 and 9) **When** the operator opens a
   service with fewer entries **Then** no block stands open at any position — the leak is not
   limited to the positions the new list happens to have.
4. **Given** an entry on air in service A **When** the operator opens service A from the picker
   **Then** that entry's block is open, its row carries `aria-current="true"` and no chevron, and
   every other block is shut.
5. **Given** an entry on air in service A **When** the operator opens service B **Then** no block
   in B is open: nothing in B is live, and A's live position does not carry over.
6. **Given** blocks opened by hand **When** the service is opened by `Enter` on the marked picker
   row, or the dock resumes the service on air at load **Then** the same reset applies — every
   explicit open path behaves alike.

### US2 — What an open must not reset (P1)

**Why this priority**: two lifetimes are already accepted behaviour — a hand-opened block survives
a live-entry crossing (spec 198, `dock/R14`), and a re-read lands where the operator is
(spec 195, `dock/R13`). A reset hung on the wrong event would delete both, and the 10 s re-read
would shut the operator's blocks every ten seconds.

**Independent Test**: with a block open by hand, project another entry — the hand-opened block
stays open. Trigger a re-read — it stays open. Neither event is an open.

**Acceptance scenarios**

1. **Given** a block opened by hand in the open service **When** a crossing makes another entry
   live **Then** the hand-opened block stays open, exactly as `dock/R14` says today.
2. **Given** a block opened by hand **When** the dock re-reads the service (an `update` message or
   the 10 s timer) **Then** the block stays open and the list stays where the operator left it.
3. **Given** any of the above **When** the page reloads **Then** no override survives — the
   existing page-memory rule is unchanged.

### US3 — The reset is silent (P2)

**Why this priority**: an open already has its own motion and its own centring rule (spec 200). The
reset must not add a collapse animation, a scroll jump or a display write on top of it.

**Independent Test**: open a service after expanding blocks elsewhere — the new list paints shut
with no morph class on any inner, the display state's bytes are unchanged, and opening the on-air
service still centres its live entry.

**Acceptance scenarios**

1. **Given** blocks open in the previous service **When** a new service is opened **Then** no
   inner in the new list carries `is-morph`, and no block animates shut — the list is drawn shut.
2. **Given** any display state **When** a service is opened **Then** the stored state is
   byte-identical before and after the open: the reset writes nothing.
3. **Given** the service on air **When** it is opened from the picker **Then** the live entry is
   centred as spec 200's open rule already does, with its block open.

### Edge Cases

- **When** the opened service has no entries **Then** the list is empty and the reset is a no-op —
  no error, no note beyond the one the dock already draws.
- **When** the opened service contains section breaks **Then** break rows keep their hairline and
  no chevron; they have no block to reset.
- **When** a hand toggle's 230 ms morph is in flight as the operator opens another service
  **Then** the old list is discarded with its animation and the new list paints shut. The slice
  does not touch the morph machinery; measured across 10 opens, the new list carried no
  `.is-morph` frame and `scrollTop` never left 0. A switch attempted mid-crossing moved the scroll
  no further (0 across 900 ms into a 27-entry list, three attempts — those attempts could not
  confirm a morph was in flight, so this is a no-regression observation, not a morph measurement).
- **When** the operator opens a service while a go to stands alone **Then** the go to's block is
  not an entry block and is untouched by the reset.
- **When** the entry that was hand-opened is live in the *other* service **Then** its position in
  the browsed service is shut — liveness belongs to the service on air, not to an index.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | An explicit open of a service SHALL discard every entry-block override before the opened service's list is painted, so each block stands shut unless its entry is live. | `dock/R14` (modified) |
| FR-002 | The reset SHALL NOT collapse the live entry's block, SHALL NOT write the display state, SHALL NOT move `aria-current`, and SHALL NOT remove the live row's selected tint or its chevron-less header. | `dock/R14`, `dock/R3` (unchanged) |
| FR-003 | The reset SHALL apply to every explicit open path — a picker row's click, `Enter` on the marked picker row, and the on-load open of the service on air — and SHALL NOT apply to a re-read (`update` message or the 10 s timer). | `dock/R14` (modified), `dock/R11`, `dock/R13` (unchanged) |
| FR-004 | A live-entry crossing inside the open service SHALL keep a hand-opened block open, and a crossing SHALL NOT reopen a block the operator closed. | `dock/R14` (unchanged) |
| FR-005 | The reset SHALL be silent: no morph, no glide, no scroll or centring beyond what an open already does, and no broadcast on the display channel. | `dock/R14` (modified), `dock/R3` |
| FR-006 | Overrides SHALL remain page memory only: nothing persisted, no new storage key, no display-state field. | `dock/R14` (unchanged) |

### Key Entities

- **Entry block override** — the existing per-entry tri-state (`open` / `closed` / unset) in page
  memory. Its identity is *(the open service, entry index)*, not the index alone: an open of a
  service ends every override recorded before it. Unset behaves as the base rule (shut).
- **Effective open state** — unchanged: `live ? open : (override ?? closed)`. The live entry is
  read from the display state and the service currently open, so it survives the reset by
  construction rather than by an exception in the reset code.
- **Explicit open** — the dock's `openService` path: picker click, picker `Enter`, and the on-load
  resume of the service on air. A re-read (`loadServiceData` from `update` or the timer) is not an
  open.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Opening another service after a hand-open leaves zero non-live open blocks. | DOM read-back: `is-open` count among non-live rows = 0 (today: 1); both the click and the `Enter` open paths (`measurements-enter.json`) |
| SC-002 | Re-opening the same service leaves zero non-live open blocks. | DOM read-back (today: 1) |
| SC-003 | Three hand-opened blocks leak nothing into a shorter service. | open positions `[]` (today: `[1, 3]`) |
| SC-004 | The live entry's block is open on return to its service, with no chevron and `aria-current="true"`. | DOM read-back: open height > 0, chevron count 0 |
| SC-005 | A crossing and a re-read each keep a hand-opened block open. | open positions before = after, for both events |
| SC-006 | An open writes nothing: the stored display state is byte-identical, and no `is-morph` appears in the new list. | `localStorage` bytes compared across 10 opens; 0 morph frames, 0 channel messages (`measurements-open-write.json`) |
| SC-007 | The dock's own modules pass — `tests.e2e.test_obs_dock`, `test_obs_dock_follow`, `test_dock_goto`, `test_dock_keys`, `test_dock_bucket_head` and `multimedia.web.test_obs_dock` — and the new reset test fails on `develop` for the reset reason, not an import. A red that is identical on `develop` is carded with that evidence, never silently accepted. | suite output on the slice and on the base |

## UI/UX

No new element, no new colour, no new motion: the change is which blocks stand open after an open.
The numbers below are the preview's measured read-back (`preview/measurements-http.json`, dark,
1×, 1280×900 page with a 420 px dock frame).

- **Layout / position**: unchanged — the runner's list, its 2.1rem number gutter and its 44px
  inner indent are the dock's existing metrics (spec 119's mockup v70), untouched here.
- **Size / spacing**: a shut block measures 0 px; the same entry's open block measures 126 px in
  service 155 (a passage) and 70 px in service 149 (an image entry). After the reset every
  non-live block in the opened service measures 0 px.
- **Colour / typography**: unchanged — the live row keeps `--sidebar-selected-bg`, other rows
  keep the resting face and the `--icon-hover-bg` hover.
- **States**:
  - *rest after an open* — every non-live header `aria-expanded="false"`, chevron right-pointing;
  - *hand-expanded* — chevron rotated 90° down, block at its natural height (unchanged);
  - *live* — block open, no chevron, `aria-current="true"` (unchanged, and preserved by the reset);
  - *empty service* — no rows, no chevron, nothing to reset;
  - *section break* — hairline, no chevron, click inert (unchanged);
  - *reduced motion* — the reset paints no morph at all, so reduce and no-preference are identical;
  - *narrow (≤860 px)* — the preview's rail stacks under the dock; the dock's own fluid layout is
    unchanged.
- **Motion**: none added. The opened list paints shut in the same frame it is built; across 10
  measured opens (both behaviours) the new list carried **0** `.is-morph` frames, `scrollTop`
  never left **0**, the stored display state was **byte-identical** before and after every open,
  and **0** messages went to the display channel (`preview/measurements-open-write.json`). The
  crossing morph (230/400 ms) and the open's centring glide (spec 200) are untouched.
- **Responsive**: the dock fills the box it is given (spec 164); the reset is independent of width.

The preview for gate 1 (approval pending): `static preview at
specs/204-dock-entry-open-reset/preview/index.html` — the product's own rendered markup,
stylesheet and dock script, with the captured entry/screen islands of five real services; a
behaviour switch runs today's rule beside the drafted one.

## Assumptions

- **A1 — the reset trigger is an explicit open of a service.** Crossings and re-reads keep
  hand-opened blocks (spec 198's and spec 195's rules stand). The question putting the three
  candidate triggers to the owner timed out twice on 2026-11-19; the recommendation was recorded
  in its place and carried to gate 1, where the owner's **accept** confirmed it. Provenance: owner
  decision at gate 1 (2026-11-19), on the recorded recommendation.
- **A2 — "open another (or even the same) entry" reads as opening a service.** The measured defect
  is positional carry-over between lists: the picker's rows open services, and only an open draws
  a different list at the same indices. Expanding another *entry header* inside one service is a
  toggle, and it already opens only its own block. Provenance: reproduction on `develop`.
- **A3 — the live-entry exception means the entry on air in the service being opened.** While
  browsing a service that is not on air, nothing is live there and every block is shut.
  Provenance: the request's own exception, read against `liveEntry()`.
- **A4 — no new look.** The reset draws the existing collapsed list; there is no new control,
  badge, animation or copy. Provenance: the request asks for a state rule, not a surface.
- **A5 — the go to's block is out of scope.** It is drawn from the display state, not from an
  entry index, so no override applies to it. Provenance: code reading of `renderBlock`.

## Clarifications

### Session 2026-11-19

- Q: which events should reset the hand-opened entry blocks — an open of a service only, every
  live-entry crossing as well, or every list rebuild including the 10 s re-read?
  → A: **timed out, no answer**. Assumed A1 (an explicit open only; crossings and re-reads keep
  hand-opened blocks; the live entry keeps its open block). Offered for reopening at gate 1; the
  second reading would supersede spec 198's `dock/R14` crossing rule and its E2E pins, and the
  third would supersede `dock/R13`'s "a re-read lands where the operator is".
- **Gate 1, 2026-11-19 — the owner answered `accept`.** That takes the drafted reading (A1): the
  reset fires on an explicit open of a service only. The two timeout records above stand as the
  history of the question; no requirement moved, so this is a confirmation, not a revision.
- **Base move and card renumber, 2026-11-19 (after gate 2).** `develop` advanced from `85319b73`
  to `ab46f384` while the pack was in review (specs 203 and 205 landed), taking `ITEM-213` with
  spec 203. The branch was fast-forwarded, the card renumbered to `ITEM-216`, and the line
  citations re-read; the reproduction above stays recorded at the sha it was measured on, and the
  red-first run re-proves the defect on the new base. No requirement changed.
- The defect was reproduced before drafting, on `develop` (`85319b73`) against the live dock:
  position 4 opened by hand in service 155 stands open in service 149 (70 px) and again in 155
  (126 px); three hand-opened positions leak as `[1, 3]` into the 5-entry service. The cause is
  `static/web/obs-dock.js`: `entryOverrides` is a page-lifetime `Map` keyed by entry index,
  `openService()` resets the service's data but not the map, and `effectiveOpen()` reads it for
  whichever service is drawn.

Zero open markers remain.
