# Research: song-row focus ring is clipped at the list top

**Spec**: `specs/223-songrow-focus-ring-clip/spec.md`
**Unknowns remaining**: 0

## D001 — The browser paints the ring, and the scrollport clips it

- **Decision**: treat the outline as the browser's UA default; change only the space available to it.
- **Rationale**: `components.css` at both the original base `bb7c1887` and the re-based base
  `e8e79dbb` has no `.songrow:focus-visible` rule. At 900×700
  the first row and `#chBody` both start at y=130, `padding-top` is `0px`, and the computed outline
  is `auto 1px rgb(16, 16, 16) 1px` — 2px of ring above the row, outside the scrollport. A pixel diff
  before/after focus shows changed pixels from y=130 down and none at y≤129: only the ring's top edge
  is missing, and the list is not scrolled (`scrollTop = 0`, `scrollHeight = clientHeight = 570`).
- **Alternatives considered**: scrolling the list — impossible at the top and wrong even if it
  worked; adding a `:focus-visible` rule that moves the ring inside (candidate B) — a different state
  rule that also restyles every row, left in the preview but not accepted; removing `overflow` — would
  break the list's scroll contract.
- **Provenance**: research — browser probes on `bb7c1887` (`:8766`) and slice 223 (`:8767`); code read
  of `components.css:1663-1698`.

## D002 — Candidate A is in scope

- **Decision**: reserve 3px of top space in the scrollport and keep the UA outline. Candidate B
  (inset 2px `--focus` ring) remains a preview comparison only.
- **Rationale**: the Clarify question for the choice timed out. SDD-08 turns a skipped question into
  a recorded assumption using the recommendation; the recommendation was A, and the spec records
  that B can be reopened at gate 1. Gate 1 was accepted on that basis.
- **Alternatives considered**: B — rejected at this stage by the recorded assumption, not by a
  measurement; asking again — the same question had already timed out once.
- **Provenance**: owner decision — gate 1 Accept 2026-11-22 on the spec carrying the skipped question.

## D003 — The space belongs on `.ch__body`, not on `#chList`

- **Decision**: change `.ch__body`'s padding from `0 0 8px` to `3px 0 8px`.
- **Rationale**: `.ch__body` is the scroll container: `overflow-y: auto`, `padding-bottom: 8px`, and
  its top edge is the clipping boundary. `#chList` is the `ul` inside it; padding there would also
  work for song rows but would miss the chapter list that shares the same scrollport, and would
  duplicate the padding concept in two places. One declaration on the owner of the clip covers both.
- **Alternatives considered**: `scroll-padding-top` — affects scroll-snap and programmatic scrolling,
  not a row already flush at scrollTop 0; `outline-offset` override — restyles the ring (candidate B);
  `margin-top` on the first row — changes the 1px pitch and the list's own geometry.
- **Provenance**: research — measured `getComputedStyle` and bounding boxes on the live page; code
  read of `components.css:1663-1683`.

## D004 — The E2E asserts geometry, not screenshot pixels

- **Decision**: assert `row.top - host.top >= outlineWidth + outlineOffset` (with the computed
  outline still `auto`), plus `scrollTop = 0` and `scrollHeight === clientHeight`; keep the before/after
  pixel diff in the preview as the human-visible proof.
- **Rationale**: the requirement is that the painted ring fit inside the scrollport. For an outside
  outline the painted top edge is exactly `outlineWidth + outlineOffset` above the row, so the
  inequality is the browser's own geometry, not a hard-coded y coordinate. A screenshot assertion
  would need a PNG decoder in a Python test and would be fragile at three viewports.
- **Alternatives considered**: assert `:focus-visible` — true both before and after the fix, proves
  nothing; assert a literal `padding-top: 3px` — tests the mechanism rather than the behaviour and
  would pass a wrong implementation; full screenshot diff — heavy and unreadable as a unit assertion.
- **Provenance**: research — the pixel-diff probe in `probe3.py` (3px injected control) and the
  measured `auto 1px … 1px` outline.

## D005 — A new E2E module with its own fixtures

- **Decision**: `tests/e2e/test_songrow_focus_ring.py` on `StaticLiveServerTestCase`, creating one
  `songs.Book` and several `songs.Song` rows per test, then opening `reverse('web-song', args=[pk])`.
- **Rationale**: `tests/e2e/test_reading.py` already owns the reading page's broad behaviour with its
  own fixtures; a small module keeps the three focus cases together and independent. No existing
  module owns song-row focus geometry.
- **Alternatives considered**: adding cases to `test_reading.py` — buries three tightly related cases
  in a 2,600-line module; using the shared database's song 1820 — a test would depend on local data.
- **Provenance**: research — `tests/e2e/test_reading.py:59-77`, `multimedia/web/reading/urls.py:6-9`.

## D006 — `bump: patch`

- **Decision**: `patch` — 1.36.8 → 1.36.9, applied in the pre-merge commit and re-checked against
  `origin/develop` then.
- **Rationale**: a defect fixed on a shipped surface; VER-10 maps a fix to `patch`.
- **Alternatives considered**: `minor` — no new capability is offered; `none` — a user-visible
  behaviour changes, which VER-05 excludes.
- **Provenance**: versioning rules VER-03, VER-04, VER-10; `VERSION` at `1.36.8` on `origin/develop`
  after slice 221 merged and this branch was re-based. The original base was `1.36.7`; the level is
  unchanged, only the number moved.
