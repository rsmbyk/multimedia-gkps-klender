# Plan 101: Brighten the translation label after flipping a Go To passage

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** ITEM-101
- **Bump:** patch

## Why

The owner reports that a Go To passage loses the translation flip's feedback
immediately: "when you open a passage via goto, and switch the translation, the
flash/highlight gone immediately. it should stay for a short time like the normal
passage."

Spec 091 already promises the brighten for a service passage cue ("the new label
brightens for about one second") and it holds there: the service branch of
`flipTranslation()` (`static/web/projector.js` 463–466) adds `.flash` to the
rebuilt label and removes it after 1000 ms. The Go To branch (446–451) returns
right after `renderDetour()` — before that code. `renderDetour()` → `renderCue()`
→ `renderDetourCue()` rebuilds the label (`cuePrefix.replaceChildren()`), so the
fresh button never carries `.flash`. The only highlight an operator sees is the
momentary hover/press colour, which ends when the node is replaced — hence
"gone immediately".

## Scope / edges

**In:**

- The TB/SIM label while a passage is open through Go To: the T key and a click
  on the label.
- The one-second brighten after the flip, then back to the resting colour.
- A verse whose other edition has no text: the flip does nothing and does not
  brighten — the same rule the service cue already applies.
- Online and saved-copy Go To.

**Out:**

- Song detours (no translation label); pressing T during a non-passage detour
  keeps its pre-existing behaviour (it falls through to the service screen —
  unchanged, see Risks).
- The service passage flip itself (already correct; kept through the same code
  path).
- The Go To panel's look, the detour open/close morph, the reading pages' TB/SIM
  switch, and any CSS change.
- Focus retention of the rebuilt label button (pre-existing in both cue paths).

## Approach

Extract the flash lifecycle from the service branch into one helper next to
`flipTranslation()`:

```js
function flashTranslationLabel() {
  window.clearTimeout(translationTimer);
  var flip = cuePrefix.querySelector('.cue-translation');
  if (!flip) return;
  flip.classList.add('flash');
  translationTimer = window.setTimeout(function () { flip.classList.remove('flash'); }, 1000);
}
```

Call it at the end of both branches, after the cue has been re-rendered (the
label node is rebuilt, so it must be flashed from the fresh DOM). In the Go To
branch, mirror the service guard before mutating: flip only when
`detour.translations[alternate]` exists, otherwise return (today it flips the
value, flips it back, and re-renders identically — no visible change, just
wasted work). No CSS change: `.cue-translation.flash { color: var(--on); }`
already exists (`static/styles/design/projector.css` 313).

## TDD

- Domain/app tests: N/A — browser cue state only; no server payload or model
  change (spec 091 precedent).
- E2E (Playwright via `StaticLiveServerTestCase`): `tests/e2e/test_projector.py`,
  class `ProjectorE2ETests`. The suite seeds only TB today; the new test needs a
  SIM fixture (Version + BookTranslation + a Matius 5:3 verse) so a detour flip
  has an edition to switch to.

## Risks

- The SIM fixture addition must not disturb existing projector assertions
  ('Matius 5' suggestion label, 'Matius 5:3' detour text, library sync). Run the
  whole `ProjectorE2ETests` class locally (targeted) after the change.
- The timer must target the label node created by the latest render and clear
  any pending timer first, so a rapid double flip restarts the hold instead of
  removing a newer flash early.
- `detour.translation` and the service `translation` stay separate pieces of
  state; the Go To branch must not touch the service screen.
- The shared helper's missing-label guard also removes a latent error where T
  during a song detour reaches the service branch and the label lookup finds
  nothing. The underlying fall-through behaviour is otherwise unchanged and out
  of scope for this slice.
