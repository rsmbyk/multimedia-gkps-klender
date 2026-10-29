# Feature Specification: The preview's verse tabs get their own row, and the reading body takes the first focus

**Slice**: `specs/153-preview-tabs-row`
**Branch**: `fix/153-preview-tabs-row`
**Created**: 2026-10-29
**Status**: Accepted (owner, gate 1, 2026-10-29)
**Input**: "when i open the preview modal for songs, it gets focused on the tabs (the ring around it). also move the tabs below the header as it gets squeezed when the title is long"

## What the dialog does today

`#previewModal` (`reading/_preview_modal.html`) is a two-band dialog: `.preview__head` — the entry's
identity, pinned above the scroller — and the scrolling `.preview__body`. `static/web/preview.js`
lifts the payload's own nodes into that header (`liftIdentity()`): `.preview__ref` / `.preview__song`
becomes the title, and a song's `.preview__tabs` is appended to the `.preview__versetabs` slot. The
header is one flex row (`components.css`: `.preview__head { display: flex; gap: 14px; padding: 14px
22px; min-height: 52px }`), where the title is `min-width: 0; overflow: hidden; text-overflow:
ellipsis; white-space: nowrap` and the tab host is `margin-left: auto`.

Two consequences, both measured on the running app (compose `web`, develop, 1.22.10, `/tatib/144/`,
1440×900, dpr 1):

- **The title is squeezed by the tabs.** The dialog is 704px wide; the header is 704×59 on a song and
  the title's box is 569.6px for a 730px string, so it ellipsizes at the 570th pixel of 660 available.
  The tab row is 76.4×30 at x=973.6 — the row's right edge.
- **The dialog opens on a verse tab.** `showModal()` gives the dialog's initial focus to its first
  focusable descendant, and since spec 085 moved the tabs into the header, that is the first
  `.preview__tab` button. `document.activeElement` is `BUTTON.preview__tab`; opened from the keyboard
  it also paints that tab's `:focus-visible` ring. The same dialog on a **passage** entry — no tabs —
  is 704×52 and focuses `DIV.preview__body`, so the tab focus is a regression from the tab lift, not a
  decision the preview ever made.
- **The dialog's Tab order runs tabs → body → out.** Measured on the same page: from the focused tab
  `1`, `Tab` reaches `#previewContent`; from the body, the next `Tab` leaves the dialog for the
  document (the scroller is the dialog's last focusable element). The tabs precede the body in DOM
  order, so taking the initial focus off the tab also takes away the one `Tab` press that used to lead
  to the reading area.

Measured on the static preview (`preview/preview.html`, same numbers as the app's dialog):

| | today | after |
| --- | --- | --- |
| dialog | 704 × 401.25 | 704 × 439.25 |
| header band | 704 × 59 | 704 × 52 |
| title box | 569.6px (of 730) | 660px (of 730) |
| tab row, from the dialog's top | 14px (inside the header) | 52px (its own row) |
| first tab, from the dialog's left | 605.6px | 22px |
| body top, from the dialog's top | 59px | 97px |
| passage header / body top | 704 × 52 / 52px | 704 × 52 / 52px |

## User Scenarios & Testing

### US1 — A long song title is no longer squeezed by the verse tabs (P1)

**Why this priority**: this is the report — the title is the entry's identity, and it currently reads
through half the room it has.

**Independent Test**: open the preview of a song whose title is longer than the dialog; the title uses
the header's whole content width before ellipsizing, and the tabs stand on a row of their own.

**Acceptance scenarios**

1. **Given** a song entry whose title is 730px long, **When** its preview opens at a 704px dialog,
   **Then** the title's box is 660px — the header's width less its 22px side paddings — and still ends
   in a single-line ellipsis.
2. **Given** the same preview, **When** the header is inspected, **Then** the tab row is not a child of
   the title band: its box starts at the title band's bottom edge, 52px from the dialog's top, and its
   first tab starts 22px from the dialog's left edge.
3. **Given** a song title shorter than the header, **When** it opens, **Then** no ellipsis appears and
   the tab row sits in exactly the same place.

### US2 — The title band and the tabs close as one header block (P1)

**Why this priority**: moving the tabs out of the title's row only helps if the header still reads as
one object; a tab row floating between the header's rule and the lyrics is the other failure mode.

**Independent Test**: with the tabs on their own row, the header draws exactly one rule, and it is the
line the lyrics start under.

**Acceptance scenarios**

1. **Given** a song preview, **When** the header block is measured, **Then** it draws one 1px
   `--divider` line below the tab row, and the title band draws none.
2. **Given** the same header, **When** the gap between the tabs and the rule, and between the rule and
   the first lyric line, are measured, **Then** they are 14px and 22px — the title band's own vertical
   padding and the body's own top padding, both unchanged.
3. **Given** an entry **with no verse tabs** — passage, text, image, audio, video, PDF — **When** its
   preview opens, **Then** the title band draws its rule exactly as today and no empty band appears.

### US3 — Opening a preview focuses the reading body, not a verse tab (P1)

**Why this priority**: it is the other half of the report, and a ring around a control the user did not
reach for reads as a state they caused.

**Independent Test**: open a song's preview; nothing carries a verse tab's focus ring, and the arrow
keys scroll the lyrics without a click first.

**Acceptance scenarios**

1. **Given** a song preview opened with the pointer, **When** the dialog is open, **Then**
   `document.activeElement` is `#previewContent` and no `.preview__tab` has focus.
2. **Given** the same preview opened from the keyboard (focus on Preview, `Enter`), **When** the dialog
   is open, **Then** focus is on `#previewContent` and the ring it paints is the body's own
   `:focus-visible` outline — not a tab's.
3. **Given** a passage or text preview, **When** it opens, **Then** focus is on `#previewContent`
   exactly as today, and no visible ring is painted for a pointer open.
4. **Given** an open song preview whose focus sits on the body, **When** `Tab` is pressed, **Then**
   focus moves to the selected verse tab, and `Shift+Tab` from that tab returns to the body — the two
   ends of the dialog's reading loop hand focus to each other instead of leaving the dialog.

### Edge Cases

- **When** a song carries twelve verse tabs at a 358px dialog **Then** the row keeps its 30px circles,
  4px gaps and horizontal scroll, and no tab wraps or shrinks.
- **When** the header is hidden (an untitled Text) **Then** the tab band is hidden too and the body
  starts at the dialog's top, unchanged.
- **When** the entry is a song with a single verse **Then** no tabs are rendered and the header is the
  52px title band — unchanged from today.
- **When** the theme is dark **Then** the rule is `--divider` `#3A362F`, the tabs keep their selected
  `--active-bg`, and every measured number is identical.
- **When** the dialog is opened by a second click while already open **Then** focus still lands on the
  body and the body is not scrolled.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A song's verse tab row SHALL be a sibling of the title band — the dialog's second child, before the body — and SHALL NOT be a descendant of `.preview__head`. | `new: reading/R28` |
| FR-002 | The title band SHALL give the title the dialog's full content width (660px at a 704px dialog) and keep the single-line ellipsis. | `new: reading/R28` |
| FR-003 | When the entry has verse tabs, the header SHALL draw exactly one rule, below the tab row; the title band SHALL draw none. When it has no tabs, the title band SHALL keep today's rule. | `new: reading/R28` |
| FR-004 | On open, keyboard focus SHALL land on `#previewContent`; no verse tab SHALL receive the dialog's initial focus, by pointer or by keyboard. | `new: reading/R28` |
| FR-005 | A preview without verse tabs SHALL be unchanged: header 704×52 and body top 52px at 1440, 358×52 and 52px at 390. | `new: reading/R28` |
| FR-006 | The tab row SHALL keep the 30×30 circles, the 4px gap and the horizontal scroll when the tabs overflow. | `new: reading/R28` |
| FR-007 | While a visible verse tab row is present and the dialog has no screen-mode footer, `Tab` on the body SHALL move focus to the selected tab and `Shift+Tab` on the selected tab SHALL return it to the body. Every other preview SHALL keep the browser's own order. | `new: reading/R28` |

### Key Entities

- **Preview header block** — the pinned area above the scroller: the `.preview__head` title band and,
  for a song, the `.preview__versetabs` band under it, closed by one 1px `--divider` rule. Hidden
  entirely for an entry with nothing to name.
- **Verse tab row** — `.preview__tabs` (`role="tablist"`), one 30px circular `.preview__tab` per shown
  verse, one `aria-selected="true"`, the others `tabindex="-1"`. It is a control over the panels inside
  the body, so it belongs to the header block and not to the scrolling content.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The title gets the header's whole width | the title's box at the 704px dialog: 569.6px → 660px, still one ellipsized line |
| SC-002 | The tabs stand on their own row, on the title's line | the tab row's top from the dialog's top: 14px (inside the header) → 52px; the first tab's left: 605.6px → 22px |
| SC-003 | The dialog opens on the body | `document.activeElement` on open: `BUTTON.preview__tab` → `DIV#previewContent`, by pointer and by keyboard; `:focus-visible` paints on the body for a keyboard open and on no tab, ever |
| SC-004 | Every other preview is untouched | a passage's header box and body top: 704×52 and 52px before and after, at 1440 and at 390 |
| SC-005 | The lyrics keep their place under the rule | the first lyric line's offset below the rule: 22px, the body's own top padding, unchanged |
| SC-006 | The keyboard keeps the tabs one press away | `Tab` sequence from the body: `#previewContent` → the selected `.preview__tab` → `#previewContent`, never the document behind the dialog |

## UI/UX

Measured on `preview/preview.html` at 1440×900 and 390×844, dpr 1, in both themes. The dialogs in the
preview take the product's own `width: min(44rem, calc(100vw - 32px))`, so the numbers are the shipped
ones.

- **Layout / position**: the dialog keeps `width: min(44rem, calc(100vw - 32px))` — 704px at 1440,
  358px at 390. The title band keeps `padding: 14px 22px` and `min-height: 52px` and now holds the
  title alone (52px, was 59px with the tabs in it). The tab band is the dialog's second child:
  `padding: 0 22px 14px`, one `border-bottom: 1px solid var(--divider)`. The title band drops its rule
  only when a visible tab band follows it (`:has(+ .preview__versetabs:not([hidden]))`), so a preview
  without tabs is unchanged. The body keeps `padding: 22px` and its top edge moves from 59px to 97px
  from the dialog's top. For this payload the dialog is 439.25px tall, against 401.25px.
- **Size / spacing**: the tabs keep 30×30 boxes and a 4px gap; the band's 14px bottom padding repeats
  the title band's own 14px, so the two rows read as one block, and the body's 22px top padding puts
  the first lyric line 22px below the rule — unchanged. First tab 22px from the dialog's left edge, on
  the title's own line.
- **Colour / typography**: nothing changes. Title `640 16px/1.3` `--ink`; tabs `560 13px` with
  `--active-bg` / `--active-ink` when selected; the rule `--divider` (`#D9D6CD` light, `#3A362F` dark).
  No new token or colour.
- **States**: pointer open (no ring anywhere) · keyboard open (the body's existing
  `:focus-visible` 2px `--focus` outline, offset −2px — no new style) · tab selected / hover / keyboard
  focus (unchanged) · 3 tabs and 12 tabs (horizontal scroll, 30px circles) · no tabs (passage, text,
  image, audio, video, PDF — unchanged) · untitled text (both bands hidden) · dark theme · reduced
  motion (no motion added).
- **Motion**: none added or removed; the dialog's own open animation is untouched.
- **Responsive**: no new breakpoint. Below 560px the title band is `padding: 12px 16px` and the tab
  band `padding: 0 16px 12px`; the header block is 95px, against today's 89.8px where `flex-wrap`
  pushed the tabs onto a second row inside the same band. The tabs keep their horizontal scroll.

## Assumptions

- **The rule falls below the tab row**, not between the title and the tabs: the title and tabs close as
  one block, and the line under them is the line the lyrics start under. The alternative — the rule
  kept directly under the title band, with the tabs floating below it — is one click away in
  `preview/preview.html` (`Rule above the tabs`) and measured 3px shorter (94px against 97px); it read
  as a row belonging to neither the header nor the lyrics, which is why it is not the default. —
- **The tab row is left-aligned** on the title's line rather than right-aligned as it was in the title
  row, because the header's left edge is the block's reading line; the tablist keeps its own horizontal
  scroll and its centred fallback is not used.
- **Initial focus goes to the scroll body**, not to the `<dialog>` element and not to the Close control:
  a preview without tabs already focuses `#previewContent` today, and the arrow/`PageUp`/`PageDown`
  handling lives there, so this restores the dialog's existing behaviour rather than adding a third.
- **The dialog keeps a two-step reading loop.** Once the body takes the initial focus, the tab row is
  the only thing before it, and the browser's own order leaves the dialog at the end; the two ends hand
  focus to each other rather than trapping the whole dialog, so no other preview's Tab order changes.
  —
- **A keyboard open paints the body's existing ring.** The rule is already in the stylesheet
  (`.preview__body:focus-visible`); the preview adds nothing. A pointer open paints no ring, in this
  Chromium, on either element — the defect the report saw is the *target* of the focus, which is a tab
  whatever the modality.
- **Only the Tata Ibadah entry preview changes.** `.preview__tabs` is rendered by no other template
  (checked: `multimedia/web/templates/reading/tatib.html` is its only source).
- **Three existing E2E cases** reach the tabs through `.preview__head .preview__tab`; they read
  `.preview__versetabs .preview__tab` after this slice. What they assert — the circles, the scroll, the
  click-to-panel behaviour — does not change.

## Clarifications

### Session 2026-10-29

- Q: none asked — the report names both defects and the preview reproduces them on develop's own
  numbers, so the open design point (which side of the tabs the header rule falls on) is carried as the
  first assumption above and is visible, and switchable, in the preview.
