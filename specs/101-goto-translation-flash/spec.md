# Spec: Brighten the translation label after flipping a Go To passage

- **ID:** 101
- **Status:** Accepted
- **Item:** ITEM-101
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** patch

## Intent

When an operator opens a passage through the projector's Go To find, the corner
cue shows the same TB/SIM translation label a service passage shows. Flipping it
currently gives no brighten at all: the detour re-renders its cue on the flip and
the fresh label never receives the flash. This slice gives the Go To passage cue
the same feedback spec 091 already requires for a service passage cue — the label
brightens for about one second, then returns to rest.

## Scope

### In scope

- The TB/SIM label of the corner cue while a Go To passage is open as a detour:
  the T key and a click both flip the projected translation in place.
- The brighten for about one second after the flip, then the return to the
  resting colour.
- A verse whose other edition has no text: the flip does nothing and nothing
  brightens.
- Online and saved-copy Go To.

### Out of scope

- Song detours (they have no translation label); pressing T during a non-passage
  detour keeps its pre-existing behaviour.
- The service passage flip itself (already correct and kept by the shared code
  path).
- The Go To panel's own look, the detour open/close morph, and the reading
  pages' TB/SIM switch.
- Focus retention of the rebuilt label button (pre-existing in both cue paths).
- Any CSS, layout, or motion change.

## Domain rules

- T or a click on the label flips only the projected translation of the detour
  passage, at the same place. The service position, the saved service entry, and
  the service order do not change (mirrors spec 091).
- The flip happens only when the other edition holds the verse; otherwise nothing
  changes and nothing brightens (the rule the service passage cue already
  applies).
- After a flip the label shows the other edition and holds the highlight colour
  for 1000 ms, then returns to rest. A repeat flip during the hold restarts the
  hold.
- The feedback is a cue state only: no layout change and no other text change.

## UI details

The look is the already-accepted corner-cue state from spec 091 (approved
shared-state preview
[preview-cue-state-colors.html](../091-projector-corner/preview-cue-state-colors.html),
"a translation flash uses the same highlight"); this slice adds no new visual,
geometry, or motion.

- **Size / spacing:** unchanged — `.cue-translation` keeps its inline-flex
  button at the current cue height, no padding change.
- **Position / layout:** unchanged.
- **Colors / typography:** rest `#514D47`; hover `#817D74`; flash (brighten)
  `var(--on)` `#E8E4DC` — rgb(232, 228, 220) — the same value as a pressed
  label.
- **States:** at rest, unchanged; hover and press, unchanged; right after a
  flip, flash for 1000 ms and then back to rest; other edition missing, no state
  change at all.
- **Responsive behavior:** unchanged (the cue line may already clip; nothing new
  is added).
- **Motion:** the existing `color 140ms ease` transition carries the colour
  change in and out; the hold itself is a plain colour state for 1000 ms (a JS
  timer, exactly as on a service passage today). No animation, so
  `prefers-reduced-motion` needs no special case.

## Acceptance scenarios

### Scenario: Flip a Go To passage with the keyboard

- **Given** a passage opened through Go To, shown as the detour screen, its cue
  label reading the edition on screen
- **When** the operator presses T
- **Then** the label shows the other edition, holds the bright colour, and
  returns to the resting colour after about one second

### Scenario: Flip a Go To passage with a click

- **Given** the same Go To passage detour
- **When** the operator clicks the label
- **Then** the same flip and one-second brighten happens

### Scenario: Flip again during the brighten

- **Given** a Go To passage detour whose label is still bright after a flip
- **When** the operator flips again
- **Then** the label shows the first edition again and the brighten restarts for
  another second

### Scenario: The other edition has no text for the verse

- **Given** a Go To passage whose other edition does not hold that verse
- **When** the operator flips
- **Then** the label does not change and no brighten appears

## Traceability

- Domain/app tests: N/A (browser cue state; no server behaviour change).
- E2E: `tests/e2e/test_projector.py::ProjectorE2ETests::test_goto_passage_translation_flip_brightens_the_label`
  — keyboard flip with brighten hold and return, click parity, repeat flip, and
  the single-edition no-op (fixture: a SIM edition for the Matius 5:3 seed).
- Implementation: `static/web/projector.js` — shared flip-feedback helper used by
  the service and Go To branches of `flipTranslation()`.
