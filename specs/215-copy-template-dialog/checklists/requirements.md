# Requirements checklist — spec 215 (the copy confirmation as a dialog, and the copy's name)

Reviewer-owned: the agent generates and never ticks. Each item asks about the requirements, never
about whether the code works.

## Completeness

- [ ] CHK001 Does the spec state what happens to the *edit dialog* while the confirmation is up — open, dimmed, inert — rather than only what the new layer looks like? [Completeness, Spec §US1, §FR-002]
- [ ] CHK002 Is the name's lifecycle complete: its default, its selection on click, the second click, the empty case, the length limit, and what the record ends up holding? [Completeness, Spec §US2, §FR-003–FR-007]
- [ ] CHK003 Is every dismissal path named — Cancel, Escape, scrim, and the failed copy — with the edit dialog's fate in each? [Completeness, Spec §US3, §FR-009, Edge Cases]
- [ ] CHK004 Is the generate flow's confirmation accounted for, so a reader knows it is not in this slice's scope? [Completeness, Spec §Assumptions]

## Clarity

- [ ] CHK005 Is "the dialog stays legible behind it" measurable as written, or does it need the scrim's opacity number to mean anything? [Clarity, Spec §SC-003, §UI/UX]
- [ ] CHK006 Does the spec say why the confirmation is a layer and not a second `<dialog>` element, instead of leaving the reader to wonder? [Clarity, Spec §Assumptions]
- [ ] CHK007 Is "clicking the field selects the whole name" distinguishable from "the field is focused on open", which the spec deliberately does not do? [Clarity, Spec §FR-004, §Assumptions]

## Consistency

- [ ] CHK008 Do FR-010's card numbers agree with spec 212's, given this slice keeps the card and moves the layer around it? [Consistency, Spec §FR-010, §UI/UX]
- [ ] CHK009 Do the capability references (`reading` R47 and R37, both modified) avoid duplicating a statement either requirement already makes? [Consistency, Spec §Functional, §Assumptions]
- [ ] CHK010 Does FR-005 (the copy takes the typed name) contradict spec 167's FR-021, which says a copy keeps the name? [Consistency, Spec §FR-005]

## Measurability

- [ ] CHK011 Can SC-002 be checked without a screenshot — is "within 1px of the viewport's centre" a number a probe can produce? [Measurability, Spec §SC-002]
- [ ] CHK012 Is SC-006's pair of indices (`0` and the value's length) the check the click behaviour needs, or does it also need the second click's caret? [Measurability, Spec §SC-006, §US2 AC3]
- [ ] CHK013 Does SC-004 cover the close as well as the open, so a dialog that grows on close still fails? [Measurability, Spec §SC-004]

## Coverage

- [ ] CHK014 Is the dark theme covered by a requirement, or only by an assumption that the tokens do the work — including the scrim, which names a colour? [Coverage, Spec §UI/UX]
- [ ] CHK015 Is the narrow window covered — what the card does at a viewport narrower than 448px plus the layer's padding? [Coverage, Spec §UI/UX, §Responsive]
- [ ] CHK016 Does the spec cover a source whose name is at the 64-character limit, or does it defer that to a marker? [Coverage, Spec §Edge Cases]
- [ ] CHK017 Is the case of copying *from a template* covered, where the source already has no date and the copy is a template again? [Coverage, Spec §US2 AC6]
