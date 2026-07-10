# Tasks: OBS-TATIB — OBS Tatib dock and source

Spec: [`spec.md`](spec.md) (`OBS-TATIB`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **OBS-TATIB-T1 — Document Tatib OBS EARS**
  - Touch: this folder
  - Verify: Align with tatib dock/source JS + Vitest
  - Covers: `OBS-TATIB-AC1`–`AC17`

- [ ] **OBS-TATIB-T2 — Keep Tatib OBS Vitest green**
  - Touch: `multimedia/obs/static/obs/tatib/**/*.test.js`
  - Verify: `npm test -- tatib`
  - Covers: `OBS-TATIB-AC2`, `AC13` (partial)

## Done when

- Spec matches as-built Tatib OBS; Vitest remains the automated proof.
