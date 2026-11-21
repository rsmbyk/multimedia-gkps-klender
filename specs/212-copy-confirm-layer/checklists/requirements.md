# Requirements checklist — spec 212 (the Copy as template confirmation as a layer)

Reviewer-owned: the agent generates and never ticks. Each item asks about the requirements, never
about whether the code works.

## Completeness

- [ ] CHK001 Is every visible change the slice makes stated as a requirement, including the one nobody asked for — the scrim's radius? [Completeness, Spec §FR-005]
- [ ] CHK002 Does the spec say what happens to the *form* while the layer is up, rather than only what the layer looks like? [Completeness, Spec §FR-002]
- [ ] CHK003 Is the closed state covered — that `hidden` still hides the layer once it carries a `display` of its own? [Completeness, Spec §FR-005, Edge Cases]
- [ ] CHK004 Is the dismissal behaviour of the confirmation (Cancel, Escape, backdrop) stated as unchanged rather than left to be inferred? [Completeness, Spec §FR-006, Edge Cases]

## Clarity

- [ ] CHK005 Is "covers the form" measurable as written, or does it need the `elementFromPoint` formulation to mean anything? [Clarity, Spec §FR-002, §SC-002]
- [ ] CHK006 Does the spec name the two conflicting card designs it chose between (167's preview, generate.css) instead of quietly picking one? [Clarity, Spec §Assumptions]
- [ ] CHK007 Is the 38px answer height justified against the preview's 36px, or is it asserted? [Clarity, Spec §Assumptions]

## Consistency

- [ ] CHK008 Do the `## UI/UX` numbers agree with the `## Success Criteria` numbers they are measured by? [Consistency, Spec §UI/UX, §Success Criteria]
- [ ] CHK009 Does FR-006 (the answers stay the editor's own buttons) contradict FR-004 (the answers read at the preview's type), given the preview styled its buttons separately? [Consistency, Spec §FR-004, §FR-006]
- [ ] CHK010 Is the capability reference (`new: reading` → R47) consistent with R37, which already covers Copy as template in the modal header? [Consistency, Spec §Functional]

## Measurability

- [ ] CHK011 Can SC-001 be checked without a screenshot — is "equal, to the tenth of a pixel" a number a probe can produce? [Measurability, Spec §SC-001]
- [ ] CHK012 Is SC-003's tolerance (± 1px) the one the preview actually holds, or an invented margin? [Measurability, Spec §SC-003]
- [ ] CHK013 Does SC-004 pin the gap *and* the right edge, so a card that is narrower than expected still fails? [Measurability, Spec §SC-004]

## Coverage

- [ ] CHK014 Is the dark theme covered by a requirement, or only by an assumption that the tokens do the work? [Coverage, Spec §UI/UX, §FR-003]
- [ ] CHK015 Is the narrow dialog covered — what happens at `min(30rem, 100vw - 32px)` with a 468px card? [Coverage, Spec §UI/UX, Edge Cases]
- [ ] CHK016 Does anything in the spec require a behaviour change to the copy itself, which this slice explicitly does not make? [Coverage, Spec §FR-006, Edge Cases]
