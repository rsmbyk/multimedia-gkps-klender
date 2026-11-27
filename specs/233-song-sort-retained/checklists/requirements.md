# Reading Checklist: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md` · **Created**: 2026-11-23 · **Depth**: Lite

- [x] CHK001 Is the reported trigger (create a song) named in a testable scenario? [Completeness, Spec §US1]
- [x] CHK002 Is the chosen root-cause scope (every in-place refresh) stated in a scenario of its own? [Completeness, Spec §US2]
- [x] CHK003 Is "retained order" observable without a new visual design, and quantified as row arrays? [Clarity, Spec §UI/UX]
- [x] CHK004 Are both sort states — `m` and `title` — covered for the create path? [Coverage, Spec §US1]
- [x] CHK005 Are edit, delete and row-click refreshes each covered? [Coverage, Spec §US2]
- [x] CHK006 Is the no-song-row case and the hymn-book case covered? [Coverage, Spec §US2]
- [x] CHK007 Is the default order on a fresh load stated, so the fix cannot turn the default into alphabetical? [Consistency, Spec §US3]
- [x] CHK008 Is the decision against browser persistence recorded rather than left ambiguous? [Ambiguity, Spec §Assumptions]
- [x] CHK009 Is the in-place (no reload) guarantee carried over from spec 225? [Consistency, Spec §US1]
- [x] CHK010 Is every functional requirement traced to at least one scenario? [Coverage, Spec §Requirements]
