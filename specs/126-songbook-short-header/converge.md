# Convergence: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md` · **Plan**: `specs/126-songbook-short-header/plan.md`
**Pass**: 1 · **Outcome**: **Converged**

## What was checked

Every requirement and acceptance scenario was checked by the method `plan.md` declared for it. Scope came
from the plan's traceability table: `multimedia/web/reading/views.py`, `static/web/offline-render.js`,
`multimedia/web/tests.py`, `tests/e2e/test_saved_render_parity.py`.

| Intent | Evidence | Result |
| --- | --- | --- |
| FR-001 · US1/AC1 · SC-001 | `test` → `multimedia.web.tests.ReadingViewTests::test_song_detail_header_cites_the_short_songbook_reference` — green; **red before the change**: `'Nyanyikanlah Kidung Baru 12' != 'NKB 12'` | holds |
| FR-001 (sub-number) · US1/AC2 | `test` → `::test_a_sub_number_follows_the_short_reference` — green; red before: `'Nyanyikanlah Kidung Baru 12B' != 'NKB 12B'` | holds |
| US1/AC4 · SC-002 | `test` → `::test_an_unnumbered_hymn_song_shows_the_reference_alone` — green; red before: `'Nyanyikanlah Kidung Baru' != 'NKB'` | holds |
| FR-002 · US1/AC3 · SC-002 | `test` → `::test_song_detail_header_falls_back_to_the_full_songbook_name` — green (guard; red if the fallback is dropped) | holds |
| FR-005 | `test` → `::test_song_detail_tab_title_uses_the_short_reference` — green; red before: `'Nyanyikanlah Kidung Baru 12 — GKPS Klender' != 'NKB 12 — GKPS Klender'` | holds |
| FR-003 · US2/AC1 · SC-003 | `test` → `::test_an_ordinary_songbook_header_keeps_its_full_name` — green | holds |
| FR-006 | `test` → `::test_an_ordinary_songbook_with_a_short_name_still_shows_its_full_name` — green (`Kidung Harian Baru`, short name `KH`) | holds |
| FR-004 · US3/AC1 · SC-004 | `test` → `tests.e2e.test_saved_render_parity.SavedRenderParityTests::test_header_and_title_agree_between_saved_and_server` — green; red before the renderer change: saved `'Hymn Test 7'` vs expected `'HT 7'` | holds |
| US3/AC1 (per-route table) | `test` → `::test_saved_documents_use_route_specific_labels_and_markup` with the new hymn `eyebrow` case — green; red before the renderer change | holds |
| US3/AC2 | `test` → the same table's existing ordinary `eyebrow` case (`Ordinary Test`) — still green, unchanged | holds |
| FR-007 · US2/AC2 · SC-005 | `test` → `multimedia.web` + `tests.e2e.test_saved_render_parity` + `tests.e2e.test_offline_library` re-run; `inspection` → on `/songs/1013/` the sidebar heading still reads `Song list — Pelengkap Kidung Jemaat`, its rows `PKJ 1`…`PKJ 4`, the songbook panel lists full names, the filter reads `Filter songs…`, and the stage title and body are unchanged | holds |

## Test evidence

| Command | Result |
| --- | --- |
| `manage.py test multimedia.web.tests.ReadingViewTests --keepdb` (before the change) | **41 tests, 4 failures** — the four red-first pins, each with the full name it used to print |
| `manage.py test multimedia.web.tests.ReadingViewTests --keepdb` (after) | 41 tests, **OK** |
| `manage.py test tests.e2e.test_saved_render_parity` (renderer reverted) | 2 tests, **2 failures** — `'Hymn Test 7' != 'HT 7'` on both new pins |
| `manage.py test tests.e2e.test_saved_render_parity` (after) | 6 tests, **OK** |
| `manage.py test multimedia.web tests.e2e.test_offline_library tests.e2e.test_saved_render_parity --keepdb` | 331 tests, **1 error** — `OfflineLibraryE2ETests::test_saved_content_and_projector_survive_disconnection` (`ERR_INTERNET_DISCONNECTED` navigating to `/projector`). Reproduced identically on the untouched `develop` checkout in `~/Projects/multimedia-gkps-klender`, so it is pre-existing and environmental, not this slice |

## Findings

| ID | Type | Severity | Source-ref | Description | Disposition |
| --- | --- | --- | --- | --- | --- |
| C1 | `unrequested` (support) | LOW | plan §Traceability | `multimedia/web/tests.py` gains `import re` and a `_eyebrow()` helper so the pins read the header paragraph rather than the whole page | awareness only — test support, not behaviour |
| C2 | `unrequested` (environment) | LOW | quickstart | `collectstatic` was run in this worktree to give the page-rendering classes the static manifest they read; the output (`_static/`) is gitignored and not part of the slice | awareness only |
| C3 | `contradicts` (test pin) | MEDIUM | spec 123 · `tests/e2e/test_reading.py::ReadingE2ETests::test_tatib_date_header_matches_songbook_header` | Spec 123's style-parity pin also asserted the song header's *text* as `Nyanyikanlah Kidung Baru 12` to prove it was measuring the right element. After this slice the header reads `NKB 12`, so the run of `tests.e2e.test_reading` failed with `'NKB 12' != 'Nyanyikanlah Kidung Baru 12'`. | The style comparison is untouched; the reference text moved to `NKB 12` with a comment saying it pins the element, not the citation's wording, and the `EYEBROW_STYLE_KEYS` comparison plus the frozen 16.5px/600/`rgb(31, 31, 29)`/0.78 values stand. | Converge would report the reading shell's style pin as still asserting the pre-slice text. | **fixed 2026-10-24** (pass 2) |

No `missing` or `partial` findings. Nothing was deleted, and no behaviour outside the plan's scope was observed.

## Pass 2 — 2026-10-24

The full `tests.e2e.test_reading` class (78 tests) was run after pass 1's scope: 77 green, 1 failure — C3.
The pin was updated and both spec-123 tests re-run green (`test_tatib_date_header_matches_songbook_header`,
`test_tatib_date_header_reflows_at_a_narrow_stage`). A re-run of the whole class then flaked one unrelated
test — `test_bible_edition_preference_returns_after_unavailable_chapter`, a 5 s visibility wait on a Bible
page's Simalungun text — which passes alone in 4.1 s and touches no code this slice changes. No task was
appended: the fix is a test's reference value, not a behaviour the artifacts did not already require.

**Outcome: Converged** (2 passes, no accepted gaps).

## History

- 2026-10-24 · pass 1 · converged · 2 findings (both `unrequested`, LOW) · no tasks appended
- 2026-10-24 · pass 2 · converged · 1 finding (C3, `contradicts`, MEDIUM) fixed · `tests.e2e.test_reading` 78 → 1 failure → green after the fix
