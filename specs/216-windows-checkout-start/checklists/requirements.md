# Requirements checklist — spec 216 (a checkout made on Windows starts the stack)

Reviewer-owned: the agent generates and never ticks. Each item asks about the requirements, never
about whether the code works.

## Completeness

- [x] CHK001 Is the *cause* stated as a requirement rather than only described in the scenario — that no build step may depend on the checkout's line endings? [Completeness, Spec §FR-001, §FR-003]
- [x] CHK002 Does the spec cover the case the report did not show, a checkout made before the pin existed, without requiring a re-clone? [Completeness, Spec §Edge Cases]
- [x] CHK003 Is the second launcher (`up.sh`) given its own requirement rather than assumed to follow `up.ps1`? [Completeness, Spec §FR-006]
- [x] CHK004 Is the exit status of a failed start covered, not only the status of a successful one with a failed check? [Completeness, Spec §US2 scenario 3, §FR-007]

## Clarity

- [x] CHK005 Is "the image strips `\r`" pinned to a place in the build, or could a reader implement it in the launcher and still claim FR-001? [Clarity, Spec §FR-001, §FR-003]
- [x] CHK006 Does the spec say which message the operator gets for which failure, or is "one line naming the cause" ambiguous between the two? [Clarity, Spec §FR-004, §FR-005, §Assumptions]
- [x] CHK007 Is "`*.ps1` keeps its CRLF" measurable as written — does any scenario show how it is checked? [Clarity, Spec §FR-002, §SC-002]

## Consistency

- [x] CHK008 Does FR-007 (a failed check never changes the exit status) contradict US2's independent test, which asks for a non-zero start to propagate? [Consistency, Spec §FR-007, §US2]
- [x] CHK009 Do the two new capabilities (`local-stack/R4`, `R5`) overlap what R1 already says about starting on an operator's computer, or is the split argued? [Consistency, Spec §Functional, docs/spec/local-stack.md]
- [x] CHK010 Is the assumption that Git for Windows defaults to `core.autocrlf=true` consistent with the edge case for a checkout made with `core.autocrlf=input`? [Consistency, Spec §Assumptions, §Edge Cases]

## Measurability

- [x] CHK011 Can SC-001 be run on a machine with no Windows checkout — is the CRLF file constructed rather than found? [Measurability, Spec §SC-001]
- [x] CHK012 Does SC-002 name the exact command and its expected output for both file kinds? [Measurability, Spec §SC-002]
- [x] CHK013 Is SC-003 honest about being inspection-only, given PowerShell is not installed on the development machine? [Measurability, Spec §SC-003, §UI/UX]
