# Feature Specification: Verse modal header draws one rule

**Slice**: `specs/226-verse-modal-header-rule`
**Branch**: `fix/226-verse-modal-header-rule`
**Created**: 2026-11-23
**Status**: Accepted (Gate 1 2026-11-23)
**Input**: "there is a duplicate short line below the new/edit verse modal's header"
**Demand**: `ITEM-241`
**Capability**: adds `reading/R54`

## User Scenarios & Testing

### US1 — The verse editor's header carries one rule (P1)

**Why this priority**: the report is about a visible double line in the editor a reader opens to
add or edit a song verse. The header already has a full-width divider; a second, shorter stroke
under the title reads as a rendering mistake and is the only thing the slice is asked to change.

**Independent Test**: at 1366×900 open a song with verses, press `Add verse`, and read the header.
The title's computed `border-bottom-width` is `0px`; the only rule in the header is the 840px
`.editor__head` divider. The gap from the title text to that rule is 16.5px — the non-verse
`New song` editor measures 16px. Repeat from a verse's edit control; both dialogs match.

**Acceptance scenarios**

1. **Given** an ordinary song with verses **When** `Add verse` opens the dialog titled `New verse`
   **Then** the header paints one horizontal rule, the full-width `.editor__head` divider, and the
   title paints no rule of its own.
2. **Given** an existing verse **When** its edit control opens the dialog titled `Edit verse n`
   **Then** the same single-rule header is painted.
3. **Given** the dialog is open **When** the header is measured **Then** the title's computed
   `borderBottomWidth` is `0px` and the head's is `1px` with `--divider` colour; no other header
   descendant paints a horizontal border.
4. **Given** the fix **When** the header is measured **Then** the title text keeps its x=289 inset,
   21px type and 21px top gap, the title's 20px bottom padding is replaced by the header's 14px
   bottom padding, and the gap from the title text to the divider is 16.5px (16px in non-verse
   editors).
5. **Given** the fix **When** the textarea, actions and dialog boxes are measured **Then** they
   keep their boxes apart from the header's 21px shorter height; the 30px border-to-label gap and
   the 21px font/640 weight stay.
6. **Given** a non-verse editor (songbook, song, Tata Ibadah) **When** its dialog opens **Then**
   its header and rules are byte-identical to the base.
7. **Given** light or dark theme and 1366×900, 900×700 or 390×844 **When** a verse dialog is open
   **Then** exactly one header rule is painted at every size.

### Edge Cases

- The loading skeleton is built without `data-editor-size="large"`, so the large-editor rule does
  not apply while the form is being fetched; it must stay that way.
- The verse editor has no `Copy as template` button, so its header row contains only the title; the
  rule under the row is still the head's own border, not the title's.
- At phone widths the dialog's `min(840px, 100vw - 32px)` width shrinks; the single rule must shrink
  with the head rather than stay at 840px.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The large-editor rule SHALL NOT paint a bottom border on the `.editor__title` inside `.editor__head`. | `new: reading/R54` |
| FR-002 | The verse editor's header SHALL paint exactly one rule: the existing 1px `--divider` bottom border of `.editor__head`, for both `New verse` and `Edit verse n`. | `reading/R54` |
| FR-003 | The title's 21px font, 640 weight, 21px top gap and x=289 text inset SHALL be unchanged. Its 20px bottom padding SHALL move to the header's 14px bottom padding so the title-to-divider gap is 16–17px, matching non-verse editors. | `reading/R54` |
| FR-004 | Non-verse editors, the loading skeleton, the form fields, the actions row and all other dialog rules SHALL be unchanged. | `reading/R54` |
| FR-005 | The single header rule SHALL follow the head's width at every viewport, including the narrow breakpoint. | `reading/R54` |
| FR-006 | The head's 16px bottom margin and the first field's 14px top margin SHALL stay, keeping the 30px gap between the divider and the `Lyric` label. | `reading/R54` |

### Key Entities

None. The change is one CSS rule over an existing dialog.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | A verse dialog's header paints one rule, not two. | Playwright read-back: `getComputedStyle(title).borderBottomWidth === '0px'` and `getComputedStyle(head).borderBottomWidth === '1px'`, with a screenshot of the header. |
| SC-002 | The rule spans the head, not the title. | Playwright: head border width 840px at 1366×900 and `min(840px, 100vw - 32px)` at narrow widths; title border width 0. |
| SC-003 | The header rhythm matches the other editors and nothing else changes. | Playwright: title text x=289, 21px font, 21px top gap, 16–17px title-to-divider gap; textarea box, actions box and non-verse headers match the base. |

## UI/UX

`live preview at http://127.0.0.1:63404/songs/1820/` — the running app's own route, with the
candidate injected by `specs/226-verse-modal-header-rule/preview/probe.py --inject-fix`. This slice's
only visible effect is a double draw, so the gate material is the measured defect and its removal;
the harness and its read-back live beside this file.

- **Before (measured, 1366×900, light)**: dialog at (263, 70) 840 × 760. The title
  `New verse` sits at (263, 70) 157.0 × 72.5 with `border-bottom: 1px solid rgb(217, 214, 205)`
  and its line ends at y=142.5. The head is 840 × 87.5 with its own 1px bottom rule at y=157.5 —
  a 15px gap between two rules of the same token.
- **After (candidate injected, same viewport)**: title box 105.0 × 31.5 at (289, 90) with
  `border-bottom: 0px none`; head 840 × 66.5 with padding `20px 26px 14px` and the only 1px
  `--divider` rule at y=135.5. Title text stays at x=289, y=91–119, 21px/640; the gap below it
  is 16.5px. The dialog stays at (263, 70) 840 × 760; the `Lyric` label moves from y=187.5 to
  y=166.5 with the header.
- **Reference rhythm**: the non-verse `New song` editor at the same viewport has a 23px top gap,
  16px title-to-divider gap and 16px divider-to-label gap. The verse dialog keeps its own 21px
  top gap and 30px divider-to-label gap (the large form's first field has a 14px top margin);
  only the title-to-divider gap is brought into line.
- **Colour / typography**: `--divider` (`rgb(217, 214, 205)` in light) stays the rule's colour; no
  new token, face or font size.
- **States**: new verse, edit verse, loading skeleton, non-verse editors, light and dark.
- **Motion**: none added or removed.
- **Responsive**: the remaining rule is the head's border, so it tracks the dialog's
  `min(840px, calc(100vw - 32px))` width; no fixed-width rule is introduced.

## Assumptions

- The fix changes two declarations of the large-editor rule at `static/styles/design/components.css:541`
  — `padding: 20px 26px` becomes `padding: 0`, `border-bottom` becomes `0` — and gives the large
  head `padding: 20px 26px 14px`. That preserves the title's 26px side and 20px top inset while
  making the title-to-divider gap 16.5px, the other editors' 16px within half a pixel.
- The cause is a specificity conflict: `.editor:has([data-editor-size="large"]) .editor__title`
  (0,3,0) outranks the header reset `.editor__head .editor__title` (0,2,0), so spec 195's
  `border: 0` never reaches the large dialog's title.
- The screenshot in the report was taken on a deployed build whose field is labelled `Lyrics`;
  the current `develop` build labels it `Lyric` but paints the same two rules, so the fix is made
  against current `develop`.
- No data, template, script or test fixture outside the CSS rule needs to change for the visible
  defect; the E2E pin is added to guard the state.

## Clarifications

No open questions. Zero clarification markers remain.

### Session 2026-11-23

- Q: "also fix the gaps between the title and border" → A: "just like the other modals's".
  Measured reference: the non-verse `New song` editor has a 16px title-to-divider gap; the verse
  header's 37.5px gap is reduced to 16.5px. The 30px divider-to-label gap stays, because the large
  dialog's first field carries its own 14px top margin.
