# Feature Specification: pending state for the Search and Media Library rail tiles

**Slice**: `specs/245-rail-fetch-feedback`
**Branch**: `fix/245-rail-fetch-feedback`
**Created**: 2026-11-26
**Status**: Accepted at gate 1 (2026-11-26, `preview/combined.html`); final state accepted by the owner 2026-11-26
**Input**: "search and media library on rails should get the same behavior when fetching the page"; clarified to "its all of them: the rails lock, the reading page progress bar, and a little bit of placeholder"
**Demand**: `ITEM-260` (card opened at delivery, 2026-11-26)
**Capability**: `new: reading/R62` — extends `reading/R61`

**Clarification**: "make the placeholder to match the real layout" — the placeholder must carry
the destination's own markup and geometry, not a minimal sketch.

Spec 243 gave every in-page rail/sidebar fetch a locked item, section bars and a stage
placeholder. Two rail destinations sit outside that path: Search keeps its last result set
through `openSearch()` → `navigate()` and Media Library is a plain document link. This slice
brings both to the same visible pending state, with a placeholder built from the real Search
or Media Library page anatomy.

"Fetching the page" means the response that produces the destination page. For Search that
is the existing last-results/home fetch; for Media Library it becomes an in-page fetch so
the reading stage can show progress. No endpoint, schema or permission changes.

## Scope

### In scope

- The Search and Media Library rail tiles in the reading shell.
- The clicked tile's lock, the reading stage's 3px progress bar and `aria-busy`, and a small
  placeholder in the real page layout while either fetch is pending.
- Settlement, supersede, failure/full-page fallback and the accessible status announcement.

### Out of scope

- The other three rail sections, the two sidebar levels, dialog/editor loading, and
  projector/dock loading states — unchanged from spec 243.
- Changing what Search resolves to, Media Library's contents, or any server-side behaviour.

## User Scenarios & Testing

### US1 — A slow rail click is acknowledged at the tile and the stage (P1)

**Why this priority**: the reported symptom is a dead-looking site while a rail destination
loads; the acknowledgement has to appear before the response, not after.

**Independent Test**: open the reading shell, set a 1.2s delay, click the Search rail tile and
read the tile and stage before the response arrives.

**Acceptance scenarios**

1. **Given** a reading shell with either rail tile visible **When** that tile is clicked and
   the response is pending **Then** the tile's SVG renders at opacity `0.45` and carries
   `aria-disabled="true"`, with no spinner, label, edge fill or ring.
2. **Given** that pending fetch **When** it is in flight **Then** a 3px bar runs at the very
   top edge of the reading stage and the stage carries `aria-busy="true"`.
3. **Given** that pending fetch **When** it is in flight **Then** the stage shows the
   destination's own anatomy — Search results use the intro, result-group head with count,
   result rows with title/meta/excerpt and Show more; Search home uses the centred 96px logo
   and search input with its submit button, with the input's own text replaced by a grey bar; Media Library uses the intro, filter chips, result
   count and sort control, then three identical file-row skeletons with icon, name, meta, unused
   line and two action bars — no date-group headings and no seeded file names or data.
4. **Given** the pending state **When** the rail or a sidebar is clicked **Then** those
   containers stay interactive; only the clicked tile and the stage are locked.

### US2 — The pending state clears when the page arrives (P1)

**Why this priority**: a stuck bar or lock is worse than no feedback.

**Independent Test**: replay a click at 0 ms and at 2.5 s and inspect both states.

**Acceptance scenarios**

1. **Given** a pending Search or Media Library fetch **When** its page paints **Then** the
   tile is enabled, `aria-busy` is removed, the bar is hidden and the placeholder is replaced
   by the real page.
2. **Given** a fetch that fails into a full page load **When** the browser leaves **Then** the
   pending state remains visible until unload, as in R61.
3. **Given** a second rail click while a write is pending **When** it arrives **Then** the
   first fetch is cancelled, its tile unlocks and the bar and placeholder retarget to the new
   destination, following R61's write-vs-write rule.

### US3 — Existing destinations and reduced-motion behavior survive (P2)

**Why this priority**: the change is feedback, not navigation semantics.

**Independent Test**: click Search after a query and compare the arriving URL with today's
last-results destination; reload with `prefers-reduced-motion: reduce` and replay.

**Acceptance scenarios**

1. **Given** a saved last result set **When** the Search rail tile is clicked **Then** it still
   opens that result set; the lock, bar and placeholder do not change the destination.
2. **Given** reduced motion **When** a fetch is pending **Then** the bar does not sweep while
   the lock, `aria-busy` and placeholder text remain.
3. **Given** a polite status region **When** the fetch starts and settles **Then** it announces
   opening and arrival once each without moving focus.

### Edge Cases

- **When** a click is repeated on the same locked tile **Then** no second fetch starts.
- **When** the delay is so short that the response arrives in the same frame **Then** the
  pending state may be skipped without leaving residue.
- **When** the shell is below 720px **Then** the placeholder keeps the same relative offsets
  from the stage as the real page at that width.
- **When** Media Library is loaded directly by URL **Then** the tile shows its server-rendered
  current-page marker and no pending state.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Search and Media Library rail tiles MUST fetch their destinations in place through the reading shell's single navigation choke point. | `new: reading/R62` |
| FR-002 | At activation the clicked tile MUST lock: its SVG at opacity `0.45`, `aria-disabled="true"`, no spinner/label/edge/ring, and re-activation impossible until settlement. | `new: reading/R62` |
| FR-003 | While the fetch is pending the reading stage MUST show a 3px bar flush with its top edge and carry `aria-busy="true"`. | `new: reading/R62` |
| FR-004 | While the fetch is pending the stage MUST show a placeholder built from the destination's own markup and classes — Search results, Search home or Media Library — at the same content offsets as the real page. | `new: reading/R62` |
| FR-005 | The rail and sidebars MUST remain interactive during the pending state; only the clicked tile and the stage are locked. | `reading/R61` |
| FR-006 | On success, failure and supersede the lock, bar, `aria-busy` and placeholder MUST clear; on full-page fallback they remain until unload. | `reading/R61` |
| FR-007 | A later page-writing click MUST cancel the in-flight fetch and retarget the bar and placeholder, following R61. | `reading/R61` |
| FR-008 | The Search tile MUST keep its last-results destination and Media Library its `/media-library/` destination. | `new: reading/R62` |
| FR-009 | The polite status region MUST announce opening and arrival once each without moving focus; reduced motion stops the bar sweep but keeps the other pending states. | `reading/R61` |
| FR-010 | No endpoint, schema or permission behaviour changes. | `new: reading/R62` |
| FR-011 | A direct Media Library load that bypasses the rail placeholder SHALL show a loading count and loading empty line until companion status/files and service references resolve, then render once; the loading line SHALL carry a small spinner centred above the text, clearing with it. | `new: reading/R62` |
| FR-012 | While a destination placeholder is shown, the previous stage content — search home, search results or the reading article — SHALL be hidden, not merely covered by a shorter skeleton. | `new: reading/R62` |

### Key Entities

- **Rail tile** — the existing Search / Media Library anchors in the reading shell; identity is
  the element id, state is locked or unlocked.
- **Pending fetch** — one in-flight navigation with destination, destination class (stage write),
  source tile and the sections it will update.
- **Stage placeholder** — a temporary node in the reading stage carrying the destination's own
  classes and row anatomy with bars where content is not yet known, positioned from the stage's
  own padding, removed on settlement.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Every simulated slow click (>=1200ms) shows the lock, bar and placeholder before the response. | Probe all four delay/click combinations in `preview/probe.py`; zero misses. |
| SC-002 | Placeholder content starts at the same offsets as the real page. | Computed box: stage +64px horizontal, +40px vertical at 1440px; 0px difference. |
| SC-003 | No pending-state residue after settlement. | `aria-busy` absent, bar hidden, placeholder hidden, tile enabled after each replay. |
| SC-004 | The rail and sidebars remain clickable while a tile is pending. | Click a different rail tile mid-fetch and observe the supersede rule. |

## UI/UX

Accepted draft preview: `preview/combined.html`; index and the three superseded options are in
`preview/index.html`. All numbers below are from `preview/probe.py` at 1440×900, dark mode,
1× device scale. The preview carries a 152px control bar, so stage-relative offsets are the
portable values.

- **Layout / position**: reading stage box in the preview x=376, y=152; placeholder content
  x=440, y=192 — the real `.read` box is also x=440, y=192, so the placeholder is +64px
  horizontal and +40px vertical from the stage.
- **Size / spacing**: progress bar 3px high, `0px` from the stage's top edge; the Search
  results placeholder shows two `.result-group` blocks (Passage 3 rows with Show more, Song
  2 rows), the Search home placeholder a 96px logo and the real input/submit pair, and the
  Media Library placeholder a 42px file icon and three identical `.media-library__file` rows,
  each with a 36px cloud bar and a 36px remove bar; no group headings or seeded file data.
- **Colour / typography**: tile SVG keeps its own artwork colour at opacity `0.45`; the bar
  uses `--active-bg` over a 22% tint of the same token; placeholder text uses `--ink` and
  `--head-ink` through the app's existing result/media classes.
- **States**: idle · loading (tile locked, bar sweeping, placeholder shown) · settled (real
  page) · reduced motion (no sweep) · quick response (no visible pending state).
- **Motion**: single 1.05s indeterminate sweep with the app's `--ease-timing` curve; no
  separate fade or delay, so lock, bar and placeholder start together.
- **Responsive**: at ≤720px the placeholder keeps the stage's own horizontal padding, as the
  real page does.

## Assumptions

- "Make the placeholder match the real layout" means seeding from the destination's own
  markup and classes, with bars only where content is not yet known — a revision of the
  earlier minimal-sketch assumption shown in the first draft preview.
- Search has two placeholder shapes: results when a last result set exists, home otherwise;
  the preview toggles between them.
- Media Library becomes an in-page fetch because the progress bar is on the reading page;
  a full document load cannot paint it.
- Search's destination is unchanged: the saved last result set when one exists, otherwise the
  home search. `openSearch()` gains only the `source` option needed to lock the clicked tile.
- The 152px preview control bar is preview chrome only and is not part of the product.

## Clarifications

### Session 2026-11-26

- Q: Which fetch behavior should the Search and Media Library rail tiles get? → A: all three —
  rail lock, reading-page progress bar and a little bit of placeholder.
- Q: Should each candidate be previewed before choosing? → A: yes, three separate previews,
  then choose; the combined shape was chosen after reviewing them.
- Q: How large should the placeholder be? → A: first a one-line sketch; revision — match the
  real layout of each destination. The sketch is superseded, not deleted; the preview keeps
  it in the earlier candidate pages for the record.

## Traceability

- **Preview**: `specs/245-rail-fetch-feedback/preview/combined.html`
- **Superseded candidates**: `preview/option-a.html`, `option-b.html`, `option-c.html`
- **Measurements**: `preview/probe.py`
- **App tests**: to be written in Plan/Checklist; none authorized by gate 1.
