# Analysis: a contents row marks its entry's kind

**Date**: 2026-11-21
**Spec**: `specs/214-sidebar-entry-kind-marks/spec.md`

## Artifacts read

- `spec.md` — `67ce0470e6dc`
- `plan.md` — `2b9d20bb00f6`
- `research.md` — `4657669ae714`
- `data-model.md` — `63227706cb55`
- `quickstart.md` — `fab787d115b3`
- `tasks.md` — `8a1d806b5017`
- `checklists/requirements.md` — `28c184386e78`
- `contracts/toc-markup.md` — `d17bebb2c3c1`
- `preview/build_preview.py` — `ade266660b54`
- `preview/probe.py` — `75e925ffcba4`

## Metrics

`8 FR · 6 SC · 4 stories (13 scenarios) · 30 traceability rows · 29 test · 1 inspection · 0 manual · 49 tasks · 0 CRITICAL · 0 HIGH · 2 MEDIUM · 1 LOW · coverage 100%`

Coverage is read from Plan's traceability table: every FR, every SC and every story scenario has a row,
and every `test` row has a red and a green task in `tasks.md`.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A001 | MEDIUM | Six traceability rows name the same test function (US2/AC1, FR-004 and SC-005 share `test_row_accessible_name_is_unchanged`; US3/AC1, FR-005 and SC-003 share `test_number_centre_and_row_heights_hold`). | Accepted. `tasks.md` creates one red/green pair per distinct function, so no task is duplicated; the table keeps each requirement's own row for Converge. |
| A002 | MEDIUM | The dock's exclusion (FR-008) rests on the sidebar mark using `.songrow__mark` while spec 144's test counts `.entry__kind-icon`. A future refactor that reuses the stage partial would silently fail that test. | Accepted with a guard: `contracts/toc-markup.md` names the class distinction, and `research.md` D001 records why the partials are copied rather than included. |
| A003 | LOW | `quickstart.md` fixes the loopback DB port at 59075, which is the running compose stack's mapped port today. | Accepted. The command is marked as tied to the running stack in the quickstart; Converge re-checks it before claiming a green run. |

No CRITICAL finding: every requirement is verifiable, every decision has provenance, and the two open
questions were answered or skipped with the recommendation recorded before this analysis ran.

## History

- **2026-11-21** — first run: 0 CRITICAL, 0 HIGH, 2 MEDIUM, 1 LOW, 100% coverage; three findings accepted, none fixed silently.
