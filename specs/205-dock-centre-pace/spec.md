# Feature Specification: the dock's re-centring keeps pace with fast advancing

**Slice**: `specs/205-dock-centre-pace`
**Branch**: `fix/205-dock-centre-pace`
**Created**: 2026-11-19
**Status**: Accepted (Gate 1, 2026-11-19)
**Input**: the owner's report, 2026-11-19 — "the centering when advancing in following mode should be
faster and less easen to reduce the screen going up and down when advancing fast enough"

Spec 200 settled the re-centring at **400 ms on a softened in-out** (half sine, half quintic
smootherstep) — tuned *up* from an earlier 190 ms ease-out during that slice's review, because a
single move read smoother with the flatter ends. That tuning optimised the **single-move** case.
This slice is the opposite condition: **advancing faster than the glide completes**. Each advance
cancels the running glide and restarts it from `t = 0`, and the softened ease-in means every restart
begins near zero velocity, so the list lags the live row and the row's offset oscillates — the
"up and down" the owner sees. The fix is the two knobs he named: a shorter pace and a less flattened
curve.

## User Scenarios & Testing

### US1 — Fast advancing keeps the live row near the middle (P1)

**Why this priority**: the operator steps through a service quickly during a live run; the list
bobbing up and down on every step is the reported defect and makes the dock hard to read while
advancing.

**Independent Test**: on the live dock with a service on air and following on, press ArrowDown
repeatedly at a fast cadence (120–300 ms) and sample the live row's offset from the scrollport centre
each frame; the mean offset during the sequence is smaller than on develop, and each single move
still lands 0 px off with no direction reversal.

**Acceptance scenarios**

1. **Given** the dock is following and a service is on air **When** the operator advances one screen
   **Then** the live row glides to the centre over ~200 ms on a sine in-out, landing 0 px off, with no
   direction reversal.
2. **Given** the dock is following **When** the operator advances 12 times at 120 ms cadence **Then**
   the mean live-row offset during the sequence is below develop's (measured 13.7 px vs 16.0 px), and
   the largest single-frame scroll step is below develop's (100 px vs 148 px).
3. **Given** the dock is following **When** the operator advances at 200 ms or 300 ms cadence **Then**
   the mean offset is below develop's at the same cadence (9.4 vs 14.6 px; 6.6 vs 11.9 px).
4. **Given** an advance crosses into another entry **When** the crossing morph runs **Then** its
   carried scroll uses the same 200 ms sine, so expand, collapse and scroll remain one motion.

### US2 — The single move stays smooth and the hand toggle is untouched (P2)

**Why this priority**: the pace must not make a single centring read as a snap, and the operator's
own block toggle is a different motion the owner did not ask to change.

**Independent Test**: press the centre control from a scrolled-away list and sample the glide; the
first and last frames are well below the peak frame (the E2E deceleration guard), and a hand
header-toggle still morphs over 230 ms on its own ease-in-out.

**Acceptance scenarios**

1. **Given** the live row is off the middle **When** the centre control is pressed **Then** the glide
   starts and finishes slowly relative to its middle (sine in-out), lands 0 px off, 0 reversals.
2. **Given** any re-centre **When** `prefers-reduced-motion: reduce` is set **Then** it is an instant
   jump, unchanged.
3. **Given** the operator clicks a non-live entry's header **When** its block toggles **Then** the
   height morphs over 230 ms on `easeInOut`, unchanged by this slice.

### Edge Cases

- **When** the list is clamped at an end **Then** the centring clamps as before; no motion past the end.
- **When** a wheel or pointerdown lands mid-glide **Then** the glide is cancelled and following ends,
  unchanged.
- **When** advances come faster than 200 ms **Then** the glide still retargets mid-flight; the shorter
  pace and less flattened ease-in reduce the lag but do not eliminate the per-crossing collapse clamp
  (see Assumptions — that reversal is a separate mechanism).

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | Every re-centre — `glideScroll`, `glideRow`, and the crossing morph's carried scroll — SHALL run over **200 ms** on a **sine in-out** curve (`ease(t) = ½ − cos(πt)/2`), replacing spec 200's 400 ms half-sine/half-smootherstep blend. The three paths SHALL read one shared duration constant and one shared curve so expand, collapse and scroll remain one motion. | `dock/R15` (modified) |
| FR-002 | The operator's hand block-toggle SHALL keep its own 230 ms `easeInOut` height morph; this slice SHALL NOT change it. | `dock/R14` (unaffected) |
| FR-003 | The reduced-motion instant path, clamping at the list's ends, and cancellation by a hand on the list SHALL be unchanged. | `dock/R15` (unaffected) |

### Success Criteria

| ID | Criterion | Verification |
| --- | --- | --- |
| SC-001 | A single centring lands 0 px off the scrollport centre with 0 direction reversals, over ~200 ms. | Live probe (`preview/probe.py`, single-move): landing_off 0, reversals 0, ~12 moving frames vs develop's ~22. |
| SC-002 | Under rapid advancing the mean live-row offset and the largest single-frame scroll step are below develop's at the same cadence. | Live probe rapid runs at 120/200/300 ms: mean_off 13.7/9.4/6.6 px vs 16.0/14.6/11.9; max_step 100/82/80 px vs 148/99/88. |
| SC-003 | The single move still decelerates into its target (sine shape), so the existing E2E guard passes. | `tests/e2e/test_obs_dock_follow.py::test_the_centring_decelerates_into_its_target` — first/last step < 0.35 × peak. |

## UI/UX

`live preview at http://127.0.0.1:8765/obs/dock` — the real dock served from this worktree (the
change is motion on the live list, so a static replica cannot show it). Fixture: the service
**Ibadah Pace Probe** (60 one-screen TEXT entries, list overflow 1873 px in a 420 × 900 pane), so
every ArrowDown crosses into the next entry. Measured by `preview/probe.py` (fresh per-frame reads;
raw frames in `preview/shots/`), dark mode at 1×:

- **Single move** (centre control from the list's end, ~940 px): develop's 400 ms softened in-out
  samples 22 moving frames, steps `8, 15, 22, 31, … 68 … 23, 15, 8, 2` px (flat both ends); the
  slice's 200 ms sine samples 12 moving frames, steps `16, 45, 70, 93, 109, 116, 117, 107, 94, 71,
  45, 15` px — a quicker start, a faster middle, half the frames. Both land 0 px off, 0 reversals.
- **Rapid advancing** (12 ArrowDowns = 6 crossings), mean |offset| during the sequence:
  120 ms cadence **16.0 → 13.7 px**; 200 ms **14.6 → 9.4 px**; 300 ms **11.9 → 6.6 px**.
  Largest single-frame scroll step: 120 ms **148 → 100 px**; 200 ms **99 → 82 px**; 300 ms **88 → 80 px**.
- **Unchanged by this slice**: peak drift 33 → 32 px and the per-crossing scroll reversal count
  (9 → 9). Each crossing still scrolls up ~105 px then clamps back ~65 px as the departing block
  collapses — the collapse clamp, a separate mechanism from the glide pace (Assumptions).
- **Hand toggle**: 230 ms `easeInOut`, untouched.

## Assumptions

- **200 ms + plain sine is the proposed candidate**, chosen as the minimal delta from spec 200:
  halve the pace and drop the smootherstep half (the "extra" ease), keeping the in-out character the
  owner approved. The duration and curve are the iteration knobs — the owner judges the live preview
  at gate 1 and may ask for faster, slower, or less/more eased; a correction there is a preview-stage
  change, not a new requirement.
- **The crossing morph shares the pace and curve** because R14/R15 require expand, collapse and
  scroll to read as one motion; giving the glide a different pace from the morph would reintroduce a
  phase boundary. The hand toggle is excluded — it is a separate motion (R14) the owner did not name.
- **The per-crossing collapse-clamp reversal is out of scope.** The 9 direction reversals under fast
  advancing come from the departing block shrinking the scroll range and the browser clamping
  `scrollTop` mid-morph, not from the glide's ease. They are unchanged here; if the owner's "up and
  down" is that jerk specifically, the next knob is the crossing morph, recorded as a follow-up.
- The fixture's TEXT entries carry two screens each, so 12 ArrowDowns advance 6 entries (30 → 36);
  the probe reports `live_end` to confirm the advances landed.