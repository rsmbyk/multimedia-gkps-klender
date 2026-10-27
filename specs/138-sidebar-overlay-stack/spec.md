# Feature Specification: On a small screen the sidebars are a drawer stack over the page

**Slice**: `specs/138-sidebar-overlay-stack`
**Branch**: `feat/138-sidebar-overlay-stack`
**Created**: 2026-10-27
**Status**: Accepted (owner, gate 1, 2026-10-27 — accepted on the live prototype after five rounds of
corrections; the two breakpoints and the four small behaviours are the owner's answer, recorded in
`## Clarifications`)
**Input**: "i want you to change the sidebar behavior on smaller screens: — only one sidebar can open at a time — it is an overlay, not pushing the page — second-level sidebars open on top of the first-level sidebars — clicking on the overlay behind the sidebars will close — clicking on the main rail will open the last opened level sidebar. if the last opened sidebar is second-level, open its first-level as well simultaneously. on mobile screens (image 2): — the sidebars are open in full size — add a top toolbar consisting only the gkps logo on the end left (with the sidebar-like icon to open the main rail) and the light/dark toggle on the end right — the main rail is now opens as a sidebar with logo and text. — clicking on the gkps logo will also open the last opened level sidebar. if opening a deeper-level sidebar, it also opens its consecutive higher-level sidebars simultaneously."
**Revised**: 2026-10-27, after the owner reviewed the live prototype — see `## Clarifications`. The
logo no longer opens anything; the toolbar's control does it all, and the second level now covers its
parent instead of leaving an edge.

## What the shell does today

Three columns ride beside the rail and each one **pushes** what is to its right: the first-level
panel (`data-nav` = `closed | mini | open`, 18.5rem for books, 26rem for Tata Ibadah), the
second-level list (`data-ch` = `closed | open` — chapter rail at rail width, or the song list at
26rem), then the stage. Below 1272px the second-level list covers its parent instead of sitting
beside it; below 720px the panel floats over the stage but the stage keeps a rail-wide margin, and
opening the second level closes the first, which returns when the second closes. There is no
backdrop and no memory of which level was open last: the rail toggles the first level only, and on a
phone the rail is still an 80px (64px at ≤560px) icon strip that eats the width the page needs.

## User Scenarios & Testing

### US1 — A drawer over the page, never a column that shrinks it (P1)

**Why this priority**: this is the request. On the 768px screen in the report the panel takes 360px
of a 768px window and the reading pane is squeezed into what is left; the operator reads a
half-width page with a list they are not looking at.

**Independent Test**: at the overlay width, open the first level and then the second; at no point
does the stage's width change, and the drawers sit over the page.

**Acceptance scenarios**

1. **Given** a window at the overlay width, **When** the first level opens, **Then** the stage keeps
   the width it had with the drawer closed, and the drawer is drawn over it.
2. **Given** the same window, **When** the second level opens, **Then** it covers the first
   completely — same left edge, same width — and the stage's width still does not change.
3. **Given** the same window, **When** a level opens, **Then** it appears to slide out from under the
   rail: the rail is painted above the drawers, so the drawer's leading edge emerges from the rail's
   right edge rather than from the window's left edge.
4. **Given** a window wider than the overlay width, **When** a drawer opens, **Then** the present
   push-and-shrink layout is unchanged.

### US2 — One stack, and only one (P1)

**Why this priority**: "only one sidebar can open at a time" with "second-level sidebars open on top
of the first-level sidebars" means a stack, not three columns: a child is drawn over its parent, and
a sibling section never opens beside it.

**Independent Test**: open Tata Ibadah's first and second level, then switch the rail to Kidung; the
Tata Ibadah drawers are gone and Kidung's own stack opens in their place.

**Acceptance scenarios**

1. **Given** an open second-level drawer, **When** a different section is chosen from the rail,
   **Then** the previous section's drawers close and the new section's first level opens.
2. **Given** the first and second levels open, **When** the second closes, **Then** the first is
   still open and drawn where it was.

### US3 — The backdrop closes, the rail restores (P1)

**Why this priority**: with no push there must be a way back that is not a hunt for a chevron, and
the rail must not lose the operator's place.

**Independent Test**: open a stack, click the dimmed page; everything closes and the stage is
untouched. Open it again from the rail; the level that was last open returns.

**Acceptance scenarios**

1. **Given** an open drawer stack, **When** the operator clicks the backdrop, **Then** the whole
   stack closes and the stage is as it was.
2. **Given** the last thing open was the second level, **When** the rail's section is chosen,
   **Then** the first level opens and the second opens with it, in one motion.
3. **Given** the last thing open was the first level, **When** the rail's section is chosen,
   **Then** the first level opens alone.
4. **Given** an open drawer, **When** the operator presses Escape, **Then** the whole stack closes and
   the page is whole again.

### US4 — A phone gets a toolbar and a real menu (P1)

**Why this priority**: on a 425px window the icon strip costs a tenth of the width and its glyphs
are unlabelled; the report asks for the toolbar and for the rail as a labelled drawer.

**Independent Test**: at the phone width the page shows one toolbar — a control, then the logo, at
the left, and the theme at the right — and nothing else of the shell until the control is pressed.

**Acceptance scenarios**

1. **Given** a phone-width window, **When** a page opens, **Then** a top toolbar is drawn with the
   **control** at its far left and the GKPS logo immediately after it, and the page beneath is full
   width.
2. **Given** the same window and nothing open, **When** the control is pressed, **Then** the main
   menu opens as a drawer at full width, listing each section with its icon **and its name**, and
   the control becomes a **close** glyph.
3. **Given** the main menu open, **When** a section is chosen, **Then** its list slides in over the
   menu — the menu stays underneath, the control stays a **close** glyph — and the list's own back
   control returns to the menu.
4. **Given** any drawer open, **When** the control is pressed, **Then** the drawer closes and the
   page is whole again; it never steps back one level.
5. **Given** a Tata Ibadah service at the phone width, **When** its list is open, **Then** no
   contents drawer is offered, and the Project control is not drawn anywhere on the page.
5. **Given** the same window, **When** the logo is pressed, **Then** nothing opens — the logo is a
   mark, not a control, and only the toolbar's control opens the shell.
6. **Given** a phone-width window, **When** a drawer is open, **Then** it covers the full width of
   the window, under the toolbar.

### US5 — Reading is not disturbed (P2)

**Why this priority**: the drawers are furniture; the page under them must still be the page the
operator was on, unchanged when they close.

**Independent Test**: scroll a long service, open a drawer stack, close it; the same scroll position
and the same content are where they were.

**Acceptance scenarios**

1. **Given** a scrolled stage, **When** a stack opens and closes, **Then** the stage's scroll
   position and width are unchanged.
2. **Given** a drawer open, **When** the page behind it is scrolled by wheel or touch, **Then** the
   page does not move: the stage's scroll is locked while any drawer is open.

### Edge Cases

- **When** the window is resized across the overlay width **Then** the shell is left in a state that
  fits the new width, with nothing open that the wider layout cannot show.
- **When** the stage has no page in it (the search landing) **Then** the drawers still open and close
  the same way.
- **When** the drawers are open and the operator navigates in place **Then** the stack stays where it
  is, as the current panel does.
- **When** a second-level list is empty **Then** opening it shows its empty state over the parent.
- **When** the phone's toolbar is on screen and a modal is open **Then** the modal is above both the
  toolbar and the drawers.
- **When** the window is rotated at a phone width **Then** the toolbar stays at the top and the
  drawers keep the window's full width.
- **When** a row is selected in the phone's menu **Then** its name and its icon carry the same ink,
  the selected colour of the icon and not the resting ink of the text.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | At or below the overlay width, opening a level SHALL NOT change the stage's width; the drawer SHALL be drawn over the page. The overlay width is **≤1272px**. | `new: reading` |
| FR-002 | At or below the overlay width, a second-level drawer SHALL cover its first-level parent exactly — same left edge, same width — and SHALL be painted above it. | `new: reading` |
| FR-003 | A drawer opening at the overlay width SHALL appear to slide out from under the rail: the rail SHALL be painted above the drawers, and a drawer at rest SHALL sit entirely behind it. | `new: reading` |
| FR-004 | At most one section's drawers SHALL be open: choosing another section closes the previous stack and opens the chosen one's first level. | `new: reading` |
| FR-005 | A backdrop SHALL cover the page behind the drawers and close the whole stack when clicked. | `new: reading` |
| FR-006 | The rail's section control SHALL reopen the last-opened level: the first level alone when that was the last level, the first and second together when the second was. | `new: reading` |
| FR-007 | At the phone width the shell SHALL draw a top toolbar holding one control at its far left, the GKPS logo immediately after it, and the light/dark control at its right end. The phone width is **≤720px**. | `new: reading` |
| FR-008 | The toolbar's control SHALL be the only thing that opens the shell on a phone, and it SHALL carry two glyphs: **menu** when nothing is open, **close** when anything is. | `new: reading` |
| FR-009 | Pressing the control while anything is open SHALL close the open drawer, not step back a level; going back one level SHALL be the drawer's own back control (FR-015). | `new: reading` |
| FR-010 | At the phone width the main rail SHALL open as a drawer listing the sections of the main menu only — each with its icon and its name — with no logo and no controls of its own. | `new: reading` |
| FR-011 | The controls the rail keeps at its foot (transfer progress and the light/dark toggle) SHALL move to the toolbar at the phone width. | `new: reading` |
| FR-012 | At the phone width every drawer SHALL be the window's full width and start under the toolbar. | `new: reading` |
| FR-013 | The stage's width, scroll position and content SHALL be unchanged by opening and closing any stack. | `new: reading` |
| FR-014 | The shell's present behaviour above the overlay width SHALL be unchanged: the same push, the same mini state, the same second level covering its parent below 1272px. | `reading/R1` |
| FR-015 | The two collapse controls inside the drawers (the first level's close and the second level's back) SHALL keep working at every width. | `new: reading` |
| FR-016 | A selected row in the phone's menu SHALL draw its name in its icon's ink, so the label reads as part of the selected control. | `new: reading` |
| FR-017 | The Project / Stop projecting control SHALL NOT be drawn at the phone width. | `new: reading` |
| FR-018 | A Tata Ibadah service SHALL offer no contents drawer at the phone width: its rows jump within the page already on screen, so the level is never opened there. | `new: reading` |
| FR-019 | At the phone width a section chosen from the menu SHALL slide its list in **over** the menu, which stays underneath, and the list's own back control SHALL return to it — the two never swap places. | `new: reading` |
| FR-020 | At the phone width a Tata Ibadah row in the section list SHALL open the service's page and close the drawers, since the contents level is not offered (FR-018); above the phone width the same row keeps opening the contents level. | `new: reading` |
| FR-021 | A sidebar row's edit control SHALL be visible without a pointer hover where the pointer cannot hover (a touch screen) and at the phone width — the exemption the entry controls and the add tiles already carry. | `new: reading` |
| FR-022 | Every icon in the phone toolbar SHALL be drawn at one size — the rail's own 24px — so the control, the foot's controls and the theme glyph read as one set. | `new: reading` |
| FR-023 | At the phone width a sidebar row SHALL stack what it carries: the name (with its `Today` badge) on one line and its date or short name on the next, so an always-visible edit control never squeezes either, and no text SHALL run under that control. | `new: reading` |

### Key Entities

- **Level** — a drawer: the main menu (`0`), the section's list (`1`), the chapter or song list
  (`2`). Today: the rail is a fixed strip, `1` is `data-nav`, `2` is `data-ch`.
- **Stack** — the levels currently open, `1` or `1+2`, belonging to one section.
- **Control** — the single toolbar button whose glyph is `menu`, `close` or `back`.
- **Last level** — the deepest level that was open for the current section, remembered so the rail
  (above the phone width) can restore it.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The stage never changes width while a drawer opens | the stage's `getBoundingClientRect().width` is identical before and after opening level 1 and level 2 |
| SC-002 | The second level covers its parent | at the overlay width, the two drawers' left edges and widths are equal |
| SC-003 | The rail paints above the drawers | the rail's effective `z-index` is greater than each drawer's, and a drawer at rest is entirely behind it |
| SC-004 | One section at a time | after switching sections with a stack open, the previous section's drawer is not rendered |
| SC-005 | The backdrop closes everything | a click on the backdrop leaves `data-nav` and `data-ch` closed and the stage's scroll unchanged |
| SC-006 | The last level is restored | after opening level 1 then 2, closing, and choosing the rail's section again, both levels are open |
| SC-007 | The phone shows one toolbar and no strip | at the phone width the toolbar is visible, the rail is not, and the stage spans the window |
| SC-008 | The control carries three states | at the phone width its glyph is `menu` closed, `close` with the menu open, `back` with a section drawer open |
| SC-009 | The menu drawer is the main menu only | at the phone width it holds the five section rows with names and icons, and no logo |
| SC-010 | The foot moved | at the phone width the transfer and theme controls are inside the toolbar, not the menu drawer |

## UI/UX

Measured on the prototype (`preview/prototype-tatib.html`, built from this branch's own page) at
1440×900, 1024×900, 768×900 and 425×900:

- **Stage width, closed → level 1 → level 2**: **1360 → 944 → 528px** at 1440 (the columns, still
  pushing); **944 → 944 → 944** at 1024; **688 → 688 → 688** at 768; **425 → 425 → 425** at 425.
- **First-level drawer**: 80px from the rail's edge, **416px** wide at 1024, **368px** at 768 (the
  page's own `--panel-w`); **425px** — the window — on a phone.
- **Second-level drawer**: the same left edge and the same width as its parent; at 1024 both are
  **80 → 496px**, at 768 both **80 → 448px**, on a phone both **0 → 425px**.
- **The rail**: **80px** (**64px** at ≤560px), painted above the drawers; the drawers' resting
  transform is their own width to the left, so they emerge from its right edge.
- **The toolbar**: **58px** tall, fixed at the top; a **42px** control, the **34px** logo, the page's
  section name, and the rail's foot (44px buttons) at the right. The stage clears it with
  `58 + 12px` of top padding.
- **The phone's menu drawer**: rows **48px** tall, **12px** apart, icon **22px** with its name
  **14.5px/600**; full window width; no logo, no foot.
- **Colours**: the backdrop is the shell's `--backdrop` (`rgba(0,0,0,.68)`); a selected menu row
  paints its name in `currentColor`, the same ink as its icon.
- **Motion**: the drawers slide on the shell's `--ease` (`cubic-bezier(.32,.72,.28,1)`); the second
  level moves one step above the first, so a stack opened from one control arrives as one motion.
  `prefers-reduced-motion` keeps the present instant behaviour.
- **States**: closed; first open; first+second open; main menu open (phone); the control in each of
  its three glyph states; a selected row in light and dark; the reduced-motion variants.

## Assumptions

- **The desktop keeps its columns.** The report is about smaller screens; above the overlay width the
  present push layout stays.
- **The drawers are the same components**, re-laid-out: the same panel, the same chapter and song
  lists, the same rows — not new markup.
- **The toolbar is fixed to the top**, so it does not scroll away with the page.
- **The logo is a mark, not a control** on a phone; it is not a link home either, unless the owner
  says so.
- **The theme control keeps its three states** (system, light, dark) wherever it is drawn.
- **No new icons or fonts**; the logo is the existing `static/assets/gkps.png`.

## Clarifications

### Session 2026-10-27

The owner reviewed the live prototype and answered seven points; each is written into the
requirements above.

- **The second level covers its parent** and slides out from under the rail — no offset, no visible
  parent edge (FR-002, FR-003, US1.2–US1.3). *Retracts* the prototype's 44px stack offset.
- **The phone's drawers are the full window width** — no inset strip (FR-012). *Retracts* the
  prototype's 12px phone inset.
- **The selected row's name takes its icon's ink** (FR-016, Edge Cases).
- **The toolbar's control sits at the far left and the logo immediately after it**, and only the
  toolbar's control opens the shell (FR-007, FR-008, US4.1, US4.5). *Retracts* FR-009 of the first
  draft — "the toolbar's logo reopens the last-opened level" — and the matching US4.4: the logo now
  opens nothing.
- **The phone's menu drawer is the main menu only**: no logo inside it, and the rail's foot moves to
  the toolbar (FR-010, FR-011, SC-009, SC-010).
- **The control becomes back or close with the state** (FR-008, FR-009, US4.2–US4.4).
- **The Project control is hidden at the phone width** (FR-017).
- **No Tata Ibadah contents drawer on a phone** — the list jumps within the page already on screen,
  so the level is not offered (FR-018).
- **The toolbar's control is close-only**; back one level belongs to each drawer's own control
  (FR-009, FR-015). *Retracts* the revision's "back" glyph: the control has two glyphs, menu and
  close, not three.
- **A section's list slides in over the menu on a phone**, and the menu stays underneath (FR-019).
- **A Tata Ibadah row on a phone opens the service's page** and closes the drawers, since there is no
  contents level to open there (FR-020).
- **A row's edit control shows without hover** on a touch screen and at the phone width (FR-021):
  the project exempts `.entry__acts` and the add tiles from hover with
  `@media (hover: none) and (pointer: coarse)`, but `.row-edit` was missed.
- **One icon size in the toolbar** (FR-022). The prototype's own control was 22px beside the
  project's 24px theme glyph — a real 2px mismatch the owner spotted, now both 24px.
- **A phone's row stacks its name and its date**, with the edit control always on (FR-023): the date
  was being clipped to `25 Okt 2…` once the pencil held the right-hand column.
- **The remaining four settled at gate 1**: the overlay starts at **≤1272px** (FR-001), the phone
  shell at **≤720px** (FR-007), **Escape closes the whole stack** (US3.4), **the page behind a drawer
  does not scroll** (US5.2), and **the toolbar is fixed** (Assumptions). Each was carried by the
  prototype; the owner accepted them unchanged.
