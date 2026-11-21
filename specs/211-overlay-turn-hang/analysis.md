# Analysis: a speaker's turn hangs under its words

**Spec**: `specs/211-overlay-turn-hang/spec.md`
**Plan**: `specs/211-overlay-turn-hang/plan.md`
**Tasks**: `specs/211-overlay-turn-hang/tasks.md`
**Run**: 2026-11-21 · base `7a0e7069`

## Artifact digests (sha256, first 12)

| Artifact | Digest |
| --- | --- |
| `spec.md` | `b308141587cc` |
| `plan.md` | `a8814e7d55e1` |
| `research.md` | `f00495f7ce62` |
| `data-model.md` | `6e375804d734` |
| `quickstart.md` | `161e691ab653` |
| `tasks.md` | `f224e3c8edd3` |
| `checklists/requirements.md` | `c49570d5e10e` |

## Checks

Manual consistency read: 6 FR + 4 SC + 6 story scenarios are all traced in `plan.md`, plus the two
inspection rows (preview, Fold target); **19/19**. The declared split `17 test · 2 inspection ·
0 manual` matches the plan's rows, and every `test` row has a task in `tasks.md`. All source and
artifact paths named in the pack exist. The requirements checklist is unticked as reviewer-owned
(SDD-15). No consistency-checker script ships in this repo, so these checks were read by hand rather
than reported from a tool.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MED | preview | `preview/index.html` | The page links the real `obs-overlay.css`, whose first rule puts `overflow: hidden` on `html`; the review document had 725 px of content below the fold and the owner could not scroll to it. | fixed before gate 2 — the preview overrides `html { overflow: auto }`; wheel scroll verified at 520×700 and 1280×800 and in the browser panel (725 px travel) |
| A2 | LOW | scope | `data-model.md` | A token-alone line (`Paragenda:`) carrying a previous voice is indistinguishable from a continuation at this seam, so it gains the indent on a screen that also paints a real mark. The classifier is unchanged. | accepted — recorded in `data-model.md` and left with ITEM-224; changing the classifier here would reopen the spec |
| A3 | LOW | test | `tests/e2e/test_obs_overlay.py` | Under MULTI_LINE a third line pairs onto a second screen, so a marked line, a continuation and a new `J.` answer cannot share one screen in the existing fixture. | fixed mechanically in T003 and D004 — separate fixtures, one single-screen, one nth-screen helper |
| A4 | LOW | process | `plan.md` | No full-suite run is declared locally; the repo runs browser E2E at the push step. | accepted — the focused overlay module is declared and green before commit |
| A5 | LOW | process | `plan.md` | `CONSTITUTION.md` is absent, so the Constitution Check has no principles to apply. | accepted — SDD-01 makes it optional |

**CRITICAL**: 0 · **HIGH**: 0 · **MED**: 1 (fixed) · **LOW**: 4

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T004, T007 |
| FR-002 | ✅ | ✅ | T004, T008 |
| FR-003 | ✅ | ✅ | T010, T007 |
| FR-004 | ✅ | ✅ | T011, T012 |
| FR-005 | ✅ | ✅ | T004 |
| FR-006 | ✅ | ✅ | T006, T008 |
| SC-001 | ✅ | ✅ | T004 |
| SC-002 | ✅ | ✅ | T006 |
| SC-003 | ✅ | ✅ | T010 |
| SC-004 | ✅ | ✅ | T013 |
| US1/AC1 | ✅ | ✅ | T004 |
| US1/AC2 | ✅ | ✅ | T004 |
| US1/AC3 | ✅ | ✅ | T005 |
| US2/AC1 | ✅ | ✅ | T010 |
| US2/AC2 | ✅ | ✅ | T011 |
| US2/AC3 | ✅ | ✅ | T011 |
| UI/UX | ✅ | ✅ | T014 — preview readout |
| overlay/R5 | ✅ | ✅ | T016 — Fold |

**Coverage**: 100% · **CRITICAL**: 0

## Applied mechanically

- Added `html { overflow: auto }` to the static review page so the real OBS sheet's browser-source
  rule does not trap the reader (A1).
- Chose five independent TEXT fixtures and one nth-screen helper instead of extending the first
  entry, so screen pairing cannot split a turn mid-test (A3).
- No requirement was rewritten and no checklist item was ticked.

## Escalated

- None. The one scope question skipped at gate 1 (token-alone shape) is recorded as an assumption
  and an ITEM; it does not change this pack.

## History
- 2026-11-21 — gate 2 read: 0 CRITICAL, 100% coverage; one MED preview defect fixed before the
  gate and re-verified.
