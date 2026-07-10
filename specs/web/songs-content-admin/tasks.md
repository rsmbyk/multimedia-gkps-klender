# Tasks: WEB-SONGS — Songs content admin (web)

Spec: [`spec.md`](spec.md) (`WEB-SONGS`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **WEB-SONGS-T1 — Document web songs admin EARS**
  - Touch: this folder
  - Verify: Align with web songs JS + Vitest path/chunk tests
  - Covers: `WEB-SONGS-AC1`–`AC10`

- [ ] **WEB-SONGS-T2 — Keep web Vitest contracts green**
  - Touch: `multimedia/web/static/web/**/*.test.js`
  - Verify: `npm test -- api-paths lyric-chunks`
  - Covers: `WEB-SONGS-AC4`–`AC6`, `WEB-SONGS-AC10`

## Done when

- Spec matches as-built web songs admin; Vitest contracts remain the proof.
