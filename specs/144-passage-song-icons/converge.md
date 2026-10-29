# Convergence: a passage and a song carry their own kind mark

**Spec**: `specs/144-passage-song-icons/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-10-28

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| The media chip's ink is `--focus` only while the local library answers; with the library unavailable both marks resolve to `--head-ink`, so "the marks differ in colour" is a property of one state, not of the page. | `partial` | FR-003, SC-002 | Measured: the first run of `test_the_mark_is_not_a_media_chip` read `rgb(100, 99, 87)` on both elements, because `media-stage.js` had put the chip in `is-unavailable`. The E2E now makes the library answer (a routed `/v1/files`) and asserts the chip's `--focus` ink there; the size (20 vs 42) and the fill (transparent vs tinted) differ in every state, which is what FR-003 asks for. |
| `analysis.md` counted 13 E2E functions; the plan names 11 (the other two matches were module names). | `partial` | Plan §Traceability, Analysis §Metrics | `grep -o 'test_[a-z0-9_]*' plan.md` returns 13 matches, two of them `test_stage_kind_marks` and `test_text_wrap`. Corrected below. |

Everything else checked by the method the plan declared:

| Requirement / scenario | Checked by | Result |
| --- | --- | --- |
| FR-001, US1.1, SC-001 | `test` — `test_a_passage_row_carries_the_passage_mark` | one mark, `data-kind-icon="scripture"`, `display: grid` |
| FR-002, US1.2 | `test` — `test_a_song_row_carries_the_song_mark` | two song marks; the path data differs from the passage's |
| FR-003, SC-002, US2.2 | `test` — `test_the_mark_is_not_a_media_chip` | 20 × 20 vs 42 × 42, transparent vs tinted, `--head-ink` vs `--focus` |
| FR-004, SC-001 | `test` — `test_a_text_row_carries_no_mark`, `test_only_passage_and_song_rows_are_marked` | 3 marks on the fixture page; the text row keeps `padding-left: 12px` |
| FR-005, SC-004, US3.1 | `test` — `test_a_passage_row_keeps_its_56px_box` | 56px box, heading's centre on the box's centre, `margin-top: 0` |
| FR-005, SC-003 | `test` — `test_no_other_block_moves` | with the mark hidden, every block's top differs by **0.0px** or by exactly **23.8px** (a declared song wrap) |
| FR-006, SC-005 | `test` — `test_the_mark_is_decorative` | `aria-hidden`, empty text, `pointer-events: none`, heading name `Matius 5:2-3` |
| FR-007, US3.3 | `test` — `test_the_mark_holds_contrast_in_both_themes` | ≥ 4.5:1 on the canvas and on the hover fill, both themes |
| FR-008 | `test` — `test_the_sidebar_and_dock_keep_their_own_rows` | 0 marks in `#chList` and 0 on `/obs/dock` |
| US3.2 | `test` — `test_the_declared_wraps_at_the_400px_pane` | pane 400px, four songs' titles 47.6px (two lines), passage 23.8px; at 1920 (pane 880px) every song is one line |
| US3.4 | `inspection` — the mark's rule block | no `transition`, nothing declared for `prefers-reduced-motion` to switch off |
| US1.3 | `manual` — `/tatib/144/` at 1440 | the open book and the note are told apart before their words are read |
| US2.1 | `manual` — same page | the 42px tinted chip still reads heavier than the 20px grey glyph |

**Suite**: `tests.e2e.test_stage_kind_marks` — **11/11 green in 46.2s** on the rebased tree
(`f85984a8`), `--keepdb`, database `gkps144`.

**Neighbours**: 184 tests across `test_tatib_entry_controls`, `test_tatib_hover`, `test_text_wrap`,
`test_media_library`, `test_song_label_typography`, `test_reading`, `test_entries` and
`test_design_tokens` — **178 green, 6 red**, and none of the six is this slice's:

| red | attribution |
| --- | --- |
| `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` | known red, card **ITEM-156** (`19.98px` against `12px`) |
| `test_the_panel_shows_its_empty_view_when_no_songbook_exists` | known red, card **ITEM-137** |
| `test_touch_controls_remain_visible_after_dismissal` | known red, card **ITEM-153** |
| `test_a_long_title_wraps_inside_the_pane`, `test_a_short_title_is_unchanged`, `test_the_add_controls_wait_for_a_hover` | reproduced on unmodified `origin/develop` (`f85984a8`) in a detached worktree — **3/3 failed the same way**; carded as **ITEM-159** |

**Renumbered while the slice ran** (three concurrent slices landed on `develop`):

| what | from | to | why |
| --- | --- | --- | --- |
| the card | `ITEM-155`, then `ITEM-156`, then `ITEM-158` | **`ITEM-160`** | slices 147 and 146 claimed 155, 156, 157 and finally 158 while this slice was in flight |
| the capability requirement | `R22` | **`R24`** | slice 146 folded `R22` (Media Library age buckets) and `R23` (transfer history) |
| the version | 1.22.5 | **1.22.8** | `develop` reached 1.22.7 through 145/147/146 |

**Also fixed in the pack**: `preview/build_preview.py` now injects a mark only where the template has
not drawn one, so the page can still be rebuilt after this slice ships (it would otherwise duplicate
every mark).

**Outcome**: converged — the one code-level finding (FR-003's colour clause) is closed by stating the
state it holds in and by the size-and-fill difference that holds in every state.
