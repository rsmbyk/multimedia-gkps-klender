# Plan 055: Give each entry a containing box with centred words and equal add-row gaps

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-057
- **Bump:** patch

## Why

Live review of `/tatib/142/` (2026-10-11) showed the pane's vertical model is still wrong after
specs 052–054: the start bar is parked above the first entry (37.6px at rest), a revealed add row
puts its buttons 4px under the entry above but 84px over the words below (the row's 10px padding
plus the next heading's 30px margin), and the 44px band (spec 053) inflates every entry with dead
space while its own controls still float over the words on tall entries. The owner's four rules —
the gaps include the control buttons, the gaps look equal, the words are centred, the controls
float at the top-right — cannot all hold while the band exists or while the row margins stay
asymmetric. One model satisfies all four: the entry is a **box containing its controls**
(min-height 52px = 8 + 36 + 8), the words centre inside it, every revealed add row keeps 8px to
the boxes above and below, and the start bar collapses and reveals like the other rows.

## Scope / edges

**In:**

- The containing box: `.tatib__item--acts` flex column, centred, `min-height: 52px`, no band.
- Add rows: rest margins `6px 0` (uniform 12px box-to-box, measured); revealed `padding: 8px 0`
  with `margin-block: 0` → 8px above and below the buttons in every reveal state.
- The start bar: collapse rules mirroring `.entry__add`, plus an `entries.js` sync (the bar is a
  *preceding* sibling — CSS cannot reveal it) and a `.entry__start-inner` wrap in the template.
- The divider (`.tatib__eos`) takes the same box: margins 0, rule at centre, note under it.
- Touch media rules extended to the bar; E2E rewrites and new assertions.

**Out:**

- The controls' look, their `top: 8px; right: 8px` spot, reveal/touch triggers (033/034/052).
- Link colours (spec 056). The editors-off pane (`.tatib__item + .tatib__item` stays 2px).
- Other panes and the empty-service block.

## Approach

- Box: `.tatib__item--acts { display: flex; flex-direction: column; justify-content: center;
  min-height: 52px; padding-top: 0; }` with the first/last flow-child margins zeroed; replaces
  053's `padding-top: 44px`. Controls keep `top: 8px; right: 8px` — inside the box, at its
  vertical centre (8 + 35.6 + 8.4 ≈ 52).
- Rows: `.entry__add { margin: 6px 0; }` at rest; revealed `padding: 8px 0; margin-block: 0;`.
  Every reveal selector already exists (adjacent-sibling, `:hover`, `:focus-within`,
  `is-revealed`); only the geometry changes.
- Bar: `.entry__start` collapse rules mirroring `.entry__add` (grid `0fr`, clipped inner,
  opacity) plus `margin-top: -30px` while revealed (cancels `.read__head`'s 30px margin) →
  measured 8px under the heading, 8px above the first words. Reveal triggers: `.is-revealed`
  from `entries.js` (extend the neighbours handler: the bar reveals while the pointer or
  keyboard focus is on the bar or the first entry), plus `:hover` / `:focus-within`; the
  template wraps the five buttons in `.entry__start-inner` (copy the `.entry__add-inner`
  pattern).
- Divider: `.tatib__eos { display: flex; flex-direction: column; justify-content: center;
  min-height: 52px; margin: 0; border-top: 0; }`; the rule drawn by `::before`, the diamond at
  the box centre (`translate(-50%, -50%)` at `top: 50%`), the note absolutely pinned at
  `top: calc(50% + 7px)`.
- The existing coarse-pointer media block gains the bar (and keeps the rows).

## TDD

- Domain/app tests: N/A (pane layout; no server data).
- E2E (Playwright via `LiveServerTestCase`): rewrites in `tests/e2e/test_tatib_entry_controls.py`
  — `test_the_controls_never_sit_on_the_words` → containment + centring; `…item_height_includes…`
  → the 52px box; `…band_tracks…` → `min-height: 52px` and `padding-top: 0px`; `…reserve_no_space`
  → uniform 12px rhythm, rows/bar 0-high; `…settles…` re-bound. New: start bar collapse/reveal
  (8/8), a gap-equality audit across first entry / card / one-liner / divider / focus (8/8),
  a centring audit (top ≈ bottom), the divider box (also `test_tatib_section_break.py` — margins
  0, rule centred), and `test_reorder.py`'s start-bar test reveals the bar before clicking.

## Risks

- **Tall entries.** No band means the floating controls overlay the first line(s) of a tall
  entry while shown — without that, "centred words + no reserved band + top-aligned floating
  controls" cannot coexist. Owner saw exactly this in the approved preview.
- **Existing assertions.** The 44px band, the 10px row padding, the 16px break margins and
  "start bar always visible" are encoded in E2E; all are rewritten red-first, not re-run.
- **Editors-off rhythm.** The on/off comparison changes (on: 12px; off: 2px); the old delta
  assertion is replaced by an absolute on-state assertion.
- **First-hover motion.** Opening the bar moves the first entry down once by the bar's revealed
  height minus the heading's 30px margin — 13.6px on one line, 47.2px when the buttons wrap
  (the test-width case) — then it stays put; the pointer path re-targets once at most, same as
  the spec-052 divider case.
