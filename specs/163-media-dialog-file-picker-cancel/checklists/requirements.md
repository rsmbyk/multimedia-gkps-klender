# Reading Checklist: dismissing the file picker leaves the New media dialog open

**Spec**: `specs/163-media-dialog-file-picker-cancel/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [x] CHK001 Is the defect stated with the mechanism that produces it — the input's own `cancel`
  bubbling to the dialog's listener — rather than only as "the modal closes"? [Clarity, Spec §What the
  page does today]
- [x] CHK002 Does the spec separate the two sources of `cancel` that reach the dialog, so a reader can
  see why one guard fixes both without breaking Escape? [Clarity, Spec §FR-001, §US2]
- [x] CHK003 Is the requirement phrased on the event's target — the state the record is in — rather than
  on the transition "the picker was open"? [Measurability, Spec §FR-001, §Assumptions]
- [x] CHK004 Does the spec name what must NOT move — the 150 ms closing motion, the other editor forms,
  the frame, the save flow — so a wider "stop closing the modal" fix is excluded by name? [Consistency,
  Spec §FR-003, §FR-004]
- [x] CHK005 Is the same-file re-pick stated as its own case, with the browser's behaviour as the reason
  rather than a decision taken here? [Completeness, Spec §Edge Cases, §Assumptions]
- [x] CHK006 Is the failure pinned by a measurement that outlives it — 248 ms to close, form discarded —
  so the criterion can be re-read as evidence? [Measurability, Spec §SC-001]
- [x] CHK007 Are the states the change must survive named — a chosen file, a typed title, the library
  tab's selection, an in-flight inspect, the error dialog? [Coverage, Spec §US1, §Edge Cases]
- [x] CHK008 Is it stated why only one dialog's listener changes, so a reader can tell a deliberate
  narrow fix from a missed one? [Consistency, Spec §Assumptions, §FR-004]

**Gate 2**: ticked by the owner on 2026-10-29 — this list, the plan with its traceability table, the
task list and `analysis.md` were presented together, and the same answer authorised implementation.
