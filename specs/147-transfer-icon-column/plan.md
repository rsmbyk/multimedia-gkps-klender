# Implementation Plan: a long transfer name ellipsizes instead of moving the row

**Spec**: `specs/147-transfer-icon-column/spec.md`
**Branch**: `feat/147-transfer-icon-column`
**Bump**: `patch`
**Preview**: `specs/147-transfer-icon-column/preview/preview.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 · Django 4.0 templates · browser CSS (`static/styles/design/components.css`) |
| Primary dependencies | none added — the existing stylesheet layer, the existing design tokens |
| Storage | none; the rows are drawn from the local companion's `/transfers` response on every poll |
| Testing | Playwright (Python) E2E via `StaticLiveServerTestCase`; `tests/e2e/test_media_library.py`, module already owns this surface |
| Target platform | every browser the app supports; the rule is plain flexbox, no feature query |
| Project type | server-rendered Django web app, no build step |
| Performance goals | none — a static declaration; no request, no reflow beyond the one already happening |
| Constraints | the dialog's 580px width and 22px padding are untouched; the row keeps `padding: 13px 4px`, `gap: 12px` and its 1px divider; no template, JS or API change |
| Scale / scope | 1 declaration in `components.css`, 3 E2E tests, 1 preview pack, 1 board card |

## Constitution Check

No `CONSTITUTION.md` exists, and SDD-01 makes it optional and never auto-created, so the check is not
applicable. The repo's own rules apply as constraints above: one declaration, no new token, no new
dependency, no template or JS change.

Re-checked after Phase 1: pass — nothing added that the constraint row does not already name.

## Phase 0 — Research

See `research.md`. Four candidate declarations were injected into the live page and measured; all
four reach the same pixels, and `flex: none` is chosen because it is the only one that states both
directions of "this is a column, not a flexible item". **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entity change; the row's three drawn fields and the invariants the fix has to
  hold.
- `contracts/` — `none` (`contracts/none.md`): no endpoint, payload, template variable, stored value
  or event.
- `quickstart.md` — the run commands, the hand checks, the E2E command, and how to regenerate the
  preview.

**The design in one declaration.** `components.css:2753` becomes

```css
.media-transfers__mark { width: 32px; flex: none; text-align: center; color: var(--focus); font-size: 22px; }
```

Nothing else changes. `width: 32px` stays as the base size, `flex: none` removes the item from the
flex shrink/grow negotiation, and the row's overflow lands entirely on `.media-transfers__main`,
which already declares `min-width: 0` and whose `strong` already declares `nowrap` +
`text-overflow: ellipsis`. The seven rows that already fit keep their exact shipped positions (glyph
702.5, text 741.0); the two long ones move onto them.

**Why no template or JS change.** `media-handoff.js:59` builds the mark as
`span.media-transfers__mark` and puts the glyph inside it; the 32px is authored in CSS and the 21px
glyph is authored in CSS. The defect is that the first of those was advisory. Fixing it in the
stylesheet keeps the renderer untouched — and the same renderer draws the rail's list, so both
surfaces are fixed by one declaration.

**What is deliberately not done.** No grid conversion (`research.md` candidate c), no `min-width`
variant (b), no `flex-shrink` variant (d), no change to `.service-media__row` (it is a grid with a
38px column and does not collapse), no wrapping of long names, no row cap, no companion change.

## Traceability

| Requirement / scenario | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 mark column is exactly 32px and cannot be narrowed | `static/styles/design/components.css:2753` | `test` → `tests/e2e/test_media_library.py::MediaLibraryE2ETests::test_every_transfer_row_shares_one_icon_column` | asserts the set of mark widths is exactly `{32.0}` |
| FR-002 a long name ellipsizes and changes neither the row's width nor its height | `components.css:2753` (the `strong`'s ellipsis already ships) | `test` → `…::test_a_long_transfer_name_ellipsizes_without_resizing_its_row` | `scrollWidth > clientWidth` and row height 72px |
| FR-003 every name and status label shares one left edge | `components.css:2752-2753` | `test` → `…::test_every_transfer_row_shares_one_icon_column` | spread of `strong` lefts and of the status `span` lefts is 0.0px |
| FR-004 the dialog keeps `min(580px, 100vw - 32px)`; the text column absorbs narrowing | `components.css:2751-2753` | `test` → `…::test_the_icon_column_holds_in_a_narrow_dialog` | 420px viewport → 382px rendered dialog, text column 284px, both spreads 0.0px, no row past the dialog's right edge |
| FR-005 nothing else about the list changes | `static/web/media-handoff.js` (untouched), `base.html:456` (untouched) | `inspection` — the rows drawn, their order, the 1px divider and the rail's own list are unchanged in the diff; `…::test_sidebar_transfer_session_shows_active_then_finished` still passes | the diff is one stylesheet line |
| US1 AC1 / AC2 | as FR-001, FR-003 | `test` → `…::test_every_transfer_row_shares_one_icon_column` | same run |
| US1 AC3 | as FR-002 | `test` → `…::test_a_long_transfer_name_ellipsizes_without_resizing_its_row` | same run |
| US2 AC1 / AC2 | as FR-004 | `test` → `…::test_the_icon_column_holds_in_a_narrow_dialog` | 420px viewport |
| Edge: every name fits / every name long | `components.css:2753` | `test` → the three tests above measure a mixed list; `inspection` — the preview's Now/Fixed panels also carry all-short rows | the column is not a function of the list |
| Edge: an active percentage label | `media-handoff.js:62` (status text), geometry by CSS | `inspection` — the preview's mark measurement counts the mark, not the label; the label's own width cannot move the mark once it is `flex: none` | no test: a running companion job is a boundary this suite already fakes, and the assertion would prove CSS |
| Edge: empty / disconnected list, the rail's list | `media-handoff.js:49-52` | `test` → `…::test_sidebar_transfer_session_shows_active_then_finished` (empty and completed states) plus `inspection` | unchanged by this slice |
| Edge: 200% zoom | `components.css:2753` | `inspection` — 32 CSS px at any zoom; no `px`→`rem` dependency added | stated in `UI/UX` |
| SC-001 glyph left spread 0.0px | `components.css:2753` | `test` → `…::test_every_transfer_row_shares_one_icon_column` | measured, not asserted from CSS text |
| SC-002 name/status left spread 0.0px | `components.css:2752-2753` | `test` → `…::test_every_transfer_row_shares_one_icon_column` | same run |
| SC-003 both long names truncate, row stays 72px | `components.css:2753` | `test` → `…::test_a_long_transfer_name_ellipsizes_without_resizing_its_row` | |
| SC-004 at 420px both spreads 0.0px and no row overflows | `components.css:2751-2753` | `test` → `…::test_the_icon_column_holds_in_a_narrow_dialog` | |
| UI/UX numbers — mark 32×33, glyph 21×21, text column 482px, dialog 580px, row 72px | `components.css:2751-2753`, `:2796` | `inspection` — `preview/README.md`'s readout table, regenerated by `build_preview.py` | the preview is the evidence |

**Verification split: 3 test · 5 inspection · 0 manual.**

## Plan exit gate

| Check | Result |
| --- | --- |
| Requirement coverage | FR-001…FR-005 all carry a row; every SC and every story scenario is mapped above |
| Entity coverage | one drawn entity (transfer row); its three fields named, none added |
| Interface coverage | `contracts/none.md` states `none` and why, in writing |
| Decision provenance | every technical choice traces to `research.md`'s measured table or to a spec assumption |
| Constitution conformance | no constitution exists (SDD-01); the constraint row is honoured |
| Zero unknowns | 0 |
| Verification declared | 3 `test` · 5 `inspection` · 0 `manual`, each naming a file and function or what to look at |
| `quickstart.md` runnable | yes — commands run as written; the only expected red is the three tests this slice writes |
