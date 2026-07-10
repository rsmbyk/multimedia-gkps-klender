# Tasks: API-SONGS — Songs content REST API

Spec: [`spec.md`](spec.md) (`API-SONGS`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **API-SONGS-T1 — Document songs API EARS from as-built tests**
  - Touch: this folder
  - Verify: Criteria align with `multimedia/songs/tests/test_api.py`
  - Covers: `API-SONGS-AC1`–`AC14`

- [ ] **API-SONGS-T2 — Keep pytest green on songs API**
  - Touch: `multimedia/songs/tests/test_api.py`
  - Verify: `pytest multimedia/songs/tests/test_api.py`
  - Covers: `API-SONGS-AC2`–`AC14`

## Done when

- Spec matches as-built API; tests remain the living proof.
