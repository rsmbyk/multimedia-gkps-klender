# Convergence: The audio projector screen shows its play/pause control

**Spec**: `specs/156-audio-play-indicator/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-10-29

Checked every row of `plan.md`'s traceability table by the method it declared, against the code in the
worktree and the runs recorded below.

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| SC-004 says "the seek bar, the times, the player box … keep their geometry", while the accepted `## UI/UX` says the cluster drops 24px because the 48px control joins the centred column: the player box is 117.91px tall where it was 69.91px | `contradicts` | SC-004 | measured: player 500 × **117.91** at y 525.05 (was 500 × 69.91 at y 549.05), seek 500 × **6** at y **603.05** (was 579.05), times 87 × **21.91** at y **621.05** (was 597.05). Root cause is the criterion's wording, not the code: FR-001 and the accepted UI/UX numbers both require the 24px shift. **Accepted**: SC-004 is read as the bar's and the times' own boxes and the player's width — all unchanged — and the 24px is the movement the owner approved at gate 1. The wording stays as accepted; recorded here rather than rewritten (BRD-09) |

**Outcome**: 1 finding, accepted as recorded above; nothing appended as a task.

### Per-row verification

| Row | Method | Evidence |
| --- | --- | --- |
| FR-001, FR-002, SC-002, US2/AC1–AC3 | `test` | `test_projector_audio_control_is_painted_and_toggles` — green: box 48 × 48 (floor 44), `::before` `border-left` `12px` paused → `0px` with a 14 × 18 block playing, `aria-label` `Play audio` → `Pause audio` → `Play audio` |
| FR-003, SC-001, US1/AC1–AC4 | `test` | `test_projector_audio_control_hides_as_the_chrome_settles_and_returns` — green: `.is-idle` after 3.7s, control opacity 0 and `pointer-events: none` (polled through the 260ms fade), box still 48px tall, seek `.52`; a `pointermove` clears the class, the control returns to opacity 1 with the bars |
| FR-004 | `test` | both cases drive real pointer clicks; `Space` keeps its path in the existing `test_projector_space_navigation_and_reset` — green |
| FR-005 | `test` | the clicks above only land with both halves: the box's `z-index: 3` + `pointer-events: none` (D002) and the guard's early return (D003). Before either, the same click produced `pointerdown`/`pointerup` and no event the control could hear |
| FR-006, SC-004 | `inspection` | `git diff --stat`: `projector.css` +17/−1, `projector.js` +5/−1, `test_audio_display.py` +42, board, card, index — no other stylesheet, template or screen |
| SC-003 | `test` | `data-playing` `false` → `true` → `false` under the two clicks |
| Edge — missing file | `test` | the module's `test_missing_audio_states` still green: the player stays hidden, the missing mark shows |
| Edge — ended | `inspection` | `media-audio.js:update()` runs on `ended`, so `data-playing` returns to `false` and the mark to the triangle; the control's visibility is the chrome's, unchanged by the end of playback |
| Edge — reduced motion | `inspection` | `projector.css:110`: `@media (prefers-reduced-motion: reduce) { .screen__audio-play, .screen__audio-seek, .screen__audio-times { transition: none } }` — the control is in the list |
| Edge — 1280 / 640 | `inspection` | `preview/measure.py`: control 48 × 48 in both; bar 500px at 1280, 384px at 640; every other number identical to 1920 |

### Where the implementation went beyond the plan

- The plan did not name a transition for the control's fade; the hide/show needs `opacity 260ms ease` in
  the transition list, matching the bar and the times. Added, and the spec's UI/UX already lists the
  motion.
- The plan's test note did not anticipate the fade: the first run asserted `opacity` once and caught the
  260ms tween mid-flight (`0.0059506`). The assertions now poll (`to_have_css`), which is the honest fix —
  the behaviour was right, the measurement was early. Recorded because it is the kind of flake that looks
  like a product bug later.

### Run

- `manage.py test tests.e2e.test_audio_display` (7 tests, database `gkps156`): the two new cases green;
  the module's one red is `test_untitled_preview_and_projector_idle_display_off`, which fails identically
  on unmodified `develop` under the same command and browser — board card ITEM-140, so this slice needs
  no card of its own.
- Red-first proof: with `projector.css` and `projector.js` reverted to the base commit and the tests kept,
  both cases fail — `expect … to_be_visible` reads `hidden` (0×0) and `border-left` reads `0px` where
  `12px` is asserted.
- `preview/measure.py` re-run after the final rules: the four states at three viewports, as tabulated in
  the gap row.

## Pass 2

Not needed — pass 1 left no actionable gap.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| SC-004's wording ("the player box keeps its geometry") disagrees with the approved 24px shift; read as the bar/times boxes and the player's width | `contradicts` | LOW | 2026-10-29 (agent, recorded; the owner approved the 24px at gate 1) |

## Cap reached

Not reached — one pass, nothing actionable.
