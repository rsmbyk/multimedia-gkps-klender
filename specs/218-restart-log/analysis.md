# Analysis: a dead companion says why

**Slice**: `specs/218-restart-log` · **Run**: 2026-11-21

## Metrics

`FR: 6/6 with tasks · scenarios: 5/5 with a verification row · coverage: 100% · markers: 0 ·
findings: 0 CRITICAL, 0 HIGH, 1 MEDIUM`

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A-01 | MEDIUM | FR-003 has no test of its own: the empty-log case is covered by `test_a_companion_that_is_not_running_is_reported`, whose stub happens to answer no log, so the assertion is indirect. | **Accepted.** The behaviour is that no blank `gkps: its last line: ` appears; the launcher test for `R5` already asserts the message set, and adding a fourth near-identical test for a blank line would be the kind of structure-only test TDD-05 warns about. |

## History

- 2026-11-21 — single run: 0 CRITICAL, 100% coverage.