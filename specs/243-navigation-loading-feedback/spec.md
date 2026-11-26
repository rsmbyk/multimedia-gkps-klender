# Feature Specification: visible pending state for rail and sidebar fetches

**Slice**: `specs/243-navigation-loading-feedback`
**Branch**: `fix/243-navigation-loading-feedback`
**Created**: 2026-11-25
**Status**: Accepted (gate 1, preview v14)
**Input**: "when you try to open anything from the sidebar, if the network is a slightly bit slow, the page and the sidebar do not show any sign that it is fetching something. sometimes the operators might think that the site is frozen"
**Demand**: `ITEM-258` (card opened at delivery)
**Capability**: `new: reading/R61`

Every in-page fetch starts at `navigate()` in `static/web/reading.js:1494`: rail
section switches (`:1329`), first-level rows (`:832`), second-level chapter/song
rows (`:900`), search and results (`:1957-1981`). The function tracks `navBusy`
but paints nothing, so a slow response looks like a dead site. Editor loads and
some projector/dock surfaces already have their own feedback; this slice is the
reading shell's navigation only.

"Changes the reading page" means **writes into the stage**, not which panel
fetched. Opening a song, a Bible verse/passage or a service writes; opening a
rail section, a Bible chapter-number list or a songbook does not. The
chapter-number list is list-only; the verse opened from it is the write.

## Scope

### In scope

- Rail and both sidebar levels in the reading shell, including the first-level row and the
  chapter-number / song / service-entry level.
- Search and history traversal to the extent they pass through `navigate()`; they inherit the
  same pending state and write-vs-list classification.
- Item lock, section bars, stage placeholder, supersede/coexist behaviour and the accessible
  status announcement.

### Out of scope

- Editor/dialog loading (specs 093 and 095) and projector/dock loading states.
- Full document loads outside the reading shell, offline saved-copy generation, and any
  endpoint, schema or permission change.

## User Scenarios & Testing

### US1 — A list-only fetch leaves the reading page alone (P1)

**Why this priority**: the common slow case is a rail or first-level click; it
must be acknowledged without inventing a page transition.

**Independent Test**: open `/`, click the Kidung rail with a delayed response,
and read the stage before and after. The same passage stays displayed the whole
time; only the rail item dims and the relevant list top shows a bar.

**Acceptance scenarios**

1. **Given** a rail click on a slow network **When** the fetch starts **Then**
   that rail item is disabled and dimmed, and a bar appears at the very top edge
   of the first-level sidebar, and of the second-level sidebar when it is open
   and will be refreshed.
2. **Given** that fetch **When** it is in flight **Then** the reading stage has
   no `aria-busy`, no loading bar and no placeholder; whatever was displayed
   stays displayed.
3. **Given** a first-level row click (songbook/book) **When** it fetches
   **Then** the row dims and a bar appears at the very top edge of the
   second-level sidebar only.
4. **Given** the chapter-number list **When** it fetches **Then** the clicked
   row dims, the second-level bar runs, and the stage is untouched.

### US2 — A page write disables the stage and seeds a layout-matched placeholder (P1)

**Why this priority**: this is the case where the stage will change; the
operator needs to see both the lock and what is coming.

**Independent Test**: click a leaf that opens a song, a verse/passage or a
service with a delayed response. Before the response the stage is disabled,
its bar runs, and the placeholder has the final page's anatomy with known
sidebar data filled in.

**Acceptance scenarios**

1. **Given** a song write **When** it is pending **Then** the stage carries
   `aria-busy="true"`, a 3px bar runs at its very top edge, and the placeholder
   uses the song layout: `HAL n` eyebrow, title from the clicked row, numbered
   `p.v` rows with multi-line bars.
2. **Given** a verse/passage write **When** it is pending **Then** the
   placeholder uses the Bible layout with `read__title`, `read__lang`,
   `read__ed`, `read__sec` and `v__n` verse numbers, seeded with the book name
   and chapter number.
3. **Given** a service write **When** it is pending **Then** the placeholder
   uses the Tata Ibadah layout with `Tata Ibadah` eyebrow, `entry__start` add
   buttons and `tatib__item` / `read__sec` / `read__sub` rows.
4. **Given** any placeholder **When** it is displayed **Then** its content
   starts at the same offsets as the real `.read` (64px left, 40px top at
   1440px), not at the stage corner.
5. **Given** a stage write settles **When** the fetched page paints **Then**
   `aria-busy` is removed, the bar clears and the real content replaces the
   placeholder.

### US3 — Another click supersedes or coexists by stage-write class (P1)

**Why this priority**: a second click must never appear to be ignored while a
slow first fetch is still live.

**Independent Test**: start a page write, then click another item; check the
status of both items and which bars remain.

**Acceptance scenarios**

1. **Given** a page fetch in flight **When** another page-writing item is
   clicked **Then** the first fetch is cancelled, its item unlocks, the new
   item locks, and the stage bar and placeholder retarget to the new item.
2. **Given** a page fetch in flight **When** a list-only item is clicked
   **Then** the first fetch continues, the stage bar remains, and the list item
   gets its own top-edge bar.
3. **Given** a list-only fetch in flight **When** a page-writing item is
   clicked **Then** the list fetch is cancelled and the stage write begins.
4. **Given** a cancelled item **When** it unlocks **Then** it can be clicked
   again immediately.
5. **Given** a fetch that fails into a full page load **When** the browser
   navigates away **Then** the pending state stays visible until unload.

## Requirements

- **FR-001** The clicked rail/sidebar item MUST enter a locked state at the
  moment of activation, and MUST NOT be re-activated until that request settles.
  On a sidebar row, its edit/delete/add controls MUST be disabled for the same
  period.
- **FR-002** The lock visual MUST be dim only: the rail icon stays in place at
  reduced opacity; a sidebar row dims. No spinner, label, edge fill or ring.
- **FR-003** Each in-flight fetch MUST show a 3px bar at the very top edge of
  every section it will update: first-level sidebar, second-level sidebar
  and/or reading page.
- **FR-004** A fetch that does not write to the reading page MUST leave the
  stage exactly as displayed: no `aria-busy`, bar or placeholder.
- **FR-005** A fetch that writes to the reading page MUST set `aria-busy` on
  the stage, show the top-edge bar and replace the stage with a placeholder
  seeded from the clicked item's sidebar data.
- **FR-006** The placeholder MUST use the real layout anatomy of Bible, song
  or Tata Ibadah pages and start at the same offsets as the real `.read`. A
  song without a hymn number MUST seed its eyebrow from the selected songbook
  name.
- **FR-007** A later click MUST cancel the in-flight fetch unless the in-flight
  fetch writes to the reading page and the new click does not; in that case
  both requests proceed and each gets its own bar.
- **FR-008** All pending state MUST clear on success, failure and supersede;
  on full-page fallback it MUST remain until unload.
- **FR-009** No loading UI may disable the rail or any sidebar container; only
  the clicked item (and the stage for writes) is locked.
- **FR-010** The function `navigate()` MUST remain the single choke point for
  pending state, including search and history traversal.

## UI/UX

Accepted preview: `preview/index.html`, with `preview/grid-v14.png` as the
contact sheet. Measured at 1440×900:

| Item | Measured value |
| --- | --- |
| Rail icon while locked | `display: block`, opacity `0.45` |
| Sidebar row while locked | opacity `0.58` |
| Bar height / top offset | 3px, `0px` from its section's top edge |
| Bar delay | shown with the fetch; no separate delay was accepted |
| Placeholder `.read` origin | x=520, y=218 — same as real `.read` (stage x=456, y=178, padding 64px/40px) |
| Bible placeholder | 5 numbered `p.v` rows |
| Song placeholder | 3 numbered `p.v` rows, 3 bars per verse |
| Service placeholder | 3 `tatib__item` rows |
| Narrow width | placeholder horizontal padding 18px at ≤720px |

Earlier rounds are kept in `preview/index-v1.html` through `index-v13.html` and
as thumbnails/links in the accepted page's **Previous** row. The cited research
is `preview/loading-patterns-research.md`; the rule history, including the
deviation from first-party guidance against disabling controls, is
`preview/rules-v5-draft.md`.

## Accessibility

- Set `aria-busy="true"` on the stage only for writes; remove it on settlement.
- Locked items carry `aria-disabled="true"`; the stage is `pointer-events: none`
  while busy but the rail and sidebars remain interactive.
- A pre-rendered polite `role="status"` region announces opening and settlement
  once; focus is not moved by the status.
- Reduced motion stops the bar's sweep; the locked state and placeholder text
  remain.

## Assumptions / deltas from the research

- First-party guidance (Primer, Wix) discourages disabling controls during
  loading. The owner explicitly overrode it: re-triggering the same item while
  its fetch is live must be impossible. This deviation is deliberate and is
  recorded rather than hidden.
- No percentage is available for a fragment fetch, so the bar is an
  indeterminate sweep, not a progress bar.
- Search and history traversal use the same pending mechanism through
  `navigate()`; their per-surface classification is unspecified here and uses
  the same write-vs-list rule.

## Clarifications (after gate 2)

These asks arrived while the build was live, after the spec and plan had been accepted. They touch
the same files and tests, so they were treated as in-slice extensions; the gates were not
re-presented. Each extends an existing requirement rather than appearing only in code.

- "the song reading page placeholder is kinda off the actual layout (the songbook and song numbers,
  title's case, the placeholder above the numbered verses)" — song eyebrow uses the row's displayed
  number, title uses the displayed title with its case, and no section bar sits above the verses.
  Extends FR-006.
- "non-hymn book's song does not have songbook name in its placeholder" — when a song row has no
  number code, the eyebrow is the selected songbook's name. Extends FR-006.
- "the control (edit, delete, etc) buttons on the sidebar row should also be disabled while
  fetching" — the row's controls share the lock and are restored with it. Extends FR-001.

## Traceability

- **Preview**: `specs/243-navigation-loading-feedback/preview/index.html`
- **Research**: `preview/loading-patterns-research.md`
- **Rules / accepted deltas**: `preview/rules-v5-draft.md`
- **App tests**: to be written in Plan/Checklist; none authorized by gate 1.
- **Implementation**: to be planned; no app code changed by this slice yet.
