# Feature Specification: Hymn songbooks above a single separator, the rest A–Z

**Slice**: `specs/128-songbook-hymn-separator`
**Branch**: `feat/128-songbook-hymn-separator`
**Created**: 2026-10-24
**Status**: Accepted (owner, gate 1, 2026-10-24)
**Input**: "can you add a separator between hymn books and non-hymn song books? only separator. no headers.
also sort the non-hymn song books alphabetically" (with the Kidung sidebar open on the running page)

## User Scenarios & Testing

### US1 — The panel separates hymn books from the ordinary songbooks with one divider, and nothing else (P1)

**Why this priority**: the Kidung panel is one flat list today, so an operator scanning for a hymn collection
and an operator scanning for a locally added songbook read the same undifferentiated column. A divider answers
"which of these are the hymn books?" without adding a word to the panel — the request's explicit constraint.

**Independent Test**: open `/songs/` on the branch: the four hymn rows come first, one rule crosses the panel,
then the ordinary rows; no heading appears above either side.

**Acceptance scenarios**

1. **Given** the Kidung panel, **When** it renders, **Then** every hymn songbook precedes every ordinary songbook, and exactly one separator sits between the last hymn row and the first ordinary row.
2. **Given** the panel, **When** it is read top to bottom, **Then** no group heading, label or caption appears on either side of the separator.
3. **Given** the separator, **When** measured in the open panel, **Then** it is the panel's own group rule: `2px` solid `--divider`, `10px` margin above and `10px` padding below, so the last hymn row's bottom to the first ordinary row's top is `22px`.

### US2 — Ordinary songbooks read A–Z; hymn books keep their present order (P1)

**Why this priority**: the separator only helps if each side then answers the question the reader has. Hymn
books carry numbers, so their order is the collection's size; the ordinary songbooks are local lists, found by
name.

**Independent Test**: on `/songs/`, the ordinary side is `a, b, Buku Ende HKBP, Lagu, Lagu Sekolah Minggu,
Lagu Setelah persembahan, Lagu setelah persembahan, Pengutusan Bahasa Indonesia, Tata Ibadah` and the hymn side
is `Haleluya, Kidung Jemaat, Pelengkap Kidung Jemaat, Nyanyikanlah Kidung Baru`.

**Acceptance scenarios**

1. **Given** ordinary songbooks whose names differ in case, **When** the group is ordered, **Then** the order is by the case- and diacritic-folded name, with the original name breaking an exact tie.
2. **Given** hymn songbooks, **When** the group is ordered, **Then** the order is unchanged: descending song count, the name breaking a tie.
3. **Given** a panel with only ordinary songbooks (no hymn book exists), **When** it renders, **Then** no separator is drawn: the single group starts flush at the panel's top.
4. **Given** the filter, **When** it empties the hymn group, **Then** the separator disappears with it and the remaining ordinary group starts flush.

### US3 — Every route that shows the panel, and the saved copy, draws the same two groups (P2)

**Why this priority**: the panel is server-rendered on three routes and rebuilt from the saved library by
`offline-render.js`; a grouping that exists on one and not the others is the class of mismatch specs 122 and
127 removed.

**Independent Test**: load the Kidung index, a songbook page and a song page, then a saved render of the same
routes from the synced library: each shows the same two groups in the same order.

**Acceptance scenarios**

1. **Given** the Kidung index, a songbook page, or a song page, **When** the panel renders, **Then** the grouping and order are identical, and `aria-current` and the row-edit button still land on the rows they did before.
2. **Given** a synced saved library, **When** any of those routes is rendered from it, **Then** its panel is built from the same two groups in the same order.

### Edge Cases

- **When** the panel filter matches rows in both groups **Then** both groups stay, each filtered, and the separator stays between them.
- **When** the filter leaves the hymn group with no rows **Then** the separator is not drawn.
- **When** two names fold to the same key (`Lagu Setelah persembahan` / `Lagu setelah persembahan`) **Then** the tie is broken by the original name, ordinally, so the order is the same in SQLite and PostgreSQL.
- **When** a songbook is deleted **Then** it leaves its group, and a group that empties out draws no separator.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The Kidung panel renders hymn songbooks before ordinary songbooks. | `new: reading/R4` |
| FR-002 | Hymn songbooks keep their present order (descending song count, name as tiebreak); ordinary songbooks are ordered by their case- and diacritic-folded name, with the original name as tiebreak. | `new: reading/R4` |
| FR-003 | Exactly one separator is drawn between the two groups, using the panel's existing group rule (`2px` `--divider`, `10px` margin and `10px` padding). | `new: reading/R4` |
| FR-004 | Neither group carries a heading, label or caption. | `new: reading/R4` |
| FR-005 | A group with no rows — because no songbook of that kind exists, or because the panel filter emptied it — draws no separator. | `new: reading/R4` |
| FR-006 | The grouping and order are the same on the Kidung index, a songbook page and a song page, and `aria-current` and the per-row edit button are unchanged. | `new: reading/R4` |
| FR-007 | A reading page rendered from the saved library draws the same two groups in the same order, using the same sort keys as the server. | `new: reading/R5` |

### Key Entities

- **Songbook** — a `songs.Book` row: `name`, `short_name`, `is_hymn_book`, and the count of its non-deleted songs. The hymn flag decides the group; the name and the count decide the order.
- **Panel group** — one `section.group` in the Kidung panel's body. The separator is the `.group + .group` rule the panel already carries, so a group is the only thing this slice adds; no new element, class or heading.
- **Sort key** — the folded comparison form of a songbook's name (`search_lib.normalize` on the server, `normalized()` in the saved renderer), compared ordinally, with the original name breaking an exact tie.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The panel shows hymn books first and the ordinary songbooks after one divider | open `/songs/` on the branch: four hymn rows, one rule, then ordinary rows |
| SC-002 | Nothing labels either group | inspect the panel's markup: no `.group__head` inside `#panelBody` on the Kidung routes |
| SC-003 | The separator's spacing is the panel's own | measured in the browser: `border-top-width: 2px`, `margin-top: 10px`, `padding-top: 10px` |
| SC-004 | Ordinary songbooks read A–Z regardless of case | the ordinary group's rendered order equals the folded alphabetical order of the fixture names |
| SC-005 | The saved copy agrees with the server | saved-versus-server parity check over the three routes: same group count and same row order |
| SC-006 | Nothing else changed | the existing reading unit and browser assertions still pass; row height stays `38px` and the row gap `1px` |

## UI/UX

Preview approved by the owner on 2026-10-24 (running page, 1600 × 1000 viewport; screenshots in the preview
folder). Measured values, not adjectives:

- **Layout / position**: the panel body stacks two `section.group` blocks with no heading. The separator is the second block's top border, crossing the panel's content width (inside the panel's `10px` side padding).
- **Size / spacing**: separator `border-top: 2px solid var(--divider)` — `rgb(217, 214, 205)` in the light theme; `margin-top: 10px` and `padding-top: 10px`, so the last hymn row's bottom to the first ordinary row's top is `22px`. Rows unchanged: `38px` tall, `1px` between rows.
- **Colour / typography**: the divider uses the panel's existing `--divider` token; no text is added, so no type change.
- **States**: filter with both groups matched (separator stays, both groups filtered) · filter that empties the hymn group (separator gone, ordinary group flush) · filter that empties the ordinary group (separator gone, hymn group alone) · no hymn books at all (single group, no separator) · `aria-current` row keeps its fill on either side.
- **Motion**: none.
- **Responsive**: none — the Kidung panel is one layout; the mini rail is Alkitab's, and the Kidung panel collapses to closed instead (see Clarifications).

## Assumptions

- **Hymn order is unchanged** — the request fixes only the ordinary side; the hymn side keeps the accepted mockup's largest-collection-first order.
- **"Alphabetical" is folded and ordinal** — case and diacritics do not decide the order, and the comparison is made on the same key on the server and in the saved renderer rather than by the database's collation, so test (SQLite) and production (PostgreSQL) agree.
- **"Only separator, no headers"** — the divider is the panel's existing group rule; no element, class or label is introduced.
- **Junk songbooks stay** — `a` and `b`, and the two case-only duplicates, are data in this installation; the slice sorts what exists and does not hide or merge it.
- **Out of scope**: the Tata Ibadah panel, the Alkitab panel, the song picker's grouping, and songbook create/edit forms.

## Clarifications

### Session 2026-10-24

- Q: none asked — the request names the separator, forbids headers, and fixes the ordinary side's order; the preview confirmed the reading before drafting.
- Q: does the Kidung panel have a mini-rail state whose spacing needs a value? → A: no. `#panelCollapse` and the idle collapse send the Kidung panel to `closed`; `mini` is set only in the Alkitab branch (`static/web/reading.js:1155`, `:1125`). A first measurement of the mini spacing was removed from US1, FR-003, SC-003 and `## UI/UX` on 2026-10-24 — it described a state this panel never reaches.
- Q: does the separator stay when the filter hides one side? → SKIPPED, assumed: it goes with the group it separated (FR-005), because a rule with nothing above it reads as a mistake.
