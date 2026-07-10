# Tasks: SONGS-BM — Song bookmarks (setlists)

Spec: [`spec.md`](spec.md) (`SONGS-BM`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **SONGS-BM-T1 — Document bookmark API + OBS activate EARS**
  - Touch: this folder
  - Verify: Align with bookmarks pytest + OBS bookmark storage tests
  - Covers: `SONGS-BM-AC1`–`AC16`

- [ ] **SONGS-BM-T2 — Keep bookmark API tests green**
  - Touch: `multimedia/bookmarks/tests/test_api.py`
  - Verify: `pytest multimedia/bookmarks/tests/test_api.py`
  - Covers: `SONGS-BM-AC2`–`AC12`

## Done when

- Spec matches as-built bookmarks; API tests remain the proof.
