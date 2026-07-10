# Tasks: API-SEARCH — Song lyric search API

Spec: [`spec.md`](spec.md) (`API-SEARCH`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **API-SEARCH-T1 — Document search API EARS**
  - Touch: this folder
  - Verify: Align with `multimedia/api/tests/test_search.py`
  - Covers: `API-SEARCH-AC1`–`AC6`

- [ ] **API-SEARCH-T2 — Keep pytest green on search**
  - Touch: `multimedia/api/tests/test_search.py`
  - Verify: `pytest multimedia/api/tests/test_search.py` (Postgres)
  - Covers: `API-SEARCH-AC2`–`AC5`

## Done when

- Spec matches as-built search; Postgres tests remain the proof.
