# Tasks: OBS-BIBLE — OBS Bible dock and source

Spec: [`spec.md`](spec.md) (`OBS-BIBLE`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **OBS-BIBLE-T1 — Document Bible OBS EARS**
  - Touch: this folder
  - Verify: Align with bible dock/source JS + Vitest
  - Covers: `OBS-BIBLE-AC1`–`AC17`

- [ ] **OBS-BIBLE-T2 — Keep Bible OBS Vitest green**
  - Touch: `multimedia/obs/static/obs/bible/**/*.test.js`
  - Verify: `npm test -- bible`
  - Covers: `OBS-BIBLE-AC2`, `AC10`, `AC8` (partial)

## Done when

- Spec matches as-built Bible OBS; Vitest remains the automated proof.
