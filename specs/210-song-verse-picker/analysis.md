# Analyze: the song entry's pickers

**Date**: 2026-11-21
**Artifacts read**: `spec.md`
(`c500bd3c7a9dc63400038dc8b24c6021c5c849c9c3d86015a67a98219c517fbb`),
`plan.md` (`e6dde588ff42d7b62ae0c0ee782eb8ebc7fcc1b5959efa76c5ec4b42413946df`),
`tasks.md` (`d29c03419a16d209958773b501378969ad50d5839825160c7a9fa93c7fbffe41`),
`checklists/requirements.md`
(`80118bf6f84c57280bf37f73c999de44a42b2dbebb6b98dbd66015e44850d0da`),
`preview/README.md` (`4a9d7935a3216f27e3a0a58e3340fe975101696934de0145d4a74d55fb30025e`)
**Metrics**: 16 FR · 5 SC · 19 acceptance scenarios · 4 edge cases · 21 tasks ·
12 checklist items · 44 traceability rows · coverage 44/44 (100%) · 0 CRITICAL ·
1 HIGH · 3 MEDIUM · 2 LOW

## Findings

| ID | Severity | Dimension | Finding | Disposition |
| --- | --- | --- | --- | --- |
| F1 | HIGH | Verification | `tests/e2e/test_entry_pickers.py` has a backdrop race that fails on unmodified `develop`; the new picker pins must not inherit it. | **Accepted, guarded** — the slice has its own E2E module (`T002`), and the known base failure stays on the board rather than being quarantined here. |
| F2 | MEDIUM | Consistency | `reading/R30` currently requires a disabled Verses trigger for a no-verses song, while FR-014 hides the whole section. | **Declared modification** — the spec names the change and `T019` folds the replacement block with the old wording visible as superseded. |
| F3 | MEDIUM | Consistency | `reading/R43` currently requires a comma-list summary while FR-012 uses collapsed en-dash ranges. | **Declared modification** — IDs and `{id, number}` payload stay unchanged; `T019` replaces only the summary clause. |
| F4 | MEDIUM | Scope | The song picker and verse picker are two concerns; the owner chose one slice. | **Accepted, recorded** — the plan separates them into US1–US4 with independent tests, and nothing is split across branches. |
| F5 | LOW | Provenance | A board card ID is not claimed in the Draft. | **Deferred by design** — `T001` re-checks free IDs and `T021` attaches the card at delivery; no number is invented here. |
| F6 | LOW | Versioning | `patch` and `minor` are both defensible for a picker revamp. | **Recorded decision** — plan declares `patch`: the existing pickers change, no new capability or breaking change is added. |

## Coverage

| Group | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001–FR-016 | ✅ 16/16 | ✅ | Every functional requirement has a named component and verification method |
| SC-001–SC-005 | ✅ 5/5 | ✅ | Focus, drag, pre-release values, dialog height and hidden states are measured |
| US1–US4 acceptance | ✅ 19/19 | ✅ | Each story scenario is a row; E2E pins are grouped by story |
| Edge cases | ✅ 4/4 | ✅ | Fetch failure, stale numbers, same-tile drag and no-result |
| Checklist | ✅ 12/12 | n/a | Reviewer-owned; generation only, none ticked |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH**: 1 · **MEDIUM**: 3 · **LOW**: 2

## Applied mechanically

- Corrected the traceability split to 40 `test` · 4 `inspection` · 0 `manual` after counting
  the table rows, so the plan and `tasks.md` agree.
- Confirmed spec 210 and `reading/R48` were free across branches and worktrees; R46 belongs to
  slice 209 and was not reused.
- Confirmed no `[NEEDS CLARIFICATION]` markers and no personal names in any repo artifact.

## Escalated

- None. The HIGH finding is reported with its guard; it does not change intent and needs no
  owner decision before gate 2.

## History

- 2026-11-21 — first analysis; 44/44 covered, zero CRITICAL, one HIGH reported with its guard.
- 2026-11-21 — mechanical delta after Converge: the plan's 19 abbreviated test paths were
  expanded to full module paths; no requirement or finding changed.
