# Tasks: DEPLOY-VERCEL — Vercel production hosting

Spec: [`spec.md`](spec.md) (`DEPLOY-VERCEL`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **DEPLOY-VERCEL-T1 — Document production EARS from deploy runbook**
  - Touch: this folder
  - Verify: Align with `docs/DEPLOY.md` + `vercel.json`
  - Covers: `DEPLOY-VERCEL-AC1`–`AC7`

- [ ] **DEPLOY-VERCEL-T2 — Treat vercel.json changes as high-risk**
  - Touch: `vercel.json`, `multimedia/wsgi.py`
  - Verify: Any change has explicit tested plan / rollback
  - Covers: `DEPLOY-VERCEL-AC2`–`AC3`

## Done when

- Spec matches production runbook; agents link here before deploy edits.
