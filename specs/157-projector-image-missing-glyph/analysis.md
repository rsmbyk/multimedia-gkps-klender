# Analysis: the projector's image placeholder waits for the image to fail

**Date**: 2026-10-29 · **Gate**: opens at zero CRITICAL and 100% coverage.
**Artifacts read** (sha256, first 12):

| Artifact | Digest |
| --- | --- |
| `spec.md` | `2d1af416d4d8` |
| `plan.md` | `6707abeba64d` |
| `research.md` | `b8768447d2bc` |
| `data-model.md` | `269503070076` |
| `contracts/none.md` | `8ef5733579fe` |
| `quickstart.md` | `067a8a809fcb` |
| `tasks.md` | `ab3b4dd5a685` |
| `checklists/requirements.md` | `bd2a8bd24354` |

**Metrics**: 6 requirements · 5 success criteria · 6 story scenarios · 4 edge cases (22 traceability
rows) · 19 tasks, five of them running tests · coverage **100%** · CRITICAL **0**. The traceability table
counts `12 test · 9 inspection · 1 manual`, the same split the plan and `tasks.md` declare.

## Findings

| ID | Severity | Kind | Artifact | Finding | Disposition |
| --- | --- | --- | --- | --- | --- |
| A1 | note | coverage | `plan.md` SC-001 | The case pins the placeholder's absence; the "picture centred on 960" half is measured by `preview/probe.py` rather than asserted. The E2E's image is 12×6 px, so a centring assertion there would measure the fixture, not a photograph. | Kept as the `inspection` row it is, with the probe's numbers quoted in the spec and re-run in T012. |
| A2 | low | coverage | `plan.md` FR-003 | The failed-state reset on leaving a screen has no E2E: while the screen is off-active it is `aria-hidden` and its nodes are `visibility: hidden`, so no assertion can separate "reset" from "still marked". | Accepted: `inspection` (T011). SDD-13's rule holds — the requirement is un-tested, not un-verifiable. |
| A3 | low | consistency | `tasks.md` T003 | The pending case registers a route that never fulfils. If the page ever aborted that fetch on its own, the case would see the glyph and go red for a reason that is not this slice's. | Accepted: the page has no fetch timeout (`media-image.js` runs under the screen's `AbortController`, aborted only by a move), and a red would be a real finding about the state. |
| A4 | none | decision | `plan.md` FR-006 | The plan declares no CSS change while the whole visible defect is a `display` value. | Recorded: `[hidden]` is already declared at `projector.css:78`, so the stylesheet needs nothing (D004); a CSS delta here would have been a second way to say the same thing. |
| A5 | none | limitation | `plan.md` manual row | The live `/projector?service=<id>` readout cannot run before the merge: the compose `web` container serves `develop`, and a worktree server is refused by the companion's origin allow-list. | Accepted as the pack's one `manual` row (T019), with the same limitation spec 150 recorded. |

No CRITICAL, no HIGH. Nothing here changes what the spec means.

## Coverage

| Requirement | In plan | In tasks | Accounts for |
| --- | --- | --- | --- |
| FR-001 | ✅ | ✅ | T002, T005, T006 |
| FR-002 | ✅ | ✅ | T009 |
| FR-003 | ✅ | ✅ | T007, T011 |
| FR-004 | ✅ | ✅ | T003, T005, T006 |
| FR-005 | ✅ | ✅ | T002, T003, T009 |
| FR-006 | ✅ | ✅ | T011, T013 |
| SC-001 | ✅ | ✅ | T002, T012 |
| SC-002 | ✅ | ✅ | T009, T012 |
| SC-003 | ✅ | ✅ | T003 |
| SC-004 | ✅ | ✅ | T004, T010 |
| SC-005 | ✅ | ✅ | T013 |
| US1/AC1…AC4 | ✅ | ✅ | T002, T009, T003, T011 |
| US2/AC1…AC2 | ✅ | ✅ | T002, T009 |
| 4 edge cases | ✅ | ✅ | T011, T012, T003 |
| manual live row | ✅ | ✅ | T019 |

**Coverage**: 100% · **CRITICAL**: 0 · **HIGH/MED/LOW**: 2 (A2, A3) · notes: 2 (A1, A4) · limitation: 1 (A5).

## Applied mechanically

- **Split verified**: the declared `12 test · 9 inspection · 1 manual` equals the table's 22 rows; the
  plan, `tasks.md` and this line now carry one number.
- **Symbol assigned**: `static/web/media-image.js` was named in the plan's non-image edge row without its
  `static/web/` prefix, so `tasks.md` T011 did not literally name it; T011 now does.
- **Manual row homed**: the plan's one `manual` row had no task behind it; T019 now carries it.

## Escalated

- Nothing. No finding changed a requirement, a scenario or an acceptance criterion.

## History

- **2026-10-29 — implement, T004's red run**: both new cases against the unmodified template and script
  failed on `AssertionError: Locator expected to be hidden / Actual value: False`, the locator resolving to
  `<svg class="screen__image-missing">` with `unexpected value "visible"` — the defect, stated by the test
  rather than by the report. After the three code changes, `tests.e2e.test_image_display` ran 6 tests,
  `OK`.
- **2026-10-29 — T013's neighbouring modules**: `test_audio_display` + `test_video_display` +
  `test_pdf_display`, 18 tests, 16 green, 2 red — `test_untitled_preview_and_projector_idle_display_off`
  and `test_navigation_and_display_off_stop_and_reset_video`, both on `body[data-showing]` staying `true`.
  They are card `ITEM-140`'s, recorded on the board as identical on `develop`; this slice never writes
  that attribute (`projector.js:403`, `:1164` untouched).
- **2026-10-29 — first run**, on the gate-1 spec and the plan: `22 rows / 12 · 9 · 1`, coverage 100%,
  CRITICAL 0, five findings — two low (the reset has no E2E; the pending case's unfilled route), two notes
  (the centring half is the probe's; no CSS despite a `display` defect), one limitation (the live row is
  post-merge). No mechanical fix survived the run except the three above, which were applied before it.
