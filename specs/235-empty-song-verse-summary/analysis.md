# Analysis: An empty song names itself in the Verses section

**Date**: 2026-11-24
**Artifacts read** (sha256, first 12): `spec.md` 69aa8fdc8303 · `plan.md` a013a2c3a75f ·
`research.md` 6f0f31206406 · `data-model.md` 3e95f93efd90 · `checklists/requirements.md` 791606764684 ·
`tasks.md` d6882eb35aa8 · `contracts/none.md` 8c6652e19ac1 · `preview/index.html` 1e7d124689da.

**Metrics**: 6 FR · 3 SC · 2 stories (9 scenarios) · 3 assumptions · 0 `[NEEDS CLARIFICATION]` ·
9 `test` / 2 `inspection` / 0 `manual` rows · 15 tasks · 0 CRITICAL · 2 HIGH · 1 MEDIUM · 0 LOW.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A1 | HIGH | `spec.md` calls the no-song state "unchanged" but gives no measurement in its own text; the number lives only in `preview/index.html`'s readout and in SDD-06's UI/UX section. | accepted — the accepted preview is the artifact that carries the 0px number, and `## UI/UX` in the spec repeats it; no intent change needed. |
| A2 | HIGH | FR-004 bundles "no stale value from the previous song" with "picker unchanged"; a single failing E2E could be blamed on either half. | accepted — T009 names the swap explicitly and T010 pins the unchanged picker; the traceability table splits them into two rows. |
| A3 | MEDIUM | `data-empty="true"` is derived from `boxes.length` in the script but from `form.song_has_no_verses` on the server. A failed verse fetch can leave zero boxes without the flag. | accepted — the edge case is stated in `data-model.md` (the empty line must not be mistaken for a successful empty result) and the fetch-failure notice is unchanged; no new task. |
| A4 | LOW | The preview's collapsed-state CSS disables the 200ms transition so a static measurement reads 0px; that line is not shipped. | mechanical — already labelled preview-only in `preview/template.html` and `preview/README.md`; not a product rule. |

## Mechanical check pass

- Every FR and SC appears in the plan's traceability table: 9/9 requirement rows, 100%.
- Every story scenario maps to an FR or an assumption: 9/9.
- Terminology is consistent: "the section" means label + panel; "the body rows" means helper row,
  tiles and readout; no drift against `docs/GLOSSARY.md`.
- Paths in `plan.md` exist in the worktree; no stale test names (`test_saved_render_parity` is not used).
- The checklist is generated and unticked; no agent tick appears.

## Gate check

CRITICAL 0, coverage 100% — gate 2 may open. HIGH findings A1/A2 are reported with their
disposition and need no code change; A3 is an accepted edge, not a gap.

## History

- 2026-11-24 — first pass against the hashes above; no re-run yet.
