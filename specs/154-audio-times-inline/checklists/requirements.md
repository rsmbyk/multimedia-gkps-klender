# Reading Checklist: an audio preview reads its times as `current / total`

**Spec**: `specs/154-audio-times-inline/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [x] CHK001 Is today's line stated with the numbers that make it a defect — elapsed at x 500→523.8, total at x 980.2→1004, 456.4px apart — rather than as "it looks split"? [Measurability, Spec §What the preview does today]
- [x] CHK002 Does the spec say which element and which rule produce that split (`tatib.html:56`, `components.css:2134`, `justify-content: space-between`), so a reader can find it without a search? [Clarity, Spec §What the preview does today]
- [x] CHK003 Is the target shape stated as an order and a position — `current / total`, right-aligned, total's edge on the bar's edge — rather than as an adjective? [Clarity, Spec §FR-001, §FR-002]
- [x] CHK004 Does the spec name the surfaces that must NOT move — the projector's own `.screen__audio-times` already reading `current / total` — so a reader does not "fix" it twice? [Consistency, Spec §US2, §FR-004]
- [x] CHK005 Is the separator's accessibility stated as a reason for a real text node rather than a pseudo-element? The pair must read as one value to a screen reader, not as two adjacent numbers. [Coverage, Spec §Assumptions]
- [x] CHK006 Does the spec bound what the change may not touch — dialog width, play button, filename, bar height, the 7px gap, the 12px type, the unavailable state — so "tidy the player" is excluded by name? [Completeness, Spec §FR-004]
- [x] CHK007 Is every state the line can be in accounted for — unknown duration, past-an-hour duration, unavailable, dark theme, narrow viewport — with the same right alignment claimed in each? [Coverage, Spec §Edge Cases]
- [x] CHK008 Does the verification pin geometry rather than computed style, so a rewrite of the rule that keeps `space-between` out of the result still passes? [Measurability, Spec §SC-001..SC-004]

**Gate 2**: ticked by the owner on 2026-10-29 — this list, the plan with its traceability table, the task
list and `analysis.md` were presented together, and the same answer authorised implementation
(F1–F4 accepted as recorded there).
