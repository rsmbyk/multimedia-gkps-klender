# Fold: reopening the projector window

**Slice**: `specs/141-projector-window-reopen`
**Capability touched**: `reading`
**Folded**: 2026-10-27

## Operations

| Operation | Requirement | Note |
| --- | --- | --- |
| modified | `reading/R14` | the phone's sentence now says "Neither the Project control nor the projector-window control SHALL be drawn", and the rest of R14 is carried verbatim |
| added | `reading/R16` | the reopen act, the control's box and name, its states, the no-write rule, and the wrap inside a narrow pane, with four scenarios. **Renumbered from R15 at the merge with slice 139**, which took R15 for the landing page; nothing about the requirement changed |
| — | `projector/R1`, `projector/R2` | no change: removing the dead `savedScreensSignature` assignment restores the behaviour spec 119 gave the page (adopting the stored service and screen on load); the capability's text was already true |

## Before / after

| | Before | After |
| --- | --- | --- |
| requirements in `docs/spec/reading.md` | 14 at this slice's Fold (15 after slice 139 merged) | 16 |
| scenarios in R14 | 7 | 7 (one sentence modified) |
| scenarios in R16 | — | 4 |
| `last folded` | 2026-10-27 | 2026-10-27 |
| `slices` | starts `138-sidebar-overlay-stack` | starts `141-projector-window-reopen` |

## Not folded

Nothing. No accepted gaps.
