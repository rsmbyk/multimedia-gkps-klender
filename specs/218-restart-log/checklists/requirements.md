# Requirements checklist — spec 218 (a dead companion says why)

Reviewer-owned: the agent generates and never ticks.

## Completeness

- [ ] CHK001 Is the empty-log case stated, or only the happy path? [Completeness, Spec §FR-003, §Edge Cases]
- [ ] CHK002 Does the spec cover the case where the log request itself fails? [Completeness, Spec §FR-003, §Assumptions]
- [ ] CHK003 Is "no log when the start failed" a requirement rather than an implication of the check not running? [Completeness, Spec §FR-004]

## Clarity

- [ ] CHK004 Is "prefixed so it is distinguishable" measurable, or does it need the exact prefix? [Clarity, Spec §FR-001]
- [ ] CHK005 Does the spec say whether the line is trimmed or passed through, including compose's own `media-1  |` prefix? [Clarity, Spec §Assumptions]

## Consistency

- [ ] CHK006 Does FR-002 (name `docker compose build`) contradict the assumption that the hint does not perform the build? [Consistency, Spec §FR-002, §Assumptions]
- [ ] CHK007 Is the claim that the log covers "every cause" consistent with the stale-image story that motivated the slice? [Consistency, Spec §Assumptions, ITEM-233]

## Measurability

- [ ] CHK008 Can SC-001 fail — would a launcher that printed only the hint pass it? [Measurability, Spec §SC-001]
- [ ] CHK009 Is SC-004's "answers one line" the real command, with the same flags the launcher uses? [Measurability, Spec §SC-004]