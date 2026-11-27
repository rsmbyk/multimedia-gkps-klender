# Reading Checklist: a created Template opens on the stage

**Spec**: `specs/234-open-created-template/spec.md` · **Created**: 2026-11-23 · **Depth**: Lite
**Owner-owned**: the agent generates these items and never ticks them.

- [ ] CHK001 Does the reported case appear as its own scenario, with the URL the save lands on? [Completeness, Spec §US1]
- [ ] CHK002 Is the current R46 wording that forbids a Template stage quoted and marked superseded, rather than silently overwritten? [Consistency, Spec §Superseded wording]
- [ ] CHK003 Is it explicit that only the Template half of R46 changes, while edits and other kinds keep the list-refresh rule? [Consistency, Spec §FR-004]
- [ ] CHK004 Are the two start points — dated list and template list — each covered? [Coverage, Spec §US1]
- [ ] CHK005 Is "in place" measurable by marker, `timeOrigin` and `data-nav`, as in spec 209? [Clarity, Spec §US2]
- [ ] CHK006 Is the restored focus and `aria-current` row stated as an observable outcome? [Coverage, Spec §US2]
- [ ] CHK007 Are the empty template's invitation and add actions named as the stage contents? [Completeness, Spec §US1/AC3]
- [ ] CHK008 Are the dated create, edit, refused create, generate and copy paths all fenced off? [Coverage, Spec §US3]
- [ ] CHK009 Is the URL's `?mode=template` choice recorded with its rationale, so it reads as a decision? [Ambiguity, Spec §Assumptions]
- [ ] CHK010 Are the UI/UX values numbers (boxes, paths, state flags), not adjectives? [Clarity, Spec §UI/UX]
- [ ] CHK011 Is the superseded E2E test named so Implement knows which assertion flips? [Traceability, Spec §Superseded wording]
- [ ] CHK012 Is every functional requirement traced to at least one acceptance scenario? [Coverage, Spec §Requirements]
