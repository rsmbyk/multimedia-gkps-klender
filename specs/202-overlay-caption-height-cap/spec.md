# Spec 202: Height-bound song caption type

- **ID:** 202
- **Status:** Accepted — owner, 2026-11-19 (the plan was accepted in conversation; this pack records it)
- **Item:** ITEM-209
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

The song caption's font size is bounded by the **stage height**, not its width. At rest it is 5 % of
that height. A lyric whose lines wrap shrinks the type until the block fits two visual rows, but the
type never goes below 2 % of the stage height. At the floor the fit stops even if the block still
exceeds two rows — the text was simply too long.

## Scope

### In scope

- The song caption's rest size in `obs-overlay.css` and the fit floor in `obs-overlay.js`.
- The capability rule and scenarios in `docs/spec/overlay.md` R2.
- E2E coverage at 1920×1080 and 1280×720, including the floor edge.

### Out of scope

- The passage and liturgy plates (their own `cqw` scale is unchanged).
- The projector's lyric fitting (`projector.js` `fit()`) and spec 091.
- Truncation of lyric text: the caption never drops lines or adds an ellipsis.

## Domain rules

- **Rest is 5 % of stage height.** `font-size: 5cqh` on `.obs-overlay__caption`.
- **Fit never goes below 2 % of stage height.** The floor is measured against the stage on each
  paint, not fixed at 11px.
- **Two rows is the target, not a guarantee.** If the floor is reached first, the block lands as it
  lands.
- **Only font-size changes.** Weight, outline, inset, centring and balanced lines are untouched.

## Acceptance scenarios

### Scenario: the rest follows the height
- **Given** a two-line lyric with no wrap need
- **When** it is on air at 1920×1080
- **Then** the caption's computed font reads 54 px and the block is 1728×151.2 at (96, 874.8)
- **When** it is on air at 1280×720
- **Then** the font reads 36 px

### Scenario: a wrapping lyric shrinks but stays above the floor
- **Given** a lyric too wide for the caption box at 54 px
- **When** it paints at 1920×1080
- **Then** the type shrinks by 4 % of the rest size per step (15 steps to the floor) until the block fits two visual rows, and never reads
  below 21.6 px

### Scenario: a lyric the floor cannot save
- **Given** a lyric that still exceeds two visual rows at 21.6 px
- **When** it paints at 1920×1080
- **Then** the type stops at 21.6 px and the block may exceed two rows

## Functional requirements

| ID | Requirement | Source |
| --- | --- | --- |
| FR-001 | The caption's resting `font-size` SHALL be `5cqh` | new |
| FR-002 | `fitCaption()` SHALL floor the type at 2 % of the stage's height per paint | `overlay/R2` modified |
| FR-003 | A screen that already fits two rows SHALL paint at the rest size with no fit carried over | `overlay/R2` |
| FR-004 | The fit SHALL change only `font-size` | `overlay/R2` |

## Success criteria

| ID | Criterion | Verification |
| --- | --- | --- |
| SC-001 | At 1920×1080 the rest font is 54 px ± 0.5; at 1280×720 it is 36 px ± 0.5 | E2E `tests/e2e/test_obs_caption_height.py` |
| SC-002 | A wrapping lyric shrinks below 54 px, never below 21.6 px, and lands within two rows | same |
| SC-003 | A lyric that cannot fit at 21.6 px stops there, with rows > 2 | same |
| SC-004 | The passage and liturgy plates keep their `cqw` scale | `tests/e2e/test_obs_overlay.py`, `test_obs_overlay_wrap.py` |

## UI/UX

- Rest 54 px at 1920×1080 (`5cqh`), 36 px at 1280×720, 108 px at 3840×2160.
- Floor 21.6 px at 1920×1080 (`2cqh`), 14.4 px at 1280×720.
- Caption box stays 90 % of the stage width (1728 px at 1920), anchored at 5 % insets.
- Preview: live — the E2E suite measures the real overlay at the two reference viewports; the
  numeric output is quoted in `converge.md`.

## Assumptions

- The OBS browser source is the container: `cqh` and `stage.clientHeight` resolve to the same height.
- The owner's "5 % / 2 %" means the font size, not the block height; the two-line target still
  governs the block.
- No separate static preview page was produced; the acceptance was given on the plan and numbers in
  conversation, and the live E2E measurement is the evidence.

## Traceability

- E2E: `tests/e2e/test_obs_caption_height.py`; existing overlay suites for no-change rows.
- Implementation: `static/styles/design/obs-overlay.css`, `static/web/obs-overlay.js`.
- Capability: `docs/spec/overlay.md` R2.
