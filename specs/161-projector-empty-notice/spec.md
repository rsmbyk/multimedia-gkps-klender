# Feature Specification: the empty notice leaves the stage when Go To shows a passage or a song

**Slice**: `specs/161-projector-empty-notice`
**Branch**: `fix/161-projector-empty-notice`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29)
**Input**: "the empty items notice on projector screen should be hidden when opening contents from goto menu"

## What the page does today

A Tata Ibadah with no items renders one paragraph under the stage (`projector.html:55-57`):

```django
{% if not screens %}
<p class="projector__empty">Nothing to show yet: this Tata Ibadah has no items.</p>
{% endif %}
```

It is a **sibling of `#projectorScreens`**, not one of the `.screen` sections. The Go To paints a
passage or a song by activating a separate `.projector-detour` node inside the stage
(`renderDetour()`, `static/web/projector.js:1148`), and that function never touches the paragraph —
so while the detour is on screen the notice keeps its place directly below it. The detour's own
`.is-active` rule cannot cover it either: the paragraph is outside the stage.

Measured against the worktree's dev server, `develop` at `24a6d6d2`, `GET /projector?service=147`
(a service with no items), 1920×1080, `g` → `Mat 5` → `Enter`:

| | stage `#projectorScreens` | notice | detour words |
| --- | --- | --- | --- |
| box | 1856×945.6 at x 32, y 32 | 755×38.4 at x 582.5, y 977.6 | fitted 103px |
| painted | detour `.is-active` | `display: block`, no `hidden` attribute | head 174.4 tall at y 32; lines 707.6 at y 270.1 |

The notice begins at y 977.6 — exactly where the stage ends — so the congregation reads the
empty-service sentence in the band under the projected verse.

The same paragraph survives a second trigger. `reflow()` (`projector.js:1372`) swaps
`#projectorScreens`' children for the response's screens when another tab posts `update`, and it
never re-syncs the notice either: a service that gains its first entry while its projector page is
open paints that entry with the empty-service sentence still below it. `adoptService()`
(`projector.js:1429-1430`) is the only path that hides it, and only for a service adopted in place.

**Why the suite did not see it.** `tests/e2e/test_projector.py::test_an_empty_service_shows_its_empty_state`
asserts the notice's copy on an empty service and stops there. No case opens the Go To over an empty
service, and no case reads a re-read that brings a service its first screens, so the paragraph's
presence under painted content was never asserted against.

## User Scenarios & Testing

### US1 — A Go To passage or song has the whole stage (P1)

**Why this priority**: it is the reported symptom, and it is painted in front of the congregation for
as long as a passage or a song is projected outside the order of service.

**Independent Test**: open an empty service's projector page, press `g`, choose a passage: the notice
is gone, the passage's words sit alone on the stage; press `Escape`: the notice returns.

**Acceptance scenarios**

1. **Given** a projector page whose service has no items, **When** it is open, **Then** the notice is
   visible under the empty stage.
2. **Given** the same page, **When** a passage or a song chosen in Go To paints its detour, **Then**
   the notice is not painted, takes no box in the layout, and the detour occupies the stage the
   notice was holding back.
3. **Given** a detour is showing on that page, **When** the operator closes it with `Escape` (or the
   cue's `Back to service`), **Then** the notice is visible again, because the service is still empty.
4. **Given** the same page, **When** the operator steps to another screen of the same song detour,
   **Then** the notice stays hidden; only closing the detour brings it back.

### US2 — The notice follows what the stage holds, not the trigger (P2)

**Why this priority**: the report named Go To, but the paragraph is keyed on the page's first
response; any later content on the same page inherits the same defect. One rule covers both.

**Independent Test**: open an empty service's projector page, add its first entry from another tab,
post `update`: the entry paints on the stage and the notice is no longer under it.

**Acceptance scenarios**

1. **Given** a projector page whose service has no items, **When** a re-read brings the service its
   first screens, **Then** the notice is hidden in that same render and the first screen is painted
   alone.
2. **Given** the same page, **When** the re-read brings no screens (the service is still empty),
   **Then** the notice remains visible.

### Edge Cases

- **When** the detour's fetch fails and the panel reports `Could not load`, **Then** no detour is
  painted and the notice stays as it is — the page still shows nothing else.
- **When** the display is released (`data-showing="false"`) while a detour is painted, **Then** the
  notice stays hidden with the detour: opening the display again returns to the detour, not to a
  notice under it.
- **When** another Tata Ibadah is adopted in place from the operator dock, **Then** the notice is
  shown or hidden by the adopted service's own screens, as today.
- **When** a song detour's second screen is blank (a verse break), **Then** the notice stays hidden —
  the detour owns the stage whatever its screen holds.
- **When** a service that has screens loses its last entry while the projector page is open,
  **Then** the notice does not appear: it is rendered by the server only when the response carries no
  screens, and this slice does not add one. Recorded as out of scope, unchanged.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A projector page whose service has no items SHALL paint its empty notice while no screen and no detour is showing. | `projector/R2` (modified) |
| FR-002 | While a Go To detour is painted, the empty notice SHALL NOT be painted and SHALL take no box in the stage's layout, so the detour is laid out in the full stage. | `projector/R2` (modified) |
| FR-003 | Closing the detour SHALL restore the empty notice when the service is still empty. | `projector/R2` (modified) |
| FR-004 | A render or re-read that finds screens SHALL hide the empty notice in that same pass, and one that finds none SHALL leave it visible. | `projector/R2` (modified) |
| FR-005 | The notice's visibility SHALL be decided in one place from the page's state — the screens it holds and whether a detour is painted — instead of by the paths that happen to change them. | `projector/R2` (modified) |
| FR-006 | The E2E suite SHALL assert the notice's absence under a detour, its return when the detour closes, and its absence after a re-read brings screens. | `projector/R2` (modified) |
| FR-007 | Nothing else changes: the notice's copy, 28px size, colour and centred position where it shows; the Go To panel, the cue, the detour's fitting and its words; no route, payload or template copy. | `projector/R2` (modified) |

### Key Entities

- **Empty notice** — `p.projector__empty`, the server-rendered sentence for a Tata Ibadah with no
  items. Carries its copy in the response, one line, `aria-live`-less, decorative in role.
- **Stage** — `#projectorScreens`, the flex child that holds the service's `.screen` sections and the
  script-made `.projector-detour` node.
- **Detour** — the temporary screen the Go To paints for a passage or a song: one `section.screen
  .projector-detour` holding a head and lines, active while `is-active` is set.
- **Page state** — the two facts the notice is decided from: `screens().length` and `detour !== null`.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | No empty-service sentence is painted under projected Go To content. | On the running page: the notice's computed `display` is `none` and its box is 0×0 while the detour is `is-active`. |
| SC-002 | The detour gets back the band the notice held. | The stage's height gains the notice's own height — 38.4px, 945.6 → 984 at 1920×1080 and 765.6 → 804 at 1440×900 — the fitted lines grow 103 → 107px (83 → 87px at 1440), and the lines' centre moves 623.9 → 647.7 (+23.8px) at 1920×1080. |
| SC-003 | Closing the detour returns the notice without a reload. | `Escape` on the detour: notice `display: block` again, same 755×38.4 box at the same y. |
| SC-004 | The rule holds for content that arrives after load. | After a re-read with screens, the notice's computed `display` is `none`; after a re-read with none, `block`. |

## UI/UX

`static preview at specs/161-projector-empty-notice/preview/preview.html` — two boards, each the
product's real `.projector__screen` at 1920×1080 with the product's own stylesheets frozen at the base
commit and `projector.js`'s fitting copied verbatim; **Today** carries the notice under the detour,
**This slice** carries it `hidden`. The live route is the same page as it stands today:
`http://127.0.0.1:8765/projector?service=147`, then `g` → `Mat 5` → `Enter`.

The change adds no new surface: it removes one paragraph from a state. The numbers below are the
consequences of that paragraph's 38.4px band, measured on the live page at 1920×1080 and repeated on
the static boards.

- **Layout / position**: the notice is the stage's next sibling in a flex column; while it is painted
  the stage ends 38.4px above the page's bottom padding. Hidden, the stage is 984 tall instead of
  945.6, the detour's box runs 32–1016 instead of 32–977.6, and its lines box starts at y 279.3
  instead of 270.1 (h 736.7 instead of 707.6) — their centre 647.7 instead of 623.9.
- **Size / spacing**: notice 755×38.4, 28px/400, unchanged wherever it shows. Fitted detour lines
  103 → 107px at 1920×1080 and 83 → 87px at 1440×900, because the fitting measures the taller stage;
  the head stays at the stage's top and is 174.4 → 181.2 tall (140.5 → 147.3 at 1440).
- **Colour / typography**: unchanged — the notice keeps `var(--head-ink)` at 28px/400; the detour keeps
  its head colour and line treatment.
- **States**: empty service at rest (notice visible) · Go To detour open (notice hidden) · detour
  closed (notice visible) · re-read with screens (notice hidden) · re-read with none (notice visible)
  · fetch failed (notice visible, no detour) · display released (notice hidden with the detour).
- **Motion**: none added. The detour's own `is-active` fade is unchanged; the notice has no transition.
- **Responsive**: the rule does not depend on width. At 1440×900 the notice is 38.4 tall and the stage
  gains the same 38.4px (765.6 → 804); the fitted detour grows 83 → 87px there.

## Assumptions

- **Hidden means out of the layout, not invisible.** The ask is "hidden"; a reserved 38.4px band under
  every projected passage would read as a phantom gap, and the stage is a flex child that already
  takes the room the notice does not. Taken: the notice carries `hidden`, so `display: none`.
- **The notice returns when the detour closes.** It is the empty state of the service, and the service
  is still empty; leaving it away would make the page claim a service it does not have.
- **The re-read case is in scope.** It is the same paragraph and the same rule, reached by the trigger
  the page already has; fixing only the Go To path would leave the sentence under the first entry of a
  service that was empty when its projector opened.
- **A page that arrives with screens never gains a notice.** The paragraph is server-rendered only
  when the response has no screens; this slice does not add one client-side, so a service emptied while
  open shows an empty stage until reload — recorded as out of scope in the edge cases.
- **The empty state's copy stays.** No wording, size or colour is part of this slice.

## Clarifications

### Session 2026-10-29

- No questions were put: the request named the state and the trigger, and every default it left open is
  recorded under Assumptions. Zero open markers remain in this pack.
