# Analysis: pending state for Search and Media Library rail tiles

**Date**: 2026-11-26
**Spec**: `specs/245-rail-fetch-feedback/spec.md`
**Plan**: `specs/245-rail-fetch-feedback/plan.md`
**Tasks**: `specs/245-rail-fetch-feedback/tasks.md`

## Artifacts read (SHA-256 at this run)

| Artifact | SHA-256 |
| --- | --- |
| `preview/media-override.yml` | `04e34167788d68856fc4807ace43a5a1301f5ebcbb68d19d6b91e9fc6fa3589b` |
| `spec.md` | `6c97f1db32cd19e851dfd76ecae7874c574af9c76c277fe649f27b809bf2df94` |
| `plan.md` | `6dd1721f9ce7391ba9bde4dfe697586458fddaae30ac94b8dbc19b3e7e5428b8` |
| `research.md` | `d709f715067359a325b098db5171b97576d5425c2e3984d6c682319e331bf4f5` |
| `data-model.md` | `27ae326ab4840520cab8e9decb34a08b64a4bfe6194d8149ff474d2e8cad4d68` |
| `quickstart.md` | `f7dc5157481f77e75cd209dd19ceba67750438be4f3a51cb7f8140acb78868b8` |
| `tasks.md` | `53cf9120bf5091394fc804548765b6032a0a57eb16ed7160d571435ccc426de2` |
| `checklists/requirements.md` | `135e46b76d7e1259b6e2df4f4e31ce62493aedbc070c04afc3c0d29e610ae9ee` |
| `contracts/README.md` | `2f8d9a1e8c11205ba4b84fd445da54a0bf139c413f3fb90d217c9dceef639965` |
| `preview/README.md` | `fa230409d6a35d23bb6c8311b1adb6eba157245ebf273643396134b3e7714cf7` |
| `preview/build_previews.py` | `c16d69d21db973d3ba3f893084426f8c9c83aa1fb7a7fc6fe8499e82eb47c678` |
| `preview/probe.py` | `690041f25f686f8968f4f1c32df882f4a7043767c1ef552e83d52de3c4abd477` |
| `preview/run_local.py` | `a653d007d3b8ef3999ac0cb7f0c3fd5afb6fa21200ce4fe3421edcaec6a3bc92` |

## Metrics

- 10 FR (13 rows) · 4 SC · 10 acceptance scenarios · 29 traceability rows · 17 tasks.
- Verification split: 18 `test` · 11 `inspection` · 0 `manual`; coverage 27/29 traceability rows (100%), each assigned to at least one task.
- Zero `[NEEDS CLARIFICATION]` markers; zero CRITICAL findings.

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | |
| FR-002 | ✅ | ✅ | |
| FR-003 | ✅ | ✅ | |
| FR-004 | ✅ | ✅ | |
| FR-004 | ✅ | ✅ | |
| FR-004 | ✅ | ✅ | |
| FR-005 | ✅ | ✅ | |
| FR-006 | ✅ | ✅ | |
| FR-006 | ✅ | ✅ | |
| FR-007 | ✅ | ✅ | |
| FR-008 | ✅ | ✅ | |
| FR-009 | ✅ | ✅ | |
| FR-010 | ✅ | ✅ | |
| SC-001 | ✅ | ✅ | |
| SC-002 | ✅ | ✅ | |
| SC-003 | ✅ | ✅ | |
| SC-004 | ✅ | ✅ | |
| US1/AC1 | ✅ | ✅ | |
| US1/AC2 | ✅ | ✅ | |
| US1/AC3 | ✅ | ✅ | |
| US1/AC4 | ✅ | ✅ | |
| US2/AC1 | ✅ | ✅ | |
| US2/AC2 | ✅ | ✅ | |
| US2/AC3 | ✅ | ✅ | |
| US3/AC1 | ✅ | ✅ | |
| US3/AC2 | ✅ | ✅ | |
| US3/AC3 | ✅ | ✅ | |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 3

## Applied mechanically

- `spec.md` status was updated to Accepted at gate 1 after the owner's word; the earlier draft
  status is superseded, not deleted.
- The verification split was counted from the plan's traceability table (16/11/0), not carried
  from the task draft.
- The first draft's "one line and two bars" placeholder was recorded as a superseded clarification
  after the owner asked for the real layout; the three destination shapes are now in FR-004.
- `preview/run_local.py` was added so the quickstart's database commands never print credentials.
- After gate 2, artifact SHAs were refreshed and the test-function names and `openSearch()` source option were recorded.
- Later passes added FR-011 (direct-load loading line and spinner), FR-012 (hide previous search shell) and the local companion override; the split and SHAs above were recounted for this report.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| H1 | HIGH | The shell hides `.search-results` and `.search-home` on the reading home state; a placeholder using those classes paints blank unless a scoped override is added. | T008 adds the override, mirroring the accepted preview. Converge checks computed `display`/`visibility` and the painted box; the cost of leaving it unmeasured is a blank stage during a fetch. |
| H2 | HIGH | An in-page Media Library visit changes `data-home` to `landing`; the rail's current-page marker and sidebar state must follow the arriving page, not the previous one. | `applyPage()` already syncs `aria-current` from the fresh document and `shell:page` re-binds the library; T009 and inspection rows confirm it. A failure would leave a stale Search highlight. |
| L1 | LOW | Reduced motion and the status announcement are inspection rows, not independently asserted by a test. | Owner defers the full browser suite to the push step. Converge reads the CSS/`announce()` call sites and the probe's reduced-motion state; cost is one visual check, not a behaviour risk. |

## Escalated

- None — no intent-changing finding; the placeholder revision was settled before gate 1.

## History

- 2026-11-26 — first run: 0 CRITICAL, 2 HIGH, 1 LOW; 27/28 rows covered; mechanical fixes above applied and re-read before this report.
