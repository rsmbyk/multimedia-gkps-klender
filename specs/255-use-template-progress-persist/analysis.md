# Analysis — spec 255

Date: 2026-11-28

## Artifacts read (SHA-256, first 16 hex)

| Artifact | SHA |
| --- | --- |
| `spec.md` | `946cd994b21179d6` |
| `plan.md` | `9b3dde6a4aa16e9d` |
| `research.md` | `18ed3e57a2193b40` |
| `data-model.md` | `54525a42e3964e7e` |
| `quickstart.md` | `11c364500c26de11` |
| `checklists/requirements.md` | `1f0215595e65fae4` |

Metrics: 11 FRs · 6 SCs · 8 story scenarios · 25 traceability rows · 23 tasks · 15 checklist items
(generated, unticked) · 8 research decisions · 0 unknowns.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| A-01 | — | Every FR and SC has a named test; split is 25 test · 0 inspection · 0 manual | None needed |
| A-02 | — | All eight story scenarios map to an FR and a test | None needed |
| A-03 | — | "Seven days" appears only as 168 hours in FR-003, UI/UX and the data model | None needed |
| A-04 | — | The indicator's no-draft state is specified on all three surfaces: `data-draft`, `aria-label`, dot span | None needed |
| A-05 | LOW | The mark is painted after load, so it cannot exist in the first server-rendered frame | Accepted — the record is browser-local; a server render cannot know it, and the paint runs synchronously before first interaction |
| A-06 | MEDIUM | `paintMark()` must remove `aria-label`, not leave a stale "draft saved" name | Addressed — D7, FR-007; asserted by `test_the_button_has_no_mark_without_a_draft` |
| A-07 | MEDIUM | The mark and the modal can disagree if expiry is applied on one path only | Addressed — D4: one `liveRecord()` for both, plus the load sweep; CHK014 checks the coherence |
| A-08 | LOW | A stage swap replaces the button after the initial paint | Addressed — D6, repaint on `shell:page` |
| A-09 | MEDIUM | The leave confirmation's copy promised "this browser session", false under the new lifetime | Addressed — FR-011 added; the copy and spec 253's assertion changed; `test_the_leave_confirmation_names_the_seven_day_lifetime` |

Critical findings: **0**. Coverage: **100%**. Gate 2 may open.

## History

- 2026-11-28 — first run; zero CRITICAL, full coverage, no mechanical fixes applied.
- 2026-11-28 — updated after FR-011 (confirmation copy) and the 4px border-box inset correction;
  metrics moved to 11 FRs / 25 rows / 23 tasks / 15 checklist items.