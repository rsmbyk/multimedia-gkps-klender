# Analysis: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md`
**Plan**: `specs/254-entity-versioning/plan.md`
**Tasks**: `specs/254-entity-versioning/tasks.md`

## Artifact SHAs

| Artifact | SHA-256 |
| --- | --- |
| `spec.md` | `522074c645df55af74594a937eee57e9b376c01abc585c3ceccb4bd55eae1fbf` |
| `plan.md` | `70685b02b9e40bdc25f539029e0422cd23bf4a5e48dfa9d8c0d2e4adaded791a` |
| `tasks.md` | `fba9737ff4c6a99cd111e5b0a5cbc0a672a6edbcec5abab0221acc5f35e83285` |
| `research.md` | `a8d55d5253eda442b320cddb86b4039883698f0cb9bd93e3cb317766070a369e` |
| `data-model.md` | `5b99981faca135ac0cd6867b8e38f162c3191fe6be5da71d17f52b35b5647e22` |

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | HIGH | design | `research.md` D004 | A widely used song bumps many service rows in one write; the locks are taken in primary-key order and only active referencing services are touched | accepted in the plan; no requirement change |
| A2 | MED | coverage | `tasks.md` | Generated rows inside template copy have no submitted field values, so no-op detection there is the row-copy shape rather than a form diff | covered by FR-015 inspection and the generate/copy wiring in T009 |
| A3 | LOW | preview | `preview/README.md` | The static page cannot show server-rendered context or make the delete POST | recorded as a preview limitation; E2E covers the live behaviour |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 3

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | |
| FR-002 | ✅ | ✅ | |
| FR-003 | ✅ | ✅ | |
| FR-004 | ✅ | ✅ | |
| FR-005 | ✅ | ✅ | |
| FR-006 | ✅ | ✅ | |
| FR-007 | ✅ | ✅ | |
| FR-008 | ✅ | ✅ | |
| FR-009 | ✅ | ✅ | |
| FR-010 | ✅ | ✅ | |
| FR-011 | ✅ | ✅ | |
| FR-012 | ✅ | ✅ | |
| FR-013 | ✅ | ✅ | |
| FR-014 | ✅ | ✅ | |
| FR-015 | ✅ | ✅ | |
| SC-001 | ✅ | ✅ | |
| SC-002 | ✅ | ✅ | |
| SC-003 | ✅ | ✅ | |
| SC-004 | ✅ | ✅ | |
| SC-005 | ✅ | ✅ | |
| SC-006 | ✅ | ✅ | |

**Verification split**: 27 test · 2 inspection · 0 manual

## Applied mechanically

- Renumbered the five cards from ITEM-269–273 to ITEM-271–275 after `origin/develop` claimed the earlier IDs; updated the card links, board rows and spec cross-references.
- Added FR-009, FR-004 and SC-006 to the task list so every requirement is named in both plan and tasks.
- Replaced the earlier `white-space: nowrap` preview candidate with the measured 560px confirmation width.

## Escalated

- None. The single genuine scope decision — including `TataIbadahItem` in the tracked set — was made by the owner during Specify.

## History

- 2026-11-28 — first analysis; zero CRITICAL, full requirement coverage, three non-blocking findings.
