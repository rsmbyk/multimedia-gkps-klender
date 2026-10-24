# Feature Specification: A song page cites its songbook by its short name

**Slice**: `specs/126-songbook-short-header`
**Branch**: `feat/126-songbook-short-header`
**Created**: 2026-10-24
**Status**: Accepted (owner, gate 1, 2026-10-24) — revised after gate 1 at the owner's decision: FR-004's capability moved from `new: saved-reading` to `new: reading`, and the slice now starts the capability tree. Gate 1 reaffirmed with gate 2 the same day.
**Input**: "i want you to use short songbook names instead of full name for the songbook header in song page" — sent with a screenshot of a Pelengkap Kidung Jemaat song page whose stage header reads `PELENGKAP KIDUNG JEMAAT 4` above the title.

## User Scenarios & Testing

### US1 — A hymn song's header is the reference the rest of the app already uses (P1)

**Why this priority**: the header is the citation the operator reads to know which song is on the stage.
Every other song surface in the app names a hymn song by `<short name> <number>` — the projector's Go To
list, the OBS song dock and its detail, the verses view, and the second sidebar on this very page, whose
selected row reads `PKJ 4` while the header above the lyrics reads `PELENGKAP KIDUNG JEMAAT 4`. The page
that shows the song is the one place that spells the songbook out in full, so the same song has two names
on one screen. A header is a citation, not a title: `PKJ 4` identifies the song, while
`Pelengkap Kidung Jemaat 4` re-states a songbook the sidebar beside it already names.

**Independent Test**: open any hymn-book song page; the header above the title shows the short reference
(`PKJ 4`), and the full songbook name no longer appears in it.

**Acceptance scenarios**

1. **Given** a song of a hymn songbook that has a short name (`Pelengkap Kidung Jemaat`, short name `PKJ`, song 4), **When** its song page is opened, **Then** the header above the title reads `PKJ 4`.
2. **Given** a hymn song with a sub-number (Kidung Jemaat 152a), **When** its page opens, **Then** the header reads `KJ 152A` — the sub-number treatment is unchanged, only the songbook part is short.
3. **Given** a hymn songbook whose short name is empty, **When** one of its songs opens, **Then** the header reads the full songbook name followed by the number, so it never begins with a bare number.
4. **Given** a hymn song with no number, **When** its page opens, **Then** the header reads the songbook's short name alone.

### US2 — An ordinary songbook's header is unchanged (P2)

**Why this priority**: an ordinary (non-hymn) songbook's songs carry no numbers, so its header is the
songbook's name and nothing else. That is the one case where the full name *is* the whole citation, and a
bare abbreviation would make the header less informative than it is today.

**Independent Test**: open a song of a non-hymn songbook; the header is that songbook's full name, exactly
as it is today.

**Acceptance scenarios**

1. **Given** a song of a non-hymn songbook, **When** its page opens, **Then** the header reads the songbook's full name.
2. **Given** every song page, **When** it renders, **Then** the second sidebar's rows and its `Song list — <name>` heading, the songbook panel's rows, the songbook filter's placeholder, and the stage title are unchanged by this slice.

### US3 — The saved song page carries the same header (P2)

**Why this priority**: the saved renderer builds the same route in the browser before the online update
replaces it, and spec 122 fixed the server page as the reference for those views. A header that differs
between the two renders is the drift 122 closed for the labels, headings and eyebrow it compared.

**Independent Test**: with the library synced, open a hymn song from the sidebar; the saved page and the
server page show the same header for every route.

**Acceptance scenarios**

1. **Given** a synced library, **When** a hymn song is rendered from it, **Then** the header equals the server page's header for the same song.
2. **Given** a synced library, **When** an ordinary songbook's song is rendered from it, **Then** the header is unchanged from today.

### Edge Cases

- **When** a hymn songbook's short name is empty **Then** the header falls back to the full name (US1/AC3) — the header never starts with the number alone.
- **When** a hymn book holds an unnumbered song **Then** the header is the songbook reference with no trailing number, and no stray space before it.
- **When** a route has no citation at all (a page whose `read_eyebrow` is empty) **Then** the element stays `hidden`, as today.
- **When** the song's songbook is soft-deleted **Then** the route still 404s and no header renders — unchanged.
- **When** the same route is opened from the saved library with the network unavailable **Then** the saved header is the final one, and it is the same text as the server's.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A song page's header SHALL cite a hymn-book song as `<short name> <number><sub-number>` — `PKJ 4` — instead of `<full name> <number><sub-number>`. | `new: reading` |
| FR-002 | When a hymn songbook's short name is empty, the header SHALL fall back to the songbook's full name before the number. | `new: reading` |
| FR-003 | A song of a non-hymn songbook SHALL keep its full songbook name as the header. | `new: reading` |
| FR-004 | The saved renderer SHALL write the same header text for the same song route, so the saved page and the server page agree. | `new: reading` |
| FR-005 | The browser tab title of a song page SHALL follow the short reference — `PKJ 4 — GKPS Klender` — so the tab names the song the way the page does. | `new: reading` |
| FR-006 | A song of a non-hymn songbook SHALL keep its full songbook name in the header even when that songbook has a short name set. | `new: reading` |
| FR-007 | Every other surface of these routes — the stage title, the stage body, the second sidebar's heading and rows, the songbook panel's rows, and the filter placeholders — SHALL be unchanged. | `new: reading` |

### Key Entities

- **Songbook** (`songs.Book`) — identified by a unique full `name`; an optional `short_name` of at most 8 characters, unique among the non-blank ones; and `is_hymn_book`, which decides whether its songs carry numbers. In the live library the four hymn songbooks have short names (`HAL`, `KJ`, `NKB`, `PKJ`) and every ordinary songbook has none.
- **Song** (`songs.Song`) — a `book`, an optional `number` and `sub_number` (e.g. `152` + `a`), and a `title`. A hymn song's reference is its book's short name plus that number.
- **Page header** (`.read__eyebrow`, `#readEyebrow`) — the citation line above a reading page's title: the book and chapter on a Bible page, the date on a Tata Ibadah page, and the song reference on a song page. One element, one rule, written per route.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A hymn song's header names the song by its short reference | `/songs/1013/` (PKJ 4): the header's text is exactly `PKJ 4`, and the string `Pelengkap Kidung Jemaat` appears nowhere in it |
| SC-002 | No song page shows a number-only header | a hymn book with a blank short name renders the full name before the number; a hymn song with no number renders the reference with no trailing space |
| SC-003 | An ordinary songbook's page is unchanged | `/songs/` for a non-hymn song: the header equals the songbook's full name, as before this slice |
| SC-004 | The saved page and the server page agree on the header | the saved-vs-server comparison: equal header text on a hymn song route and on an ordinary song route |
| SC-005 | Nothing else on these routes moves | the sidebar heading, the sidebar rows, the filter placeholders, the stage title and the stage body are equal to the pre-slice page |

## UI/UX

Text only, in an element that already exists — no new component, colour, size or position. Numbers measured
on the running branch at `localhost:8768`, `/songs/1013/` (PKJ 4), with Playwright at 1440, 1280, 768 and
390 px; the "today" figures are the same element on develop at `localhost:63404`.

- **Layout / position**: unchanged — the first line of `.read__head`, above `.read__row` and its title (`reading/base.html:355`); `margin: 0 0 10px`.
- **Size / spacing**: the type is untouched — 16.5px / weight 600 / line-height 1.65 (27.225px) / letter-spacing 1.98px / `--ink` at `.78` opacity. The text shortens, and that is the whole visible change: `Pelengkap Kidung Jemaat 4` measures 292.64 × 27.22 px (one line) at 1440 and 1280, but 243.22 × 54.44 px at 768 (the stage is 243 px wide) and 290 × 54.44 px at 390 — it wraps to two lines on a narrow stage. `PKJ 4` measures 49.56 × 27.22 px and stays on one line at all four widths, so the header block is 27.22 px shorter at 768 and 390 and the title moves up by that much.
- **Colour / typography**: unchanged; the capitals come from the existing `text-transform: uppercase`, so the marked-up text stays `PKJ 4` and renders `PKJ 4`.
- **States**: the header is not interactive — no hover, focus, active or disabled state applies. Its only state is `hidden`, used when a route carries no citation, and that is unchanged.
- **Motion**: none — no transition, and nothing animates on the saved→online swap.
- **Responsive**: the header becomes single-line at every breakpoint (see Size / spacing); at 768 the stage is 243 px wide, so the shorter text is what lets it stop wrapping.

## Assumptions

- **The short name is the citation, not a different value in the data.** `songs.Book.short_name` already holds `PKJ`, `KJ`, `NKB` and `HAL` in the live library, and the other song surfaces already print it; this slice changes which field the header reads, nothing about what the fields hold. — taken because the request names the short name as the source and the field exists.
- **The ordinary-songbook header keeps the full name**, even if a short name is ever set. — the owner's answer to FR-006: an ordinary songbook's header is its name.
- **The saved renderer is in scope.** — taken because spec 122 established saved/server parity as the contract for these routes, and this header is one of the fields that parity covers.
- **The slice starts the capability tree**, `docs/spec/reading.md`, and the saved copy is a requirement *inside* `reading` rather than a capability of its own — the saved page is a rendering mode of the same behaviour. — the owner's answer when the tree was raised; the `saved-reading` label that spec 125's requirements used folds into that file.

## Clarifications

### Session 2026-10-24

- Q: the song page's browser tab title is built from the same citation as the header, so it says `Pelengkap Kidung Jemaat 4 — GKPS Klender` today — should the tab follow the short name too, or keep the full songbook name? → A: follow the page; the tab reads `PKJ 4 — GKPS Klender`.
- Q: an ordinary songbook's header is only its name — keep the full name, or use the short name when one is set? → A: keep the full name; an ordinary songbook's header is its name.
- Q: this repo has no `docs/spec/` capability tree, so the requirements' `new: reading` / `new: saved-reading` labels had no home — record `n/a` again, or start the tree? → A: start the tree.
- Q: should `saved-reading` be its own capability file? → A: no — one file, `docs/spec/reading.md`, with the saved-copy parity as a requirement inside it. (Supersedes the `new: saved-reading` label in FR-004; recorded in the status line.)
- No other open item: the empty-short-name fallback, the unnumbered song, the sub-number treatment and the saved-render parity all follow from the existing citation rule and are recorded as requirements or edge cases. **Zero `[NEEDS CLARIFICATION]` markers remain.**
