# Feature Specification: A Go To still names itself with no service under it

**Slice**: `specs/227-goto-cue-empty-service`
**Branch**: `fix/227-goto-cue-empty-service`
**Created**: 2026-11-23
**Status**: Accepted (Gate 1 2026-11-23)
**Input**: "when you open a goto when the projector window has no service or the service has no entries, the cue does not display the goto information (passage, song) and its related controls"
**Demand**: `ITEM-242`
**Capability**: modifies `projector/R2`

## User Scenarios & Testing

### US1 — The corner cue belongs to the Go To, not to the service beneath it (P1)

**Why this priority**: the operator drives the corner cue — it names what is on air and carries
the translation flip, bait keys and Back. A Go To is defined as standing alone when the projector
has no service, and a service may hold no entries at all. In both cases the detour paints, but the
cue is blank, so the operator loses the passage or song label and every control that goes with it.
This is the only behaviour the report asks to change.

**Independent Test**: open `/projector` with no service (or `/projector?service=<empty>` for a
service with no items), press `g`, choose a passage or a song, and read the cue. The prefix names
the chosen content, a passage offers its translation flip, a song offers one bait key per bait,
and Back reads `back to service`. Closing the Go To returns the empty stage and its notice.

**Acceptance scenarios**

1. **Given** a projector opened without `?service=` and no stored service **When** a passage Go To
   starts **Then** the cue prefix names the passage, the translation flip shows its edition, and
   Back reads `back to service`.
2. **Given** a projector opened for a service with no entries **When** a song Go To starts **Then**
   the cue prefix names the song and one `.cue-bait` per bait is drawn.
3. **Given** a Go To is up with no entries underneath **When** a step or bait jump is made **Then**
   the cue keeps naming the Go To and its buttons keep working.
4. **Given** the Go To is closed with Back **When** the service still holds nothing **Then** the
   empty notice returns and the cue falls back to its blank, entryless state.
5. **Given** a service with entries **When** a Go To starts and ends **Then** the cue behaves
   byte-for-byte as before — the change adds no branch for the populated case.
6. **Given** a Go To started from the dock or a reading page **When** the projector shows it with
   no entries **Then** the cue is the same as for one started on the projector.

### Edge Cases

- A projector with no stored state at all, and one whose stored state names no service, both
  paint no screens; neither may suppress the Go To's cue.
- A service that holds only templates has no projector screens; it takes the same path as an empty
  service.
- The empty-service notice is a sibling of the stage, not a screen; its visibility must not be
  used as a proxy for whether the cue may render.
- A running cue label (an untitled text entry) cannot exist with no entries, so clearing those
  labels before the detour branch is inert in this state.

## Requirements

### Functional

| ID | Requirement | Capability |
| --- | --- | --- |
| FR-001 | A Go To detour SHALL paint the corner cue when the projector holds no screens, whether because no service is open or because the service has no entries. | `modified: projector/R2` |
| FR-002 | The detour cue SHALL show the Go To's label, its translation flip for a passage, its bait buttons for a song, its screen progress and a Back control naming the service. | `modified: projector/R2` |
| FR-003 | The check for a detour SHALL run before any early return caused by an empty entries list; the populated service's cue path SHALL be unchanged. | `modified: projector/R2` |
| FR-004 | Closing the Go To over an empty service SHALL restore the empty notice and leave no Go To controls in the cue. | `modified: projector/R2` |
| FR-005 | No new state, message, endpoint or template SHALL be introduced; the Go To remains the one field of `gkps-display`. | `modified: projector/R2` |

### Key Entities

None. The change is the order of two guards in an existing render function.

## Success Criteria

| ID | Criterion | How it is measured |
| --- | --- | --- |
| SC-001 | With no service, a passage Go To's cue names the passage and offers its flip and Back. | Playwright read-back of `#cue-prefix`, `.cue-translation` and `#cue-next-name`. |
| SC-002 | With an empty service, a song Go To's cue names the song and offers one bait button per bait. | Playwright read-back of `#cue-prefix` and `#cue-baits .cue-bait`. |
| SC-003 | The populated-service cue, the detour's stage and the empty notice are unchanged. | The 23 pre-existing tests in `test_goto_shared_state` and `test_dock_goto` stay green. |

## UI/UX

`live preview at http://127.0.0.1:8765/projector` — the slice worktree's own server, code and assets;
open `/projector`, press `g`, search a song and press Enter. The harness is
`specs/227-goto-cue-empty-service/preview/probe.py` (`--base`, `--query`), which reads the cue from
the live route.

- **Before (measured, Playwright at 420×800, unfixed code)**: both new tests fail on
  `AssertionError: 'Matius 5' not found in ''` and `AssertionError: 'NKB 43' not found in ''` —
  `#cue-prefix span` is empty, `#cue-prefix .cue-translation` is absent, `#cue-baits .cue-bait`
  counts 0 and `#cue-next-name` is empty while `.projector-detour.is-active` paints the content.
- **After (measured, 420×800)**: the cue sits at (32, 756) 280 × 24; the prefix at (73, 756)
  259.6 × 24 reads `HAL 1 Jahowa Sihol Pujionku ·`; seven `.cue-bait` buttons read `1`–`7`; the
  Back control at (502.9, 761) 129 × 16 reads `back to service`. A passage in the E2E fixture
  reads `Matius 5… ·` with a `TB` flip.
- **Typography and colour**: unchanged — the cue uses the product's own `.cue`, `.cue-bait`,
  `.cue-translation` and `.cue-next` rules; no new token, face or size.
- **States**: no service; service with no entries; service with entries; passage; song; Back;
  dock- and reading-started Go To.
- **Motion**: none added or removed.
- **Responsive**: the cue is the same DOM at every viewport; no new fixed-size box.

## Assumptions

- The cause is guard order in `static/web/projector.js` `renderCue()`: the empty-stage early
  return precedes the `if (detour)` branch, so a Go To over zero screens never reaches
  `renderDetourCue()`, which already handles a missing return entry by naming `service`.
- The fix is to check `detour` first, keep `clearRunningCueLabels()` ahead of it, and move the
  entries check below; no other file needs to change for the visible defect.
- `renderDetourCue()` needs no edit: `entryAt(current)` returns null when there are no screens,
  so Back reads `back to service` without a special case.
- The two new tests are pinned in `tests/e2e/test_goto_shared_state.py` because that module owns
  the shared Go To state and already has a no-service fixture.
- The bump is `patch`; the version is applied at delivery, not in the implementation commits.

## Clarifications

No open questions. Zero clarification markers remain.
