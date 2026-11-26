# Analysis: picker popout scrollbar edge

**Date**: 2026-11-26
**Spec**: `specs/244-picker-menu-scrollbar-edge/spec.md`

## Artifacts read (SHA-256 at this run)

| Artifact | SHA-256 |
| --- | --- |
| `spec.md` | `d06650626160b681146df056388522db758da4d717d2beaab1b46a4dfd162475` |
| `plan.md` | `0ac59baf2da612209c68e3a649ca107967b310e9c047400e30ffbc5719b9b6ec` |
| `research.md` | `2b7f8dcb4bf9727581834daf18b0bd5feae1a606d0208525c7521edad6f59272` |
| `data-model.md` | `aecdd5e6704dbfbf47d34d8abc40da273929beaf8400c56f7cc88c70d0b90636` |
| `quickstart.md` | `62377756bf3ea70bf79939a10db32e90481ec2b33d7eebeddcdd4e0f12d443b5` |
| `tasks.md` | `026d6c7bff32147864005209af23f20e5b51956253a640d5361823aeef819d2d` |
| `checklists/requirements.md` | `db5e729467f03ce7f5191cdb49f9e09ba7c1f3c6b9eb837c72bc5f5f408ebd0f` |
| `checklists/checklist.md` | `230fa2980705651ea1692d5e221128b5d93fe374ef58d4da53a21932489a2206` |
| `contracts/README.md` | `1e5b87bf6ac24c946d091a95bb16bc87339c408a7e5bea2bf8682071e2125261` |
| `preview/README.md` | `9d3f8dba530320bd02729c9d35b012c1c61286296c552152af1a79b2845daf3a` |
| `preview/measure.py` | `f524a3660bf91f0f5a82fdb93c4bbbd9711e0414b1b3dd989f4f2ff8e26924aa` |
| `preview/edges.py` | `e70076ac6538f74c8b86fec68cb9bf2fb781faf503a86c890648dbae6a3ea6f9` |

## Metrics

- 7 FR · 4 SC · 8 acceptance scenarios · 19 traceability rows · 16 tasks.
- Verification split: 14 `test` · 5 `inspection` · 0 `manual`; coverage 19/19 traceability rows
  (100%), each assigned to at least one task.
- Every `test` row has a red and a green task in `tasks.md` except the two rows backed by the
  already-accepted spec 238 modules (FR-005, SC-004, US2/AC4), which are regression confirmations at
  the push step rather than new behaviour.
- Zero `[NEEDS CLARIFICATION]` markers; zero CRITICAL findings.

## Mechanical fixes applied before this run

- The gate-1 probes were first kept in a scratch directory that prunes after 24h; both were copied
  to `preview/measure.py` and `preview/edges.py`, and their paths in `quickstart.md` and
  `preview/README.md` were updated. `edges.py` was corrected to use its `page` argument and to
  measure the literal one-option Obaja menu rather than a filter that still matched 14 chapters.
- `spec.md` §UI/UX gained the measured one-option numbers (`scrollHeight == clientHeight == 42`,
  0px gutter) so the state is stated as a number, not an adjective. No requirement, scenario or
  boundary changed.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| H1 | HIGH | Five inspection rows (FR-002, FR-004, FR-007, US1/AC3, US1/AC4) rest on computed styles and the live preview rather than a painted-pixel assertion. The bar has no DOM node; geometry proves the scrollport's position, not the thumb's colour or corner clip. | Accepted for gate 2 with the cost stated: a future engine could change pseudo-element painting without CI noticing. Converge checks each computed value and the live corner; no extra test task is added because no DOM observable exists. |
| H2 | HIGH | The dark-theme and flipped-menu states are declared reachable but not independently measured; the frozen numbers come from the light, downward menu at 1440×900. | Verify in Converge via `preview/README.md` steps and record the readings in `converge.md`. The rule is on a shared selector, so the same 1px relationship is structural; leaving it unmeasured costs one visual check, not a behaviour risk. |
| L1 | LOW | `quickstart.md` still names `<throwaway>` for the test database instead of a fixed name. | Intentional: a hard-coded name could be locked by a parallel session. Chosen at run time; no fix. |
| L2 | LOW | The scope excludes other dropdown surfaces (OBS dock find, media chooser, date popover), which may have their own inset bars. | Owner-limited scope from Clarify; recorded as an assumption. A later card can cover those surfaces. |

## History

- 2026-11-26 — first run: 0 CRITICAL, 2 HIGH, 2 LOW; 19/19 rows covered; two mechanical fixes above
  applied and re-read before this report.
