# Feature Specification: The Media Library list holds still while it refreshes

**Slice**: `specs/148-media-library-refresh-flicker`
**Branch**: `feat/148-media-library-refresh-flicker`
**Created**: 2026-10-28
**Status**: Accepted (owner, gate 1 and gate 2, 2026-10-28)
**Input**: "why does the screen (or view?) flicker/shake when i click the upload button?" — owner report with a screencast of `/media-library/` on `localhost:63404`, whose list jumps twice, once per upload click

## What the page does today

Every action on `/media-library/` that ends in `refresh()` draws the file list **twice**.
`static/web/media-library.js:146` is the refresh:

```js
return Promise.all([request('/status'), request('/files')]).then(function (results) {
  files = results[1].files || []; uses = null; setStatus(results[0]); render();   // :148
  return fetch(page.dataset.referencesUrl, …)                                    // :149
    .then(… references …)
    .then(function (references) {
      uses = references.uses || {}; protectedFiles = …;
      return write('/references', …).then(function (synced) {
        files = synced.files || []; render(); return true;                        // :155
      });
    })
    .catch(function () { uses = null; render(); return false; });                 // :157
```

`render()` (`:93`) is `list.replaceChildren()` followed by a full rebuild of every row. The first pass
runs with `uses = null`, and a row's `used by` block is only drawn when `uses` is known — otherwise
`:67` draws the one-line `Service uses unavailable` placeholder. So the first pass draws every row
**shorter** than the second pass, and the list below the first row jumps up and then back.

The two blocks that decide a row's height, `static/styles/design/components.css:627-628`:

| Line | Block | Box |
| --- | --- | --- |
| `:627` | `.media-library__unused` (the placeholder) | `margin-top: 4px`, 12px text → one 18px line |
| `:628` | `.media-library__uses` (the references) | `margin-top: 8px`, `gap: 4px`, 12px text → 18px for one reference, 40px for two |

Measured on the owner's own library (`/media-library/`, 1920×1100, the page on `localhost:63404`),
sampling layout every animation frame:

| | with references | first pass (`uses = null`) | after |
| --- | --- | --- | --- |
| rows 1–8 | 119 / 101 / 123 / 101 / 101 / 101 / 101 / 97 px | 97 px each | restored |
| `#mediaFileList` height | 1024 px | **956 px** (−68) | 1024 px |
| row 1 top | 258 | 258 | 258 |
| row 2 top | 377 | **355** (−22) | 377 |
| row 3 top | 478 | **452** (−26) | 478 |
| row 4 top | 653 | **601** (−52) | 653 |

The first row does not move — nothing above it changed height — and every row below it shifts by the
sum of the shrinking rows above it, which is why the jump grows down the list.

The intermediate pass is on screen for 16 ms in a fast run and 85 ms when the references request is
slower (38 ms on the page's first load). The owner's screencast shows exactly that: the first row's
name and metadata stay put, everything from its `used by` line down moves up 22px, growing to 26px+
further down, and returns — twice, once per upload click.

The actions that end in `refresh()`, and therefore jolt the list: **Share online** (`:82`),
**Remove** — even before the confirmation is answered (`:90`) — **Remove file** confirmed (`:141`),
**Save setting** (`:139`), and the page's own first load (`:160`). The 2s status poll
(`static/web/media-handoff.js:155`, delivered through the `media:status` listener at `:161`) calls
`render()` with unchanged data and does **not** move anything; that was measured too, so this slice
leaves it alone.

## User Scenarios & Testing

### US1 — The list never moves while it refreshes (P1)

**Why this priority**: this is the report. The jump lands on the page's most-used actions — the one
that uploads a file, the one that removes one — and it reads as the page re-drawing itself under the
operator's eyes. A list that shifts 22px under a click also moves whatever the pointer is on.

**Independent Test**: drive one refresh from a click, sample `#mediaFileList`'s rows every frame, and
compare each row's top against its settled top: one value per row, from the click to the settled list.

**Acceptance scenarios**

1. **Given** a library whose files carry service references, **When** the owner clicks a row's
   **Share online**, **Then** no row's top changes in any frame between the click and the settled list.
2. **Given** the same library, **When** the owner opens **Remove** and cancels the dialog, **Then** no
   row's top changes in any frame.
3. **Given** the same library, **When** the owner saves a **Media Library setting**, **Then** no row's
   top changes in any frame.
4. **Given** the page is being opened, **When** the list appears, **Then** it appears once, already
   carrying its references, and no frame shows a row shorter than its settled height.
5. **Given** a transfer is running and the 2s status poll re-renders the list, **Then** nothing moves.

### US2 — A file whose references are known never shows the placeholder (P2)

**Why this priority**: the shrink is the placeholder. Even without a height change it would flash
`Service uses unavailable` over a file the page already knows is used by two services — a statement
that was true for one frame and never true of the data.

**Independent Test**: hold the references response open for 300 ms and sample every frame; no frame
may contain a `.media-library__unused` line inside a row whose file has references.

**Acceptance scenarios**

1. **Given** the list has already drawn with its references, **When** any refresh re-renders it,
   **Then** no frame contains `Service uses unavailable` for a file whose references were known.
2. **Given** the references request fails, **When** the list draws, **Then** it draws once with
   `Service uses unavailable` and stays where it is.
3. **Given** a first load that is still waiting for its references, **When** the list has not drawn
   yet, **Then** it does not draw an empty or placeholder list first.

### Edge Cases

- **When** the library holds no files, or the companion is unavailable **Then** the empty state and
  the disconnected copy are drawn exactly as today, in one pass.
- **When** a file has two or more references (the tallest row, 123px) **Then** it is still drawn at its
  full height in the only frame it appears in.
- **When** the owner changes a filter, a sort or the Unused toggle during a refresh **Then** the list
  re-draws from the current data, still without an intermediate pass.
- **When** the references request is slow (300 ms, or a timeout) **Then** the list appears once, later,
  and does not appear early in a shorter shape.
- **When** `prefers-reduced-motion` is on **Then** the requirements are unchanged — there is nothing to
  animate; the jolt is layout, not motion.
- **When** the page is at a narrow width where a reference line wraps to three lines **Then** the same
  single pass applies; the height rule is not a constant this slice writes.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A refresh SHALL draw the file list at most once. It SHALL NOT draw an intermediate state in which a file's known service references are replaced by the `Service uses unavailable` placeholder. | `new: reading` → R22 |
| FR-002 | No row SHALL change position during a refresh: every frame from the triggering action to the settled list shows the same row tops as the settled list. | `new: reading` → R22 |
| FR-003 | The page's first load SHALL draw the list once, already carrying its references; when the references request fails, it SHALL draw once with the placeholder and keep it. | `new: reading` → R22 |
| FR-004 | The 2s status poll SHALL keep re-reading the companion and SHALL remain visually inert while the data has not changed. | `new: reading` → R22 |
| FR-005 | Nothing else about the page changes: the files and their order, the rows' markup and heights, the filters, the sort, the Unused toggle, the cloud control's states, the dialogs, the requests made to the companion, and the page's document title. | `new: reading` → R22 |

### Key Entities

- **Refresh** — one read of the companion's `/status` and `/files` plus the same-origin references
  response, ending in one draw of the list. No field is added, removed or re-shaped by this slice.
- **File row** — one companion file: `name`, `family`, `uploaded_at`, `size`, its `uses` (service
  references) and its cloud state. The row's height is a function of its `uses`: 97px with none,
  101px with one 18px line, 119–123px with a wrapped or two-line block.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Across a refresh driven by Share online, Remove-cancelled, Save setting and a first load, the number of distinct tops per row is 1. | E2E: `requestAnimationFrame` sampling of every `.media-library__file`'s `getBoundingClientRect().top` from the click to the settled list |
| SC-002 | With the references response held for 300 ms, the number of sampled frames containing `.media-library__unused` inside a row whose file has references is 0. | E2E: same sampler, over the held window |
| SC-003 | One refresh replaces `#mediaFileList`'s children at most once. | E2E: `MutationObserver` counting `childList` replacements between the click and the settled list |
| SC-004 | The list's height after the first load equals its settled height, and never grows after it appears. | E2E: `#mediaFileList` `getBoundingClientRect().height`, sampled every frame |
| SC-005 | The row count, order, text, cloud state and document title after a refresh are identical to today's. | E2E: the existing `tests/e2e/test_media_library.py` cases re-run unchanged |

## UI/UX

**Live preview at `http://localhost:63404/media-library/`** (the compose `web` service on `develop`,
already running). There is no new look to approve: this slice changes *when* the list is drawn, not
what it looks like. The gate's material is therefore the defect itself, reproducible by hand on that
route — click a row's **Remove** and cancel, or click **Settings** and save, and the list jumps
22px and back. The measured numbers are in *What the page does today*.

- **Layout / position**: unchanged at rest — rows 97/101/119/123px, list 1024px, first row top 258 at
  1920×1100. What changes is that those are the only values any frame shows.
- **Size / spacing**: unchanged; `.media-library__uses` keeps `margin-top: 8px`, `gap: 4px`, 12px text,
  and `.media-library__unused` keeps `margin-top: 4px`, 12px text. No `min-height` is introduced.
- **Colour / typography**: unchanged.
- **States**: the list's own states are reloading · empty · disconnected · filtered-empty · populated,
  and each must reach the same settled geometry in one draw. Hover, focus, active and disabled states
  of the row controls are untouched.
- **Motion**: none is added. The requirement is the absence of a layout jump during the 16–85ms window
  that draws it today.
- **Responsive**: unchanged at every width; the reference block wraps by its own text, and this slice
  does not write a height constant.

## Assumptions

- **The fix belongs in the refresh/render sequence, not in CSS.** A `min-height` on the `used by` block
  would hide the jump while still flashing `Service uses unavailable` over a file whose references are
  known, and would move every row's settled height. The requirement is one draw, so the drawing is
  what changes.
- **The first paint may arrive one same-origin round-trip later.** Drawing the list only once the
  references are known is what removes the first-load jump; the alternative — draw immediately, expand
  after — *is* the defect. The references response is served by this same Django process.
- **The 2s poll keeps its full rebuild.** It was measured inert with unchanged data, and turning
  `render()` into a differencing update is a redesign nobody asked for. It is named out of scope.
- **The placeholder stays for the case it is for.** A failed references request still draws it; that is
  the honest degraded state and it now costs no jump.
- **In-flight slices 145, 146 and 147 also touch this page.** This slice changes `refresh()` and the
  render call sites only — not the row markup, the file metadata line or the grouping — so their
  changes land independently.
- **No API, template, CSS or server change.** `static/web/media-library.js` plus an E2E case; the
  companion's endpoints, the `/media-library/references/` view and the page's markup are untouched.
- **The verification seam is E2E.** The defect is a transient that a settled-DOM assertion passes
  straight through, so the test samples frames rather than the end state.

## Clarifications

### Session 2026-10-28

- No open items. The mechanism was measured on the running page before Specify (layout sampled every
  animation frame, on two separate refreshes and the first load), so zero open markers remain. Both
  readings the request left silent are listed under Assumptions; the last row is the one that can be
  vetoed at the gate.
