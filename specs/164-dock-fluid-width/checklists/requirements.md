# Reading Checklist: the dock fills whatever panel it is given

**Spec**: `specs/164-dock-fluid-width/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [ ] CHK001 Is the defect stated with develop's own numbers — the panel held at 560 × 900 at x 680 in a 1920 window — rather than as "too narrow"? [Measurability, Spec §What the page does today]
- [ ] CHK002 Is the cause pinned to the one declaration (`max-width: 560px` with `margin: 0 auto`) and shown to be the only width rule in the sheet, so no second cause can explain the strip? [Clarity, Spec §What the page does today]
- [ ] CHK003 Does the spec say what "fills the width" means at the row level (the panel's width less the body's 8px side padding), so a reviewer can tell a fill from an inset column? [Precision, Spec §FR-004, §SC-003]
- [ ] CHK004 Is the rejected bucket-per-column variant recorded with its measured widths, so the same complaint cannot produce it again? [Consistency, Spec §Assumptions A3]
- [ ] CHK005 Is the one column stated as a requirement (FR-003) instead of a layout accident, with a check that `display` stays `block` and all sections share one x? [Coverage, Spec §US2, §SC-004]
- [ ] CHK006 Does the spec protect everything that must not move — row height, badges, transport, scrollbar, and every box at 560px and below — by name? [Consistency, Spec §FR-006, §US3]
- [ ] CHK007 Is horizontal overflow an explicit success criterion rather than an implication of the fill? [Measurability, Spec §SC-002]
- [ ] CHK008 Does the spec name the preview as the real route served from the slice's worktree, and say that resizing the window is the test? [Traceability, Spec §Preview]
- [ ] CHK009 Are the two E2E tests named by file and behaviour, with the red-on-1.23.1 claim stated as something a reviewer can re-run? [Traceability, Spec §SC-005]

**Gate 1**: presented unticked on 2026-10-29 — the tick list stays the owner's; the agent never ticks it.
