# Feature Specification: Bible rail from Media Library opens its books

**Slice**: `specs/246-media-library-bible-rail`
**Branch**: `fix/246-media-library-bible-rail`
**Created**: 2026-11-27
**Status**: Accepted (gate 1, 2026-11-27)
**Input**: "when i open bible from rail while in media-library page, it says 'no books yet'. but when i open another menu from rails first (or afterwards) and open it again, it shows normally"
**Demand**: `ITEM-263` (created in this slice)
**Capability**: `new: reading/R63` — Media Library is not a reading section

The Media Library page is rendered from the reading shell but carries no sidebar lists. The shell's
base template still declares `data-section="alkitab"` on every page that does not name a section, so
the live shell believes Alkitab is already selected when Media Library is on stage. A click on the
Alkitab rail tile therefore takes the toggle branch — it opens the empty sidebar instead of fetching
`/bible/`. The operator sees "No books yet." until another section is fetched first.

The fix gives the Media Library page its own section identity. Any section rail click from that page
is then a section change, so the shell fetches that section's root and its real sidebar rows. No
endpoint, schema, permission, CSS or JavaScript behaviour changes; only the server-rendered
`data-section` value of the Media Library page.

## Scope

### In scope

- The `data-section` value carried by `/media-library/`, both on a direct load and when the shell
  swaps the page in from the rail.
- The first Alkitab, Kidung and Tata Ibadah rail click after Media Library is on stage.

### Out of scope

- Search / Media Library pending-state feedback (`reading/R62`) — unchanged.
- Media Library's file list, dialogs, companion and cloud state — unchanged.
- Sidebar contents, selection state and navigation of the three reading sections — unchanged.
- Projection/dock surfaces — unchanged.

## User Scenarios & Testing

### US1 — The Bible rail fetches its books on the first click from Media Library (P1)

**Why this priority**: the reported failure has a simple workaround but leaves a visibly broken
empty sidebar on the normal path.

**Independent Test**: open `/`, click the Media Library rail tile, then click the Alkitab rail tile
and count `/bible/` requests and `#panelBody .book` rows.

**Acceptance scenarios**

1. **Given** the Media Library page on stage **When** the shell reads its section **Then** that
   section is `media-library`, not `alkitab`, `kidung` or `tatib`.
2. **Given** that page **When** the Alkitab rail tile is clicked **Then** the shell fetches
   `/bible/` in place and the sidebar shows its real book rows; no `No books yet.` empty state is
   visible.
3. **Given** that page **When** the Kidung or Tata Ibadah tile is clicked first **Then** that
   section's root is fetched, and a following Alkitab click fetches `/bible/` as in scenario 2.

### US2 — Section switching elsewhere is unchanged (P2)

**Why this priority**: the fix changes a value read by the shared rail handler; existing navigation
must keep its behaviour.

**Independent Test**: from a reading section, click a different section tile and compare the
fetched URL and sidebar state with the current app.

**Acceptance scenarios**

1. **Given** a reading section on stage **When** its own rail tile is clicked **Then** the shell
   still toggles the open panel without a fetch.
2. **Given** a reading section on stage **When** another section's tile is clicked **Then** the
   shell fetches that section's root as before.
3. **Given** a direct load of `/media-library/` **When** the page paints **Then** its own rail tile
   is marked current by the server and the stage shows the library, with no pending-state residue.

### Edge cases

- **When** the Media Library page arrives through the rail's in-place fetch **Then** the swapped
  shell adopts the same `media-library` section as a direct load.
- **When** the browser is below 720px **Then** the rail click still performs a section fetch; the
  drawer's open/closed state is unchanged by this slice.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Media Library page SHALL declare `data-section="media-library"` on its document root. | `new: reading/R63` |
| FR-002 | A section rail click from the Media Library page SHALL fetch that section's root through the shell's existing navigation path. | `new: reading/R63` |
| FR-003 | The first Alkitab click from Media Library SHALL populate the sidebar with real book rows and show no empty-list copy. | `new: reading/R63` |
| FR-004 | Clicking a section's own tile while that section is on stage SHALL keep the existing toggle behaviour. | `new: reading/R63` |
| FR-005 | The Media Library tile's `aria-current="page"` marker, stage contents and pending state SHALL be unchanged. | `new: reading/R63` |
| FR-006 | No endpoint, schema, permission, CSS or JavaScript behaviour SHALL change. | `new: reading/R63` |

### Key Entities

- **Section identity** — the document root's `data-section`, read by the rail handler and the
  shared shell; the Media Library is a destination, not one of the three reading sections.
- **Reading section tile** — Alkitab, Kidung or Tata Ibadah rail tile, whose click is a section
  change when its `data-panel` differs from the live section.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | From Media Library, the first Alkitab click makes one `GET /bible/` request. | Playwright request count; base 0, fixed 1. |
| SC-002 | The sidebar shows real book rows after that click. | `#panelBody .book` count; base 0, fixed >0. |
| SC-003 | The empty-list block is hidden after that click. | `#panelEmpty.hidden === true`; base false, fixed true. |
| SC-004 | No other rail navigation behaviour changes. | Targeted E2E navigation lanes green. |

## UI/UX

No new visual state: the fix changes which page the first rail click fetches. Measured on the live
app at 1440×900, dark mode, 1×, clicking through from `/`:

| State | `data-section` | `/bible/` requests on first Alkitab click | `#panelBody .book` | Empty title visible |
| --- | --- | --- | --- | --- |
| Media Library, before click (base) | `alkitab` | — | 0 | `No books yet.` |
| After first Alkitab click (base) | `alkitab` | 0 | 0 | `No books yet.` |
| After Kidung then Alkitab (base) | `alkitab` | 1 | 66 | hidden |
| Media Library, before click (fixed) | `media-library` | — | 0 | `No books yet.` (panel closed) |
| After first Alkitab click (fixed) | `alkitab` | 1 | 2 | hidden |

The 66-book figure is from the compose-backed app at 63404; the 2-book figure is from the preview's
SQLite sample. `preview/probe.py` prints both surfaces with their own datasets — the assertion is
the request count and the hidden empty state, not the row count's absolute value.

Live preview: `http://127.0.0.1:8769/` — open the home page, click the Media Library rail tile,
then click Alkitab. The unchanged code on `origin/develop` at 63404 reproduces the base column.

## Assumptions

- "Open bible from rail while in media-library page" means the shell's Alkitab rail tile while
  `/media-library/` is on the stage, reached by clicking through from home; both the in-place rail
  path and a direct library load are covered.
- A section rail click from a destination that owns no section is always a section change; the
  shell's existing `navigate()` path then handles pending state and history as in R61/R62.
- The app's three reading sections keep their existing names (`alkitab`, `kidung`, `tatib`);
  `media-library` is used only as a non-section value.
- No new visual treatment is wanted: the empty state stays as it is for a genuinely empty Bible list.

## Clarifications

- No clarification markers remained after Specify; no Clarify questions were needed.

## Traceability

- **Preview**: live preview at `http://127.0.0.1:8769/` (spec worktree dev server).
- **Measurements**: reproduction probe and gate-1 probe in `preview/probe.py`.
- **App tests**: one E2E regression named in Plan/Checklist; authorized by this spec.
