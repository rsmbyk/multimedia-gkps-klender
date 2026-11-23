# Analysis: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md`
**Plan**: `specs/233-song-sort-retained/plan.md`
**Tasks**: `specs/233-song-sort-retained/tasks.md`

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | drift risk | `plan.md` | The one-line implementation is already present uncommitted in the worktree because the change was proved from a live preview before gate 1 | recorded in the spec's reproduction table; no rewritten evidence, no gate bypass |
| A2 | LOW | naming | `spec.md` | Card ITEM-247 is reserved but not yet opened; the owner accepted the spec directly rather than promoting a card | T009 opens it in Speccing in this slice's PR; no intent change |
| A3 | INFO | scope | `spec.md` | Browser persistence across a full reload was offered and not chosen | recorded as an assumption, not an open question |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ T002, T008 | re-sort after reconciliation |
| FR-002 | ✅ | ✅ T002 | button and rows agree |
| FR-003 | ✅ | ✅ T003 | default `m` unchanged |
| FR-004 | ✅ | ✅ T007 + inspection | non-song lists and hymn books |
| SC-001 | ✅ | ✅ T002 | base fails `['Beta','Zebra','Alpha']` |
| SC-002 | ✅ | ✅ T004–T006 | three refresh paths |
| SC-003 | ✅ | ✅ T007 | other sections, default order |
| US1/AC1 | ✅ | ✅ T002 | |
| US1/AC2 | ✅ | ✅ T003 | |
| US1/AC3 | ✅ | ✅ T002 | no reload |
| US2/AC1 | ✅ | ✅ T004 | |
| US2/AC2 | ✅ | ✅ T005 | |
| US2/AC3 | ✅ | ✅ T006 | |
| US2/AC4 | ✅ | inspection | T007, US3/AC1 inspection |
| US3/AC1 | ✅ | inspection | `songRowEls()` filters `.songrow` |
| US3/AC2 | ✅ | ✅ T007 | fresh load default |

**Coverage**: 100% (16/16) · **CRITICAL**: 0 · **HIGH/MED/LOW**: 0/0/2

## Applied mechanically

- Aligned the traceability split with the task table: 13 `test` rows and 3 `inspection` rows; no
  `manual` rows were declared.
- Checked requirement IDs FR-001–004 and SC-001–003 against both the spec and the plan; no orphans.
- Confirmed the preview tier matches the change: a fetch-driven in-place refresh cannot be shown by
  a static page, so the live route is named.

## Escalated

No intent-changing findings; the single ambiguity was resolved at Specify through the question
tool (retain after every in-place refresh), with the losing alternatives recorded in the spec.

## Artifact SHAs read

- `spec.md` `9b0fc682284a87662db6ad74ea4c856911562ca874a99fac73c85860bfc36737`
- `plan.md` `01729ec56f8f8c11ec38300951490f215eb4021449f8a561bf6cef8334548e0a`
- `tasks.md` `a56e61d99e26f95fab29829eda5c836180fceb60a4465beade6ce37259dc4971`
- `research.md` `39c78cf73899d8b11378b4cee869b99538e9f79be3a1cec11d6365c1e0645c6d`
- `data-model.md` `f426ac07d25050e509ed13286079c6f2d32c5dc7c696c7aeb3ca22cccd1579c7`
- `quickstart.md` `67e67350dc4eff31ea8234f73c31e93726fb275a54732e8a7cab7ca3e2579829`
- `contracts/README.md` `dca001e532770fcf38bc42837662fe03fdb0c85cb531f70ba9c6464841a38cb0`
- `checklists/requirements.md` `76e83b4cfb7739cfcbda251e75c46b3e6fd8a7917f1c7351e711b3a4fd15f6e2`
- `preview/README.md` `5aceb0f8b0a44ee73d1fd8b4144e9f03951db5bb0921b3e438c3d23928eceb16`

## History

- 2026-11-23 — first analysis: zero CRITICAL, 100% coverage, two LOW records (live-preview edit
  already in the tree; card to be opened during Implement).
