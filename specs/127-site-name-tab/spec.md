# Feature Specification: The tab names the site, and the index's tab stops at the name

**Slice**: `specs/127-site-name-tab`
**Branch**: `fix/127-site-name-tab`
**Created**: 2026-10-24
**Status**: Accepted (owner, gate 1, 2026-10-24)
**Input**: "rename the site's name in tab from \"GKPS Klender\" to \"Multimedia GKPS Klender\". also remove any trailing when opening index \"/\"." (sent with a screenshot of the home page at `localhost:63404`: the vertical tab strip shows the active tab truncated to `GKPS Klender — Sea…`, and the page below is the search-first landing)

## User Scenarios & Testing

### US1 — Every reading tab names the site the way the product is named (P1)

**Why this priority**: the browser tab is the only place the site names itself on every page, and it
currently names a namespace rather than the product. The rest of the application — the site root's own
`index.html`, the maintenance notice, the manage and Tata Ibadah pages — already says `Multimedia GKPS
Klender`; the reading surfaces are the ones that disagree.

**Independent Test**: load every reading route in a browser and read `document.title`: each ends with
` — Multimedia GKPS Klender`, behind the same leading text it carries today.

**Acceptance scenarios**

1. **Given** a Bible chapter open on the stage, **When** the operator reads the tab, **Then** it reads `<book name> <chapter> — Multimedia GKPS Klender` (`1 Musa 1 — Multimedia GKPS Klender` on the SIM edition, `Kejadian 1 — Multimedia GKPS Klender` on TB).
2. **Given** a song page, **When** it opens, **Then** the tab reads `<citation> — Multimedia GKPS Klender`, the citation still following spec 126's short-reference rule (`PKJ 4 — Multimedia GKPS Klender`).
3. **Given** a Tata Ibadah service, **When** it opens, **Then** the tab reads `<service name> — Multimedia GKPS Klender`.
4. **Given** a section landing, **When** it opens, **Then** the tab reads `Alkitab`, `Kidung`, or `Tata Ibadah` followed by ` — Multimedia GKPS Klender`.
5. **Given** the search results, **When** a query returns results, **Then** the tab reads `Results for “<canonical>” — Multimedia GKPS Klender`; an empty query reads `Search — Multimedia GKPS Klender`.
6. **Given** the Media Library, **When** it opens, **Then** the tab reads `Media Library — Multimedia GKPS Klender`.

### US2 — The index's tab is the site name alone (P1)

**Why this priority**: the index is the page a person leaves open, and in a vertical tab strip its tab is
truncated before the second word. The trailing tagline spends the tab's whole width repeating what the
page's own search field already says.

**Independent Test**: open the site root and read the tab: `Multimedia GKPS Klender`, with nothing after it.

**Acceptance scenarios**

1. **Given** the site root `/`, **When** it opens with maintenance off, **Then** the tab reads exactly `Multimedia GKPS Klender`.
2. **Given** the temporary home `/home/`, **When** it opens, **Then** the tab reads exactly `Multimedia GKPS Klender`.
3. **Given** `/search` with no query, which renders the same landing, **When** it opens, **Then** the tab reads exactly `Multimedia GKPS Klender`.
4. **Given** the index with maintenance on, **When** it opens, **Then** the maintenance notice's title is unchanged — it already reads `Situs sedang dalam pemeliharaan — Multimedia GKPS Klender`.

### US3 — The saved copy writes the same titles (P2)

**Why this priority**: a reading page built from the synced library is shown before the online update
replaces it, and spec 122 fixed those saved pages as the server route's own copy; a tab that changes name
when the online page arrives is the same class of mismatch that spec fixed for headers and labels.

**Independent Test**: render each route from the saved library and compare `document.title` with the
server page's; they are equal, name included.

**Acceptance scenarios**

1. **Given** a synced saved library, **When** an Alkitab, Kidung, or Tata Ibadah route is rendered from it, **Then** its `document.title` equals the server page's, ` — Multimedia GKPS Klender` included.
2. **Given** the same library and the home route, **When** it is rendered from it, **Then** the title is `Multimedia GKPS Klender` alone, as the server page's is.
3. **Given** the reading page already on the stage, **When** the operator switches Bible edition in place, **Then** the in-place title update writes `<book name> <chapter> — Multimedia GKPS Klender`.

### Edge Cases

- **When** a hymn songbook has no short name **Then** the tab keeps spec 126's fallback and still ends with ` — Multimedia GKPS Klender`.
- **When** a route is opened with JavaScript disabled **Then** the server-rendered `<title>` already carries the new name; nothing waits for script.
- **When** the saved render is final because the network is unavailable **Then** it carries the same title it would have shown online.
- **When** the page's visible text is read **Then** nothing changed: the heading, the search field's label, the logo's alt text and the rail's labels keep the congregation name `GKPS Klender`.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The document title of the index — `/`, `/home/`, and `/search` with no query — is exactly `Multimedia GKPS Klender`, with no trailing tagline. | `reading/R3` |
| FR-002 | The document title of every other reading page ends with ` — Multimedia GKPS Klender`, behind the leading text it carries today. | `reading/R3` |
| FR-003 | The leading text of each route is unchanged: the Bible's book name and chapter, a song's short citation, a service's name, and the section or page labels `Alkitab`, `Kidung`, `Tata Ibadah`, `Search`, `Results for “<canonical>”`, `Media Library`. | `reading/R1`, `reading/R3` |
| FR-004 | The saved renderer writes the same two shapes: the home route's title is the site name alone, and every other saved route's title is its leading text followed by ` — Multimedia GKPS Klender`. | `reading/R2` |
| FR-005 | The in-place title update after a Bible edition switch writes the same suffix, so the tab does not change name when the edition does. | `reading/R3` |
| FR-006 | No visible text changes: headings, the search field's accessible name, the logo's alt text and the rail's labels keep `GKPS Klender`. | `reading/R3` |

### Key Entities

- **Document title** — the text a browser shows in its tab; produced by three places that must agree: the server-rendered `<title>` (Django views and template defaults), the saved renderer (`static/web/offline-render.js`), and the in-place update in `static/web/reading.js`.
- **Site name** — `Multimedia GKPS Klender`, the product name the application already uses outside the reading surfaces (`multimedia/web/templates/index.html`, the maintenance notice, the manage and Tata Ibadah pages).
- **Congregation name** — `GKPS Klender`, still the name in the page's visible or assistive text (headings, `alt`, `aria-label`); the slice does not move it.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The index's tab is exactly `Multimedia GKPS Klender` | open `/`, `/home/` and `/search` on the running branch and read `document.title`: equal to the string, nothing after it |
| SC-002 | Every other reading tab ends with the site name | the same reading on a Bible chapter, a song, a service, a section landing, the results page and the Media Library |
| SC-003 | The saved page and the server page agree on the title | the saved-versus-server parity regression over every route it covers: equal titles, name included |
| SC-004 | Nothing else on the page changed | the existing unit and browser assertions for headings, labels, placeholders and rows are re-run unchanged and still pass |

## UI/UX

No visual design change: the deliverable is the tab's text. Recorded because the tab is the surface.

- **Layout / position**: unchanged; the tab's leading text keeps its position, the name keeps the tail.
- **Size / spacing**: the index's tab shrinks from `GKPS Klender — Search Alkitab, Kidung, and Tata Ibadah` (60 characters) to `Multimedia GKPS Klender` (24), so it no longer truncates in the vertical tab strip the request's screenshot shows; every other tab grows by 10 characters (`GKPS` → `Multimedia GKPS`), which their leading text already dominates.
- **Colour / typography**: browser chrome owns the tab; nothing in the page changes.
- **States**: the maintenance state's title is untouched (it already carries the new name).
- **Motion**: none.
- **Responsive**: none — a tab's width is the browser's, not the page's.

## Assumptions

- The product name is `Multimedia GKPS Klender`, taken from `multimedia/web/templates/index.html`, the
  maintenance notice and the manage/Tata Ibadah templates, which already use it. The reading surfaces are
  the exception this slice removes.
- The request's "remove any trailing when opening index" is the index's trailing tagline, not the URL's
  path: an HTTP request for the site root always carries the path `/`, so no URL change is possible. The
  owner confirmed the reading in the request session.
- The congregation name in visible and assistive text is out of scope: the request names the tab, and a
  page that renamed its own heading to the product name would read as a different change.

## Clarifications

### Session 2026-10-24

- Q: the "trailing" part — what exactly should go? → A: the index's trailing tagline. The tab reads just `Multimedia GKPS Klender`; other pages keep `<content> — Multimedia GKPS Klender`.
- Q: does the rename apply only to the index, or to every page title? → A: every page title — Bible, Kidung, Tata Ibadah, search, media library.
- Q: could "remove any trailing" mean the URL's trailing slash? → A: no; the root path is `/` by definition, and the request's screenshot shows the address without one.
