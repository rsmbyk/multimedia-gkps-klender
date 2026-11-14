# Convergence: the overlay reads by kind

**Spec**: `specs/180-overlay-text-styles/spec.md`
**Passes**: 2 of 3

Every row was checked by the method the plan declared for it: `test` rows by running the suite that names them,
`inspection` rows by measuring the live page at 1920×1080 on service 144 (`Ibadah Minggu`, 25 Oct 2026) or, where a
screen does not exist in that service, on the preview state the spec cites.

## Pass 1 — 2026-10-30

### Checked by test — 20 rows

`tests.e2e.test_obs_overlay` (10) + `tests.e2e.test_obs_dock` (5) + `multimedia.web.test_obs_dock` (1) +
`multimedia.web.tests.ServiceProjectorTests` (the payload test) run together: **Ran 26 tests … OK**. The rows they
carry are FR-001…FR-004a, FR-007…FR-013, SC-003…SC-007, US1/AC2, US2/AC5, US3/AC3, US3/AC5.

### Checked by inspection — 6 rows

| Row | What was measured | Result |
| --- | --- | --- |
| FR-005 | `.obs-overlay__plate` fill and border on the live page | `rgba(10,12,16,.88)`, `1px rgba(255,255,255,.12)` — matches |
| FR-006 | insets, min/max width, type scale | `left/right 96px`, `bottom 54px`, `min-width 34%`, `max-width 90%`, `font-size 36px` — matches |
| SC-001 | the caption's box at 1920×1080 | **1728×202 at (96, 824)**, 72 px, weight 800, transparent fill — matches |
| SC-002 | the passage card's box | **1728×238 at (96, 788)**, 36 px / weight 500 — matches |
| SC-002a | the liturgy panel's box | **1555×201 at (182, 825)** titled, **1553×145** untitled — the spec said 1544×201 at (188, 825) (see G1) |
| US1/AC3, US2/AC4 | the reference-only and single-answer states | preview states 3 and 7: no empty title, no orphan hairline, answer panel 653×83 — matches |

Reduced motion (US3/AC4): with `prefers-reduced-motion: reduce` emulated, a panel arriving fires **no**
`animationstart` and carries no motion class — it paints as a cut, as required.

### Gaps

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| G1 — the liturgy panel's recorded box is 9–11 px narrower than it paints, and its x is 6 px off | `contradicts` (spec at fault) | SC-002a | live page and preview state 5 both paint 1555×201 at (182, 825); the spec's 1544×201 at (188, 825) predates the last padding pass |
| G2 — service 144 has no *titled* liturgy screen, so SC-002a's number was taken from preview state 5 rather than from the live service | `partial` (evidence, not behaviour) | SC-002a | a scan of screens 20–83 of service 144 found no plate carrying a kicker; the titled case exists only in the preview, whose markup and stylesheet are the product's own |

**Root causes**: G1 is the spec's — a stale measurement, corrected mechanically (see below). G2 is neither: the
behaviour is right, the evidence source is named instead of implied.

**Outcome**: both resolved before pass 2 — G1 corrected in `spec.md` (`## UI/UX` and `SC-002a` now carry 1555/1553),
G2 recorded here as the named source of that row's evidence. No task appended for either, because no code changed.

## Pass 2 — 2026-10-30

Re-checked the two touched rows: the liturgy panel measured again at 1920×1080 (1555×201 at (182, 825) with a title,
1553×145 without) and the spec read back to confirm both places carry it. The remaining 25 rows are untouched by the
correction and keep their pass-1 evidence.

**Outcome**: Converged — nothing remains.

## Accepted gaps

`none` — no gap was carried to the owner, so nothing is excluded from Fold.

## Cap reached

`n/a` — two passes, no third needed.
