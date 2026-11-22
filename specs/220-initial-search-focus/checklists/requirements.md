# Reading Checklist: Focus only the empty search landing

**Spec**: `specs/220-initial-search-focus/spec.md` · **Created**: 2026-11-22 · **Depth**: Lite

- [ ] CHK001 Does US1 cover each requested entry path to the empty landing: `/`, empty `/search`, and the Search rail with no remembered result? [Coverage, Spec §US1]
- [ ] CHK002 Is focus limited to the empty landing and explicitly excluded from direct or restored results? [Consistency, Spec §FR-001–FR-003]
- [ ] CHK003 Does the spec state that focusing preserves the typed value, does not select it, and does not scroll? [Completeness, Spec §FR-002]
- [ ] CHK004 Is the compact results field's state after an in-place landing-to-results transition unambiguous? [Clarity, Spec §US1/AC4]
- [ ] CHK005 Does the spec resolve its conflict with accepted Spec 139 FR-006 before acceptance? [Consistency, Spec §FR-006]
- [ ] CHK006 Are reading pages and other section landings explicitly excluded from automatic focus? [Coverage, Spec §FR-004]
- [ ] CHK007 Are the focus-visible treatment and no-motion/no-scroll requirements preserved without assuming a new visual design? [Scope, Spec §UI/UX]
- [ ] CHK008 Can every focus claim be observed through the browser's active element and keyboard typing without a test helper stealing focus? [Measurability, Spec §Success Criteria]
- [ ] CHK009 Do the section indexes that paint the same landing (`/bible/`, `/songs/`, `/tatib/`) focus like `/`, while reading routes stay unfocused? [Coverage, Spec §FR-001, §FR-004]
