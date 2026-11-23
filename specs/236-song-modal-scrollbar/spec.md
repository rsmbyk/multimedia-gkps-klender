# Feature Specification: the song entry modal has no scrollbar of its own

**Slice**: `specs/236-song-modal-scrollbar`
**Branch**: `fix/236-song-modal-scrollbar`
**Created**: 2026-11-24
**Status**: Draft — Gate 1 pending
**Input**: "the new/edit song entry modal should not have that scroll bar"
**Demand**: `ITEM-251` (new card)
**Capability**: `new: reading/R58`
**Preview**: `specs/236-song-modal-scrollbar/preview/index.html` (static preview at this path)

The shared editor is one native `<dialog class="editor">`. Its stylesheet gives it
`max-height: min(86vh, 46rem)` and puts scrolling in the child `.editor__content`
(`overflow-y: auto; min-height: 0`). The dialog itself keeps the browser's default
`overflow: auto`, so any descendant that paints past the dialog's padding box makes
the *dialog* a second scroll container and draws a scrollbar on its right edge.

The song-entry form collapses its Verses section with
`.editor__verse-panel[hidden] { display: grid; grid-template-rows: 0fr }`. The
collapse is deliberate — it animates — but the panel's children still have boxes,
and its absolutely positioned live-region line ends 10px below the dialog's content
box. On `New song` (no song chosen) and on `Edit song` for a song with no verses, the
dialog therefore scrolls 10px and shows the scrollbar the operator reported.

Live measurement from the slice's base commit `be9863d2` (127.0.0.1:8770, 1366×900,
dark theme, `#editorModal` after clicking **+ Song** on a Tata Ibadah):

| Element | clientHeight | scrollHeight | `offsetWidth - clientWidth` | `overflow-y` |
| --- | --- | --- | --- | --- |
| `.editor` — New song, base | 246px | 256px | 5px | `auto` |
| `.editor__content` — same state | 246px | 246px | 0px | `auto` |
| `.editor` — Edit song with verses, base | 410px | 410px | 0px | `auto` |

The target state is a dialog whose own edge never scrolls; overflow is clipped at its
14px rounded corner, while the content wrapper keeps its own scrolling for forms that
are genuinely taller than the cap.

## User Scenarios & Testing

### US1 — New song has no scrollbar (P1)

**Why this priority**: this is the reported surface. The scrollbar sits on the modal's
rounded right edge and reads as a defect even though all fields are already visible.
**Independent Test**: open **+ Song** on a service; the dialog has no scrollbar gutter
and cannot be scrolled by wheel or thumb drag.

**Acceptance scenarios**

1. **Given** a service with edit permission **When** the operator opens **New song**
   **Then** the dialog's `offsetWidth - clientWidth` is `0px`, its computed
   `overflow-y` is `clip`, and no scrollbar is painted on its right edge.
2. **Given** that open dialog **When** the operator wheels over it or drags at its edge
   **Then** the dialog does not scroll and the form stays in place.
3. **Given** that open dialog **When** the Song field is focused and typed into
   **Then** the results menu still opens past the dialog's bottom edge, inside the
   window, without resizing the dialog (`reading/R48` survives).

### US2 — Edit song has no scrollbar in the collapsed state (P1)

**Why this priority**: the same shared shell and the same collapsed verse panel occur
when editing a song that has no verses; fixing only the new form would leave the
reported fault in place under a different name.
**Independent Test**: open the edit modal for a song whose verse panel is collapsed;
assert the same zero-gutter, non-scrollable dialog.

**Acceptance scenarios**

1. **Given** a song entry whose Verses section is collapsed **When** the operator
   opens its edit modal **Then** the dialog has no scrollbar gutter and stays put under
   a wheel gesture.
2. **Given** a song entry with verses whose panel is settled **When** its edit modal
   opens **Then** the dialog box is unchanged at 410px tall and still has no scrollbar.

### US3 — Other editor forms are unaffected (P2)

**Why this priority**: the declaration lives on the shared `.editor` rule. The fix
must not remove the scrolling that taller forms depend on, or clip their controls.
**Independent Test**: open a large editor (a verse or a text entry) and a tall form at
a short viewport; the content wrapper scrolls, while the dialog edge stays clean.

**Acceptance scenarios**

1. **Given** a `data-editor-size="large"` form **When** it opens **Then**
   `.editor__content` remains its scroll container and all fields stay reachable.
2. **Given** a short window that caps the dialog **When** the form overflows **Then**
   the overflow scrolls inside `.editor__content`, not on the dialog's own edge.
3. **Given** any modal's date picker or other popover **When** it opens **Then** it is
   still painted outside the dialog; only the dialog's own overflow is clipped.

### Edge Cases

- **When** the verse panel is animating between collapsed and settled **Then** no
  scrollbar flashes on the dialog edge.
- **When** the window is 390px wide or the theme is light **Then** the same rule holds;
  no scrollbar appears on either dialog edge.
- **When** overflow remains in the collapsed panel's clipped content **Then** it is
  clipped, not made scrollable — `scrollHeight` may still exceed `clientHeight`, and
  the observable is the missing scrollbar gutter and the computed `overflow`.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | The shared `.editor` dialog SHALL NOT be a scroll container; its own edge SHALL carry no scrollbar in any song-entry state. | `new: reading/R58` |
| FR-002 | Overflow at the dialog's edge SHALL be clipped, not exposed as a scrollport. | `new: reading/R58` |
| FR-003 | Scrolling for forms taller than the cap SHALL remain on `.editor__content`. | `new: reading/R58` |
| FR-004 | The dialog's box (480px default width, 14px corner radius), the collapsed verse panel's animation, and fixed-position pickers/popovers SHALL be unchanged. | `new: reading/R58` |

### Key Entities

- **`.editor`** — the shared `<dialog>` in `static/styles/design/components.css`; one
  CSS declaration owns its overflow.
- **`.editor__content`** — the inner scrollport; already `overflow-y: auto; min-height: 0`.
- **`.editor__verse-panel[hidden]`** — the animated collapsed section whose clipped
  descendants create the base state's 10px overflow.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | New song shows no dialog scrollbar | browser readout: gutter `0px`, `overflow-y: clip`, no wheel movement |
| SC-002 | Edit song shows no dialog scrollbar in collapsed and settled states | same readout on both song entry variants |
| SC-003 | Tall forms still scroll inside the content wrapper | `.editor__content` scrollTop changes under wheel; dialog scrollTop stays `0` |
| SC-004 | Nothing else moves | dialog box, panel animation and picker escape match the base numbers in the preview |

## UI/UX

Measured in the static preview built from the real rendered dialog markup and the
slice's own CSS, 1366×900, dark theme; the preview's before numbers match the live
page above exactly.

| State | Dialog width | Dialog client / scroll height | Scrollbar gutter | `overflow-y` |
| --- | --- | --- | --- | --- |
| New song — before | 480px | 246 / 256px (10px overflow) | 5px | `auto` |
| New song — after | 480px | 246 / 256px (clipped) | 0px | `clip` |
| Edit song with verses — before | 480px | 410 / 410px | 0px | `auto` |
| Edit song with verses — after | 480px | 410 / 410px | 0px | `clip` |

The corner radius stays 14px; clipping at the edge replaces the scrollbar rather than
moving it into the content wrapper. Toggle **Switch to light** in the preview for the
light state; narrow/tall states are reached by resizing the preview window so the
dialog's `86vh` cap engages.

## Assumptions

- The fix is one declaration on `.editor`; no template, script or endpoint changes.
- The collapsed verse panel keeps its `grid-template-rows: 0fr` animation — its
  overflow is clipped by the dialog, not removed by hiding the panel outright.
- Spec 235 (empty-song verse summary) is merged on develop; it changes what the panel shows,
  not which element scrolls. The new/edit scrollbar rule applies to both panel states.
- `bump: patch` is expected for a user-visible fix; the level is declared at Plan and
  reviewed at gate 2, not fixed here.
- The card is new (`ITEM-251`); the owner promotes it to `Ready` after gate 1.
