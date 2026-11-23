# Convergence: a created Template opens on the reading stage

## Pass 1 — 2026-11-23

**Artifacts read**: `spec.md` (`ac14075f…`), `plan.md` (`1e827c0d…`), `tasks.md` after Implement
(`b911ce47…` at Analyze; T001–T009 ticked since), `analysis.md`, `docs/spec/reading.md` R46,
`static/web/reading.js`, `tests/e2e/test_editor.py`.

**Checked**: every row of Plan's traceability table by the method it declared.

- **19 `test` rows** — checked by the targeted Django/Playwright run on the dedicated
  `test_gkps234` database: the six new spec 234 cases plus the six existing spec 209/215/167
  cases, `12 tests … OK`. Red evidence was collected first with base `reading.js`: five of the new
  cases failed on the list URL, and the no-reload guard passed there by design (it guards an
  invariant, not the change). The full browser suite is deferred to the push step.
- **`D002 seam` (inspection)** — `git diff -- static/web/reading.js` shows one condition and one
  URL expression inside the `editor:saved` create branch; `editor_save` still returns
  `record_kind`, no endpoint, form or template changed.
- **`D004 level` (inspection)** — `VERSION` is still `1.36.19`; the plan declares `patch`, to be
  applied with the changelog line in the pre-merge delivery commit.
- **User story scenarios** — each is covered by the named test above; the empty template's
  invitation and actions are asserted visible in `test_an_empty_created_template_shows_its_add_actions`.
- **Superseded wording** — the old template assertion is gone from `test_editor.py`; its text is
  preserved in `spec.md` and will replace R46 at Fold.

| Finding | Type | Evidence | Disposition |
| --- | --- | --- | --- |
| none | missing | all 21 rows have a check | — |
| none | partial | every assertion ran in the targeted pass | — |
| none | contradicts | code, spec and tests agree on `/tatib/<id>/?mode=template` | — |
| none | unrequested | diff limited to the create branch and its tests | — |

**Outcome**: converged at pass 1. No accepted gaps. Fold may write the `reading/R46` delta.

## Push-step verification

The two relevant browser modules were run in full on the dedicated `test_gkps234` database:

| Code | Result |
| --- | --- |
| slice head | `85 tests … FAILED (errors=5)` — all six spec 234 cases pass; the five errors are date-picker/pointer cases |
| base `be9863d2` with the same test files | `85 tests … FAILED (failures=5, errors=5)` — the same five errors plus the five expected red spec 234 cases |

The five errors are identical on base and slice: two viewport variants of
`test_date_picker_cells_are_square_across_widths_and_month_lengths`,
`test_pointer_closed_editor_does_not_leave_its_row_control_visible`,
`test_tatib_date_picker_loads_saved_date_and_clears_on_edit`, and
`test_tatib_date_picker_selects_clears_and_supports_keyboard`. They are pre-existing board demand,
not regressions from this slice.
