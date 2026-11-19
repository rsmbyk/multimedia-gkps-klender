# Convergence: the dock follows the live entry only when following

**Spec**: `specs/200-dock-centre-triggers/spec.md`
**Plan**: `specs/200-dock-centre-triggers/plan.md`
**Tasks**: `specs/200-dock-centre-triggers/tasks.md`
**Date**: 2026-11-18

## Phase 1: Convergence

Checked every row of the plan's 69-row traceability table against the implemented code, plus the
three inspection items and the source tree. Method per row: `test` → the named E2E method was run;
`inspection` → the named file was read; `manual` → declared as a manual check in `quickstart.md`.

| ID | Type | Requirement / area | Evidence | Outcome |
| --- | --- | --- | --- | --- |
| C1 | partial → fixed | FR-006 browsing crossings centred anyway | `finishMorph()` called `centerRow` for every morph; corrected to centre only on the instant reduced-motion path (`carry && !moved`). `test_advances_follow_when_following_and_not_when_browsing` passes | fixed |
| C2 | partial → fixed | SC-001 ≤1 px landing after an advance | the old `offsetTop`/rect mix and a mid-glide band move landed 32–69 px short; `glideRow()` now drives the live row's own offset to zero on the same 400 ms soft in-out curve, and `updateBand()` holds during a centring. All landing assertions pass | fixed |
| C3 | contradicts → fixed | FR-006 transport Next must not change the mode | the first implementation put re-entry on `#nextBtn`; the owner corrected it to the sticky band, and the handler was reverted to a plain `step(1)`. US1/AC7 and US4/AC3 pass | fixed |
| C4 | partial → fixed | FR-007 held press suspends the clock | the earlier E2E asserted an exact `scrollTop` and failed on an unrelated re-read clamp; changed to assert no upward centring glide, which is what the requirement says | fixed |
| C5 | unrequested | `bandHoldUntil`, `glideRow`, `rowOffset` | implementation refinements needed to keep one motion and an exact landing; no new behaviour is exposed, no display record or interface changed | retained — declared as refinement, not a behaviour change |
| C6 | accepted gap | FR-006 browsing crossing reflow (gate-2 finding A4) | block heights still animate in browsing; the browser can clamp `scrollTop` down when content shrinks. No centring glide runs (asserted). Cost: the operator may press the centre control sooner | accepted at Gate 2, not folded as a defect |
| C7 | checked by inspection | I1 markup/CSS | `#centreBtn` is the middle `.navpair` child, `navbtn`, `tabindex="-1"`, titled and crosshair SVG; no CSS file changed | pass |
| C8 | checked by inspection | I2 display record | no `following` reference in `display.js`; no verb, field or channel message added | pass |
| C9 | checked by inspection | I3 local mode | `following`, `lastNotice`, `IDLE_MS`, `holding` and `bandHoldUntil` are page-memory only; no localStorage write or postMessage | pass |
| C10 | test | all 14 E2E methods | `tests.e2e.test_obs_dock_follow` — 14/14 OK (111.8 s) on throwaway DB `gkps200` | pass |
| C11 | test | regression probe | two pre-existing dock tests (keyboard steps, screen-row projection) — 2/2 OK | pass |
| C12 | test | syntax | `node --check static/web/obs-dock.js` — clean | pass |
| C13 | manual | M1–M3 | listed in `quickstart.md`; not executed in this headless run | declared |

**Outcome**: **Converged**, with one accepted gap (C6 / gate-2 A4). No CRITICAL or HIGH gap remains;
every `test` row was actually run, `inspection` rows were read, `manual` rows are declared.

## History

- Pass 1, 2026-11-18 — 69 traceability rows checked; six defects found, five fixed in code/tests and
  one carried as the gate-2-accepted reflow gap; two inspection items and one regression probe green.
- Pass 2, 2026-11-18 — owner reported a flash at the idle threshold. Live probing showed it was the
  spec-195 10 s re-read, not the 15 s clock: 445 DOM mutations in one frame at 9.284 s, including a
  full `entryList.replaceChildren()` that dropped the hovered header and repainted under the pointer.
  Fixed by comparing the fresh payload with the painted one and skipping the rebuild when unchanged;
  same probe now records zero mutations after startup. New test
  `test_the_reread_does_not_rebuild_an_unchanged_list` added; suite 15/15 green. Outcome: Converged.
- Pass 3, 2026-11-19 — owner asked for every re-centre to slow into its target. Replaced the cubic
  glide and the crossing morph's ease-in-out with one quintic ease-out (`easeOutQuint`), leaving the
  operator's own block toggle on ease-in-out. Live per-frame steps changed from
  `90, 74, 59, 47, 36, 26, 18, 12, 6, 3, 1` to `137, 93, 61, 38, 22, 12, 5, 3, 1` px; the last
  third fell from 9.9% to 3.1% of the first third. New deceleration test red before / green after,
  suite 16/16 green. Outcome: Converged.
- Pass 4, 2026-11-19 — owner said the quintic still felt too fast and wanted the last stretch eased
  out. Changed the shared curve to quadratic (`easeOut`), which cuts the first frame from 137 px to
  63 px and leaves 33 px in the last third (was 9 px) so the row visibly settles into place.
  Duration stays 190 ms; the operator's toggle stays ease-in-out. Threshold in
  `test_the_centring_decelerates_into_its_target` retuned to the gentler curve; suite 16/16 green.
  Outcome: Converged.
- Pass 5, 2026-11-19 — owner asked to soften slightly more. Lowered the shared exponent from 2 to
  1.6 at the same 190 ms: first-frame step 63 px → 51 px, last third 33 px → 54 px, so the row keeps
  moving gently as it settles instead of arriving in a few tiny steps. Deceleration guard retuned;
  suite 16/16 green. Outcome: Converged.
- Pass 6, 2026-11-19 — owner asked for more softening. Exponent 1.6 → 1.3 at 190 ms: first-frame
  step 51 px → 42 px, last third 54 px → 77 px, so the pace is nearly even while still easing into
  the target. Guard retuned; suite 16/16 green. Outcome: Converged.
- Pass 7, 2026-11-19 — the owner noted the exponent changes achieved nothing: duration was still
  190 ms. Re-based the problem: discovered a self-contained tuning harness (`preview/tune-built.html`,
  built by `build_tune.py` from real dock CSS) that plays two candidates side by side, at 1× or
  slowed, with per-frame speed traces. Applied the smoother candidate to the product — 400 ms sine
  in-out for glides and the crossing morph, the operator's own toggle left at 230 ms ease-in-out.
  Live steps now `2, 5, 8 … 24 … 5, 2` px over 24 frames with 0 px off target; E2E waits and the
  motion guard retuned, suite 16/16 green. This is a candidate for the owner to compare in the
  harness, not a final comfort verdict. Outcome: Converged, pending owner's pick.
- Pass 8, 2026-11-19 — owner asked for a little more easing at both ends. Blended the 400 ms sine
  in-out curve 50/50 with quintic smootherstep: first/last frame 2 px → 1 px, peak frame 24 px →
  27 px, still 24 frames and 0 px off target. Added a `sine 400` preset beside `smooth 400` in the
  harness so the two curves can be compared directly. Suite 16/16 green. Outcome: Converged,
  pending owner's pick.
- Pass 9, 2026-11-19 — owner required that opening a service already on the projector and overlay
  re-enters following. FR-014 was narrowed to exclude the on-air case and FR-015 added; `openService`
  now sets following before the rows are painted and `loadServiceData` centres once after `sync()`.
  The new E2E was red on the mode flag and then on the missing centre; a first draft also projected
  screen 0 (unreachable from the list top), fixed by placing a deep screen. 17/17 green. Outcome:
  Converged.
- Owner acceptance, 2026-11-19 — the owner accepted the slice as it stands: the 400 ms soft in-out
  re-centre (the *smooth 400* candidate in the harness) and following on opening the on-air service.
  No push, PR, merge, version bump or card closure is authorised by this word.
