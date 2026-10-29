# Convergence: dismissing the file picker leaves the New media dialog open

**Spec**: `specs/163-media-dialog-file-picker-cancel/spec.md`
**Passes run**: 2

## Pass 1 — 2026-10-29

**What was checked**: all 21 rows of `plan.md`'s traceability table, each by the method it declared.
`test` rows against `tests/e2e/test_media_library.py` (the four new cases, then the module in full);
`inspection` rows against the diff of `static/web/media-entry.js` and the code paths the plan names;
the `manual` row against the probe run on the live route.

| Row | Declared | Result |
| --- | --- | --- |
| FR-001 · FR-002 · FR-003 · SC-001 · SC-002 · SC-003 · SC-004 · US1 AC1…AC4 · US2 AC1 · edge "same file re-picked" | `test` | **green** — the four cases, `Ran 4 tests … OK` before the module run; module `Ran 42 tests`, one failure, the pre-existing `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` (19.7 ≠ 12, ITEM-156). No case that is green on `develop` turns red here (SC-004 as settled at gate 2). |
| FR-004 · US2 AC2 · US2 AC3 · edges "mid-inspect", "the error dialog is open", "reduced motion", "reopened afterwards" | `inspection` | **checked by inspection** — the diff adds one guard to the dialog's `cancel` listener and nothing else; `#mediaErrorDialog` is a sibling (`base.html:454`), the other editor kinds have no file input, the wrapped `close()` and its `prefers-reduced-motion` branch sit above the guard and are untouched. |
| Live: the real system picker, dismissed by hand | `manual` | **partial** — the replayed dismissal was checked live on `http://localhost:8814/tatib/149/` (`preview/picker_probe.py` → `OK`, dialog, title and chosen file all survive; Escape still closes). The real system picker is the owner's own check (`T015`), still open. |

**Findings**

| # | Type | Finding | Evidence |
| --- | --- | --- | --- |
| C1 | `missing` | none | every row has its declared evidence |
| C2 | `partial` | the `manual` row's second half — a person dismissing the real picker | the probe covers the event path; the native dialog cannot be driven by any automation |
| C3 | `contradicts` | none | the code states the same rule the spec does: a `cancel` closes the dialog only when it targets the dialog |
| C4 | `unrequested` | none | the diff adds a guard and four cases; no surface, endpoint or copy was touched |

**Outcome**: converged. SC-004 read as *no case that is green on `develop` turns red here*, per the
gate-2 answer; the one `partial` row is a manual check the owner owns, recorded here rather than claimed.

## Pass 2 — 2026-10-29, after the rebase

**Why**: `origin/develop` moved 19 commits while this slice ran, to `f8e0bb81`. The branch was rebased onto
it before delivery: `VERSION` was already `1.23.0` (so the bump became `1.23.1`), `reading/R28…R31` had
been taken by four other slices (so this slice's requirement is **R32**), and the board had reached
`ITEM-175` (so the card is **ITEM-176**).

**Checked again**: the same 21 rows, against the rebased tree.

| Row group | Result |
| --- | --- |
| the four `test` cases | **green** — `Ran 4 tests … OK` in 10.2s on the new base |
| the module (SC-004) | **46 tests, one failure** — `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen` (19.75 ≠ 12), the same ITEM-156 red the module carried before the rebase; no case green on `develop` turned red |
| the live row | **checked** — `preview/picker_probe.py` on `http://localhost:8814/tatib/149/` returned `OK` again with the rebased code served (collectstatic re-run, server restarted) |
| `inspection` rows | **checked by inspection** — the guard is still the only code change in `media-entry.js`; the rebase added none |

**Outcome**: converged on the new base. The identifiers moved (R28 → R32, ITEM-168 → ITEM-176,
1.22.12 → 1.23.1); no requirement, task or piece of evidence did.
