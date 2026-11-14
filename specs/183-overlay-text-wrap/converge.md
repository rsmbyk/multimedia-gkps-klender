# Converge: the overlay's text wraps inside the box that owns it

**Slice**: `specs/183-overlay-text-wrap` · **Traceability**: [`plan.md`](./plan.md)

## Pass 1 — 2026-11-02

**Checked**: every row of `plan.md`'s traceability table, by the method it declares — the seven
functional requirements, the six success criteria and the story scenarios — against the working tree
(one declaration in `static/styles/design/obs-overlay.css`, one test module, no other code touched),
then the two modules' own runs and the probe's numbers.

**Evidence**

| Check | What it returned |
| --- | --- |
| `manage.py test tests.e2e.test_obs_overlay_wrap` | `Ran 7 tests … OK` (19.57s) |
| `manage.py test tests.e2e.test_obs_overlay tests.e2e.test_obs_overlay_wrap` | `Ran 17 tests … OK` (48.97s) — the 119/180 module untouched and green |
| the same module on the unfixed sheet (`git stash` of the one file) | 3 failures: 733.85px and 747.48px of body ink past the plate, and `'normal' != 'break-word'` |
| `preview/probe.py --size 1920x1080` / `--normal` | after: 32.22 / 24.39px **inside** the plate; before: 710.45 / 722.08px past it |
| `preview/probe.py --size 1280x720`, `960x540` | after: inside at both; before: 433.95 / 438.70 and 355.22 / 302.03px past |
| controls at all three frames | 823.72×201.13, 652.80×139.94, 548.14×135.06, 435.19×94.28, 419.34×102.02, 326.39×71.44 — identical in both builds |
| sheet diff | `static/styles/design/obs-overlay.css`: one declaration inside the `.obs-overlay__line` block |

**Findings**: none against the table — 13/13 rows held, by the method each declares. One correction
inside the slice's own tooling, recorded because it changed a number before it reached the spec:
`probe.py`'s first pass measured a text element's ink against **its own box less the plate's padding**,
which reported a false 23.4px spill on a control state; the measurement was corrected to compare ink
with the element's own edge (and, separately, with the plate's).

**Outcome**: converged for the scope it was written against — the plate's body. The owner then widened
that scope at gate 2, so this pass is **superseded**, not final.

## Pass 2 — 2026-11-02 (after the scope widened)

**Checked**: the same table, rewritten for the wider scope — FR-001 across the body, the words column,
the kicker, the title and the caption; FR-006 the caption's own look; SC-001 seven states; SC-006 the
caption's weight, centring and balance — against the working tree, with the tests and the preview
rebuilt rather than trusted.

**Evidence**

| Check | What it returned |
| --- | --- |
| the wider cases written first, on the body-only sheet | 4 failures: caption ink **2,035.20px** past its box, verse title **230.79px** past the plate, and `'normal' != 'break-word'` on the stage — the red run that justifies moving the declaration |
| the module after the move (`stage`) | `Ran 9 tests … OK` |
| both modules | `Found 19 test(s) … Ran 19 tests in 53.990s … OK` |
| `preview/probe.py`, `--size 1920x1080` / `--normal` | after, every state **inside**: report −32.22, pasted link −24.39, caption 0 (5 rows, 403.19 tall), title −28.5 (3 rows), passage body −26.47, kicker 0 (963.44 × 139.94) |
| the same at 1280×720 and 960×540 | caption 1,336.81 → inside (268.75 tall) and 1,017.61 → inside (201.56); title 178.59 → inside and 104.69 → inside; every other state inside |
| controls and the kicker at all three frames | 823.72×201.13, 652.80×139.94, 548.14×135.06, 435.19×94.28, 419.34×102.02, 326.39×71.44, 963.44×139.94, 642.95×94.28, 480.70×71.44 — identical in both builds |
| review page | seven states, deep links, no console error; caption reads `4 r · 2,035.20px past` before and `5 r · inside` after, title `2 r · 231.78px past` → `3 r · inside` |
| sheet diff | one declaration moved from `.obs-overlay__line` to `.obs-overlay__stage`, with the comment rewritten; nothing else in the sheet |

**Findings**

| # | Type | Finding | Disposition |
| --- | --- | --- | --- |
| 2 | contradicts → code at fault | the first pass's own pinning test asserted the caption and the heading compute `normal`; the widened scope contradicts it | fixed: the test is deleted and replaced by `test_song_caption_wraps_its_long_run`, `test_a_passage_heading_wraps_its_long_run` and `test_the_rule_is_inherited_from_the_stage` |
| 3 | partial → code at fault | the kicker case asserted a second row; a 64-character kicker at `.5em` cannot outgrow the plate, so the assertion described a state that cannot exist | fixed: the case asserts ink and the plate's growth, and research D007 records why |
| 4 | — | No remaining gap: 7/7 requirements, 6/6 criteria and every story scenario hold by their declared method | — |

**Outcome**: converged again, for the wider scope — no `missing`, `partial`, `contradicts` or
`unrequested` gap. Fold may run.
