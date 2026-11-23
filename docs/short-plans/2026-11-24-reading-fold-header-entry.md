# Short plan: restore the spec 235 entry in the reading capability header

**Branch**: `docs/reading-fold-header-entry` (docs-only, no spec number)
**Created**: 2026-11-24
**Owner approval**: "open a docs-only fix slice for the header", 2026-11-24, after the merge defect was reported
**Bump**: `none` — internal documentation; VER-05 says no VERSION change and no changelog entry
**Preview**: `n/a — docs-only, the artifact is the capability file itself`
**Plan / Research / Data-model / Contracts / quickstart**: `n/a — docs-only short plan`

## Demand

PR #612 squash-merged spec 235 as `fead48b3`, but resolving the header conflict against spec 234
rebuilt the `**slices**` line from develop's copy and dropped `235-empty-song-verse-summary`.
The R30 and R48 folds are correct on develop; only the header's slice list is wrong.
`docs/PROCESS.md` SDD-23 requires the header to prepend the slice ID at Fold.

## Scope

One line in `docs/spec/reading.md`: prepend `235-empty-song-verse-summary` to the `**slices**`
list, ahead of `234-open-created-template`. No other file, no behaviour, no card, no version.

## Checklist (reviewer-owned, never ticked by the agent)

- [ ] CHK001 Is the missing entry identified by its exact slice ID and its source PR? [Traceability, §Demand]
- [ ] CHK002 Is the change confined to the header line, with the R30/R48 bodies untouched? [Scope, §Scope]
- [ ] CHK003 Does `bump: none` follow VER-05 for internal docs? [Consistency, header]

## Tasks (≤6)

- [X] T001 Branch `docs/reading-fold-header-entry` off `fead48b3` (`origin/develop` after the merge); spec 236 and ITEM-251 found already claimed, so the docs-only path is used.
- [X] T002 Prepend `235-empty-song-verse-summary` to the `**slices**` line in `docs/spec/reading.md`.
- [X] T003 Verify by inspection: the line contains 235 then 234, the rest of the list is byte-identical to develop, and no other file changed.
- [ ] T004 Report and ask before pushing; no push without the owner's word.

## Verification split

0 test · 1 inspection · 0 manual. No tests are relevant to a one-line documentation header.

## Verification

`git diff --numstat origin/develop -- docs/spec/reading.md` → `1 1`: exactly one line changed, the header slices list now reads 235 then 234 with the remainder byte-identical. VERSION and CHANGELOG untouched (bump: none, VER-05). No tests apply to a docs-only header.
