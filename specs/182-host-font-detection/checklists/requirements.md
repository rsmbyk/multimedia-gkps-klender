# Requirements Checklist: the computer's own fonts reach the converter

**Spec**: `specs/182-host-font-detection/spec.md` · **Created**: 2026-11-01 · **Depth**: Standard

Focus areas: Startup & portability · Font resolution · Operator override · Measurability.

- [ ] CHK001 Are the platforms a launcher must support named for every startup scenario? [Completeness, Spec §US1]
- [ ] CHK002 Is "the stack starts" defined as all three services running plus the app answering 200, rather than the command exiting? [Clarity, Spec §SC-001]
- [ ] CHK003 Does FR-001 say where the fallback path resolves, not merely that it must not be empty? [Clarity, Spec §Requirements/Functional]
- [ ] CHK004 Are absent, empty and unreadable font directories each given a defined outcome? [Coverage, Spec §Edge Cases]
- [ ] CHK005 Is precedence between the operator's directory and the computer's own fonts decided rather than described? [Consistency, Gap]
- [ ] CHK006 Is the licence boundary stated so that "no font file enters the image" can be checked? [Measurability, Spec §FR-006]
- [ ] CHK007 Does every requirement name a platform, or say explicitly that it covers all of them? [Completeness, Spec §Requirements/Functional]
- [ ] CHK008 Is the computer that already holds fonts under the old home-directory default covered by a scenario, so a working install is not silently reset? [Coverage, Spec §FR-007]
- [ ] CHK009 Is the added start-up cost bounded by a number rather than by "does not become slow"? [Measurability, Spec §SC-005]
- [ ] CHK010 Is the dependency between the renderer identity and the font inventory stated where the derivative is decided? [Consistency, Spec §FR-008]
- [ ] CHK011 Can a reader tell whether plain `docker compose up` remains a supported start command? [Clarity, Spec §Assumptions]
- [ ] CHK012 Is the capability split decided before the delta is written at Fold? [Completeness, Gap]
- [ ] CHK013 Are per-user font directories distinguished from system-wide ones wherever they are mounted? [Precision, Spec §FR-002, §FR-003]
- [ ] CHK014 Is the absence of a preview justified by a stated reason rather than left blank? [Completeness, Spec §UI/UX]
- [ ] CHK015 Is the substitute mapping still asserted as the fallback, and not as the default drawing? [Consistency, Spec §US2]
- [ ] CHK016 Does the spec say what happens when a computer's font directory holds a thousand files? [Coverage, Gap]
- [ ] CHK017 Is every success criterion observable by a command a reviewer can run? [Measurability, Spec §Success Criteria]
- [ ] CHK018 Is the PowerShell assumption written down rather than implied? [Clarity, Spec §Assumptions]
