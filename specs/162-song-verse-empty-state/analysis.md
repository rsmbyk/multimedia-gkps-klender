# Analysis: A song with no verses is named, not mistaken for no song

**Spec**: `specs/162-song-verse-empty-state/spec.md`
**Plan**: `specs/162-song-verse-empty-state/plan.md`
**Tasks**: `specs/162-song-verse-empty-state/tasks.md`

**Run**: 2026-10-29 · artifacts read: `spec.md` `4ed436846e44` · `plan.md` `fa152972b1f8` ·
`tasks.md` `6ab75c4330d7` (sha256, first 12) ·
**Metrics**: 5 requirements · 4 success criteria · 6 story scenarios · 5 edge cases · 20 traceability
rows · **17 test** · **3 inspection** · **0 manual** · coverage 100% · CRITICAL 0

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | LOW | coverage | `spec.md` §Edge Cases | The edit form's first paint for a song **with** verses still reads `Pick a song first` until the script sets `All verses`. Pre-existing, and invisible in practice — the modal injects the fragment and wires it in one script turn — but a reader of FR-002 may expect the whole line to be server-rendered. | not this slice — recorded here, and `data-model.md` states the invariant only for the verse-less case |
| A2 | LOW | consistency | `entries.py` | `song_has_no_verses` is a form property while the other four lines live in the script: two homes for one line's states. | accepted — the property covers exactly the state the server can be wrong about, and `contracts/none.md` says the script owns every later line |
| A3 | LOW | performance | `models.py` | The split refusal runs `song.verse_set.filter(is_deleted=False).exists()` — one extra query, only when a save is already failing. | accepted — a failed save is not a hot path, and caching the fact would be the second source D005 rejects |
| A4 | LOW | measurability | `spec.md` §SC-003 | SC-003 names the live page's 436px width while the preview sheet is 480px wide, so the preview's own number differs by the sheet. | accepted — the spec says the live page's box; the preview's 38px height is the invariant, and `plan.md`'s SC-003 window row names 436/338 as inspection |

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T003, T004 |
| FR-002 | ✅ | ✅ | T005, T006 |
| FR-003 | ✅ | ✅ | T003, T004 |
| FR-004 | ✅ | ✅ | T008, T009 |
| FR-005 | ✅ | ✅ | T003 (the two existing song E2Es), T012 |
| SC-001 | ✅ | ✅ | T003 |
| SC-002 | ✅ | ✅ | T003 |
| SC-003 | ✅ | ✅ | T003 (box), T011 (both widths) |
| SC-004 | ✅ | ✅ | T010 |
| US1/AC1–AC2 | ✅ | ✅ | T003 |
| US1/AC3 | ✅ | ✅ | T012 (existing E2Es) |
| US1/AC4 | ✅ | ✅ | T005, T006 |
| US2/AC1 | ✅ | ✅ | T008, T009, T010 |
| US2/AC2 | ✅ | ✅ | T008 (the existing test is kept, not rewritten) |
| Edge — failed fetch | ✅ | — | inspection row, needs no task (C-SDD-TDD: `inspection` never enters TDD) |
| Edge — stored verses | ✅ | ✅ | T007 |
| Edge — one-verse song | ✅ | ✅ | T012 |
| Edge — narrow dialog | ✅ | ✅ | T011 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 0/0/4

## Applied mechanically

- The verification split in `plan.md` and `tasks.md` said 14 test; the traceability table carries 17.
  Corrected, not re-derived from the code.
- `data-model.md`'s invariant originally forbade `Pick a song first` for **any** picked song, which the
  accepted FR-002 does not require (finding A1). Narrowed to the verse-less case so the artifact states
  what the slice actually builds.
- `spec.md` §UI/UX said "the longest candidate line"; only the approved line survives Clarify, so the
  sentence now names it as the approved one.

## Escalated

- Nothing: no finding changes intent, so no question was put to the owner. A1 is the only one that
  could have — it would have needed a decision about widening FR-002 to every edit first paint — and
  it is explicitly out of the accepted scope.
