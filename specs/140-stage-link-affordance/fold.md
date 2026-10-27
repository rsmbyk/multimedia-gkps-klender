# Fold: The stage's entry links read as text until hovered

**Capability**: `docs/spec/reading.md`
**Folded at**: 2026-10-27

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `added` | `R16` | A stage entry link reads as text until it is pointed at: ink at rest with no underline, a 3px underline on hover and keyboard focus, the controls in a column of their own so nothing is drawn under a title, and icon-only controls on a phone. |

## Drift guard

- **Files changed in this capability**: `static/styles/design/components.css` (the `.entry__jump`
  rule, the `.tatib__item--acts` column, the `.entry__ctrl` label collapse),
  `multimedia/web/templates/reading/tatib.html` (each control's word wrapped in
  `.entry__ctrl-label`), `static/styles/design/tokens.css` (`--link` comments only).
- **Header**: `last folded` 2026-10-27, `140-stage-link-affordance` prepended to `slices`.
- **Declared no behaviour change**: no — one requirement added, no existing one modified. Spec 056's
  colour rule was never folded (this file starts at spec 126), so there is no requirement to replace;
  `R16` states the behaviour that now holds.

<!-- A changed file with no delta is CRITICAL; Fold refuses to complete. -->
