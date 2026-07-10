# Plan: DEPLOY-VERCEL — Vercel production hosting

Spec: [`spec.md`](spec.md) (`DEPLOY-VERCEL`)

## Approach

Capture as-built production constraints from `docs/DEPLOY.md` into a numbered
spec so agents treat routing/env rules as acceptance criteria, not folklore.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Config | `vercel.json`, `.python-version` |
| Entry | `multimedia/wsgi.py` (`app`) |
| Settings | `multimedia/settings.py` (`VERCEL` branches) |
| Docs | `docs/DEPLOY.md` |

## Contracts

- Legacy builds + catch-all routes → WSGI `app`.
- Env and WhiteNoise behavior per deploy doc.

## Risks and rollout

- Changing `vercel.json` can take production down with opaque 404s — require
  tested plan.

## Non-goals

- Hosting migration; Docker production.
