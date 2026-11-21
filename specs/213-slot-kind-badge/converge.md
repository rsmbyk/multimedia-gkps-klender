# Converge 213: a slot states the kind it resolves to

**Date**: 2026-11-21 · **Pass**: 1 · **Traceability read**: `plan.md` § Traceability

## What was checked

Every row of the plan's traceability table was re-assessed against the tree as it now stands — not
against the task boxes. The suites run were `tests.e2e.test_tatib_templates` (33 now, 32 before),
`tests.e2e.test_stage_kind_marks` (11), `multimedia.web.tests` (329) — **373 tests, 1 failure**, and
that failure is the known-red ITEM-217 (see F4). The probes were `probe_adopted.py` and
`probe_glyphs.py`.

## Findings

| # | Row | Type | Evidence | Disposition |
| --- | --- | --- | --- | --- |
| F1 | FR-001, FR-002, FR-007, SC-001, SC-002 | complete | `test_a_slot_row_carries_the_kind_it_resolves_to` green: five badges, `['song','scripture','media','text','song']`, four distinct path sets; `SlotKindBadgeTests` (3 unit tests) green for the four readable kinds, the unreadable row and the dated service | none |
| F2 | FR-003, SC-003 | complete | the same test asserts the frame's computed `stroke-dasharray` is `2.8px, 2.4px` on every slot row and that the fill-in mark keeps `M10 6.8v6.4M6.8 10h6.4` | none |
| F3 | FR-004, SC-005 | complete, **checked by test with a substitution** | the test asserts `aria-hidden="true"` and empty `textContent` on every badge rather than comparing the row's accessible name: this Playwright build (no `Locator.aria_snapshot`, no `page.accessibility`) has no name readout. An `aria-hidden` element with no text cannot contribute to a name, so the two are equivalent in effect — but the record says which one was actually run | none; the substitution is stated, not glossed |
| F4 | baseline | **known red, not this slice** | `multimedia.web.tests.ServiceProjectorTests.test_the_shortcuts_sheet_names_audio_and_video_in_groups_of_their_own` fails identically on unmodified `develop` (`a6d1002c`) with the same three-column diff. It is board card ITEM-217's list (the shortcuts sheet) | accepted — not this slice's; the slice touches no shortcuts code |
| F5 | FR-005, SC-004 | complete | every slot row's `y`/`height`, every title's `x` and the page's scroll height compare equal with the badge drawn and with it suppressed; `probe_adopted.py` reports `2278` vs `2278` in both themes | none |
| F6 | FR-006 | complete | computed ink `rgb(156,154,145)` on disc `rgb(20,19,15)` dark = **6.59:1**; `rgb(100,99,87)` on `rgb(247,245,241)` light = **5.57:1**; the four fill states set `background-image`, asserted in the test | none |
| F7 | US2/AC1 "both carry the same note glyph" | **partial — wording** | measured: the entry's mark path is `M9 17.4V5.6l10.2-2v11.6|circle|circle` at 20px; the badge's is `M4.5 8.7V2.8l5.1-1v5.8|circle|circle` at 10px. The same note in form, drawn on the badge's own 12-unit grid — which is D003's decision and is stated in `## UI/UX`. The scenario's phrase "the same note glyph" reads as byte-identical | accepted, recorded: the grid difference is deliberate and documented; a reader who wants identity will find the two path sets in this line. Not a code defect and not worth reopening Specify for a phrase the `## UI/UX` already qualifies |
| F8 | US3/AC1–3 | complete | no motion: `transition-duration` is `0s` on every badge; no wrap: the title column is untouched (F5); `prefers-reduced-motion` has nothing to reduce | none |
| F9 | Edge: unfinished choice | complete | the fixture's no-options choice is badged (`song`) and its row still reads `No options yet` | none |
| F10 | Edge: the Use template dialog | complete — **unrequested work avoided** | the dialog's slot rows carry no `.slot__mark` at all, so nothing was added there; `_generate_modal.html` is untouched by this slice | none |
| F11 | Edge: sidebar | complete | `#chList` carries no badge; asserted by the unit test's dated-service page and by `test_stage_kind_marks`' own surface check | none |
| F12 | record drift | **contradicts — fixed** | `_slot_kind_badge.html`'s comment still explained the grid choice with the *11px* candidate's number ("at 8.5px"), stale after the owner chose B | fixed in this pass: the comment now states the 10px box and the ~0.75px stroke it would produce on a 24-unit grid |

## The defect this slice carried into gate 1, and its fix

The badge's glyph did not paint on the live page at gate 1: the preview page carried its own
`fill: none; stroke: currentColor`, and the product's rule did not, so the shipped `<svg>` fell back to
`fill: rgb(0,0,0)` — a black glyph on a near-black disc. Every box measurement was right, which is why
nothing caught it until the pixels were read as text. It is fixed by declaring the paint on the
template's own `<svg>` (D006) and guarded by an assertion that the computed `fill` is `none`.

## Outcome

**Converged** — 12 rows complete, 1 partial accepted with its wording recorded (F7), 1 record drift
fixed (F12), 1 known-red excluded with evidence (F4). No CRITICAL. No unrequested behaviour.
