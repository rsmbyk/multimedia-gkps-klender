# Converge — spec 215

**Pass 1** · 2026-11-21 · checked against `plan.md`'s traceability table.

## What was checked

Every row of the traceability table, by the method it declared: the `test` rows by running the two
lanes, the two `inspection` rows by opening the rebuilt preview in both themes and reading the
picture.

| Lane | Baseline (branch, before the slice) | After |
| --- | --- | --- |
| `multimedia.web.test_tatib_templates` | 35 tests, OK | **41 tests, OK** (+6) |
| `tests.e2e.test_tatib_templates` | 33 tests, OK | **38 tests, OK** (+5) |
| `multimedia.web` (whole app) | 444 tests, 2 failures + 8 errors | unchanged: the 8 errors are the local manifest-static trap (`Missing staticfiles manifest entry for 'assets/gkps.png'`), and both failures reproduce on `origin/develop` at `467968b0` in a detached worktree — they are ITEM-217's known red |

## Findings

| # | Row | Type | Evidence | Outcome |
| --- | --- | --- | --- | --- |
| 1 | FR-001, SC-001, SC-002, SC-004, US1/AC1, US1/AC3, US1/AC4 | — | `test_the_copy_confirmation_covers_the_window` measures at 1440×900 and 900×700: `position: fixed`, the layer's rect equals the viewport's, the card's centre is the viewport's centre, the dialog's height is unchanged on open and on close, and `elementFromPoint` at the form's Save lands inside the layer | **converged** |
| 2 | FR-002's *inert* half | — | the same test: `hitInsideLayer` is true at both sizes | **converged** |
| 3 | **FR-002's *legible* half** | `partial` | `SC-003` passes as written — the dialog's title text is unchanged and its rendered colour differs from the scrim's fill — but the inspection shows the dialog is a dimmed **silhouette**: the card (341.7px) is taller than either dialog (312.5 / 241.3), so the dialog's own text sits *behind the card*, not behind the scrim. "Dimmed by a scrim light enough to leave it readable" overstates what the surface does; nothing readable is left of the dialog's text at either size. | **reported — see below** |
| 4 | FR-003, SC-005, SC-009, US2/AC1 | — | `test_the_confirmation_offers_the_source_name_plus_copy` (`value="Ibadah Minggu (Copy)"`) and `test_a_long_source_name_is_trimmed_to_fit_the_copy_name` (a 64-character source → 57 characters + ` (Copy)`) | **converged** |
| 5 | FR-004, SC-006, US2/AC2, US2/AC3 | — | `test_the_name_selects_itself_on_the_first_click` (selection `[0, 21]`, typing replaces it) and `test_a_second_click_places_a_caret` (start == end) | **converged** |
| 6 | FR-005, SC-007, US2/AC4 | — | `test_a_copy_takes_the_posted_name` (unit) and `test_copy_as_template_asks_and_copies` (E2E: typed `Model Minggu Pagi`, the created row carries it, the source keeps `Ibadah Minggu`) | **converged** |
| 7 | FR-006, SC-008, US2/AC5 | — | `test_a_blank_name_cannot_be_accepted` (spaces → `disabled`, one character → enabled) | **converged** |
| 8 | FR-007 | — | `maxlength="64"` on the field; `test_a_copy_refuses_a_blank_name` and `test_a_copy_refuses_a_name_over_64_characters` both answer 400 and leave no row | **converged** |
| 9 | FR-008, FR-010, US3/AC1 | — | `test_the_copy_confirmation_card_matches_the_preview`: 448 × 341.7, 22px padding, 14px radius, the parts in the accepted order, the three fact strings, the answers 8px apart and 22px inside the right edge | **converged** |
| 10 | FR-009 | — | `test_escape_closes_the_confirmation_and_not_the_dialog`: the layer hides and `#editorModal.open` stays true | **converged** |
| 11 | FR-011, SC-010, US3/AC2 | — | `test_the_scrim_closes_the_confirmation`: a click on the card's heading does not dismiss, a click on the layer does, and the dialog stays open | **converged** |
| 12 | US2/AC6 | — | `test_a_template_copy_keeps_its_slots` (existing) still passes, and the confirmation renders for a template's dialog with its own default (`Skeleton (Copy)`) | **converged** |
| 13 | SC-003, US1/AC2 | `inspection` | the rebuilt preview, dark and light: the dialog's shell and field shapes are visible behind the layer, its text is not — the same finding as #3 | **checked by inspection** |
| 14 | — | `unrequested` | none found: every rule added to `components.css` serves FR-006, FR-008 or FR-010, and the light-theme scrim override serves FR-002 | **converged** |

## Finding #3, stated plainly

The owner accepted a preview in which the confirmation card sits over the dialog, larger than it. That
is what shipped, and it is what the E2E tests pin. What did **not** ship is the adjective the spec put
on it: FR-002 says the dialog stays *legible*, and it does not — the card covers the dialog's text
entirely at both dialog sizes.

Two ways out, and the choice is the owner's:

- **Amend the wording** (recommended): R47 says the dialog "stays open and visible as a dimmed
  silhouette behind the layer, and is inert while the confirmation is up". One clause, no code, and it
  describes what the accepted preview actually shows.
- **Reopen at Specify** (SDD-21's rule for a spec-at-fault conflict): the spec pack re-enters at
  Specify, which by SDD-25 invalidates this plan and sends the slice back through the gates.

## Outcome

**Converged with one reported spec conflict** (finding #3). Every other row converged on the method it
declared. No `missing`, no `contradicts` in the code, one `partial` that belongs to the spec's wording
rather than to the code.

Pass count: **1 of 3.**
