# Analysis — remove the offline library; the projector fetches on selection

**Date**: 2026-10-26 · **Slice**: `specs/136-remove-offline-library`
**Artifacts read** (sha256, first 12):

| Artifact | SHA |
| --- | --- |
| `spec.md` | `f7d5e265facb` |
| `plan.md` | `d9271bc008d4` |
| `tasks.md` | `ae474e2cfd35` |
| `research.md` | `05e2b8f625e0` |
| `data-model.md` | `c9f4d0229532` |
| `contracts/projector-goto.md` | `04139c54103d` |
| `quickstart.md` | `14944706f448` |
| `checklists/requirements.md` | `3cc14e4021ef` |

**Metrics**: 12 `FR` · 7 `SC` · 29 story scenarios · 8 edge cases · 40 tasks · requirement coverage
**12/12** · success-criterion coverage **7/7** · verification **41 test · 2 inspection · 2 manual** ·
unknowns **0**.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | HIGH | FR-002 ("the browser SHALL hold no library copy") had no scenario for a browser that already holds one, yet the cleanup is the only way the requirement becomes true for a returning user. | **Fixed (mechanical)** — task `T039` added, seeding the old database and worker and asserting their removal. The requirement's wording already covers it; the spec is unchanged. |
| A2 | HIGH | `JsonResponse` serialises with `json.dumps`' default separators, which would put the index ~30% over `SC-005`'s byte budget even though the compact measurement passes. | **Fixed (mechanical)** — the plan's server design now pins `separators=(',', ':')`; `T015` inherits it, and `T014`'s size test measures the serialised response, not the dict. |
| A3 | MEDIUM | `FR-012`'s row in the traceability table named a test no task wrote. | **Fixed (mechanical)** — task `T040` added for `test_an_empty_service_shows_its_empty_state`. |
| A4 | MEDIUM | FR-008 ("the matcher keeps its rules") is verified by inspection only; the parity test (`T029`) compares rows, not the rule identity. A future edit could keep the rows while quietly changing a ladder. | **Accepted** — the code is not edited; the inspection is `projector-library.js`'s `lookup()` body compared before and after, which is stronger evidence for "unchanged" than any assertion about outcomes. |
| A5 | LOW | US3.3 (the panel closes and the page regains focus) rests on a `manual` check; there is no automated focus assertion. | **Accepted** — the focus path is the existing `closeFind()`, untouched, and the preview cannot show it. Cost of leaving it: one manual step at Converge. |
| A6 | LOW | The previews pose the loading states; they cannot fetch, so the lock's behaviour is not visible in them. | **Accepted** — stated in `preview/README.md`; the behavioural evidence is the E2E set in `T022`/`T026`. |
| A7 | LOW | `docs/PRODUCT.md` was assumed to carry an offline promise; it does not (grepped 2026-10-26). | **Fixed (mechanical)** — `T031` now says so instead of implying an edit. |

No CRITICAL findings. No requirement lacks a task; no task exists without a requirement row.

## History

- **2026-10-26** — first run, before gate 2: 4 mechanical fixes (A1, A2, A3, A7), 3 accepted (A4, A5,
  A6), 0 CRITICAL, coverage 12/12 FR and 7/7 SC.
