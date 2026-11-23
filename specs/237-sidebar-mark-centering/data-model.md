# Data Model: sidebar mark centring

**Spec**: `specs/237-sidebar-mark-centering/spec.md`

## Entities

No persisted entity is added, removed or changed. The slice touches one CSS rule; no
model, migration, form, serialiser or template is involved.

## Existing boxes the rule relies on

| Box | Current rule | Role in this slice |
| --- | --- | --- |
| `.songrow` | `display: flex; align-items: baseline; gap: 8px; min-height: 38px; padding: 7px 10px` in `#chList` | the flex line whose baseline alignment causes the fault |
| `.songrow__c` | `flex: none; min-width: 24px` plus `align-self: center` under `:root[data-section="tatib"] #chList` and `.reorder__ghost` | the reference column; already centred by spec 063 |
| `.songrow__mark` | `flex: none; width: 16px; height: 16px; display: block` | the span to centre |
| `.songrow__mark--slot` | `position: relative` | positioning context for the corner badge |
| `.slot__badge` | `position: absolute; right: -3px; bottom: -2px; width: 11px; height: 11px` | moves with its centred parent; unchanged |
| `.songrow__t` | `-webkit-line-clamp: 3; overflow-wrap: anywhere; min-width: 0` | the label; unchanged |

**Relationships**: `.songrow` contains the number, mark and label in that order. The
drag copy (`.reorder__ghost`) is a detached clone of the row's `innerHTML`, converted
to inert spans by `static/web/reorder.js:268`. **Validation**: none. **State
transitions**: none — the rule applies in every theme and row state.

## Invariants

- The mark's box centre equals its row's box centre within 1px (FR-001, SC-001).
- The mark stays 16×16px at x 42px; the label stays at x 66px with its three-line
  clamp (FR-002, SC-002).
- The drag copy's mark uses the same alignment as its number (FR-003, SC-003).
- No surface outside the contents list and its drag copy changes (FR-004).

## Not modelled

- No new CSS custom property: the change uses the existing `align-self` mechanism.
- No new state flag: the rule is scoped by section and container, not by data.
