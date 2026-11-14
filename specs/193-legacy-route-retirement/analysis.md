# Analysis: Retired Addresses

**Spec**: `specs/193-legacy-route-retirement/spec.md`
**Plan**: `specs/193-legacy-route-retirement/plan.md`
**Tasks**: `specs/193-legacy-route-retirement/tasks.md`

**Slice**: `specs/193-legacy-route-retirement` · **Run**: 2026-11-14 · **Gate 2 pre-read**

## Artifacts read

| Artifact | SHA (git hash-object) |
| --- | --- |
| `spec.md` | `f72a9cfd4b08bc94b97e98b568ef66ca8a4515d3` |
| `plan.md` | `14a74ea3c8982165cee5fb4d03caf36db7444233` |
| `research.md` | `396c6b94ee5d3e0dad855bd2c0ad12de753aca1f` |
| `data-model.md` | `daac479f40cc253c8ad2d3042e96362580097bab` |
| `contracts/routes.md` | `852b23c4d2429b88b8d2f60e177dbed66d9762c8` |
| `quickstart.md` | `938fc300e5d61f25bdfb31e26d6351d1c4b21b1e` |
| `tasks.md` | `237835c0e41db0d291306d3da069606dfe7addaa` |
| `checklists/requirements.md` | `8469e766a9876982d828fb1dafefca2208f4db15` |

## Metrics

`FR: 13/13 with tasks · scenarios: 14/14 with a verification row · coverage (traceability): 100% ·
markers: 0 · findings: 0 CRITICAL, 2 HIGH, 1 MEDIUM, 1 LOW`

Coverage is read from Plan's traceability table, not re-derived from tasks (SDD-17). The split it
declares is `20 test · 3 inspection · 2 manual`; every `test` row names a function and every
inspection row names what to look at.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A-01 | HIGH | design | `plan.md` FR-006a | The hover-revealed instruction needs a pointer. An OBS browser source has none until the operator clicks *Interact*, and a touch device has no hover at all, so the "where to point the source instead" sentence is reachable only through one deliberate act. | **Accepted by design.** The owner chose a watermark at 20% with the instruction one hover away, and named OBS's *Interact* as the way in (spec Clarifications, 2026-11-14). The resting line already identifies the source; the hover line is the repair instruction, not the identification. No code change. |
| A-02 | HIGH | coverage | `tasks.md` T014 | `reverse('web-home')` has 76 call sites across 11 modules (40 in `tests/e2e/test_reading.py`, 14 in `test_editor.py`, 5 each in two others, and a tail across six more). A missed one is a `NoReverseMatch` at test time, and the targeted Django module cannot see the E2E modules. | **Covered by T014 + T027.** T014 sweeps by grep before the suite runs; T027 runs the whole suite and requires every remaining failure to be one of the eleven pre-existing red items. Recorded because the count is the risk. |
| A-03 | MEDIUM | security | `plan.md` `successor()`; `tasks.md` T019/T020 | A computed same-origin path is not automatically safe: Chromium reads `/\evil.example` as `//evil.example`, so an archive address could name another host. The first draft of `successor()` had no guard. | **Fixed in the pack before Gate 2.** `archive()` unquotes its tail, `successor()` answers `/` for a backslash path, and T019 asserts `/archive/%5Cevil.example` → `/`. Verified against Django's resolver: the test client decodes `%5C` before the URLconf sees it, so the captured tail already carries the backslash. |
| A-04 | LOW | maintainability | `multimedia/urls.py`; research D005 | `/obs/blank` is a live surface registered in the root URLconf beside `/obs/dock`, deliberately outside `multimedia/obs/`. A later tidy-up could move it into `obs/urls.py`, and next release's deletion would take the live page with the retirement. | **Accepted, mitigated by the block comment.** The `spec 193` comment in `multimedia/urls.py` says the page stays; FR-010's inspection names it as *not* part of the deletion set. No test can prevent a future move. |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T012/T013 |
| FR-002 | ✅ | ✅ | T015/T016 |
| FR-003 | ✅ | ✅ | T002/T003 |
| FR-004 | ✅ | ✅ | T004/T005 |
| FR-005 | ✅ | ✅ | T009 |
| FR-006 | ✅ | ✅ | T006/T007 |
| FR-006a | ✅ | ✅ | T006/T010 |
| FR-006b | ✅ | ✅ | T006/T008 |
| FR-007 | ✅ | ✅ | T017 |
| FR-008 | ✅ | ✅ | T019/T020 |
| FR-009 | ✅ | ✅ | T021 |
| FR-010 | ✅ | ✅ | T023 (inspection) |
| FR-011 | ✅ | ✅ | T018 |
| SC-001 | ✅ | ✅ | T011 |
| SC-002 | ✅ | ✅ | T008 + T010 |
| SC-003 | ✅ | ✅ | T017 |
| SC-004 | ✅ | ✅ | T022 |
| SC-005 | ✅ | ✅ | T021 |
| US1 / AC1–4 | ✅ | ✅ | T002–T011 |
| US2 / AC1–4 | ✅ | ✅ | T012–T018 + T024 |
| US3 / AC1–6 | ✅ | ✅ | T019–T022 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 2/1/1

## Applied mechanically

- FR-011 was missing from the spec as a requirement: the Assumption said the three `/songs/books*`
  routes already pointed at the reading pages, and they point at `/manage/` instead. It is now
  `FR-011` in the Requirements table, the Assumption is rewritten with the correction, and
  `SC-004`'s measurement includes the three legacy moves. Shown at Gate 2 as a spec correction.
- FR-011's archive consequence was missing from research D007, the plan, the contract and T019:
  `/archive/songs/books` would have answered 302 to an address that then 301s — a two-hop chain
  exactly where an old link would arrive. `LEGACY` and `successor()` now share the three rules, and
  the contract gained the archive row.
- The backslash guard (A-03) was added to `successor()`, T001, T019 and the contract in the same
  pass.
- `plan.md`'s FR-011 row still described the old `RedirectView(pattern_name=…)` design after the
  design note changed; corrected to `retirement.LEGACY` + `web/urls.py`.
- `quickstart.md` gained the two not-yet-runnable notes the Plan exit gate requires (the slice's
  own suite does not exist until T002/T010) and the `/archive/songs/books` line in the loop.

No requirement lacks a task, no terminology drift, no same-statement duplicates, no stale paths
or IDs. The checklist's twenty items map to the spec's sections (CHK001–002, 009, 015, 018 →
§Requirements; CHK003, 008, 011 → §Edge Cases; CHK004, 007, 014, 017 → §Success Criteria and
§UI/UX; CHK005, 010, 016 → §Assumptions and FR-010; CHK006, 012 → §Assumptions; CHK013 → §User
Scenarios US1; CHK019 → US3; CHK020 → §Clarifications).

## Escalated

Nothing. Every finding is either accepted by design with its reason or was mechanical and is
recorded above; no finding changes what the owner approved at Gate 1.

## History

- 2026-11-14 — first run: 0 CRITICAL, 100% coverage → gate 2 opens.
