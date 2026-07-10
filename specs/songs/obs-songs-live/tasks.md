# Tasks: OBS-SONGS — OBS Songs dock and source

Spec: [`spec.md`](spec.md) (`OBS-SONGS`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **OBS-SONGS-T1 — Document Songs OBS EARS**
  - Touch: this folder
  - Verify: Align with dock/source JS + Vitest
  - Covers: `OBS-SONGS-AC1`–`AC20`

- [ ] **OBS-SONGS-T2 — Keep Songs OBS Vitest green**
  - Touch: `multimedia/obs/static/obs/songs/**/*.test.js`
  - Verify: `npm test -- songs`
  - Covers: `OBS-SONGS-AC2`, `AC10`–`AC12` (partial)

## Done when

- Spec matches as-built Songs OBS; existing Vitest remains the automated proof.
