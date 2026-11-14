# Fold: Match the Tata Ibadah date header to the songbook header

**Capability**: `n/a — this repo has no docs/spec/ capability tree (owner decision at gate 2, 2026-10-24);
starting the tree is its own slice, not a header fix`
**Folded at**: 2026-10-24

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| none | — | no capability tree to apply a delta to; the behaviour lives in `specs/123-tatib-date-header-parity/spec.md` and in `CHANGELOG.md` under `[Unreleased]` |

## Drift guard

- **Files changed in this capability**: `static/styles/design/components.css`,
  `tests/e2e/test_reading.py`
- **Declared no behaviour change**: no — the changes are FR-001…FR-003 themselves
- **Guard result**: `n/a — the guard compares changed files against tree deltas, and there is no tree. When
  the tree is created, this slice's behaviour enters it as the initial `reading header` requirements.`
