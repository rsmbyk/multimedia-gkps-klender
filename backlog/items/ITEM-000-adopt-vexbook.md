---
id: ITEM-000
status: in-review
title: Adopt vexbook process at v0.4.0
type: chore
priority: P0
effort: M
created: 2026-09-30
updated: 2026-09-30
spec:
branch: chore/readopt-vexbook-v0.4.0
pr: 256
archived_at:
archive_reason:
bump: none
release_version:
---

# ITEM-000: Adopt vexbook process at v0.4.0

## Summary

Adopt the vexbook process into this existing repository, following
[`docs/ADOPT.md`](../../docs/ADOPT.md). This is the first-time adopt: copy the
process file set from vexbook `v0.4.0`, write one thin adoption ADR, create the
ITEM board and reusable stubs, and wire the agent rules to the binding docs.

Docs-only. `bump: none` — no product behavior or shipped version changes.
Per ADOPT, the adopt itself is not a numbered spec; the first behavior change
after adopt goes through SDD.

## Notes

- Source: vexbook `v0.4.0`.
- The process file set is copied verbatim (PROCESS, KICKOFF, ADOPT, SDD-GATE,
  reusable `_template`s, PR template).
- `VERSION` is bootstrapped to `0.4.6` (latest tag reachable from `main`);
  confirm or adjust.
- Git model recorded as Git Flow and locked with merge rules in ADR 0002
  (features squash-merge to `develop`; releases/hotfixes merge-commit to `main`;
  remote branch deleted after merge, local kept).
- Product `CHANGELOG.md` format conversion is out of scope (flagged in ADR 0001).

## Acceptance sketch

- Process file set present and identical to vexbook `v0.4.0`.
- Adoption ADR 0001 exists at the next free number.
- `docs/PROCESS.md`, `docs/KICKOFF.md`, and `docs/rules/SDD-GATE.md` are binding.
- ITEM board, reusable stubs, and `specs/` index exist.
- `AGENTS.md` references every must-apply shared doc.

## Links

- Spec: — (docs-only adopt per ADOPT)
- Related items:
