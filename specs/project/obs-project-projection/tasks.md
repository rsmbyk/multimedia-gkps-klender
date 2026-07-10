# Tasks: OBS-PROJECT — Combined OBS project projection

Spec: [`spec.md`](spec.md) (`OBS-PROJECT`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **OBS-PROJECT-T1 — Document project OBS EARS**
  - Touch: this folder
  - Verify: Align with project source/settings JS + Vitest
  - Covers: `OBS-PROJECT-AC1`–`AC11`

- [ ] **OBS-PROJECT-T2 — Keep project Vitest green**
  - Touch: `multimedia/obs/static/obs/project/**/*.test.js`
  - Verify: `npm test -- project`
  - Covers: `OBS-PROJECT-AC3`, `AC11` (partial)

## Done when

- Spec matches as-built project projection; Vitest remains the automated proof.
