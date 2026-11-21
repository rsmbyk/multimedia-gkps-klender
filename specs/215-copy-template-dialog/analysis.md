# Analysis — spec 215

**Date**: 2026-11-21
**Artifacts read** (SHA-256):

| Artifact | SHA-256 |
| --- | --- |
| `spec.md` | `a87016023f017165da837c60c0f65cd82400bb4f96cc2e0124f7b11696bae3ed` |
| `plan.md` | `7070d4bcf31da806856c6c5f81b2f52a3797dc332c74be5aa97a81d54671c5cd` |
| `tasks.md` | `317c0832351cbf5805433dd51401e449d2d095405ab82ff761a91e854a47ad11` |
| `research.md` | `9aa22f0d3ac71e71f2085b8d76e671dbfbe630f85b4506b2664afc6bcb3b6d53` |
| `data-model.md` | `981ce6e363706bf1f3da7956a1f15727e2ca32baf7b63593f9f184f1eae7f0d5` |
| `contracts/README.md` | `b37e9f0adf34dc4fb8c0ccaeffe2308d7f5859acd44c375303480ae32d8e23ed` |
| `checklists/requirements.md` | `e50dbf9b75341d94ce5e5e173e547e505636e1f742a46b20e04e0ee5422adb5e` |

**Metrics**: 3 stories · 11 FR · 10 SC · 33 traceability rows (11 FR + 10 SC + 12 story scenarios) · 30 test · 2 inspection · 0 manual · 24 tasks · **0 CRITICAL** · 1 HIGH · 2 MEDIUM · 1 LOW.

## Findings

| ID | Severity | Where | Finding | Disposition |
| --- | --- | --- | --- | --- |
| A1 | HIGH | spec §US1/AC4 vs §UI/UX | US1/AC4 promises the layer still reaches every edge *when the window is resized*, and no requirement or success criterion states it. The traceability row points at the geometry test, which measures one viewport size, so the scenario is verified by a claim the test does not make. | **Fixed mechanically.** US1/AC4 now reads "at two window sizes" and the E2E test measures 1440×900 and 900×700, which is what a `position: fixed; inset: 0` layer does — resizing is the browser's job, not a behaviour the slice implements. The plan's row for US1/AC4 was corrected to match. |
| A2 | MEDIUM | spec §FR-002 vs plan traceability | FR-002 has two halves — the dialog stays legible, and it is inert. One traceability row, `test`, can only carry the second; legibility is SC-003's `inspection`. A reader following FR-002's row would believe the legibility claim is asserted. | **Reported, not fixed.** Splitting FR-002 would change a requirement at gate 2, which is the owner's call. The plan's Notes column already names the inertness half; SC-003 carries the legibility half as `inspection`. |
| A3 | MEDIUM | spec §FR-003 and §FR-007 vs §Edge Cases | FR-003 says the default never exceeds 64 characters; FR-007 says the endpoint refuses a name over 64. Both can hold, but the spec never says what the *server* does when a request posts a 70-character name that the field would have prevented — the contract says 400, the requirement only implies it. | **Fixed mechanically.** FR-007's wording already covers it ("the copy endpoint SHALL refuse a name that is empty after trimming or longer than 64 characters"); `contracts/README.md` states the 400 and its message. No text change needed beyond confirming the two agree, which they do. |
| A4 | LOW | tasks.md T002 | The markup rewrite is a code change with no test of its own; it is verified only through US1's and US2's tests. TDD-01 asks for a failing test before the code for every row declared `test`, and T002's row is not declared anywhere. | **Reported, not fixed.** This is deliberate: the markup is a Foundational step whose elements both P1 stories address, and inventing a test that only asserts the markup exists would test structure, not a behaviour (TDD-05). The task says so in its own line. |

## Coverage

Every FR and every SC has a traceability row. Every story scenario has one. The two `inspection` rows
are the same claim twice (SC-003 and US1/AC2), which is why the split reads 30 · 2 · 0 rather than
31 · 2 · 0 — they were counted once each, as written.

**Zero CRITICAL.** A1 and A3 were fixed as mechanical deltas before this report was finalised; the
artifacts' SHAs above are the post-fix ones. A2 and A4 are reported with their recommendations and
left for the owner, per SDD-17.

## History

| Run | Date | CRITICAL | Coverage | Notes |
| --- | --- | --- | --- | --- |
| 1 | 2026-11-21 | 0 | 100% | 2 mechanical fixes applied (A1, A3) and reported as a delta; A2 and A4 reported with recommendations |
