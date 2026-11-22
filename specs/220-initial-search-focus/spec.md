# Feature Specification: Focus only the empty search landing

**Slice**: `specs/220-initial-search-focus`
**Branch**: `fix/220-initial-search-focus`
**Created**: 2026-11-22
**Status**: Accepted (Gate 1 2026-11-22)
**Input**: "when you open the search page, the search bar should get focus"; clarified as "only on initial search bar, not the one with the search results", and as "the landing focuses wherever it paints".
**Demand**: `ITEM-235`
**Capability**: modifies `reading/R15` (focus clause only) and adds `reading/R50`

## User Scenarios & Testing

### US1 — The empty search landing is ready for typing (P2)

**Why this priority**: the public site opens on search, but a fresh landing leaves focus on the page, so beginning a query costs an extra click. The compact field shown with results is a different state and must not be auto-focused.

**Independent Test**: open `/` in a fresh browser context and send keyboard input without clicking the field or using a test helper that focuses it. The query appears in the initial search field; after submission, results appear and the compact field no longer holds focus.

**Acceptance scenarios**

1. **Given** a fresh browser context **When** `/` opens the empty search landing **Then** DOM focus is on `#searchQuery`, its value is unchanged, and the page has not scrolled.
2. **Given** a fresh browser context **When** `/search` opens without a valid query **Then** DOM focus is on the landing's `#searchQuery`.
3. **Given** a fresh browser context **When** a section index `/bible/`, `/songs/` or `/tatib/` paints the same empty landing **Then** DOM focus is on `#searchQuery`, because the surface is identical.
4. **Given** a reading page and no remembered search **When** the Search rail destination or the home logo opens the empty landing in place **Then** focus moves to `#searchQuery` after the landing is visible.
5. **Given** the landing field has focus and contains a query **When** the query is submitted and results open **Then** the field is blurred, focus leaves `#searchQuery`, and the query and result set remain visible.
6. **Given** `/search?q=<valid query>` opens directly, or the Search rail restores a remembered result set **When** the results state is shown **Then** the compact `#searchQuery` is not focused by this behavior; the existing result, query and scroll state are retained.
7. **Given** a Bible, Kidung or Tata Ibadah reading page opens **When** its stage is shown **Then** no search field receives automatic focus.

### Edge Cases

- **When** `/search` has no valid query and renders the landing state **Then** the landing field receives focus even if the URL contains an invalid query; its value is not cleared or selected by this behavior.
- **When** opening or focusing the landing field could scroll the document **Then** focus is established without changing the page's scroll position.
- **When** a valid search result is restored from the current tab's snapshot **Then** focus is not redirected to the compact search field.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Wherever the public search landing is painted — `/`, `/search` without valid results, or a section index `/bible/`, `/songs/`, `/tatib/` — the landing input `#searchQuery` SHALL receive DOM focus on full-page load and when in-page navigation opens a fresh landing. The field SHALL be visible before focus is assigned, and the same surface SHALL behave the same way whatever rail section is selected. | `new: reading/R50` |
| FR-002 | Establishing landing focus SHALL NOT change the field's value, start a search, select its text, or change the document's scroll position. | `reading/R50` |
| FR-003 | When a query is submitted from a focused landing and results become visible, the landing field SHALL be blurred so it is no longer the active element as the compact field. Directly opened or restored results SHALL NOT automatically focus that field. Existing query, result, snapshot and scroll behavior SHALL remain intact. | `reading/R50` |
| FR-004 | Reading pages (`home="reading"`, `data-read="on"`) SHALL NOT receive automatic focus in `#searchQuery`, and neither SHALL the results state. | `reading/R50` |
| FR-005 | Search matching, query grammar, result ordering, URL/history behavior, and the search field's dimensions and position SHALL otherwise remain unchanged. | `reading/R50` |
| FR-006 | This slice supersedes only the final clause of accepted Spec 139 FR-006 (“no focus change on load”) for the empty search landing. The no-transition and no-page-scroll clauses remain binding. | modifies `reading/R15` |

### Key Entities

None. Focus is transient browser state; this change adds no stored data or interface.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A fresh empty search landing is immediately ready for typing, on every route that paints it. | Playwright E2E: after opening `/`, `/search`, `/bible/`, `/songs/` and `/tatib/` in a fresh context, `document.activeElement.id === 'searchQuery'`; send keys without clicking or calling `locator.fill`. |
| SC-002 | Opening a fresh landing in the single-page shell also focuses its input. | Playwright E2E: from a reading route with no saved query, click the Search rail control; after the landing appears, `document.activeElement.id === 'searchQuery'`. |
| SC-003 | Results never take automatic focus into their compact field. | Playwright E2E: direct valid results load and Search-rail restoration leave `document.activeElement !== #searchQuery`; after submitting from the landing, focus is not left on that field when results are active. |
| SC-004 | Focusing the landing does not disturb the current page state. | Playwright E2E: `scrollY` and the field's value stay unchanged across focus; keyboard entry still submits through the existing route. |
| SC-005 | Reading routes remain outside the focus behavior while the section indexes do not. | Playwright E2E: `/bible/1/1/`, `/songs/1/` and `/tatib/1/` do not auto-focus `#searchQuery`; `/bible/`, `/songs/` and `/tatib/` do. |

## UI/UX

`static preview at specs/220-initial-search-focus/preview/index.html` — the existing search shell's landing and results states, assembled from rendered project markup, styles and assets, with focus on the landing field only.

- **Layout / position**: no geometry change. The landing field keeps its existing 610×56px box, its top at 422px (centre 450) in a 1440×900 viewport and 354×56px with its top at 394px (centre 422) at 390×844 — measured identical on the preview and on the served page. In results state the compact field's top stays 46px (≥721px) / 82px (≤720px) and the results section starts at 128px / 164px.
- **Size / spacing**: unchanged; no new control, padding or spacing.
- **Colour / typography**: unchanged. Keep the existing focus-visible treatment (2px `--focus` outline, 2px offset); add no new token or font.
- **States**: empty landing with the field focused; results with the compact field not automatically focused; reading routes unchanged. Existing hover, active, error and loading states are unchanged.
- **Motion**: no transition or entrance motion; focusing the field does not scroll the page.
- **Responsive**: preserve the existing landing geometry from 320px through 1920px, including the 1272px and 720px layout boundaries.

## Assumptions

- "Initial search bar" means the full-size input on the empty search landing, not the compact field shown above search results.
- The landing state is wherever the landing is painted: `/`, `/search` when search does not render valid results, and the section indexes `/bible/`, `/songs/` and `/tatib/`. Measured: `#searchHome` is byte-identical on all five (1299 bytes, `sha1 c19937db…`) and only `data-section` on the root differs, so a rail section changes the sidebar, not the stage. Reading routes paint no landing (`display: none`). A direct valid search URL is the results state.
- The existing field value, matching behavior and tab-local result snapshots are not reset or changed by focus.
- The visual focus indicator remains the one already defined by the product; whether programmatic focus paints its `:focus-visible` outline is checked in the preview and browser test, not redesigned here.
- Geometry measurements are relative to the browser layout viewport consumed by the app shell; desktop browser chrome reduces `innerHeight` below the outer window height.
- The request changes focus behavior only. Spec 139's centring, geometry, no-transition and no-scroll requirements remain in force; only its no-focus-on-load clause for the empty search landing is superseded.

## Clarifications

### Session 2026-11-22

- Q: Which search field should receive focus? → A: Only the initial search bar, not the one with the search results.
- Q: Should this behavior supersede Spec 139 FR-006's “no focus change on load” clause for the empty search landing? → A: Yes, supersede only that focus clause; preserve the no-scroll and no-transition clauses.
- Q: After submitting from the focused landing, should focus leave the field when results appear, or stay in the same compact field? → A: Move focus out when results appear; only the empty landing auto-focuses.
- Q: The section indexes `/bible/`, `/songs/` and `/tatib/` paint the same empty landing as `/`. Should they focus too? → A: The landing focuses wherever it paints; reading routes stay unfocused. This supersedes the earlier assumption that only `/` and `/search` are landing states.
- **Superseded decision**: Spec 139 FR-006's “no focus change on load” remains the accepted historical rule for its geometry slice, but Spec 220's owner clarification overrides that clause only for the empty search landing. Its no-motion and no-scroll requirements, and its results/reading view geometry, remain unchanged.

No `[NEEDS CLARIFICATION]` markers remain.
