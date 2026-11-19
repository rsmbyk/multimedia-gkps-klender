# Requirements Checklist: A whisper of a tint on an open entry header

**Spec**: `specs/206-dock-expanded-tint/spec.md` · **Created**: 2026-11-19 · **Depth**: Standard

## Completeness
- [ ] CHK001 Is the tint given as a number the stylesheet can carry, not as "slightly darker"? [Completeness, Spec Domain rules / UI/UX]
- [ ] CHK002 Is the open state named as the attribute the dock already exposes — `aria-expanded` — rather than a new class? [Completeness, Spec FR-008]
- [ ] CHK003 Is the boundary of the paint stated: the header line, the chevron inside it, and nothing of the block? [Completeness, Spec FR-006 / Scope]
- [ ] CHK004 Are both themes written down as computed colours rather than one literal colour? [Completeness, Spec UI/UX]
- [ ] CHK005 Is what does *not* change listed — hover, live, focus, chevron, block surface, JavaScript? [Completeness, Spec Scope / FR-004/FR-005]

## Clarity
- [ ] CHK006 Is "softer than hover" expressed as a measurable relation, not an adjective? [Clarity, Spec UI/UX — 8-level vs 16-level step]
- [ ] CHK007 Does the spec settle what an open *and* hovered header shows, instead of leaving two rules to fight? [Clarity, Spec FR-004 / Assumptions]
- [ ] CHK008 Is the cascade order named as the mechanism, given three selectors of equal weight? [Clarity, Spec FR-003 / UI/UX]
- [ ] CHK009 Does the tint's timing follow a value already in the sheet rather than a new duration? [Clarity, Spec FR-007]

## Coverage
- [ ] CHK010 Is the live row covered as an exemption — it is always `aria-expanded="true"` and must never be tinted? [Coverage, Spec FR-005 / US1 scenario 4]
- [ ] CHK011 Is a closed header covered, so "no tint" is proven and not assumed from the open rule alone? [Coverage, Spec FR-002 / SC-001]
- [ ] CHK012 Is the hover replacement covered on an open header, not only on a closed one? [Coverage, Spec SC-002]
- [ ] CHK013 Are the rows that never expand covered — section breaks and empty blocks? [Coverage, Spec Edge cases]
- [ ] CHK014 Is a no-change row declared for the rest of the dock, so the slice cannot quietly move another state? [Coverage, Spec SC-004]

## Consistency
- [ ] CHK015 Does the tint use the sheet's existing rail-and-ink expression, as `.nextband:hover` already does? [Consistency, Spec Domain rules / preview]
- [ ] CHK016 Is the same percentage stated in the spec, the card and the preview controls? [Consistency, Spec UI/UX / Card]
- [ ] CHK017 Does the modified capability rule keep R14's existing chevron, toggle and live clauses instead of replacing them? [Consistency, Spec FR table — all `dock/R14` modified]
