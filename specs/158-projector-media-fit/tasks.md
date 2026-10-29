# Tasks: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md`
**Plan**: `specs/158-projector-media-fit/plan.md`
**Verification split**: 19 test · 3 inspection · 0 manual

Two modules carry every `test` row — `tests/e2e/test_image_display.py` (`ImageDisplayE2ETests`) and
`tests/e2e/test_pdf_display.py` (`PDFDisplayE2ETests`). The 1440×900 window both modules open gives a
stage of **1376×804** (`.projector__screen` padding 32/32/64).

## Phase 1 — Setup

- [X] T001 `tests/e2e/test_image_display.py` — add the second and third media entries the fit cases need
      (a 24×6 landscape PNG and a 600×300 one) to `setUp`, each with its own `MediaIdentity`, and route
      their bytes in `_page()` beside the existing 12×6 stub. No production code.

## Phase 2 — Foundational

- [X] T002 `static/styles/design/projector.css` — `.screen.is-fitted .screen__image, … .screen__pdf-page
      { max-width: none; max-height: none; flex: none }`, `.screen.is-fitted .screen__image-box,
      … .screen__pdf-box { overflow: hidden }`, and `body.projector.media-overflow .mouse-zone
      { cursor: grab }` / `:active { cursor: grabbing }`. Nothing reaches it until T0xx adds the class.

## Phase 3 — US1 (P1) 🎯 MVP · a small image fills the stage

**Goal**: an image smaller than the stage paints at the smaller of the two ratios, whole and centred.
**Independent test**: `test_projector_enlarges_a_small_image_to_the_stage` at 1440×900 → 1376×688.

- [X] T003 [P] [US1] red — `test_projector_enlarges_a_small_image_to_the_stage`: open the projector on the
      media screen, assert the painted box is 1376×688 (±1) against the 12×6 PNG, then `set_viewport_size`
      to 1024×768 (stage 960×672) and assert 960×480 (±1) — the same rule at a second window (SC-001,
      SC-003, FR-006).
- [X] T004 [P] [US1] red — `test_a_landscape_image_fits_by_its_width`: the 24×6 PNG paints 1376×344
      (±1) — width-bound (SC-006, FR-001 AC3).
- [X] T005 [P] [US1] red — `test_a_large_image_still_shrinks`: the 600×300 PNG paints 1376×688 (±1)
      — the same rule below 1 (US1 AC2).
- [X] T006 [US1] green — `static/web/projector.js`: `fitMedia(host, natural, element)` and
      `applyPan(element)` (D001/D004 shapes in `plan.md`), `renderImageScreen` calling it after
      `GKPSMediaImage.load` resolves, `clearImageScreen` dropping `is-fitted`, the transform and
      `media-overflow`.
- [X] T007 [US1] green — the existing `resize` listener re-fits the showing image, keeping `fitState`.

## Phase 4 — US2 (P1) · a PDF page fills the stage the same way

**Goal**: a page paints at the same ratio, sharp at the display's pixel ratio.
**Independent test**: `test_projector_enlarges_a_pdf_page_to_the_stage` → 603×804 from a 300×400 page.

- [X] T008 [P] [US2] red — `test_projector_enlarges_a_pdf_page_to_the_stage`: the first page of the
      three-page PDF paints 603×804 (±1) (SC-002, FR-002).
- [X] T009 [US2] green — `static/web/media-pdf.js`: `paint(…, options)` with
      `{fit: 'contain'|'width'|'height', upscale}`; `scale = Math.min(1, scale)` only when `upscale` is
      false; the pixel-ratio expression untouched (contract `none.md`).
- [X] T010 [US2] green — `projector.js` `paintPDFScreen()` passes `{fit: fitState, upscale: true}`,
      records the returned size as the overflow, and re-applies the pan; `clearPDFScreen()` resets the
      class, the transform and `media-overflow`.

## Phase 5 — US3 (P1) · `T` switches the axis

**Goal**: `T` alternates fit width ↔ fit height, starts from the smaller fit, and never touches a passage.
**Independent test**: one `T` on the enlarged image → 1608×804, cut 116 each side; a second returns.

- [X] T011 [P] [US3] red — `test_projector_t_toggles_fit_width_and_height`: 1376×688 → 1608×804
      (cut 116/116) → back, with the painted box measured each time (SC-004, FR-003, FR-004).
- [X] T012 [P] [US3] red — `test_projector_t_toggles_the_page_fit_and_keeps_it_across_pages`: 603×804 →
      1376×1834 (cut 515/515), still that after `ArrowRight` to page 2, and back to the fit after
      `Control+ArrowRight` to the next entry (SC-005, FR-005).
- [X] T013 [US3] green — `projector.js`: `toggleFit()`, the `fitHost` reset inside `fitMedia`/`paintPDFScreen`,
      and the keydown branch `if (imageHost || pdfHost) toggleFit(); else flipTranslation();`.

## Phase 6 — US4 (P1) · the overflow is panned

**Goal**: dragging or the wheel moves the zoomed page inside its overflow, clamped, without eating clicks.
**Independent test**: drag the fit-width image past its end → `translate` stops at ±116.

- [X] T014 [P] [US4] red — `test_projector_pans_the_overflow_by_drag_and_wheel`: `mouse.down/move/up`
      moves `translate`; a drag past the end clamps at ±116; the wheel moves the same axis and clamps;
      the wheel does nothing on the default fit; the computed cursor is `grab` (SC-008, SC-009, FR-009,
      FR-010, FR-012).
- [X] T015 [P] [US4] red — `test_projector_press_without_drag_still_steps`: a 4 px press on the right
      third still steps the showing screen once and leaves `translate` empty (SC-010, FR-011).
- [X] T016 [US4] green — `projector.js`: the four pointer handlers on `.mouse-zones`
      (`pointerdown`/`pointermove`/`pointerup`/`pointercancel`), the 4 px `moved` threshold, and the
      one-shot `suppressClick` guard at the top of the existing click handler.
- [X] T017 [US4] green — the `wheel` listener (`{passive: false}`), active only while `media-overflow`
      is set (D006).

## Phase 7 — US5 (P2) · the sheet lists the key

**Goal**: `K` shows the new group, in the middle column, and the sheet keeps its height.
**Independent test**: the sheet contains a group whose heading is `Image and PDF` and whose row reads
`Fit Width / Fit Height` with `T`.

- [X] T018 [P] [US5] red — `test_shortcut_sheet_lists_the_fit_key`: open the projector, press `K`, assert
      the group heading, the row's label and its `T` keycap; assert the sheet's height is at most the
      window's (SC-007, FR-007).
- [X] T019 [US5] green — `multimedia/web/templates/reading/projector_controls.html`: the group after
      *Library Detour* in the middle column.

## Phase 8 — Polish

- [X] T020 Rebuild the preview against the shipped code (`python3 specs/158-projector-media-fit/preview/build_preview.py`)
      and check its numbers against the tests' by eye — `inspection`.
- [X] T021 Run both modules and `tests.e2e.test_projector` together; the passage `T`, the cue, the mouse
      zones and the detours must be unchanged — `inspection` of the run plus FR-008's test rows.

## Phase 9 — Convergence

<!-- written by Converge only; absent until it runs -->
