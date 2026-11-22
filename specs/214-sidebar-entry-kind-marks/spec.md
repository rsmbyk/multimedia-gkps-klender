# Feature Specification: a contents row marks its entry's kind

**Slice**: `specs/214-sidebar-entry-kind-marks`
**Branch**: `feat/214-sidebar-entry-kind-marks`
**Created**: 2026-11-21
**Status**: Draft
**Input**: "i want you to add as a column after the entry order number in service entry sidebar the corresponding icon/mark of the entries" — owner, 2026-11-21.

## What the page does today

The Tata Ibadah's second sidebar column (`#chList`, rendered by `reading/_toc.html`) is the running order.
Each numbered row is one `<a class="songrow">` holding the order number and the label:

```html
<span class="songrow__c">{{ item.n }}</span>
<span class="songrow__t">…label…</span>
```

`.songrow__c` is a **54.39px**-wide, left-aligned number at **10px** from the row's edge; the label starts
**74.39px** from that edge. A section break is a different shape (`li.toc__eos`): it carries `data-num`
but paints no visible number, only a 1px rule, and its box is **13px** tall.

The row's kind is stated only in words. Every other surface marks it in a shape: the stage draws a
20px book or note for a passage or song (spec 144, `reading/R25`), a 42px tinted chip for a media file,
and a 13px corner badge on a slot's mark (spec 213). Spec 144 FR-008 and spec 213's sidebar edge case
explicitly kept `#chList` and the dock on their own anatomy, and `tests/e2e/test_stage_kind_marks.py`
asserts there is no `.entry__kind-icon` inside `#chList`. This slice reverses that boundary for
`#chList` only; the dock stays as it is.

Measured on the static preview (built from the product's `tokens.css`, the live `.songrow` rules in
`components.css` and a clone of `_toc.html`'s markup) in a **404px** pane — the width a 1440px window
leaves with both sidebars open — at 1× in Chromium, light and dark:

| | number x from row edge | mark x | label x from row edge | contents list height |
| --- | --- | --- | --- | --- |
| today, no column | **10px** | — | **74.39px** | **354.25px** |
| A · number box unchanged | **10px** | **74.39px** | **100.39px** | **354.25px** |
| B · compact number box (24px), break row unchanged | **10px** | **42px** | **66px** | **354.25px** |

The mark adds no height to any numbered row: in all three columns the six numbered rows measure
79.2 / 52 / 52 / 52 / 52 / 52px, with the same line counts, and the list keeps its **354.25px** height.
B's 24px number box holds up to **three digits** (999); a fourth digit grows it to 29.75px and moves the
mark 5.75px right. A's 54.39px box holds seven.

## User Scenarios & Testing

### US1 — The running order can be scanned by kind (P1)

**Why this priority**: this is the request. The sidebar is where the order is arranged and read; which
kind each step is should be known before its words are, the way the stage already says it.

**Independent Test**: a service holding a legacy text row, a passage, a song, a media file, a fill-in, a
choice, a section-break entry and a legacy EOS row; every numbered row paints a distinct mark in a
column after its number, and the eight marks are pairwise distinguishable.

**Acceptance scenarios**

1. **Given** a passage and a song in one service, **When** the contents list is drawn, **Then** each
   row carries its own mark in the column after the number and the two marks differ.
2. **Given** a media file, a text entry and a legacy text row, **When** the list is scanned, **Then**
   each carries a mark and none of the three is mistaken for another.
3. **Given** a template's fill-in and choice rows, **When** the list is drawn, **Then** each carries the
   slot's own mark, distinct from an ordinary entry's.
4. **Given** all the kinds on one page, **When** the gutter is scanned without reading the labels,
   **Then** the kinds are told apart.

### US2 — The mark is decorative and stays out of the row's way (P1)

**Why this priority**: the label already names the entry and is the row's link; the mark must not add a
second tab stop, a tooltip, a pointer target or a changed accessible name.

**Independent Test**: compare the accessible name and the tab order of every row before and after; the
mark is `aria-hidden`, contains no focusable element and takes no pointer.

**Acceptance scenarios**

1. **Given** any numbered row, **When** it is read by assistive technology, **Then** its accessible name
   is byte-identical to today's.
2. **Given** the pointer is over a mark, **When** the row is hovered, **Then** the row's own fill and
   link behaviour are exactly as they are today.
3. **Given** keyboard focus on a row, **Then** focus lands on the row's link or its grip, never the mark.

### US3 — The row keeps its rhythm and its three-line cap (P2)

**Why this priority**: spec 063 fixed the number's vertical centring, spec 135 the three-line clamp and
spec 143/137 the way a long run wraps at the pane. A mark that moves a row or pushes text past the pane
breaks those contracts.

**Independent Test**: measure each row's top and height, the number's centre, the label's line count and
the list's scroll height before and after at 404px and 280px panes in both themes.

**Acceptance scenarios**

1. **Given** a numbered row of any line count, **When** the mark is drawn, **Then** the number stays
   centred on the row and the row's box is unchanged from what the narrower label column allows.
2. **Given** a label that needs three lines, **When** the column is added, **Then** it still ends in `…`
   on the third line and nothing is painted past the pane's right edge.
3. **Given** a deleted target, **When** its row is drawn, **Then** it still carries its kind mark.
4. **Given** `prefers-reduced-motion`, **When** the row is drawn, **Then** nothing is animated.

### Edge Cases

- **When** the row is a section break, **Then** it keeps its rule and gains no mark: it paints no visible
  order number today, so the column has no seat on that row. *(Skipped question, recommendation recorded
  and adopted — see Clarifications.)*
- **When** the row is a legacy `TataIbadahItem`, **Then** it is marked as text; it carries no `kind`
  field, so the mark is chosen from the row's own shape, not from a new database value.
- **When** a slot's `fill_kind` cannot be read, **Then** its row carries the slot mark without a kind
  modifier, never a broken or empty glyph — the same degradation spec 213 chose for its badge.
- **When** a media target is missing, **Then** the row still carries its media mark; the mark states the
  kind, not availability.
- **When** the drawer/phone widths apply (below 1272px / 720px), **Then** the column keeps the same
  order and size as at the full pane.
- **When** the list is rebuilt in place after a save or delete, **Then** every new row carries its mark
  without a reload — the mark is server-rendered markup, not script injected after paint.
- **When** the dock's entry list is drawn, **Then** it carries no marks: only `#chList` is in scope.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Every numbered row in `#chList` SHALL paint a kind mark in a dedicated column immediately after its order number and before its label. | `new: reading` |
| FR-002 | The mark SHALL differ per kind: passage, song, media, text and section break, with a legacy row marked as text; a fill-in or choice SHALL carry the slot mark **with its corner kind modifier** from spec 213, so the frame and `+`/`◎` stay and the badge names the resolved kind. | `new: reading` |
| FR-003 | The mark SHALL be present in the first response and after any in-place rebuild, from the row's own kind, with no new model field or migration. | `new: reading` |
| FR-004 | The mark SHALL be `aria-hidden`, take no pointer and add no focusable element; every row's accessible name SHALL be byte-identical. | `new: reading` |
| FR-005 | The number SHALL keep its left edge (10px) and vertical centring in a 24px box that grows only past three digits; the label SHALL keep its three-line clamp, its `…` and its wrap at the pane's edge. | `new: reading` |
| FR-006 | A row whose target is deleted, and a legacy row, SHALL still paint their kind mark. | `new: reading` |
| FR-007 | The marks SHALL be legible in both themes, on the hover fill and on the selected row tint, at the stage's meta-text contrast or better. | `new: reading` |
| FR-008 | The OBS dock's entry list SHALL NOT carry the marks; only the reading sidebar's contents list is in scope. | `new: reading` |

### Key Entities

- **Contents kind mark** — an inline, decorative glyph in a new `.songrow__mark` column, rendered by
  `reading/_toc.html` from a `mark` value added to each `toc` row in `reading/views.py::_tatib_stage`.
- **Mark set** — passage (open book), song (beamed note), media (framed play), text (three lines),
  fill-in and choice (the existing dashed slot marks **plus** the spec 213 corner badge naming the
  resolved kind), section break (the stage's diamond, only if the open question is answered yes).

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | Every numbered row is marked | on a service holding all kinds: one `.songrow__mark` per `.songrow`, with pairwise different `data-mark` values |
| SC-002 | The mark sits after the number | the mark's left edge is ≥ the number's right edge + 1px and its right edge is ≤ the label's left edge on every row |
| SC-003 | The number's seat does not move | every `.songrow__c` left edge (10px) and y-centre, and every row height, are unchanged from the no-column baseline; its box is 24px for 1–3 digits |
| SC-004 | The label still clamps at three lines | a long label still shows three line boxes ending `…`, and no row scrolls horizontally at 404px and 280px |
| SC-005 | Reachability is unchanged | the mark is `aria-hidden="true"`, holds no control, and every row's accessible name is byte-identical to the baseline |
| SC-006 | Both themes hold contrast | `--head-ink` on `--canvas` is **5.57:1** light and **6.59:1** dark, measured from the product's tokens |

## UI/UX

Measured on the static preview at `specs/214-sidebar-entry-kind-marks/preview/index.html`, assembled
from the product's own `tokens.css`, the live `.songrow` rules and a clone of `_toc.html`'s markup, in a
404px pane at 1440×900, 1×, both themes. The three columns are *today*, *A* and *B*; the number under
each is from `preview/probe.py`.

- **Layout / position**: **B adopted.** The number keeps its **10px** left edge but its box narrows from
  **54.39px** to **24px** (growing only past three digits); the mark is a **16 × 16px** column starting at
  **42px** from the row's edge and the label sits at **66px** — 8.39px left of today. Candidate A, whose
  number box stayed 54.39px and whose label moved right 26px, was seen and not taken.
- **Size / spacing**: the mark's box is **16px** in a row whose gap becomes **8px**; the slot's corner
  modifier is **11px** and overhangs the mark by 3px right / 2px bottom. The divider row takes no mark.
  No column is narrower than 16px at any pane width.
- **Colour / typography**: the glyph is `--head-ink` — **#646357** on light `--canvas` **#F7F5F1**
  (**5.57:1**), **#9C9A91** on dark `--canvas` **#14130F** (**6.59:1**). It inherits the row's ink on the
  selected tint, the way `.songrow__verses` already does. Stroke is the product's 24-viewBox, 1.8 stroke,
  round-cap language; the slot's two marks keep their own 20-viewBox. A slot's corner modifier is an
  **11px** disc with an **8px** glyph on the 12-unit grid, scaled from spec 213's 13px/10px badge to this
  16px mark; the disc paints the row's own face so it never reads as a hole on the hover fill. Adding the
  badges changes no row's height — the list stays **354.25px** in both themes.
- **States**: at rest · hovered · selected (`aria-current`) · drag ghost · deleted target · both themes.
  The mark is decorative and takes no pointer or focus in any state.
- **Motion**: none.
- **Responsive**: the column is fixed-width, so it does not change with the drawer or phone widths; at
  the 280px pane the label loses the same 26px (A) and keeps wrapping inside the pane (spec 137).
- **The cost, stated plainly**: under A the label column narrows by **26px** (74.39 → 100.39px from the
  row edge), so a title sitting on a wrap boundary may gain one line; in the preview's six rows the line
  counts and the list height are unchanged (**354.25px**), and the live page's wrapping is measured
  during Converge. Under B the number's own gutter is rebuilt from 54.39px to 24px, which changes the
  geometry spec 063 fixed.

## Assumptions

- **The surface is `#chList` only.** The request says "service entry sidebar" — the contents column,
  not the first-level service list, the stage, the projector's entry list or the OBS dock (FR-008).
- **Every kind is marked.** "The corresponding icon/mark of the entries" is read as one mark per entry,
  including text and the two slot kinds; the glyphs already exist in the product for all but a section
  break, whose diamond the stage already draws.
- **No new data.** The kind is already resolved for every `toc` row in `_tatib_stage`; the mark is a new
  key on that row and a new class in the template, not a model field or a migration (FR-003).
- **Server-rendered.** The mark is present in the first response and survives the in-place rebuild the
  way the row's number and label do.
- **The divider row keeps its rule** whatever else it gains; the mark is additive and never replaces
  the existing separator.
- **This reverses spec 144 FR-008 for `#chList` only.** The dock keeps its own anatomy and the
  `.entry__kind-icon` test stays green because the new mark uses its own class.

## Clarifications

### Session 2026-11-21

- Q: Which layout — A (number box unchanged, label right 26px) or B (compact 24px number box, label 8px
  left of today)? → A: **B** (owner, 2026-11-21), after seeing both at 1× in both themes and asking how
  many digits fit the 24px box. The three-digit limit is recorded under FR-005 and UI/UX.
- Q: Should a fill-in or choice carry the bare slot mark or the spec 213 kind modifier? → A: **the
  modifier** (owner, 2026-11-21): the dashed frame and `+`/`◎` stay and the corner badge names the
  resolved kind. Recorded in FR-002 and the mark set.
- Q: Does the section-break divider row carry a mark, even though it paints no visible order number? →
  **not asked; skipped with the recommendation recorded**: no mark for this slice. Its rule is already
  the break's mark and adding one changes the divider row's height and a geometry other specs fixed. The
  owner chose B from a preview whose break row carried no mark. Reopening it is a revision at Specify,
  not a defect.

**Zero `[NEEDS CLARIFICATION]` markers remain.**
