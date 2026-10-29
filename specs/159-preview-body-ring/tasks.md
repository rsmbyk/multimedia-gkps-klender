# Tasks: a preview's play shortcut paints nothing on the dialog's edge

**Spec**: `specs/159-preview-body-ring/spec.md`
**Plan**: `specs/159-preview-body-ring/plan.md`
**Verification split**: 17 test · 5 inspection · 2 manual

## Phase 1 — Setup

- [X] T001 [P] Create `tests/e2e/test_preview_body_ring.py` with the fixture only, no cases: a
  `MediaIdentity` for audio and one for video, a MEDIA `ServiceEntry` for each on one service page, and
  `page.route('http://127.0.0.1:63174/v1/files/<sha>', …)` serving bytes with the CORS header — the
  shape of `tests/e2e/test_audio_display.py:33-90`. No dependency, ignore-file or route of the product
  changes.

## Phase 2 — Foundational: the red run before any product code

Written and run **before** `components.css` or `preview.js` is touched, so each case fails for its own
reason rather than for a typo (TDD-02).

- [X] T002 [P] [US1] Write the three cases that must fail today, in
  `tests/e2e/test_preview_body_ring.py`:
  `test_a_space_press_leaves_no_ring_on_the_audio_preview` (pointer open, space, click in the body,
  space again — `getComputedStyle(body).outlineStyle` must read `none` at each step and `data-playing`
  must toggle), `test_a_space_press_leaves_no_ring_on_the_video_preview`, and
  `test_a_keyboard_opened_preview_wears_the_ring_until_the_first_space` (focus the opener, `Enter`, the
  outline is `2px solid rgb(28, 92, 60)` at `-2px`; one space → `none`).
- [X] T003 [P] [US2] Write the two cases that guard the indicator — `test_tab_brings_the_ring_back_after_a_space_press`
  and `test_the_next_preview_gets_its_ring_back`. They pre-assert the suppressed state, so they are red
  before the fix like the rest; what they add is the return path, which the T002 cases do not cover.
- [X] T004 Run T002 and T003 against the unmodified page and record the output in `analysis.md`: all
  five red on `outlineStyle === '2px'` where `none` is asserted. T003's two do not stay green — the
  plan's F2 guess was wrong, and the record says so.

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: a key that operates the player leaves no indicator on the body, and the ring the dialog drew
on a keyboard open goes with it.
**Independent test**: the three T002 cases go green and the two T003 guards stay green.

- [X] T005 [US1] `static/styles/design/components.css` — add
  `.preview__body.is-shortcut:focus-visible { outline: none; }` directly beneath the body's existing rule
  at `:2093`.
- [X] T006 [US1] `static/web/preview.js` — add `markShortcut(on)` (a `classList.toggle` on `content`) and
  call `markShortcut(true)` in the audio branch (`:579-585`) and the video branch (`:586-592`) as the
  player toggles. The three T002 cases go green; **both T003 guards go red here**, which is the trap
  D002 predicted.
- [X] T007 [US1] `static/web/preview.js` — clear the class when a preview opens (`:496-517`) and in the
  close handler (`:616`); `test_the_next_preview_gets_its_ring_back` returns to green.

## Phase 4 — US2 (P2)

**Goal**: the indicator is never lost to a keyboard reader.
**Independent test**: `test_tab_brings_the_ring_back_after_a_space_press` is green, and the spec-071
arrow cases in `tests/e2e/test_entry_preview.py` are unchanged and green.

- [X] T008 [US2] `static/web/preview.js` — in the modal's keydown listener (`:571`), clear the class on
  `Tab`. `test_tab_brings_the_ring_back_after_a_space_press` returns to green.
- [X] T009 [US2] Re-run `tests/e2e/test_entry_preview.py` — `test_clicking_long_preview_text_allows_arrow_key_scrolling`
  and `test_short_preview_arrow_keys_do_not_scroll_the_page` (FR-003) must be green with no change to
  `preview.js:476-484`.

## Phase 5 — Polish

- [X] T010 [P] Re-run `tests/e2e/test_audio_display.py`, `tests/e2e/test_image_display.py` and
  `tests/e2e/test_pdf_display.py` — the player, the image preview and the PDF preview are untouched and
  stay green (FR-004).
- [X] T011 `inspection` — read the whole diff: one CSS declaration, one helper and four call sites. No
  template, no `tabindex`, no `media-audio.js` / `media-video.js`, no geometry token, no copy.
- [X] T012 `specs/README.md` — the index row for 159, `Accepted`. Done at gate 1, when the spec was
  accepted, rather than here.
- [X] T013 Fold: add R31 to `docs/spec/reading.md` and move the header's `last folded` and `slices`.
- [X] T014 `VERSION` `1.22.10` → `1.22.11` and one `### Fixed` line under `## [Unreleased]` in
  `CHANGELOG.md`, in the pre-merge commit.
- [ ] T015 Delivery, after the report: open the PR as a draft, then read `ITEM-171`'s state — it is in
  `Ready`, so set `in-review`, write `pr:` and move the board row, and push that one commit
  (`C-BOARD-GIT`).

## Phase 6 — Convergence

- [ ] T016 [Convergence, post-merge] `manual` — `collectstatic` inside the `web` container, restart it,
  open an audio preview, press space twice: the dialog's edge stays clean. One Tab paints
  `2px solid rgb(28, 92, 60)`. Screenshot at 1512 × 900 against 1.22.10 (SC-001, SC-004).
