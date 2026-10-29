# Projector Checklist: the image placeholder waits for the image to fail

**Spec**: `specs/157-projector-image-missing-glyph/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [ ] CHK001 Is the reported symptom pinned to boxes and pages (picture 520–1319, glyph 1330–1389, centres 583.5/584 at 1920×1200) rather than described as "an icon appears"? [Measurability, Spec §What the page does today]
- [ ] CHK002 Does the spec name the mechanism — `missing.hidden` is an expando on an `SVGSVGElement` and the attribute the CSS keys on is never written — so no competing explanation (a stray template, a CSS rule, a second element) fits? [Clarity, Spec §What the page does today]
- [ ] CHK003 Is the suite's blind spot named as part of the defect, with both the case that passes for the wrong reason and the case that never looked? [Completeness, Spec §What the page does today, §US2, §FR-005]
- [ ] CHK004 Are the three states the screen can be in enumerated, including the one nobody reported (pending, which also leaks the glyph)? [Coverage, Spec §US1, §Success Criteria SC-003]
- [ ] CHK005 Is the 40px claim measured on the product's own stylesheet rather than asserted from the rule? [Measurability, Spec §UI/UX, §SC-001]
- [ ] CHK006 Does the spec say what must NOT move — geometry, size, colour, the other four placeholders, their cases — so a wider "tidy-up" is excluded by name? [Consistency, Spec §FR-006, §Assumptions]
- [ ] CHK007 Is there a second stage size, so the fixed 1920×1200 board cannot hide a size-dependent rule? [Coverage, Spec §UI/UX responsive row]
- [ ] CHK008 Is the capability number stated as a new requirement in an existing file (R3), rather than a new capability or a copied requirement? [Consistency, Spec §Assumptions, `docs/spec/projector.md`]
- [ ] CHK009 Is the bump declared (`patch`) and its reason given? [Completeness, Spec §Assumptions]
- [ ] CHK010 Does every requirement carry a capability, and every scenario an observable outcome? [Completeness, Spec §Requirements, §User Scenarios]

**Specify**: the spec was validated against these ten items before gate 1, one iteration — `FR-002`…
`FR-006` now cite `new: projector` → R3 rather than a number that does not exist yet. The boxes are the
reviewer's to tick (SDD-15); they stay empty until gate 2.

**Gate 1**: accepted by the owner on 2026-10-29 — this list, `spec.md`, the static preview at
`specs/157-projector-image-missing-glyph/preview/preview.html` and the probe's numbers were presented
together.
