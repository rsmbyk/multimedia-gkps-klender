# Feature Specification: Song-row focus ring is clipped at the list top

**Slice**: `specs/223-songrow-focus-ring-clip`
**Branch**: `fix/223-songrow-focus-ring-clip`
**Created**: 2026-11-22
**Status**: Accepted (Gate 1 2026-11-22)
**Input**: "i dont know how that focus ring gets there, but it clearly shows that the top is clipped"
**Demand**: `ITEM-238`
**Capability**: adds `reading/R52`

## User Scenarios & Testing

### US1 — The top row's focus ring is drawn in full (P1)

**Why this priority**: a keyboard reader who Tabs onto the first song sees a ring that marks where
focus sits. On the current page the ring's top edge is cut off by the scrollport because the row
sits flush with it; the indicator is visibly incomplete exactly where a reader starts navigating.

**Independent Test**: at 900×700 open `/songs/1820/` in dark mode, click the first `#chList`
row, press any key, and compare a screenshot before and after focus around the row's top edge.
The painted ring must have a complete top edge inside `#chBody`; the row's text, height and
selection state must be unchanged.

**Acceptance scenarios**

1. **Given** the first song row is at `scrollTop = 0` with its top equal to `#chBody`'s top
   **When** it is focused by Tab **Then** its whole focus indicator is visible inside the
   scrollport, including the top edge.
2. **Given** the row holds focus from a pointer click **When** any key is pressed **Then** the
   browser promotes it to `:focus-visible` and the full ring appears — the pointer click alone
   paints nothing.
3. **Given** the chosen fix **When** the row is not focused **Then** its computed outline remains
   `none 0px`, and its hover and `aria-current="true"` fills are unchanged.
4. **Given** the list is scrolled to the bottom **When** the last row is focused **Then** its ring
   is not clipped by the bottom edge either; the existing 8px bottom padding is preserved.
5. **Given** dark or light theme and a 1440×900, 900×700 or 390×844 viewport **When** the songs
   list is open and its first row is focused **Then** the complete ring is visible with the theme's
   focus colour. At the phone breakpoint the list is a drawer, so it must be opened first.
6. **Given** the chosen fix **When** the first sidebar's rows and song detail pages are used
   **Then** their focus behaviour is byte-identical to the base.

### Edge Cases

- The symptom is not a scrolled list: at 900×700 `#chBody` has `scrollHeight = clientHeight =
  570` and `scrollTop = 0`. Any fix that only changes scroll position cannot pass scenario 1.
- A three-line song row measures 57.5px against the 38px single-line row; the fix must not clamp
  or resize either.
- The list's existing 10px side padding already leaves room at the left and right edges; only the
  top edge lacks space.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | When a `.songrow` in `#chList` holds keyboard focus, its focus indicator SHALL be painted in full inside the `#chBody` scrollport, including the top edge when the row is first. | `new: reading/R52` |
| FR-002 | The fix SHALL NOT change the row's height (38px single-line, 57.5px three-line sample), its 1px pitch, its text, its order, or the hover and `aria-current="true"` fills. | `reading/R52` |
| FR-003 | An unfocused `.songrow` SHALL keep `outline: none 0px`; focus is the only state that paints a ring. | `reading/R52` |
| FR-004 | With the songs list open, the complete ring SHALL be visible in both themes at 1440×900, 900×700 and 390×844, and when the list is scrolled to its last row. | `reading/R52` |
| FR-005 | The first sidebar, the song detail page and every other focusable control SHALL keep their existing focus styles and geometry. | `reading/R52` |
| FR-006 | The slice SHALL reserve 3px of space above the first row in the `#chBody` scrollport and keep the browser's default outline; it SHALL NOT restyle the ring or move any other box. | `reading/R52` |

### Key Entities

None. The change is a CSS state rule over an existing list.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | The focused first row's ring has a complete top edge inside `#chBody`. | Playwright pixel diff before/after focus over the row's top boundary; changed pixels appear at or below the scrollport top, never only on the sides. |
| SC-002 | The cause is the scrollport boundary, not a scrolled list. | Playwright: `#chBody` `scrollTop = 0`, `scrollHeight = clientHeight` before focus. |
| SC-003 | Row geometry and states are unchanged. | Playwright: same row count, same first four row tops modulo the candidate's declared 0px or 3px offset, same 38px/57.5px heights, same `aria-current` and hover colour. |
| SC-004 | The ring is visible through keyboard focus and through key-after-pointer focus. | Playwright: Tab to the row in one run; click then press `a` in another; assert the same complete ring in both. |
| SC-005 | No ring paints on an unfocused row. | Playwright: computed `outlineStyle === 'none'` before focus and after moving focus away. |

## UI/UX

`static preview at specs/223-songrow-focus-ring-clip/preview/index.html` — the live reading page's
real markup, tokens, fonts and stylesheets, with a switcher for **Current**, **A · 3px space** and
**B · inset ring**; click **Focus top row**, then press any key. The same three states are available
live at `http://127.0.0.1:8767/songs/1820/` with the candidate CSS injected by the probe.

- **Current (measured, 900×700, dark)**: row top `130.0px`, `#chBody` top `130.0px`,
  `padding-top: 0px`, `scrollTop: 0`, computed outline `auto 1px rgb(16, 16, 16) 1px` — 2px of
  ring sits above the row and is clipped. A pixel diff before/after focus shows changed pixels
  starting at y=130 and none at y≤129.
- **Candidate A**: `#chBody` `padding-top: 3px`; first row top `133.0px`, gap `3.0px`, the next
  rows at `172.0 / 230.5 / 269.5px`; the browser outline is unchanged and its top edge is drawn.
- **Candidate B**: row top stays `130.0px`; outline becomes `2px solid rgb(124, 156, 240)
  offset -2px` in dark mode; no box moves, and the ring is drawn inside the row.
- **States**: unfocused, Tab-focused, pointer-clicked then keyed, selected row, hovered row,
  scrolled-to-last-row, dark and light, 1440×900 / 900×700 / 390×844.
- **Motion**: none added or removed.
- **Colour / typography**: A changes neither; B uses the existing `--focus` token already used by
  other controls. No new token or font.

## Assumptions

- The ring is the browser's UA outline, not a product rule: no `.songrow:focus-visible` selector
  exists in `static/styles/design/components.css` at the re-based base `e8e79dbb` (and at the
  original base `bb7c1887`).
- Focus reaches the row by Tab, or by a key pressed while pointer focus is still on the row; the
  pointer click alone does not satisfy `:focus-visible`.
- The first sidebar's `.book` rows and other pages are out of scope even where they share a class.
- Candidate A's 3px value is the measured minimum clearance for a 1px outline at a 1px offset;
  acceptance asserts the relationship (ring inside the scrollport), not a hardcoded page coordinate.
- Candidate B (inset `--focus` ring, no geometry change) was offered in the preview but timed out
  at Clarify. Its recommendation — candidate A — is recorded as this assumption and can be reopened
  at gate 1; B stays visible in the preview for comparison, not in scope.
- Zero `[NEEDS CLARIFICATION]` markers remain; the single Clarify question was skipped and is
  recorded above rather than deferred.
