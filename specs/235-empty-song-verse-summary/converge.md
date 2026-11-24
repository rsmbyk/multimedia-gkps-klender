# Convergence: An empty song names itself in the Verses section

## Phase 1: Convergence

Each row is checked by the method its traceability entry declared, against the code at the
end of Implement. No row is typed `partial` or `contradicts`.

| Requirement | Method | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001 / US1-AC1 | `test` | `tests.e2e.test_entries.EntryModalE2ETests::test_an_empty_song_shows_only_the_verse_summary` — label visible, panel visible, only `This song has no verses` — **pass** | pass |
| FR-002 / US1-AC2–3 | `test` | same E2E — quick row, tiles and readout hidden, zero boxes, bottom border `0px`, panel ~39px — **pass** | pass |
| FR-003 / US1-AC4 | `test` | `ServiceEntryViewTests::test_an_edit_form_for_a_verse_less_song_states_it_in_the_markup` — panel not `hidden`, `data-empty="true"`, `data-settled="true"` — **pass** | pass |
| FR-004 / US2-AC1 | `test` | same E2E — empty → populated swap removes `data-empty`, restores three boxes and `Bait 1`; re-pick restores the summary-only state — **pass** | pass |
| FR-004 / US2-AC2–3 | `test` | `test_the_song_pick_searches_and_the_verses_start_all_checked`, `test_single_verse_song_keeps_checked_verse_and_disables_picker` — **pass** | pass |
| FR-005 / US1-AC5 | `test` | updated `test_a_song_with_no_verses_is_named_and_cannot_be_saved` plus `ServiceEntryTests::test_a_song_entry_with_no_verses_names_the_song` and `test_a_song_entry_keeps_at_least_one_verse` — **pass** | pass |
| FR-006 | `inspection` | `git diff --stat`: only `_entry_form.html`, `components.css` and `entries.js` changed on the product side; the song stage, projector and dock are untouched | pass |
| SC-001 | `test` | new E2E, Add state — **pass** | pass |
| SC-002 | `test` | new E2E, zero visible controls — **pass** | pass |
| SC-003 | `test` | new E2E's no-song 0px assertion and the two full-picker pins — **pass** | pass |
| FR-004 motion | `inspection` | `git diff static/web/entries.js` is one hunk in `verseSummary()`; the `panel.hidden` / `data-settled` reveal branch below it is byte-identical, so the 200 ms curve is unchanged | pass |

## Verification runs

- **Red**: three targeted pins — server fragment failed on `hidden`, both E2E pins timed out
  waiting for `data-empty` / `data-settled`. Failed for the intended reasons.
- **Green**: the same three pins — 3/3 OK in 7.9 s.
- **Broader**: `ServiceEntryViewTests` + `EntryModalE2ETests` + `multimedia.tatib.tests`,
  198 run / 5 non-green: `test_an_empty_service_invites_the_first_item` (error),
  `test_legacy_tatib_list_keeps_its_route_and_payload_fields`,
  `test_image_projection_is_one_image_screen`,
  `test_an_empty_service_places_its_tiles_a_quarter_of_the_way_down`,
  `test_the_add_controls_wait_for_a_hover`. All five reproduce **byte-identically** on
  unmodified `develop` at `be9863d2` in a separate worktree with a throwaway DB — pre-existing
  reds (ITEM-184, ITEM-217 and the empty-tiles card), not slice regressions.
- Heavy suite deferred to the push step, per repo convention.

## Outcome

Converged on pass 1 with zero gaps and no accepted gaps. Fold may run.
