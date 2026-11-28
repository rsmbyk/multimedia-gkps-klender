# Analysis: an open modal keeps the scroll to itself

**Date**: 2026-11-28
**Artifacts read** (first 16 hex of SHA-256): `spec.md` `fa355938d355dd2f`, `plan.md`
`dfb9678dc01f208b`, `tasks.md` `74ec66de9dff9151`, `research.md` `4baecd9e9a1b311a`.

**Metrics**: 5 FR · 4 SC · 3 stories · 8 scenarios · 14 traceability rows · 8 decisions ·
22 tasks · verification split 7 test · 6 inspection · 1 manual · 0 CRITICAL · 14/14 coverage.

| ID | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| A1 | `ITEM-277` is `ready` with an empty `issue:` field; no tracker anchor exists yet. | LOW | **Open by design, resolved at delivery**: D008 records why the remote write waits for the push word; the anchor is created and `issue:` written before the first push, and the PR body cites `Refs #<number>`. Cost of leaving it now: a reader cannot follow a tracker link until delivery. |
| A2 | The live preview holds uncommitted CSS; the selector list was expanded after the first gate-1 measurement. | MEDIUM | **Resolved**: `collectstatic` was re-run, the served stylesheet was checked for the new selectors, and both probes were re-run; every frozen `UI/UX` number still matches. Cost paid: one probe pair. |
| A3 | No route in this app has document scroll at the measured viewport, so the probe gives `body` a synthetic 4000px height. | MEDIUM | **Resolved with a stated limit**: the stylesheet under test is the CSS each real server serves, and the two cases the owner reported are reproduced (end-of-range and zero-range). Production confirmation is a declared `manual` row; the probe does not claim a deployment observation. |
| A4 | The static preview inlines both full `components.css` copies, making a 394KB page. | LOW | **Accepted**: the control must be the base commit's real CSS, not a hand-trimmed copy; the toggle was driven in Chromium and computed styles switch `auto`/`visible` ↔ `contain`/`hidden`. No in-chat directive is emitted for this page, so the chat-frame verifier rule is not triggered. |
| A5 | The E2E module named in the traceability table does not exist yet, and browser suites are deferred to the push step by the owner's standing preference. | MEDIUM | **Open by design**: Plan names the file and six behaviours, Tasks pairs each `test` row with a failing-test and a pass task, and SC-001 declares the base/slice red-green comparison. Gate 2 is asked to accept this timing; nothing in the pack claims a green suite before it has run. |

**Mechanical check**: every FR, SC and story scenario appears in Plan's traceability table; every `test`
row has a paired red/green task; no stale spec/card IDs (257 / ITEM-277 everywhere); no duplicated
requirements; `quickstart.md` links the contracts and data model instead of copying them. No
mechanical delta was needed.

**Coverage** reads Plan's table: 14/14 rows have a task and a declared verification method. Zero
CRITICAL findings, full coverage; A1 and A5 are timing findings resolved by the declared delivery
steps, not gaps in the plan.

## History

- 2026-11-28 — first Analyze after gate 1; five findings recorded, zero CRITICAL, gate 2 ready to
  present.
