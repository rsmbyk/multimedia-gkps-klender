---
id: ITEM-135
status: in-progress
title: 'Carry the 2026-10-25 grammar vintage into the process page'
type: chore
priority: P2
effort: S
created: 2026-10-25
updated: 2026-10-25
spec:
branch: docs/process-vintage-2026-10-25
pr:
issue: https://github.com/rsmbyk/multimedia-gkps-klender/issues/388
closed_at:
closed_reason:
bump: none
release_version:
---

# ITEM-135: Carry the 2026-10-25 grammar vintage into the process page

## Summary

`docs/PROCESS.md` was generated at vintage 2026-10-24 and has drifted from the grammar behind it:
one rule is missing, nine were reworded by the parent/tip split, and the page carries none of the
operative detail under its rules. This slice regenerates it at vintage 2026-10-25 and leaves the
`repo:` blocks byte-identical.

## Notes

- **Missing:** `VER-10` maps the level to what changed — breaking is `major`, a new capability
  `minor`, a fix `patch`.
- **Reworded by the split:** `SDD-12`, `GIT-01`, `GIT-04`, `GIT-05`, `VER-02`, `VER-04`, `BRD-08`,
  `BRD-09`, `BRD-10` — the generic wording now sits on the parent (`receiving branch`, `the
  integration branch`, `a board word`) and the model-specific reading on the tip.
- **Detail restored:** six rules had indented detail lines in the grammar that the first generation
  dropped. The page held the rule's name and none of its numbers, prohibitions or file names.
- **Grammar defect fixed first:** the 2026-10-25 rename of the seam directory to
  `vexbook-contracts/` was applied by substring and also rewrote the *slice's* own `contracts/`
  folder in `SDD-12`, the `SK:plan` anchor and the plan template. Corrected in the grammar before
  this regeneration; without it the page would have taught `specs/NNN/vexbook-contracts/`.
- No `VERSION` change and no changelog line: documentation only, `bump: none`.

## Acceptance sketch

- `verify_process.py` against the branch: 77/77 rule IDs, verbatim text, vintage 2026-10-25,
  balanced `repo:` markers, `AGENTS.md` clean, templates matching the grammar — exit 0.
- The five `repo:` blocks are byte-identical to the previous commit.
- `AGENTS.md` still states what the repository uses and holds no rule text or rule IDs.
- ADR 0006 names the same vintage as the page.

## Links

- Spec: —
- Related items: ITEM-130 (the page was first generated at vintage 2026-10-24)
