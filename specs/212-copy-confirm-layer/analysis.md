# Analysis: the Copy as template confirmation is a layer of the edit modal

**Spec**: `specs/212-copy-confirm-layer/spec.md`
**Plan**: `specs/212-copy-confirm-layer/plan.md`
**Tasks**: `specs/212-copy-confirm-layer/tasks.md`
**Run**: 2026-11-21 · base `245399fe` (VERSION 1.35.2)

## Artifact digests (sha256, first 12)

| Artifact | Digest |
| --- | --- |
| `spec.md` | `d68459de2888` |
| `plan.md` | `04f4bff1f066` |
| `research.md` | `6e3225d157a4` |
| `data-model.md` | `2bd905846166` |
| `quickstart.md` | `3776c03e9e16` |
| `tasks.md` | `669553012534` |
| `checklists/requirements.md` | `bf5e2cb0a7bd` |
| `contracts/README.md` | `ab7675d47bdc` |

## Checks

`check_pack_consistency.py` — the script spec 209's analysis names — is not in this repository and not
anywhere on this machine (`find /home/rsmbyk -name check_pack_consistency.py` returns nothing), so its
four checks were run by this pack's own `preview/analyze.py` instead:

```
COVERAGE 10/10 ids traced — PASS
SPLIT declared (13, 2, 0) = counted (13, 2, 0) — PASS
ASSIGNMENT 10/10 ids named in tasks — PASS
PATHS 25/25 exist — PASS
```

The preview probe ran three times during this pass (`preview/probe.py`: the first candidate, after the
scrim's radius fix, after the preview-font fix), and its final output is what the numbers in `## UI/UX`
are taken from.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | MED | version | `plan.md` | The bump was declared as 1.35.1 → 1.35.2, but spec 211's release landed on `develop` mid-flight and `origin/develop` is now **1.35.2** (`4a388682 release: 1.35.2`), so the declared patch number was already spent. | fixed mechanically — branch fast-forwarded to `245399fe`, plan and tasks now declare **1.35.2 → 1.35.3** |
| A2 | MED | preview | `preview/index.html` | The preview's `body` carried `font: 400 13px/1.5`, which the dialog inherited: the *current* state measured 425.5px tall with a 15.21px `h3`, where production measures 476.8px with an 18.72px `h3`. The control state was therefore not the product's. | fixed mechanically — the 13px font now applies to the preview's bar and note only; `body` keeps the product's own 16px, and the current state now matches production to a tenth of a pixel (476.8 / 436 × 235.5 / 18.72px / 16px) |
| A3 | LOW | process | `plan.md` | `CONSTITUTION.md` is absent, so the Constitution Check has no principles to apply. | accepted — SDD-01 makes it optional; nothing to escalate |
| A4 | LOW | scope | `plan.md` | The pack introduces no token (`--radius-dialog`) even though the scrim's 14px now duplicates `.editor`'s radius by hand (D003). | accepted — a token touches every dialog in the product; recorded in D003 as the durable fix this slice does not take |
| A5 | LOW | test | `tasks.md` | The existing generate-page test (`test_a_fill_in_and_a_choice_settle_then_create`) is relied on to prove the scoping in D001 protects `generate.css`, but it asserts behaviour, not the generate confirmation's card metrics. | accepted — the scoping is visible in the diff; a metric test on the generate card would assert a surface this slice did not change |

**CRITICAL**: 0 · **HIGH**: 0 · **MED**: 2 · **LOW**: 3

Both MED findings are fixed, not carried. Neither touches a requirement or an acceptance criterion, so
neither reopens the cycle at an earlier stage (SDD-25): A1 is a number in the plan, A2 is the fidelity
of the preview's control state — the proposal's own numbers did not move.

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T003 | the layer covers the dialog; the height does not change |
| FR-002 | ✅ | ✅ T003 | the form beneath is inert (`elementFromPoint`) |
| FR-003 | ✅ | ✅ T004 | the card's box: width, padding, radius, fill, shadow |
| FR-004 | ✅ | ✅ T004 | the type scale and the right-aligned actions row |
| FR-005 | ✅ | ✅ T003 | the scrim's radius; `hidden` still hides the layer |
| FR-006 | ✅ | ✅ T010 | the answers stay the editor's buttons; the copy still navigates |
| SC-001 | ✅ | ✅ T003 | height equality to a tenth of a pixel |
| SC-002 | ✅ | ✅ T003 | layer rect = dialog rect; the hit test names the confirmation |
| SC-003 | ✅ | ✅ T004 | the preview's card numbers on the shipped page |
| SC-004 | ✅ | ✅ T004 | the answers' right edge and their 8px gap |
| US1/AC1–AC4 | ✅ | ✅ T003, T006–T008 | the four scenarios |
| US2/AC1–AC3 | ✅ | ✅ T004, T009, T012 | card, type, dark theme |
| Edge: narrow dialog | ✅ | ✅ T013 | `inspection` |
| Edge: generate unchanged | ✅ | ✅ T011 | `inspection` by test, D001 by diff |

**Coverage**: 10/10 requirement ids, 0 untraced.

## History

- **2026-11-21** — first run, base `245399fe`. 0 CRITICAL, 0 HIGH, 2 MED (both fixed), 3 LOW (accepted).
  Gate 2 may open.
