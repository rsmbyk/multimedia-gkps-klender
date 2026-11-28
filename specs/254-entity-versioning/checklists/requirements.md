# Requirements Checklist: entity versions and safe concurrent edits

**Spec**: `specs/254-entity-versioning/spec.md` · **Created**: 2026-11-28 · **Depth**: Standard

- [ ] CHK001 Are all six tracked objects named in FR-001 also named in the Key Entities list? [Completeness, Spec §Requirements]
- [ ] CHK002 Does FR-002 say what "identical values" means for JSON fields and ordered lists? [Clarity, Spec §Requirements]
- [ ] CHK003 Does FR-003 state which error code and body the 409 carries, as FR-013 promises? [Consistency, Spec §Requirements]
- [ ] CHK004 Is the row-lock scope in FR-004 specific enough to test without inspecting the implementation? [Measurability, Spec §Requirements]
- [ ] CHK005 Does FR-005 cover creates from every entry point, including template generate and copy? [Completeness, Spec §Requirements]
- [ ] CHK006 Does FR-006 enumerate every child write that moves a service version, including reorder and legacy items? [Coverage, Spec §Requirements]
- [ ] CHK007 Is "any referenced song or verse changes" in FR-007 bounded to the fields the owner confirmed? [Clarity, Spec §Requirements]
- [ ] CHK008 Does FR-008 keep the server refusal authoritative while FR-012 disables the button? [Consistency, Spec §Requirements]
- [ ] CHK009 Does FR-009 define which songbook rows are eligible when some songs are hymns? [Clarity, Spec §Requirements]
- [ ] CHK010 Does FR-011 define whether a hidden or inactive Tata Ibadah still counts? [Clarity, Spec §Requirements]
- [ ] CHK011 Is the distinct-service count demonstrated with two entries in one service and one template? [Coverage, Spec §User Scenarios]
- [ ] CHK012 Does SC-001 measure the 409 case in the same terms as FR-003? [Consistency, Spec §Success Criteria]
- [ ] CHK013 Is SC-003 measurable per covered child write rather than as a single aggregate? [Measurability, Spec §Success Criteria]
- [ ] CHK014 Does the UI/UX section name the two dialogs whose states change, even though numbers are pending? [Completeness, Spec §UI/UX]
- [ ] CHK015 Are the retracted answers (cases 1–4 and the reorder-only propagation scope) recorded visibly? [Consistency, Spec §Clarifications]
- [ ] CHK016 Is every deferred live-surface behaviour named as a separate card rather than left inside this spec? [Completeness, Spec §Clarifications]
- [ ] CHK017 Are any error or empty states of the delete confirmation dialog covered by a scenario? [Coverage, Gap]
- [ ] CHK018 Is the migration's effect on existing API serializers stated anywhere? [Completeness, Gap]
