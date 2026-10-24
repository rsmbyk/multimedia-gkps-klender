# Feature Specification: A saved hymn song page never shows the song sort control

**Slice**: `specs/125-saved-song-sort-parity`
**Branch**: `fix/125-saved-song-sort-parity`
**Created**: 2026-10-24
**Status**: Accepted (owner, gate 1, 2026-10-24)
**Input**: "when you open a hymn-book song from the sidebar, there is a brief moment the song filter button at the top of the sidebar appear and then disappear again" (sent with a screenshot of `/songs/139/`: the NKB song list, the song filter at the top of the second sidebar, and its sort button visible beside it)

## User Scenarios & Testing

### US1 — Opening a hymn-book song shows the server's control set at once (P1)

**Why this priority**: the sort button is not offered for a hymn book — its songs stay in number order
(spec 011) — so its appearance is wrong at every moment it is on screen, and the filter field shifts
width under the pointer while the operator is reaching for it.

**Independent Test**: with the saved library synced, open a hymn song through the Kidung sidebar and
sample the sort control on every animation frame; it is never visible, and the song filter keeps one
width throughout.

**Acceptance scenarios**

1. **Given** a synced saved library and an online session, **When** the operator opens a song of a hymn songbook from the second sidebar, **Then** the sort control is hidden in the first rendered frame and stays hidden after the online update, and the song filter's width does not change while that song page is on the stage.
2. **Given** the same saved library with the network unavailable, **When** the operator opens that song, **Then** the sort control stays hidden and the sidebar otherwise renders as it does today.
3. **Given** a song of an ordinary (non-hymn) songbook, **When** the operator opens it from the sidebar, **Then** the sort control is visible before and after the online update, as it is today.

### US2 — The saved song page matches the server for this control (P2)

**Why this priority**: the mismatch is a saved-render parity gap of the kind spec 122 closed for
labels, headings and references; this control was outside the fields that spec's regression compares,
so the same gap would return unnoticed.

**Independent Test**: for every songbook in the synced library, compare the saved render's sort control
with the server page's own; the `hidden` state agrees on every route.

**Acceptance scenarios**

1. **Given** a synced library containing hymn and ordinary songbooks, **When** each songbook's first song page is rendered both from the saved library and from the server, **Then** the sort control's hidden state is equal in both documents for every route.
2. **Given** the same comparison on a songbook's list page, **When** a hymn and an ordinary book are compared, **Then** their sort control states are unchanged from today: hidden for the hymn book, visible for the ordinary one.
3. **Given** the existing saved-parity browser regression, **When** it compares a song route, **Then** it compares the sort control's hidden state among its fields, so a reintroduced mismatch fails it.

### Edge Cases

- **When** a hymn book holds a song with no number **Then** the page still hides the sort control; the citation fallback does not affect it.
- **When** the saved library has no songbook containing the requested song **Then** the route falls back to the server page, and nothing about this control changes.
- **When** the operator is offline and the online update never runs **Then** the hidden state of the first saved frame is the one that stays.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A song page rendered from the saved library hides the sort control when the song's book is a hymn book. | `new: saved-reading` |
| FR-002 | Opening a hymn-book song in place never paints the sort control, so no frame shows it appearing and then disappearing. | `new: saved-reading` |
| FR-003 | A song page rendered from the saved library keeps the sort control visible for a non-hymn songbook, as the server page does. | `new: saved-reading` |
| FR-004 | The saved reading libraries' parity regression compares the sort control's hidden state on every route it already covers, alongside the labels, headings and references it compares today. | `new: saved-reading` |
| FR-005 | Every other saved-render and server field on these routes — headings, filter labels and placeholders, songbook rows, song references, eyebrow, stage body, add controls — is unchanged. | `new: saved-reading` |

### Key Entities

- **Song sort control** — the button beside the song filter (`#songSort`) that switches the second sidebar between last-modified and alphabetical order. The server page omits it for a hymn book, whose songs stay in number order (spec 011); it is present for an ordinary songbook.
- **Saved render** — the reading page built in the browser from the synced library (`static/web/offline-render.js`) and shown before the online update replaces it.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A hymn song opened from the sidebar shows no sort control at any point | home → Kidung → NKB → first song on the running site, sampling `#songSort`'s rendered width and `hidden` on every animation frame: no frame with a visible control, and one filter width across the frames where that song page is on the stage |
| SC-002 | The saved page and the server page agree on the control for every song route in the library | the parity regression's saved-vs-server field comparison over every songbook's song route: equal `hidden` state for each |
| SC-003 | An ordinary songbook's song page is unchanged | the same comparison on the ordinary songbook's song route: the control stays visible before and after the online update |

## UI/UX

No new visual design: the target is the server page already shipped for `/songs/<id>/`, which specs 004
and 122 fixed as the reference. What changes is the absence of a transient.

- **Layout / position**: unchanged — the sort button sits in `.ch__search` beside the song filter on the route where it is offered at all.
- **Size / spacing**: measured on the current build at `localhost:8768` while opening NKB's first song: the control appears at 38 × 38 px and the song filter narrows from 339 px to 293 px; both revert when it hides. After the fix neither frame exists; the filter stays 339 px.
- **Colour / typography**: unchanged.
- **States**: hidden on a hymn song page (server parity); visible on an ordinary songbook's song page, with its existing hover and focus states.
- **Motion**: none added — the defect is a transition that happens because two renders disagree, and removing it is the change.
- **Responsive**: unchanged; the control's narrow-layout treatment is untouched.

## Assumptions

- The server's rule stands: a hymn book keeps number order and offers no sort control (spec 011; the
  server pins the same expectation in `multimedia/web/tests.py`). The slice corrects the saved render,
  not the server page, because spec 122 fixed the server page as the reference for saved views.
- The fault reaches every song of every hymn book, not only the one in the report — the saved render
  decides the control from the section alone, while the server decides it from the book.
- The songbook list page's saved render already agrees with the server on this control, so it is a
  guard in this slice rather than a thing to change.

## Clarifications

### Session 2026-10-24

- No open question: the request names the trigger (opening a hymn-book song from the sidebar) and the observable (a control appears and disappears), and the reproduction confirms both.
- Q: how does the fault appear on the running site? → A: with the saved library synced, opening the first song of NKB from the sidebar renders the saved page with the sort control visible for about 220 ms; the online update that follows hides it and returns the filter field to its full width. A screenshot of the same moment on `/songs/139/` shows the control beside "Filter songs…".
- Q: what does the saved renderer base the control on today? → A: the section only, always offering it on a Kidung page; the server bases it on the book's hymn flag.
