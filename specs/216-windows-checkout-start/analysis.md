# Analysis: a checkout made on Windows starts the stack

**Slice**: `specs/216-windows-checkout-start` · **Run**: 2026-11-21 · **Gate 2 pre-read**

## Artifacts read

| Artifact | SHA (git hash-object) |
| --- | --- |
| `spec.md` | `e1b738969832448055154fcfed8b0ae2429590cf` |
| `plan.md` | `a55b7ad72aae210e434966d7b53739cc3fae5883` |
| `research.md` | `57154b7703f1e432853e6865ae65229895995eb2` |
| `data-model.md` | `002081112549012c4a0c4e823c01abc48f6fe049` |
| `contracts/none.md` | `b41d14f2bad1169772cadb8b22f49976ef15f996` |
| `quickstart.md` | `09cdbcd4810fc5c31e9c4a2c75aa90e77c87a6b7` |
| `tasks.md` | `8f19adb2a37f75fc40a947d2bcad41dbef0cb697` |
| `checklists/requirements.md` | `7ce8cb4d3e549c2f276469ee4ec3da13b4ba2897` |

## Metrics

`FR: 7/7 with tasks · scenarios: 11/11 with a verification row · coverage (traceability): 100% ·
markers: 0 · findings: 0 CRITICAL, 0 HIGH, 2 MEDIUM, 1 LOW`

Coverage is read from Plan's traceability table, not re-derived from tasks (SDD-17): FR-001 → T001
(`test`) and T003 (placement, `test`); FR-002 → T004/T005 (`test`); FR-003 → T006 (`inspection`);
FR-004 → T014 (`inspection`); FR-005 → T010 (`test`) with the `up.ps1` half in T014's notes; FR-006 →
T008/T009 (`test`); FR-007 → T011/T012 (`test`). SC-001 → T001 (`test`) + T007 (`manual`);
SC-002 → T004 (`test`); SC-003 → T014 (`inspection`); SC-004 → the whole launcher module staying
green. US1's three scenarios → T001/T007, T004, T006. US2's three → T008/T014, T010, T012. The five
edge cases → T001 (pre-pin checkout), T004 (`*.ps1` untouched), T004 (`up.sh` under Git Bash), T011
(any non-zero exec status reports), T010 (an empty mount is not reported as dead).

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A-01 | MEDIUM | SC-001's end-to-end row (T007) converts `docker/entrypoint.sh` to CRLF **in the working tree** and must restore it. An interrupted run leaves a modified tracked file, and the next `git diff` shows a whole-file change that reads like damage. | **Accepted.** The file is tracked, so `git checkout -- docker/entrypoint.sh` restores it, and the task names the restore in the same line. Doing it on a copy instead would not exercise the build context, which is the whole point of the row. |
| A-02 | MEDIUM | The FR-002 test reads `git check-attr`, so the suite now needs the tests to run inside a git checkout. A source tarball with no `.git` would fail on the attribute row. | **Accepted.** `tests/test_docker_compose.py` and `tests/test_launcher_fonts.py` already read repository files directly and assume a checkout; CI clones. The alternative — parsing `.gitattributes` by hand — would test the file's text instead of git's answer, which is the thing the checkout depends on. |
| A-03 | LOW | The `up.ps1` half of FR-004/FR-006/FR-007 rests on inspection: PowerShell is not installed on the development machine (D006), so a Windows operator is the first person to run that block. | **Accepted, recorded.** The same limit is already written into `tests/test_launcher_fonts.py`'s docstring for the block this slice changes, and the failure the slice fixes was itself reported from Windows — the block's next real run is the proof. |
| — | — | No CRITICAL. No requirement lacks a task; no terminology drift (the spec says *companion*, *launcher*, *strip*, *pin* throughout); no same-statement duplicates; no stale paths or IDs. | — |

No mechanical fixes were applied: the first run needed none. The checklist's thirteen items map to the
spec's sections — CHK001/CHK003/CHK004 → §Requirements and §US2, CHK002 → §Edge Cases,
CHK005/CHK006/CHK007 → §FR-001–FR-003, CHK008/CHK009/CHK010 → §Functional and §Assumptions,
CHK011/CHK012/CHK013 → §Success Criteria and §UI/UX.

## History

- 2026-11-21 — first run: 0 CRITICAL, 100% coverage → gate 2 opens.
