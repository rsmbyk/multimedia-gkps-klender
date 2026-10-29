# Analysis: a media size reads in the unit that still shows its number

**Date**: 2026-10-28 · **Spec**: `specs/145-media-size-precision/spec.md`, accepted at gate 1 the same day ·
**Plan/tasks**: this commit
**Preview**: live — `http://127.0.0.1:8821/tatib/149/` → **New media**

**Metrics**: 4 requirements · 4 success criteria · 12 tasks · requirement coverage **100%** ·
traceability rows **5/5 declared** (3 requirements + 2 criteria; FR-004 and SC-001/SC-002 fold into the
same test row) · verification split **3 test · 1 inspection · 1 manual** · open findings **4 LOW**,
0 HIGH, 0 CRITICAL.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| F1 | LOW | task | `tasks.md` T005 | The media E2E fake replies to `/inspect` with a fixed `size: 2048`, so a test written against it would prove `2 KB` but never the 12,345-byte case the report names. | **Fixed mechanically**: the new test's companion handler derives `size` from the posted body's length, so the byte count under test is the file the browser actually uploaded. No spec change. |
| F2 | LOW | coverage | `plan.md` §Traceability | `GB` is unreachable through an upload — the 200 MB cap sits four orders of magnitude below it. | **Closed at Converge**: the test asserts `window.gkpsFormatSize(200000000)` and `(1000000000)` against the shipped function on the shipped page, so the unit chain is `test`, not `inspection`. |
| F3 | LOW | ambiguity | `spec.md` FR-003 | "and any later size label" cannot be enforced by a test — a future surface may import its own formula. | **Accepted**: the requirement is a convention; its enforceable half (the three present surfaces) is a test. |
| F4 | LOW | environment | `tests/e2e/test_media_library.py` | `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` fails on this branch and on unmodified `develop`: the gap above a media entry measures **19.89px** at 390px where the test asserts **12px ± 1**. | **Carded** as ITEM-156 — not this slice's to fix. |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T003, T005, T006 |
| FR-002 | ✅ | ✅ | T003, T005 |
| FR-003 | ✅ | ✅ | T004, T006, T007, T008 |
| FR-004 | ✅ | ✅ | T003, T005 |
| SC-001 | ✅ | ✅ | T005 — table of byte counts |
| SC-002 | ✅ | ✅ | T005 — exact strings |
| SC-003 | ✅ | ✅ | T008 — card and library in one run |
| SC-004 | ✅ | ✅ | manual — DevTools read of the line |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 4 LOW

## Applied mechanically

- Traceability collapsed to five rows: FR-004 and SC-001/SC-002 are proven by the same table-driven
  assertion as FR-001/FR-002, so listing them separately would name one test four times.
- `data-model.md` and `contracts/` are `none`, stated explicitly rather than left absent.

## Escalated

- Nothing: no finding changed what the spec means.

## History

| Run | Metric line | Result |
| --- | --- | --- |
| 2026-10-28 · pass 1 | 4 req · 4 criteria · 12 tasks · 5 rows · 100% coverage · 3 LOW | gate 2 open — 0 CRITICAL |
| 2026-10-28 · pass 2 | 4 req · 4 criteria · 12 tasks (12 done) · 5 rows · 100% coverage · 4 LOW | 518 unit tests green; media E2E 23/24, the red one carded as ITEM-156 (identical on `develop`); F2 closed at Converge |
