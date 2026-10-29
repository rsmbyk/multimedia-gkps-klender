# Tasks: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md`
**Plan**: `specs/154-audio-times-inline/plan.md`
**Verification split**: 8 test · 5 inspection · 5 manual
**Order actually used**: T001 → T002 → T003 (red) → T004 → T005 (green) → T006 → T007. One thread, no
`[P]` pair ran concurrently: T002 and T003 touch the same file and T004 is T003's dependency.

## Phase 1 — Setup

- [X] T001 Measure the line before touching anything: compose `web` at `/tatib/144/`, entry `e1`,
  1440×900 — elapsed x 500→523.8, total x 980.2→1004, 456.4px apart, `justify-content: space-between`,
  accessible text `0:000:10`. No setup task exists: no dependency, no ignore-file change, no route.

## Phase 2 — Foundational

- [X] T002 [US1] Write `test_preview_times_read_current_over_total_beside_the_bar` and its helper
  `_assert_times_are_one_right_aligned_pair` in `tests/e2e/test_audio_display.py`: the text shape, one
  line, 5px either side of the separator, order, the pair's right edge on the bar's, the played time in
  the bar's right half, re-measured after `Space` and a seek.
- [X] T003 Run T002 against the **unmodified** product and record the red: `unexpected value "0:000:10"`
  — the line has no separator to see, before any geometry is reached.

## Phase 3 — US1 (P1) 🎯 MVP

- [X] T004 `multimedia/web/templates/reading/tatib.html:56` — add
  `<span class="audio-player__separator">/</span>` between the two time spans, leaving both
  `data-audio-*` attributes in place and in order.
- [X] T005 `static/styles/design/components.css:2134` — `.audio-player__times`:
  `justify-content: space-between` → `flex-end`, plus `align-items: baseline` and `gap: 5px`. Nothing
  else in the rule changes.
- [X] T006 Run T002 green, and the module with it: 6 cases, the new one passing, the only red the known
  `test_untitled_preview_and_projector_idle_display_off` (identical on unmodified `develop` — ITEM-140).
- [X] T007 Live preview at `http://localhost:8814/tatib/144/` — measure the pair in idle, playing, ended,
  dark and at 420×820; record the numbers in spec §UI/UX (SC-001, SC-002, E1, E4, E5).

## Phase 4 — US2 (P2)

- [X] T008 Check the projector's line is untouched and reads the same shape: `projector.html:47` and
  `projector.css:94` are absent from the diff; both lines read `played / total` (US2-S1, US2-S2, E2).

## Phase 5 — Polish

- [X] T009 Board and pack: card ITEM-163 in `backlog/items/`, its row in `backlog/board.md` under
  Speccing, slice row in `specs/README.md`, this pack, `analysis.md`, `converge.md`, `fold.md`.
- [X] T010 Delivery content, written before the push so the branch carries it: `VERSION` 1.22.10 →
  1.22.11 and one `### Fixed` line under `[Unreleased]` in `CHANGELOG.md`; the card moves to `in review`
  and its board row to the In review column.
- [X] T011 Held for the merge amend: the Done row with its PR link, and the card's `closed_at`,
  `closed_reason` and `bump: patch` — done in the pre-merge commit, 2026-10-29.
