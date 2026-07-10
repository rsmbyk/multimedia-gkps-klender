# Tasks: DEPLOY-LOCAL — Local Docker Compose runtime

Spec: [`spec.md`](spec.md) (`DEPLOY-LOCAL`) · Plan: [`plan.md`](plan.md)

## Checklist

- [x] **DEPLOY-LOCAL-T1 — Document local Compose EARS**
  - Touch: this folder
  - Verify: Align with README + `docker-compose.yml` + `.env.example`
  - Covers: `DEPLOY-LOCAL-AC1`–`AC6`

- [ ] **DEPLOY-LOCAL-T2 — Manual smoke (optional)**
  - Touch: Compose stack
  - Verify: `docker compose up` → http://127.0.0.1:8000/
  - Covers: `DEPLOY-LOCAL-AC4`

## Done when

- Spec matches as-built local runtime docs.
