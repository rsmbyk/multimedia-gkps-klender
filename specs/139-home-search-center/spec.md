# Feature Specification: The landing search field sits on the window's middle

**Slice**: `specs/139-home-search-center`
**Branch**: `feat/139-home-search-center`
**Created**: 2026-10-27
**Status**: Draft
**Input**: "center the search bar vertically" — with a 1920×1200 screenshot of the landing page, the
field visibly below the window's middle.

## User Scenarios & Testing

### US1 — The landing field is the page's middle line (P1)

**Why this priority**: this is the report. The landing page has exactly one control, and today it sits
below the window's middle at every width: the section centres the logo and field *as one block*, so the
field's own centre lands half the logo block below the section's middle — measured +49px at 1440×900,
and +85px on a 390×844 phone, where the section is also 36px taller than the space the stage leaves it.
The field is the thing a person aims at; the logo is decoration above it.

**Independent Test**: open `/` at 1440×900 and at 390×844; the field's border box is centred on the
window's middle within 1px, the logo is entirely inside the window above it, and the document is
exactly one window tall.

**Acceptance scenarios**

1. **Given** a 1440×900 window **When** `/` is opened **Then** the field's box runs from 422 to 478 and
   its centre (450) equals the window's middle (450), and the logo's box ends 26px above the field.
2. **Given** a 390×844 phone **When** `/` is opened **Then** the field's centre (422) equals the
   window's middle (422), the logo's top edge is at 272 and fully painted, and the document's height
   equals the window's.
3. **Given** a 1024×768 window **When** `/` is opened **Then** the field's centre is 384, as at every
   other width tested.
4. **Given** a landing page **When** the window is resized from 1920×1000 down to 320×568 **Then** the
   field stays on the middle line at every stop, with no sideways scroll and no second window of
   content below the fold.

### US2 — The views that are not the landing keep their geometry (P1)

**Why this priority**: the field is drawn by the same section in three states, and the compact bar on a
results page is at the top on purpose. A centring change that also moved it would trade one report for
another.

**Independent Test**: submit a query and open a reading page; the results bar's field keeps its top
edge (46px at 1440×900, 82px on a 390×844 phone), the results list starts at 128px / 164px, and the
reading page is unchanged.

**Acceptance scenarios**

1. **Given** a query submitted at 1440×900 **When** the results page is drawn **Then** the field's top
   edge is 46 and the results list starts at 128 — the same numbers as before this slice.
2. **Given** a reading page **When** it is drawn **Then** no search section is painted and the reading
   column occupies the stage exactly as before.

### Edge Cases

- **When** the window is shorter than the logo plus the field plus the stage's padding (320×568)
  **Then** the field is still centred and the logo is still fully inside the window; nothing is clipped
  at the top.
- **When** the layout swaps to the phone toolbar (≤720px) **Then** the field is centred inside the space
  the stage leaves under the toolbar, not in the window's raw middle — the two coincide because the
  section now measures the stage's real padding.
- **When** a query is submitted and the results page is then resized **Then** the compact bar stays at
  the top of the stage; it never recentres.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | On the landing page the search field's border box SHALL be vertically centred on the window's middle, within 1px, at every width from 320px to 1920px and at every height that fits the logo and the field. | `new: reading` |
| FR-002 | The logo SHALL sit above the field, fully inside the window, keeping the 26px gap it has today between its bottom edge and the field's top edge. | `new: reading` |
| FR-003 | The landing page SHALL stay exactly one window tall: the document's scroll height SHALL equal the window's height, adding no vertical or horizontal scrollbar. | `new: reading` |
| FR-004 | The phone layout (≤720px, where the stage pads for the toolbar) SHALL centre the field on the same terms as the desktop layout — the section's height SHALL be derived from the stage's real top and bottom padding, not from `--pad-top` alone. | `new: reading` |
| FR-005 | The results view's compact bar and the reading view SHALL keep the geometry they have today: the field's top edge at 46px (≥721px) / 82px (≤720px) and the results list at 128px / 164px. | `new: reading` |
| FR-006 | The centring SHALL hold without motion: no transition, no scroll of the page itself, and no focus change on load. | `new: reading` |

### Key Entities

None — this slice changes where one existing element is painted, and adds no stored data.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The field is on the window's middle line at every tested width | Playwright: `Math.abs(fieldRect.top + fieldRect.height/2 - innerHeight/2) ≤ 1` at 1920×1000, 1440×900, 1280×800, 1272×800, 1024×768, 834×1112, 721×900, 720×900, 600×800, 390×844, 320×568 |
| SC-002 | The landing page adds no scrolling | `documentElement.scrollHeight === innerHeight` and `scrollWidth === clientWidth` at the same widths |
| SC-003 | The logo stays whole above the field | `logoRect.top ≥ 0` and `fieldRect.top - logoRect.bottom === 26` at the same widths |
| SC-004 | The other two states do not move | results: field top 46 / 82 and results top 128 / 164, unchanged from the numbers measured on `develop` today; reading: search section not painted |

## UI/UX

`static preview at specs/139-home-search-center/preview/after-home.html` — the rendered landing page,
the project's real stylesheets, and `after.css` holding only the changed rules; `before-home.html` is
the same page without that file.

Numbers, measured in Chromium against the rendered page (field border box, window middle in brackets):

| Window | Field centre today | Field centre after | Logo top today → after | Document height |
| --- | --- | --- | --- | --- |
| 1920×1000 | 549 (500) | 500 | 399 → 350 | 1000 → 1000 |
| 1440×900 | 499 (450) | 450 | 349 → 300 | 900 → 900 |
| 1280×800 | 449 (400) | 400 | 299 → 250 | 800 → 800 |
| 1024×768 | 433 (384) | 384 | 283 → 234 | 768 → 768 |
| 720×900 | 535 (450) | 450 | 385 → 300 | 900 → 900 |
| 390×844 | 507 (422) | 422 | 357 → 272 | 844 → 844 |
| 320×568 | 369 (284) | 284 | 219 → 134 | 568 → 568 |

- **Layout / position**: the field's box centre is the window's middle; the logo (96×96) is drawn
  above it with its 26px gap; the field keeps its 610×56 box and the button its 44×44 inset of 6px.
- **Size / spacing**: nothing changes size. The section fills the stage's content box exactly, so the
  logo's top edge moves up by the 49px (desktop) / 85px (phone) the field rises.
- **Colour / typography**: unchanged — no token, colour, or font declaration in the change.
- **States**: hover, focus, active, disabled, empty, error, loading are untouched; the results view's
  compact bar stays at the top; the reading view never paints this section.
- **Motion**: none added — the field does not travel on load, and there is no transition on the
  section's height.
- **Responsive**: the centring holds at 320–1920px, in both the drawer layout (≤1272px) and the phone
  toolbar layout (≤720px). Two numbers behind today's phone offset: the section is 36px taller than the
  stage's content box (it subtracts `--pad-top` 40 instead of the toolbar's 76), and the field is 61px
  below the section's own middle — half the 96+26 logo block.

## Assumptions

- "Center the search bar vertically" means the field's own box on the window's middle line, with the
  logo above it — not the logo-and-field block, which already measures centred today (±5px) and whose
  centring is what puts the field 49px low.
- The window is the reference, not the stage's content box: the stage pads 40px above and 64px below,
  so a section centred inside it lands 12px above the window's middle. The spec cancels that
  difference rather than inheriting it, because a person measures against the window.
- The results and reading views are out of scope; the results bar's position at the top is a decision
  of spec 004 and is not reopened here.
- The change is CSS-only: no markup, no template context, no JavaScript and no new asset.
- No animation is wanted; the bar does not drift while the window resizes.
- The phone's pre-existing 36px overhang (FR-004) is fixed *as part of* centring, since leaving it would
  make the claim false at four widths below 720px.

## Clarifications

### Session 2026-10-27

- No question was left open. The request's one ambiguity — the field, or the logo-and-field block — is
  settled by measurement rather than by asking: the block is already centred on the window within 5px
  at every width (1920×1000: block 399–577 in a 1000px window), so a report that the page reads as
  un-centred can only be about the field, which measures 49px low. See the first assumption.
