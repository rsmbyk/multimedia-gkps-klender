# Feature Specification: An open modal keeps the scroll to itself

**Slice**: `specs/257-modal-scroll-containment`
**Branch**: `fix/257-modal-scroll-containment`
**Created**: 2026-11-28
**Status**: Accepted — gate 1, 2026-11-28 (permission to plan only)
**Capability read before writing**: `docs/spec/reading.md` (dialog geometry, preview scrolling and
scrollbar contracts; `R58` covers the editor's own edge and `R31` the preview's shortcut, but no
requirement covers where a wheel goes once a modal's own view stops scrolling, so this slice adds
one rather than rewriting either)
**Input**: "when you scroll when a modal is open and the view has reached the end of scrolling, or if
the view has no scrolling at all, the views behind it get the scroll instead"

## User Scenarios & Testing

### US1 — A wheel spent at the end of a modal's view stays there (P1)

**Why this priority**: This is the reported defect. Every modal scrollport — editor content, preview
body, picker options, media lists — used the browser's default `overscroll-behavior: auto`, so once
its own range was used up the remaining wheel delta chained to the next scrollport. In the live
before/after probe eight 220px wheel steps over a 617px editor range moved the document from
scrollY 600 to 1700; the slice leaves it at 600.

**Independent Test**: With the before and after servers side by side, open an editor whose content
has 40 rows, wheel past its end, and read the document offset: before it moves, after it does not.
The content still reaches its own maximum in both.

**Acceptance scenarios**

1. **Given** an open editor whose content has a 617px scroll range and a scrollable document behind it,
   **When** eight 220px wheel steps land over that content,
   **Then** `scrollTop` ends at 617 and the document's `scrollY` stays at its opening value.
2. **Given** an open Preview whose body has a 512px range,
   **When** the wheel passes that range,
   **Then** the body stays at 512 and the document does not move.
3. **Given** a nested picker whose options have an 870px range inside an editor whose content has a
   341px range,
   **When** ten 220px wheel steps land over the options,
   **Then** the options end at 870, the editor stays at **0** (before: 341), and the document stays put
   (before: 600 → 1480).

### US2 — A modal with nothing to scroll gives the wheel to nobody (P2)

**Why this priority**: The owner named this case separately. A short `.editor__content` is still
`overflow-y: auto` but has a zero range; with the default behaviour the wheel goes straight through
to the document (before: 600 → 2360 over eight steps). Containment on a zero-range scrollport alone
does not stop that in Chromium, so the document itself must be held still for as long as a dialog is
open.

**Independent Test**: Open the editor on a short form, wheel over both its content and its header:
the document offset does not change on either side of the modal.

**Acceptance scenarios**

1. **Given** an open editor whose content has no scroll range,
   **When** eight 220px wheel steps land over the content,
   **Then** the content stays at 0 and the document stays at 600.
2. **Given** the same short editor,
   **When** the wheel lands over the header instead,
   **Then** the document still stays at 600.
3. **Given** the dialog is closed again,
   **When** the page is scrolled,
   **Then** it scrolls normally from the same offset it had when the dialog opened (600).

### US3 — Every modal scrollport follows the same rule (P2)

**Why this priority**: The defect is a class, not one dialog. The editor's date popover, the media
tab's library panel, the Transfers and service-media lists, the Generate body and its chooser list,
and the Preview body all have their own scrollports; fixing only the reported one would leave the
same leak in the next modal opened.

**Independent Test**: Read computed styles on each named scrollport with a dialog open; every one
reads `overscroll-behavior-y: contain`, and the dialog itself reads `contain` too.

**Acceptance scenarios**

1. **Given** any native dialog from the reading or Generate surfaces,
   **When** it is open,
   **Then** the root's computed `overflow-y` is `hidden` and every named scrollport inside reads
   `contain`.
2. **Given** a nested confirmation dialog opened over another dialog,
   **When** it closes,
   **Then** the root stays held until the last `dialog[open]` is gone.

## Edge Cases

- A native dialog in the top layer does not chain to a sibling pane behind it (verified: a scrollable
  `.panel__body` stayed at 0); the leak is to the document and between nested scrollports inside the
  dialog. Both are covered.
- Wheel over the dialog's chrome — header, padding, title band — has no inner scrollport to absorb
  it; the root hold is what stops the page from moving.
- Keyboard arrow/Page-Down scrolling in the Preview body still works: the root hold stops propagation
  past the scrollport, not scrolling of the focused scrollport.
- The narrow-window drawer already holds the page with `:root[data-drawer-open] { overflow: hidden }`;
  the new rule uses the same declaration keyed on `dialog[open]`, so the two cannot disagree.
- Opening and closing a dialog causes no measured layout shift: `documentElement.clientWidth` was
  1200 before, during and after in both sides, and the dialog box measured 480×100 at (360, 300) in
  both.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | While any native `dialog[open]` is present, the document SHALL NOT scroll from wheel input over the dialog. | `reading/R66` |
| FR-002 | A modal's own scrollport SHALL keep scrolling to its range and SHALL NOT chain to an ancestor scrollport at its end. | `reading/R66` |
| FR-003 | A modal scrollport with no range SHALL pass no scroll to the document or to its parent scrollport. | `reading/R66` |
| FR-004 | The rule SHALL cover the editor content and date popover, picker options, media library panel, Preview body, Transfers and service-media lists, Generate body and chooser list, and the dialog elements themselves. | `reading/R66` |
| FR-005 | Closing a dialog SHALL restore normal document scrolling at the offset it had when the dialog opened, with no measured layout shift. | `reading/R66` |

### Key Entities

- **Modal scrollport** — an element inside an open `<dialog>` with `overflow-y: auto` (editor content,
  picker options, preview body, media lists, Generate body/chooser) or the dialog's own UA scrollport.
- **Document scrollport** — `document.scrollingElement`; the page behind the dialog, held while a
  dialog is open.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | All three live before/after cases keep the document at 600 while their inner scrollports reach their listed maxima | `specs/257-modal-scroll-containment/preview/probe.py`, two URLs, JSONL output |
| SC-002 | Every named scrollport computes `contain` and the root computes `hidden` with a dialog open | probe's computed-style block |
| SC-003 | No geometry or scroll-position regression on open/close | `preview/geometry.py`, both sides |
| SC-004 | The page scrolls again after close, from the same offset | `preview/geometry.py`, both sides |

## UI/UX

**Preview shapes** (both reachable by hand):

- Static: `specs/257-modal-scroll-containment/preview/index.html` — the real dialog markup and the
  real design CSS, with a "Before (base CSS)" / "After (slice CSS)" toggle, buttons to open the
  editor, the nested picker and the Preview, a tall page behind them, and a live readout of document
  offset, root overflow and inner `overscroll-behavior-y`. Its CSS is assembled by
  `preview/build_preview.py` from commit `1cd9f081` and the worktree, so the control cannot drift
  into a second "after".
- Live: `http://127.0.0.1:8765/` serves the slice worktree with the change applied to its own CSS;
  control at `http://127.0.0.1:63404/` serves unmodified `1cd9f081`. The probes use these two
  servers, not an injected stylesheet.

| Case (1200×700, Chromium, wheel steps of 220px) | Before = `1cd9f081` | After = slice worktree |
| --- | --- | --- |
| Editor content, range 617px — document `scrollY` | 600 → **1700** | 600 → **600** |
| Editor content own `scrollTop` | 0 → 617 | 0 → 617 |
| Short editor (no range) — document `scrollY` | 600 → **2360** | 600 → **600** |
| Wheel over editor header — document `scrollY` | 600 → 2360 | 600 → 600 |
| Nested picker: options `scrollTop` | 0 → 870 | 0 → 870 |
| Nested picker: editor content `scrollTop` (leak) | 0 → **341** | 0 → **0** |
| Nested picker: document `scrollY` | 600 → **1480** | 600 → **600** |
| Inner `overscroll-behavior-y` (editor / options) | `auto` / `auto` | `contain` / `contain` |
| Root `overflow-y` while open | `visible` | `hidden` |
| `clientWidth` before / open / after close | 1200 / 1200 / 1200 | 1200 / 1200 / 1200 |
| Dialog box before vs after | 480×100 at (360, 300) | 480×100 at (360, 300) |

No colour, typography or spacing changes: the only visible difference is that the page behind stops
moving. The numbers above are DOM offsets, computed styles and box geometry, not adjectives.

## Assumptions

1. Every native `<dialog>` in the app is a modal layer and should hold the page, including the small
   confirmation dialogs. This default was taken because the report names modals generally and no
   dialog in the codebase is a non-modal popover.
2. "The views behind it" means the document scrollport and, for nested popouts, the enclosing modal
   scrollport. A top-layer dialog does not chain to a sibling reading pane; this was measured, not
   assumed.
3. The wheel is the input under test; touch fling follows the same scroll-chaining model in Chromium
   but is not separately measured here.
4. The root hold is CSS-only: no `body` class is toggled, no listener is added, so a dialog shown by
   any script gets the same behaviour.
5. The change is a `patch` bump: a user-visible defect is repaired with no endpoint, schema or route
   change.
6. **Chronology**: the CSS edit is present uncommitted in the slice worktree and is the live preview;
   the spec pack is written after the measurement so its `UI/UX` values are the observed ones. No
   commit precedes Fold.
7. Card `ITEM-277` is reserved by the agent from the owner's report and sits in `Speccing`; only the
   owner promotes it to `Ready` at gate 1.

## Clarifications

None. Specify produced no `[NEEDS CLARIFICATION]` markers: the report named the behaviour, the
surface survey settled the class of scrollports, and the before/after probe settled the observable.
